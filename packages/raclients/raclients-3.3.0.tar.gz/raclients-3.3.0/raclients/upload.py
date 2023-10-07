# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from typing import Any
from typing import Callable
from typing import Generator

from pydantic import AnyHttpUrl
from pydantic import parse_obj_as

from raclients.auth import AuthenticatedHTTPXClient
from raclients.auth import keycloak_token_endpoint


def upload_file(
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str,
    mo_url: str,
    filepath: str,
    filename_in_mo: str,
) -> None:
    """Upload file to OS2mo."""
    url = f"{mo_url}/graphql/v15"

    with open(filepath, "rb") as file:
        # HTTPX inserts a default filename "upload" when there is no filename.
        # We need to empty string or strawberry think all of these are files
        # and none is map/operations.
        form = {
            "operations": (
                "",
                '{"query": "mutation($file: Upload!) { upload_file( file_store: EXPORTS, file: $file, force: true ) }", "variables": {"file": null}}',
            ),
            "map": ("", '{"file": ["variables.file"]}'),
            "file": (filename_in_mo, file),
        }
        with AuthenticatedHTTPXClient(
            client_id=client_id,
            client_secret=client_secret,
            token_endpoint=keycloak_token_endpoint(
                auth_server=parse_obj_as(AnyHttpUrl, auth_server),
                auth_realm=auth_realm,
            ),
        ) as client:
            r = client.post(url, files=form)
            r.raise_for_status()


@contextmanager
def file_uploader(settings: Any, filename: str) -> Generator[str, None, None]:
    """Return a temporary file, that will be uploaded to OS2mo when the context
    manager exits."""
    try:
        # JobSettings
        client_id = settings.client_id
        client_secret = settings.client_secret
        auth_server = settings.auth_server
        auth_realm = settings.auth_realm
        mora_base = settings.mora_base
    except AttributeError:
        # dict
        client_id = settings["crontab.CLIENT_ID"]
        client_secret = settings["crontab.CLIENT_SECRET"]
        auth_server = settings["crontab.AUTH_SERVER"]
        auth_realm = "mo"
        mora_base = settings["mora.base"]

    with NamedTemporaryFile() as fp:
        tmp_filename = fp.name
        yield tmp_filename
        upload_file(
            client_id,
            client_secret,
            auth_server,
            auth_realm,
            mora_base,
            tmp_filename,
            filename,
        )


def run_report_and_upload(
    settings: Any,
    filename: str,
    run_report_function: Callable,
    report_function: Callable,
    *report_function_args: tuple[Any, ...],
) -> None:
    """Run a report and upload it to OS2mo."""
    with file_uploader(settings, filename) as report_file:
        run_report_function(
            report_function,
            *report_function_args,
            report_file,
        )

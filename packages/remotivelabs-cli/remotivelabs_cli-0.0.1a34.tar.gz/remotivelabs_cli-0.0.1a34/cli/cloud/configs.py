import shutil
import sys

import requests
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import rest_helper as rest

app = typer.Typer()


@app.command("list")
def list_signal_databases(project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f'/api/project/{project}/files/config')


@app.command("delete")
def delete(signal_db_file: str = typer.Argument("", help="Signal database file"),
           project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_delete(f'/api/project/{project}/files/config/{signal_db_file}')


@app.command()
def download(signal_db_file: str = typer.Argument("", help="Signal database file"),
             project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:

        rest.ensure_auth_token()

        progress.add_task(description=f"Downloading {signal_db_file}", total=None)

        # First request the download url from cloud. This is a public signed url that is valid
        # for a short period of time
        get_signed_url_resp = requests.get(
            f'{rest.base_url}/api/project/{project}/files/config/{signal_db_file}/download',
            headers=rest.headers, allow_redirects=True)
        if get_signed_url_resp.status_code == 200:

            # Next download the actual file
            download_resp = requests.get(url=get_signed_url_resp.text, stream=True)
            if download_resp.status_code == 200:
                with open(signal_db_file, 'wb') as out_file:
                    shutil.copyfileobj(download_resp.raw, out_file)
                print(f"{signal_db_file} downloaded")
            else:
                sys.stderr.write(f"Got unexpected status {download_resp.status_code}\n")
        else:
            sys.stderr.write(f"Got unexpected status {get_signed_url_resp.status_code}\n")

# @app.command()
# def upload(file: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
# files = {'upload_file': open(file, 'rb')}
# values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
# rest.headers["content-type"] = "application/octet-stream"
# r = requests.get(f"{rest.base_url}/api/project/{project}/files/recording/upload/{file}", headers=rest.headers)
# print(r.status_code)
# print(r.text)

# curl -X PUT -H 'Content-Type: application/octet-stream' --upload-file docker-compose.yml 'https://storage.googleapis.com/beamylabs-fileuploads-dev/projects/beamyhack/recording/myrecording?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=recordings-upload-account%40beamycloud-dev.iam.gserviceaccount.com%2F20220729%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220729T134012Z&X-Goog-Expires=3000&X-Goog-SignedHeaders=content-type%3Bhost&X-Goog-Signature=d1fa7639349d6453aebfce8814d6e5685af03952d07aa4e3cb0d44dba7cf5e572f684c8120dba17cbc7ea6a0ef5450542a3c745c65e04272b34265d0ddcf1b67e6f2b5bfa446264a62d77bd7faabf45ad6bd2aec5225f57004b0a31cfe0480cba063a3807d86346b1da99ecbae3f3e6da8f44f06396dfc1fdc6f89e475abdf969142cef6f369f03aff41000c8abb28aa82185246746fd6c16b6b381baa2d586382a3d3067b6376ddba2b55b2b6f9d942913a1cbfbc61491ba6a615d7d5a0d9a476c357431143e9cea1411dfad9f01b1e1176dc8c056cbf08cccfd401a55d63c19d038f3ab42b712abc48d759047ac07862c4fae937c341e19b568bb60a4e4086'

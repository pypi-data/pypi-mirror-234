import glob
import json
import os
import re
import shutil
import sys

import requests
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import rest_helper as rest

app = typer.Typer()


def uid(p):
    print(p)
    return p['uid']

# to be used in options
#autocompletion=project_names)
def project_names():
    r = requests.get(f'{rest.base_url}/api/bu/{rest.org}/project', headers=rest.headers)
    # sys.stderr.write(r.text)
    if r.status_code == 200:
        projects = r.json()
        names = map(lambda p: p['uid'], projects)
        return (list(names))
    else:
        sys.stderr.write(f"Could not list projects due to {r.status_code}\n")
        # os.kill(signal.SIGSTOP)
        raise typer.Exit(0)
        # return []

        # return map(list(r.json()), lambda e: e.uid)


#    return ["beamyhack"]


@app.command("list")
def listRecordings(is_processing: bool = typer.Option(default=False, help="Use this option to see only those that are beeing processed or are invalid"),
                   project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    """
    List all recording sessions in a project. You can choose to see all valid recordings (default) or use
    --is-processing and you will get those that are currently beeing processed or that failed to be validated.

    """

    if is_processing:
        rest.handle_get(f"/api/project/{project}/files/recording/processing")
    else:
        rest.handle_get(f"/api/project/{project}/files/recording")



@app.command(help="Shows details about a specific recording in project")
def describe(recording_session: str = typer.Argument(..., help="Recording session id"),

             project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}")


def doStart(name: str, project: str, api_key: str, return_response: bool = False):
    if api_key == "":
        body = {"size": "S"}
    else:
        body = {"size": "S", 'apiKey': api_key}
    return rest.handle_post(f"/api/project/{project}/brokers/{name}", body=json.dumps(body),
                            return_response=return_response)


@app.command(help="Plays all recording files or a single recording")
def play(recording_session: str = typer.Argument(..., help="Recording session id", envvar="REMOTIVE_CLOUD_RECORDING_SESSION"),
         broker: str = typer.Option(..., help="Broker name to play on"),
         ensure_broker_started: bool = typer.Option(default=False, help="Ensure broker exists, start otherwise"),
         broker_config_name: str = typer.Option("default", help="Specify a custom broker configuration to use" ),
         project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        rest.ensure_auth_token()
        v = progress.add_task(description=f"Verifying broker {broker} exists...", total=100)

        r = requests.get(f'{rest.base_url}/api/project/{project}/brokers/{broker}', headers=rest.headers, )
        progress.update(v, advance=100.0)
        if r.status_code == 404:
            if ensure_broker_started:
                progress.add_task(description=f"Starting broker {broker}...", total=1)
                r = doStart(broker, project, '', return_response=True)
                if r.status_code != 200:
                    print(r.text)
                    exit(0)
            else:
                print("Broker not running, use --ensure-broker-started to start the broker")
                exit(0)
        elif r.status_code != 200:
            sys.stderr.write(f"Got http status code {r.status_code}")
            typer.Exit(0)

        progress.add_task(
            description=f"Uploading recording {recording_session} to {broker} and setting play mode to pause...",
            total=None)
        # if recording_file == "":
        #    rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/upload",
        #                    params={'brokerName': broker})
        # else:
        broker_config_query=""
        if (broker_config_name != "default"):
            broker_config_query = f"?brokerConfigName={broker_config_name}"

        rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/upload{broker_config_query}",
                        params={'brokerName': broker})


@app.command(help="Downloads the specified recording file to disk")
def download_recording_file(
        recording_file_name: str = typer.Argument(..., help="Recording file to download"),
        recording_session: str = typer.Option(..., help="Recording session id that this file belongs to", envvar='REMOTIVE_CLOUD_RECORDING_SESSION'),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Downloading {recording_file_name}", total=None)

        # First request the download url from cloud. This is a public signed url that is valid
        # for a short period of time
        rest.ensure_auth_token()
        get_signed_url_resp = requests.get(
            f'{rest.base_url}/api/project/{project}/files/recording/{recording_session}/recording-file/{recording_file_name}',
            headers=rest.headers, allow_redirects=True)
        if get_signed_url_resp.status_code == 200:

            # Next download the actual file
            download_resp = requests.get(url=get_signed_url_resp.json()["downloadUrl"], stream=True)
            if download_resp.status_code == 200:
                with open(recording_file_name, 'wb') as out_file:
                    shutil.copyfileobj(download_resp.raw, out_file)
                print(f"{recording_file_name} downloaded")
            else:
                sys.stderr.write(download_resp.text)
                sys.stderr.write(f"Got http status {download_resp.status_code}\n")
        else:
            sys.stderr.write(get_signed_url_resp.text)
            sys.stderr.write(f"Got http dd status {get_signed_url_resp.status_code}\n")


@app.command(name="delete")
def delete(recording_session: str = typer.Argument(..., help="Recording session id"),
           project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    """
    Deletes the specified recording session including all media files and configurations.

    """
    rest.handle_delete(f"/api/project/{project}/files/recording/{recording_session}")


@app.command(name="delete-recording-file")
def delete_recording_file(recording_file_name: str = typer.Argument(..., help="Recording file to download"),
           recording_session: str = typer.Option(..., help="Recording session id that this file belongs to", envvar='REMOTIVE_CLOUD_RECORDING_SESSION'),
           project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    """
    Deletes the specified recording file

    """
    rest.handle_delete(f'/api/project/{project}/files/recording/{recording_session}/recording-file/{recording_file_name}')

@app.command()
def upload(path: str  = typer.Argument(..., help="Path to valid recording to upload"),
           project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Uploading {path}", total=None)

        filename = os.path.basename(path)
        rest.ensure_auth_token()
        rest.headers["content-type"] = "application/octet-stream"
        r = requests.post(f"{rest.base_url}/api/project/{project}/files/recording/{filename}", headers=rest.headers)
        if r.status_code == 200:
            headers = {}
            headers["content-type"] = "application/x-www-form-urlencoded"
            r = requests.put(r.text, open(path, 'rb'), headers=headers)
            print(
                "File successfully uploaded, please run 'remotive cloud recordings list' to verify that the recording was successfully processed")
        else:
            print(r.text)

@app.command()
def upload_broker_configuration(
        directory:str = typer.Argument(..., help="Configuration directory"),
        recording_session: str = typer.Option(..., help="Recording session id", envvar='REMOTIVE_CLOUD_RECORDING_SESSION'),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT'),
        overwrite: bool = typer.Option(False, help="Overwrite existing configuration if it exists")
):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:

        # Must end with /
        if not directory.endswith("/"):
            directory = f'{directory}/'

        #
        # List files in specified directory. Look for interfaces.json and use that directory where this is located
        # as configuration home directory
        #
        files = list(filter(lambda item : "interfaces.json" in item, glob.iglob(directory + '**/**', recursive=True)))
        if len(files) == 0:
            sys.stderr.write("No interfaces.json found in directory, this file is required")
            raise typer.Exit(1)
        if len(files) > 1:
            sys.stderr.write(f"{len(files)} interfaces.json found in directoryw which is not supported")
            raise typer.Exit(1)
        broker_config_dir_name = os.path.dirname(files[0]).rsplit('/', 1)[-1]

        #
        # Get the current details about broker configurations to see if a config with this
        # name already exists
        #
        task=progress.add_task(description=f"Preparing upload of {broker_config_dir_name}", total=1)
        details_resp=rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}", return_response=True)
        details=details_resp.json()
        existing_configs = details['brokerConfigurations']
        if (len(existing_configs) > 0):
            data=list(filter(lambda x : x['name'] == broker_config_dir_name, existing_configs))
            if len(data) > 0:
                if (overwrite):
                    rest.handle_delete(f'/api/project/{project}/files/recording/{recording_session}/configuration/{broker_config_dir_name}', quiet=True)
                else:
                    sys.stderr.write("Broker configuration already exists, use --overwrite to replace\n")
                    raise typer.Exit(1)

        #
        # From the list of files, create a tuple of local_path to the actual file
        # and a remote path as it should be stored in cloud
        #
        file_infos = list(map(lambda item :
                     { 'local_path' : item,
                     'remote_path' : f"/{broker_config_dir_name}{item.rsplit(broker_config_dir_name,1)[-1]}"} ,glob.iglob(directory + '**/*.*', recursive=True)))

        #
        # convert this remote paths and ask cloud to prepare upload urls for those
        #
        json_request_upload_urls_req = {
            'name' : 'not_used',
            'paths' : list(map(lambda x: x['remote_path'], file_infos))
        }

        response = rest.handle_put(url = f'/api/project/{project}/files/recording/{recording_session}/configuration', return_response=True, body=json.dumps(json_request_upload_urls_req))
        if (response.status_code != 200):
            print(f'Failed to prepare configuration upload')
            print(f'{response.text} - {response.status_code}')
            raise typer.Exit(1)
        progress.update(task, advance=1)

        task=progress.add_task(description=f"Uploading {broker_config_dir_name} ({len(file_infos)} files)", total=len(file_infos))

        #
        # Upload urls is a  remote_path : upload_url dict
        # '/my_config/interfaces.json' : "<upload_url>"
        #
        upload_urls = json.loads(response.text)

        # For each file - upload
        for file in file_infos:
            key=file['remote_path']
            path=file['local_path']
            url=upload_urls[key]
            upload_task=progress.add_task(description=f"Uploading {key}", total=1)
            headers={
                'Content-Type' : "application/x-www-form-urlencoded"
            }
            r = requests.put(url, open(path, 'rb'), headers=headers)
            progress.update(task, advance=1)
            if r.status_code != 200:
                print("Failed to upload broker configuration")
                print(r.status_code)
                print(r.text)
                typer.Exit(1)
            progress.update(upload_task, advance=1)

        print(f"Successfully uploaded broker configuration {broker_config_dir_name}")



@app.command(help="Downloads the specified broker configuration directory as zip file")
def download_configuration(
        broker_config_name: str = typer.Argument(..., help="Broker config name"),
        recording_session: str = typer.Option(..., help="Recording session id", envvar='REMOTIVE_CLOUD_RECORDING_SESSION'),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')
):
    rest.ensure_auth_token()
    # print(rest.base_url)
    r = rest.handle_get(
        url=f"/api/project/{project}/files/recording/{recording_session}/configuration/{broker_config_name}",
        return_response=True)
    # print(r.status_code)
    # print(r.headers)
    # print(get_filename_from_cd(r.headers.get('content-disposition')))
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    open(filename, 'wb').write(r.content)
    print(f'Downloaded file {filename}')

@app.command(help="Downloads the specified broker configuration directory as zip file")
def delete_configuration(
        broker_config_name: str = typer.Argument(..., help="Broker config name"),
        recording_session: str = typer.Option(..., help="Recording session id", envvar='REMOTIVE_CLOUD_RECORDING_SESSION'),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')
):

    rest.handle_delete(
        url=f"/api/project/{project}/files/recording/{recording_session}/configuration/{broker_config_name}")



def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

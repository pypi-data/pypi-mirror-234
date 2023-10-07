from pathlib import Path
import os
import sys
import json
import typer
from . import rest_helper as rest

app = typer.Typer()

token_file_name = str(Path.home()) + "/.config/.remotive/cloud.secret.token"
config_dir_name = str(Path.home()) + "/.config/.remotive/"


@app.command(name="create", help="Create and download a new personal access token")
def get_personal_access_token(
        activate:bool = typer.Option(False, help="Activate the token for use after download")
):
    rest.ensure_auth_token()
    rest.handle_post('/api/me/keys')

    response = rest.handle_post(url='/api/me/keys',
                                return_response=True)

    if response.status_code == 200:
        name = response.json()['name']
        path_to_file = write_personal_token(f"personal-token-{name}.json", response.text)
        print(f"Personal access token written to {path_to_file}")
        if not activate:
            print(f"Use 'remotive cloud auth tokens activate {os.path.basename(path_to_file)}' to use this access token from cli")
        else:
            do_activate(path_to_file)
            print("Token file activated and ready for use")
        print('\033[93m This file contains secrets and must be kept safe')
    else:
        print(f'Got status code: {response.status_code}')
        print(response.text)


@app.command(name="list", help="List personal access tokens")
def list_personal_access_tokens():
    rest.ensure_auth_token()
    rest.handle_get('/api/me/keys')


@app.command(name="revoke", help="Revoke the specified access token")
def revoke(
        name: str = typer.Option(..., help="Name of the access token to revoke")
):
    rest.ensure_auth_token()
    rest.handle_delete(f'/api/me/keys/{name}', success_msg="Successfully revoked")

@app.command()
def describe(
        file: str = typer.Option(..., help="File name")):
    """
    Show contents of specified access token file
    """
    print(read_file(file))


@app.command()
def activate(
        file: str = typer.Argument(..., help="File name")):
    """
    Activate a access token file to be used for authentication.

    --file

    This will be used as the current access token in all subsequent requests. This would
    be the same as login with a browser.
    """
    do_activate(file)

def do_activate(file:str):
    # Best effort to read file
    if os.path.exists(file):
        token_file = json.loads(read_file_with_path(file))
        write_token(token_file['token'])
    elif os.path.exists(str(Path.home()) + f"/.config/.remotive/{file}"):
        token_file = json.loads(read_file(file))
        write_token(token_file['token'])
    else:
        sys.stderr.write("File could not be found \n")

@app.command(name="list-files")
def list_files():
    """
    List personal access token files in remotivelabs config directory
    """
    personal_files = filter(lambda f: f.startswith('personal'), os.listdir(config_dir_name) )
    for file in personal_files:
        print(file)


def read_file(file):
    f = open(str(Path.home()) + f"/.config/.remotive/{file}", "r")
    token = f.read()
    f.close()
    return token


def read_file_with_path(file):
    f = open(file, "r")
    token = f.read()
    f.close()
    return token


def write_token(token):
    f = open(token_file_name, "w")
    f.write(token)
    f.close()


def write_personal_token(file:str, token:str):
    path = str(Path.home()) + f"/.config/.remotive/{file}"
    f = open(path, "w")
    f.write(token)
    f.close()
    return path

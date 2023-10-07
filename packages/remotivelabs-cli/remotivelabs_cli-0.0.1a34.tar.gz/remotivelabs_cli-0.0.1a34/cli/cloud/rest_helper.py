import sys

import requests
import os
import json
import logging
from pathlib import Path
from os.path import exists
import typer
import pkg_resources

from rich.console import Console
from cli import settings

err_console = Console(stderr=True)

if 'REMOTIVE_CLOUD_HTTP_LOGGING' in os.environ:
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
global baseurl
base_url = "https://cloud.remotivelabs.com"

if 'REMOTIVE_CLOUD_BASE_URL' in os.environ:
    base_url = os.environ['REMOTIVE_CLOUD_BASE_URL']

# if 'REMOTIVE_CLOUD_AUTH_TOKEN' not in os.environ:
#    print('export REMOTIVE_CLOUD_AUTH_TOKEN=auth must be set')
#    exit(0)

# token = os.environ["REMOTIVE_CLOUD_AUTH_TOKEN"]
# headers = {"Authorization": "Bearer " + token}

headers = {}
org = ""

token = ""

cli_version = pkg_resources.get_distribution('remotivelabs-cli')


def ensure_auth_token():
    global token

    # if 'REMOTIVE_CLOUD_ORGANISATION' not in os.environ:
    #    print('You must first set the organisation id to use: export REMOTIVE_CLOUD_ORGANISATION=organisationUid')
    #    raise typer.Exit()
    global org
    # org = os.environ["REMOTIVE_CLOUD_ORGANISATION"]

    #    if not exists(str(Path.home()) + "/.config/.remotive/cloud.secret.token"):
    #        print("Access token not found, please login first")
    #        raise typer.Exit()

    #    f = open(str(Path.home()) + "/.config/.remotive/cloud.secret.token", "r")
    token = settings.read_token()
    #    os.environ['REMOTIVE_CLOUD_AUTH_TOKEN'] = token
    global headers
    headers = {
        'Authorization': "Bearer " + token.strip(),
        'User-Agent': f'${cli_version.project_name} ${cli_version.version}',
    }


def handle_get(url, params=None, return_response: bool = False):
    if params is None:
        params = {}
    ensure_auth_token()
    r = requests.get(f'{base_url}{url}', headers=headers, params=params)

    if return_response:
        check_api_result(r)
        return r
    print_api_result(r)


def has_access(url, params={}):
    ensure_auth_token()
    r = requests.get(f'{base_url}{url}', headers=headers, params=params)
    if r.status_code == 401:
        return False
    else:
        return True


def check_api_result(response):
    if response.status_code > 299:
        err_console.print(f':boom: [bold red]Got status code[/bold red]: {response.status_code}')
        if response.status_code == 401:
            err_console.print("Your token has expired, please login again")
        else:
            err_console.print(response.text)
        exit(1)


def print_api_result(response):
    if response.status_code >= 200 and response.status_code < 300:
        if len(response.content) > 4:
            print(json.dumps(response.json()))
        exit(0)
    else:
        err_console.print(f':boom: [bold red]Got status code[/bold red]: {response.status_code}')
        if response.status_code == 401:
            err_console.print("Your token has expired, please login again")
        else:
            err_console.print(response.text)
        exit(1)
    # typer.Exit(1) did not work as expected


def handle_delete(url, params={}, quiet=False, success_msg="Successfully deleted"):
    ensure_auth_token()
    r = requests.delete(f'{base_url}{url}', headers=headers, params=params)
    if r.status_code == 200 or r.status_code == 204:
        if not quiet:
            print_api_result(r)
    else:
        print_api_result(r)


def handle_post(url, body=None, params={}, return_response: bool = False):
    ensure_auth_token()
    headers["content-type"] = "application/json"
    r = requests.post(f'{base_url}{url}', headers=headers, params=params, data=body)

    if return_response:
        check_api_result(r)
        return r

    print_api_result(r)


def handle_put(url, body=None, params={}, return_response: bool = False):
    ensure_auth_token()
    headers["content-type"] = "application/json"
    r = requests.put(f'{base_url}{url}', headers=headers, params=params, data=body)

    if return_response:
        check_api_result(r)
        return r

    print_api_result(r)

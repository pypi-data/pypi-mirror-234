import json
from typing import List

import typer

from . import rest_helper as rest
from . import service_account_tokens

app = typer.Typer()


@app.command(name="list", help="List service-accounts")
def list_service_accounts(project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/admin/accounts")


@app.command(name="create", help="Create service account")
def create_service_account(
        name: str,
        role: List[str] = typer.Option(..., help="Roles to apply"),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    data = {
        'name': name,
        'roles': role
    }
    rest.handle_post(url=f"/api/project/{project}/admin/accounts", body=json.dumps(data))


@app.command(name="update", help="Update service account")
def update_service_account(
        service_account: str = typer.Option(..., help="Service account name"),
        role: List[str] = typer.Option(..., help="Roles to apply"),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):

    rest.handle_put(url=f"/api/project/{project}/admin/accounts/{service_account}", body=json.dumps(role))


@app.command(name="delete", help="Delete service account")
def delete_service_account(
        name: str,
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_delete(url=f"/api/project/{project}/admin/accounts/{name}")


app.add_typer(service_account_tokens.app, name="tokens", help="Manage project service account access tokens")

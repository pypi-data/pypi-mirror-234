import json
import typer
from . import rest_helper as rest

app = typer.Typer()


@app.command(name="list", help="List your projects")
def list_projects(organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION')):
    r = rest.handle_get(url=f'/api/bu/{organisation}/me',  return_response=True)
    if r.status_code == 200:
        # extract the project uid parts
        projects = r.json()['projects']
        projects = map(lambda p: p['uid'], projects)
        print(json.dumps(list(projects)))
    else:
        print(r.status_code)
        print(r.text)


@app.command(name="create")
def create_project(
    organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION'),
    project_uid: str = typer.Option(..., help="Project UID"),
    project_display_name: str = typer.Option(default="", help="Project display name")
):

    create_project_req = {
        'uid': project_uid,
        'displayName': project_display_name if project_display_name != "" else project_uid,
        'description': ''
    }

    rest.handle_post(url=f'/api/bu/{organisation}/project', body=json.dumps(create_project_req))


@app.command(name="delete")
def delete(project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_delete(url=f'/api/project/{project}')
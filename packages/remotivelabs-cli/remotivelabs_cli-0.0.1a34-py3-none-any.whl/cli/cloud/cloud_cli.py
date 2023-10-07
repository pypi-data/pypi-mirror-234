import json

import typer

from . import recordings, brokers, configs, auth, service_accounts, projects
from . import rest_helper as rest

app = typer.Typer()


@app.command(help="List licenses for an organisation")
def licenses(
        organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION'),
        filter: str = typer.Option("all", help="all, valid, expired")
):
    rest.handle_get(f"/api/bu/{organisation}/licenses", {'filter': filter})


@app.command(help="List your available organisations")
def organisations():
    r = rest.handle_get(f"/api/home", return_response=True)
    if r.status_code == 200:
        j = list(map(lambda x : x["billableUnitUser"]["billableUnit"]["uid"], r.json()))
        print(json.dumps(j))
    else:
        print(f"Got status code: {r.status_code}")
        print(r.text)


app.add_typer(projects.app, name="projects", help="Manage projects")
app.add_typer(auth.app, name="auth")
app.add_typer(brokers.app, name="brokers", help="Manage cloud broker lifecycle")
app.add_typer(recordings.app, name="recordings", help="Manage recordings")
app.add_typer(configs.app, name="signal-databases", help="Manage signal databases")
app.add_typer(service_accounts.app, name="service-accounts", help="Manage project service account keys")


if __name__ == "__main__":
    app()

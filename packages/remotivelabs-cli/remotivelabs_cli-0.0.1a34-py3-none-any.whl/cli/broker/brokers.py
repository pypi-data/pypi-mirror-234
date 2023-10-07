import signal as os_signal
from time import sleep
from typing import List
import os

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
)

from . import playback, record, files, signals, export, scripting
from .lib.broker import Broker

app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def main(
        url: str = typer.Option(None, is_eager=False, help="Broker URL", envvar="REMOTIVE_BROKER_URL"),
):
    # This can be used to override the --url per command, lets see if this is a better approach
    if url is not None:
        os.environ["REMOTIVE_BROKER_URL"] = url
    # Do other global stuff, handle other global options here
    return


@app.command(name="x-diagnose")
def diagnose(
        namespace: List[str] = typer.Option([], help="Namespace to diagnose"),
        all_namespaces: bool = typer.Option(False, help="Scan all namespaces, must be true if no namespaces provided"),
        wait_for_traffic: bool = typer.Option(False, help="Wait until traffic is found on any bus"),
        quiet: bool = typer.Option(False, help="Do not prompt me"),
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    """
    [Experimental] - Performs a scan on specified buses to see if the is any traffic coming on the buses. This works
    for both recordings and live data

    """

    if not quiet:
        do_it = typer.confirm("""
        This will perform recordings on selected buses, make sure there are no recordings currently running on the broker.
        """)
        if not do_it:
            print("Skipping diagnosis")
            raise typer.Abort()

    broker = Broker(url, api_key)
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:

        if len(namespace) > 0 and all_namespaces:
            print("No namespaces should be supplied when all-namespaces is used")
            raise typer.Exit(1)
        if len(namespace) == 0 and not all_namespaces:
            print("No namespaces chosen")
            raise typer.Exit(1)

        if all_namespaces:
            namespace = broker.list_namespaces()

        if wait_for_traffic:
            progress.add_task(description=f"Scanning for traffic on  {namespace} [Ctrl+C to exit] ", total=1)
        else:
            progress.add_task(description=f"Scanning for traffic on  {namespace}... (just a few seconds)", total=1)

        def on_sigint(sig, frame):
            progress.add_task(description=f"Cleaning up, please wait...", total=None)

        os_signal.signal(os_signal.SIGINT, on_sigint)

        broker.diagnose(namespace, wait_for_traffic)


@app.command(help="Discover brokers on this network")
def discover():
    # print("Not implemented")

    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)

    services = ["_remotivebroker._tcp.local."]
    # services = list(ZeroconfServiceTypes.find(zc=zeroconf))

    print("\nLooking for RemotiveBrokers on your network, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()


def on_service_state_change(
        zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    # print(f"Service {name} state changed: {state_change}")

    if state_change is ServiceStateChange.Removed:
        print(f"Service {name} was removed")

    if state_change is ServiceStateChange.Updated:
        print(f"Service {name} was updated")

    if state_change is ServiceStateChange.Added:
        print(f"[ {name} ]")
        info = zeroconf.get_service_info(service_type, name)
        # print("Info from zeroconf.get_service_info: %r" % (info))

        if info:
            # addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            for addr in info.parsed_scoped_addresses():
                print(f'RemotiveBrokerApp: http://{addr}:8080')
                print(f'RemotiveBroker http://{addr}:50051')
            # print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            # print(f"  Server: {info.server}")
            # if info.properties:
            #    print("  Properties are:")
            #    for key, value in info.properties.items():
            #        print(f"    {key}: {value}")
            # else:
            #    print("  No properties")
        else:
            print("  No info")
        print('\n')


app.add_typer(playback.app, name="playback", help="Manage playing recordings")
app.add_typer(record.app, name="record", help="Record data on buses")
app.add_typer(files.app, name="files", help="Upload/Download configurations and recordings")
app.add_typer(signals.app, name="signals", help="Find and subscribe to signals")
app.add_typer(export.app, name="export", help="Export to external formats")
app.add_typer(scripting.app, name="scripting")

if __name__ == "__main__":
    app()

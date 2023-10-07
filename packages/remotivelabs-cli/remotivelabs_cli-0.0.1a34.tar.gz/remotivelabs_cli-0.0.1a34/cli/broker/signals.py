import json
import os
import signal as os_signal
from typing import List
import grpc
import plotext as plt
import typer
from rich import print as rich_rprint

from .lib.broker import Broker
from .lib.errors import ErrorPrinter as err_printer


app = typer.Typer(help=help)

signal_values:list = list()

@app.command(help="List signals names on broker")
def signal_names(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option(None, help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    try:
        broker = Broker(url, api_key)
        # print("Listing available signals")
        available_signals = broker.list_signal_names()
        print(json.dumps(available_signals))
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)


def read_scripted_code_file(file_path: str) -> str:
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check your file path.")
        exit(1)

@app.command(help="Subscribe to signals")
def subscribe(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY'),
        signal: List[str] = typer.Option([], help="List of signal names to subscribe to"),
        namespace: str = typer.Option(None, help="Cloud Broker API-KEY or access token",
                                      envvar='REMOTIVE_BROKER_API_KEY'),
        on_change_only: bool = typer.Option(default=False, help="Only get signal if value is changed"),
        script: str = typer.Option(None, help="Supply a path to Lua script that to use for signal transformation"),
        x_plot: bool = typer.Option(default=False, help="Experimental: Plot the signal in terminal - Only one signal suppoerted")
        # samples: int = typer.Option(default=0, he)

):
    print("Subscribing to signals, press Ctrl+C to exit")
    plt.title("Signals")

    def exit_on_ctrlc(sig, frame):
        os._exit(0)

    def on_frame_plot(x):
        global signal_values
        plt.clt() # to clear the terminal
        plt.cld() # to clear the data only
        y = list(map( lambda s: s['value'], list(x)))
        signal_values = signal_values + y
        if len(signal_values) > 1000:
            signal_values = signal_values[len(signal_values) - 1000:]
        plt.plot(signal_values)
        plt.sleep(0.001) # to add
        plt.show()

    def on_frame_print(x):
        rich_rprint(json.dumps(list(x)))

    os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

    if x_plot:
        on_frame_func = on_frame_plot
    else:
        on_frame_func = on_frame_print

    try:
        broker = Broker(url, api_key)
        if script is not None:
            script_src = read_scripted_code_file(script)
            broker.subscribe_on_script(script_src, on_frame_func, on_change_only)
        else:
            broker.subscribe(signal, namespace, on_frame_func, on_change_only)
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)


@app.command(help="List namespaces on broker")
def namespaces(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option(None, help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):

    try:
        broker = Broker(url, api_key)
        namespaces_json = broker.list_namespaces()
        print(json.dumps(namespaces_json))
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)
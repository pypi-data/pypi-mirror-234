import os
import signal as os_signal
from typing import List

import grpc
import typer

from .lib.broker import Broker
from .lib.errors import ErrorPrinter as err_printer

app = typer.Typer(rich_markup_mode="rich", help="""
Export subscribed signals to different formats, currently only InfluxDB line protocol
but more formats will come soon
""")


@app.command()
def influxdb(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option(None, help="Cloud Broker API-KEY" ,
                                    envvar='REMOTIVE_BROKER_API_KEY'),
        signal: List[str] = typer.Option(..., help="List of signal names to subscribe to"),
        namespace: str = typer.Option(..., help="Cloud Broker API-KEY or access token",
                                      envvar='REMOTIVE_BROKER_API_KEY'),
        on_change_only: bool = typer.Option(default=False, help="Only get signal if value is changed"),
        output: str = typer.Option(None, help="Write results to file, defaults to stdout")

):
    """
    Exports subscribed signals to InfluxDB line-protocol, really useful to dump some signals into
    influxdb for offline analysis and insights.

    This is a sample for exporting and importing to InfluxDB using remotive-cli and influx-cli

    [bold]Export:[/bold]
    remotive broker export influxdb --url [URL] --output signals.influx --namespace VehicleBus  \\
        --signal Control.SteeringWheel_Position --signal Control.Accelerator_PedalPosition \\
        --signal GpsPosition.GPS_Longitude --signal GpsPosition.GPS_Latitude

    [bold]Output:[/bold]
    Control, SteeringWheel_Position=1.0,Accelerator_PedalPosition=0,Speed=0 1664787032944374000
    GpsPosition, GPS_Longitude=12.982076,GPS_Latitude=55.618748 1664787032948256000

    [bold]Import:[/bold]
    influx write --org myorg -b my-bucket -p ns --format=lp  -f signals.influx


    """

    if output is not None:
        f = open(output, "w")

    def exit_on_ctrlc(sig, frame):
        if output is not None:
            f.close()
        os._exit(0)

    def per_frame_influx_line_protocol(x):

        signals = list(x)
        if len(signals) == 0:
            return

        frame_name = signals[0]["name"].split(".")[0]
        signals_str = ",".join(list(map(lambda s: f'{s["name"].split(".")[1]}={s["value"]}', signals)))
        influx_lp = f"{frame_name},namespace={namespace} {signals_str} {round(signals[0]['timestamp_us'] * 1000)}"
        if output is not None:
            f.write(f"{influx_lp}\n")
        else:
            print(f"{influx_lp}")

    # TODO - support for csv
    #def csv(x):
        # list = list(x)
        # print(x)
        #l = list(x)
        #print(l)
        # ll=list(map(lambda s : s, l))
        # for s in l:
        # dt = datetime.fromtimestamp(s["timestamp_nanos"] / 1000000)
        # t=datetime.isoformat(dt)
        # t=rfc3339.format_millisecond(dt)
        # rich_rprint(len(l))
        #lat = (l[0])
        #lon = l[1]
        #dt = datetime.fromtimestamp(lat["timestamp_nanos"] / 1000000)
        # t=datetime.isoformat(dt)
        #t = rfc3339.format_millisecond(dt)
        # name = s["name"]
        # value = s["value"]
        #if output is not None:
        #    f.write(f'coord,{lat["value"]},{lon["value"]},{t}\n')
        #else:
        #    print(f'coord,{lat["value"]},{lon["value"]},{t}')
        #if output is not None:
        #    f.flush()
        # print(x["timestamp_nanos"])
        # rich_rprint(json.dumps(list(x)))

    os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

    # print(namespace)
    # signals2 = list(map( lambda s: s['signal'], broker.list_signal_names2(namespace)))
    try:
        broker = Broker(url, api_key)
        broker.subscribe(signal, namespace, per_frame_influx_line_protocol, on_change_only)
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)

from .lib.errors import ErrorPrinter as err_printer
import typer
from string import Template
from typing import List

from rich import print as rich_print

app = typer.Typer(rich_markup_mode="rich", help="""
[Experimental] - Generate template lua script for input and output signals
""")


def write(signal_name, script):
    path = f"{signal_name}.lua"
    f = open(path, "w")
    f.write(script)
    f.close()
    print(f"Secret token written to {path}")


@app.command("new-script")
def new_script(
        input_signal: List[str] = typer.Option(..., help="Required input signal names"),
        input_namespace: str = typer.Option(..., help="Input namespace for signals (only one supported)"),
        output_signal: str = typer.Option(..., help="Name of output signal"),
        save: bool = typer.Option(False, help="Save file to disk - Default stored as {outout_signal}.lua")
):
    def to_local_signal(sig_name):
        t = Template("""
    {
        name = "$sig_name",
        namespace = "$namespace"
    }"""
                     )
        return t.substitute(sig_name=sig_name, namespace=input_namespace)

    local_signals = ",".join(list(map(to_local_signal, input_signal)))

    template = Template("""

local local_signals = {$local_signals
}

-- Required, declare which input is needed to operate this program.
function input_signals()
    return local_signals
end

-- Provided parameters are used for populating metadata when listing signals.
function output_signals()
    return "$output_signal"
end

-- Invoked when ANY signal declared in "local_signals" arrive
-- @param signals_timestamp_us: signal time stamp
-- @param system_timestamp_us
-- @param signals: array of signals containing all or a subset of signals declared in "local_signals". Make sure to nil check before use.
function signals(signals, namespace, signals_timestamp_us, system_timestamp_us)
    
    -- TODO - replace this code with what you want todo
    
    if signals["$signle_input_signal"] == 0 then
        return return_value_or_bytes(0)
    else
        return return_value_or_bytes(signals["$signle_input_signal"] * 2)
    end 
end

-- helper return function, make sure to use return_value_or_bytes or return_nothing.
function return_value_or_bytes(value_or_bytes)
    return value_or_bytes
end

""")
    script = template.substitute(local_signals=local_signals, signle_input_signal=input_signal[0],
                                 input_namespace=input_namespace, output_signal=output_signal)

    if save:
        write(output_signal, script)
    else:
        rich_print(script)

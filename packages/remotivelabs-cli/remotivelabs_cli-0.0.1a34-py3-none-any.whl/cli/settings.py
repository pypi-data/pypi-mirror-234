from pathlib import Path
import os
from rich.console import Console
err_console = Console(stderr=True)

config_dir_name = str(Path.home()) + "/.config/.remotive/"
token_file_name = str(Path.home()) + "/.config/.remotive/cloud.secret.token"


def read_token():

    if not os.path.exists(token_file_name):
        err_console.print(f':boom: [bold red]Access failed[/bold red] - No access token found')
        err_console.print("Login with [italic]remotive cloud auth login[/italic]")
        err_console.print("If you have downloaded a personal access token, you can activate "
                          "it with [italic]remotive cloud auth tokens activate [FILE_NAME][/italic]")
        exit(1)

    f = open(token_file_name, "r")
    token = f.read()
    f.close()
    return token
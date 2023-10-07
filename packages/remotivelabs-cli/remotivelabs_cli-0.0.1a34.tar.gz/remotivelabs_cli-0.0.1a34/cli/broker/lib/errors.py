import grpc
import os
from rich.console import Console

err_console = Console(stderr=True)


class ErrorPrinter:

    @staticmethod
    def print_grpc_error(error: grpc.RpcError):
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            is_access_token = os.environ["ACCESS_TOKEN"]
            if is_access_token is not None and is_access_token == "true":
                err_console.print(f':boom: [bold red]Authentication failed[/bold red]: {error.details()}')
                err_console.print(f'Please login again')
            else:
                err_console.print(f':boom: [bold red]Authentication failed[/bold red]')
                err_console.print(f'Failed to verify api-key')
        else:
            # print(f"Unexpected error: {error.code()}")
            err_console.print(f':boom: [bold red]Unexpected error, status code[/bold red]: {error.code()}')
            err_console.print(error.details())
        exit(1)

    @staticmethod
    def print_hint(message:str):
        err_console.print(f":point_right: [bold]{message}[/bold]")

    @staticmethod
    def print_generic_error(message:str):
        err_console.print(f":boom: [bold red]Failed[/bold red]: {message}")

    @staticmethod
    def print_generic_message(message:str):
        err_console.print(f"[bold]{message}[/bold]:")
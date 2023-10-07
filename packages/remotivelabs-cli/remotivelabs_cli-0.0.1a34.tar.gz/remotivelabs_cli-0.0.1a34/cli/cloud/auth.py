import os
import os
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

import typer

from . import auth_tokens
from . import rest_helper as rest

from cli import settings

apa = settings.config_dir_name

help = """
Manage how you authenticate with our cloud platform
"""

app = typer.Typer(help=help)

app.add_typer(auth_tokens.app, name="tokens", help="Manage users personal access tokens")
config_dir_name = settings.config_dir_name  # str(Path.home()) + "/.config/.remotive/"
token_file_name = settings.token_file_name  # str(Path.home()) + "/.config/.remotive/cloud.secret.token"


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        # self.send_response(301)
        # self.send_header('Location', 'https://cloud.remotivelabs.com')
        # self.end_headers()
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return

    def do_GET(self):
        self._set_response()
        self.wfile.write("Successfully setup CLI, return to your terminal to continue".encode('utf-8'))
        path = self.path
        time.sleep(1)
        httpd.server_close()

        killerthread = Thread(target=httpd.shutdown)
        killerthread.start()

        if not os.path.exists(config_dir_name):
            os.makedirs(config_dir_name)
        write_token(path[1:])
        print("Successfully logged on, you are ready to go with cli")


def start_local_webserver(server_class=HTTPServer, handler_class=S, port=0):
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)


#
# CLI commands go here
#

@app.command(name="login")
def login():
    """
    Login to the cli using browser

    This will be used as the current access token in all subsequent requests. This would
    be the same as activating a personal access key or service-account access key.
    """
    start_local_webserver()
    webbrowser.open(f'{rest.base_url}/login?redirectUrl=http://localhost:{httpd.server_address[1]}', new=1,
                    autoraise=True)
    httpd.serve_forever()


@app.command()
def whoami():
    """
    Validates authentication and fetches your user information
    """
    rest.handle_get('/api/whoami')


@app.command()
def print_access_token():
    """
    Print current active access token
    """
    print(read_token())


@app.command(help="Clear access token")
def logout():
    os.remove(settings.token_file_name)
    print("Access token removed")


def read_token():
    #f = open(token_file_name, "r")
    #token = f.read()
    #f.close()
    return settings.read_token()


def read_file_with_path(file):
    f = open(file, "r")
    token = f.read()
    f.close()
    return token


def read_file(file):
    f = open(str(Path.home()) + f"/.config/.remotive/{file}", "r")
    token = f.read()
    f.close()
    return token


def write_token(token):
    f = open(token_file_name, "w")
    f.write(token)
    f.close()

# Key stuff
# f = open(str(Path.home())+ "/.remotivelabs/privatekey.json", "r")
# j = json.loads(f.read())
# print(j['privateKey'])
# key = load_pem_private_key(bytes(j['privateKey'],'UTF-8'), None)
# print(key.key_size)
#
# "exp": datetime.now(tz=timezone.utc)
# encoded = jwt.encode({"some": "payload"}, j['privateKey'] , algorithm="RS256", headers={"kid":  j["keyId"]})
# print(encoded)

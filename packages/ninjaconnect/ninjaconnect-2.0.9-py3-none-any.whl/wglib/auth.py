import http.server
import socketserver
import webbrowser
import os
import secrets
from urllib.parse import urlparse, parse_qs
import json
import requests
import keyring
from wglib.storesess import Store
from time import sleep
from rich import print
from rich.progress import Progress
from rich.panel import Panel
from rich.console import Console
import sys
console = Console()
PORT = 5000
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "openid profile email"
# def load_env(file_path=None):
#     if file_path is None:
#         # Get the directory of the script where this function is called
#         script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#         # Construct the path to the .env file relative to the script's directory
#         file_path = os.path.join(script_dir, "wglib/auth.env")

#     try:
#         with open(file_path, "r") as file:
#             lines = file.readlines()
#             for line in lines:
#                 parts = line.strip().split("=")
#                 if len(parts) == 2:
#                     key, value = parts
#                     os.environ[key] = value
#     except FileNotFoundError:
#         print(f"The .env file ({file_path}) was not found.")


# load_env()
CLIENT_ID = "022bd40f1de027c146914ea0a6a1adeb72f39b10c88a01a3d804a0c8a542ba1b"
CLIENT_SECRET = "1ef3abd5e8c5238424cb9e24b0debbb1d9776536b45c7b69c441c251af662cb3"
GITLAB_AUTH_URL = "https://git.selfmade.ninja/oauth/authorize"
GITLAB_TOKEN_URL = "https://git.selfmade.ninja/oauth/token"

state = secrets.token_urlsafe(10)
state_storage = {}

auth_url = f"{GITLAB_AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&state={state}&scope={SCOPE}"


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global token_info
        url = self.path
        callback_url = urlparse(url=url)
        query_params = parse_qs(callback_url.query)
        code = query_params.get("code", [""])[0]
        received_state = query_params.get("state", [""])[0]
        if received_state not in state_storage:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Invalid Authorization failed".encode("utf-8"))
            return

        del state_storage[received_state]
        token_data = {
            "client_id": CLIENT_ID,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "scope": SCOPE,
        }
        login_response = {
            "message": "Gitlab Authorization Successful",
            "status": "success",
        }

        auth_success = json.dumps(login_response)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(auth_success.encode("utf-8"))

        token_response = requests.post(GITLAB_TOKEN_URL, data=token_data)
        if token_response.status_code == 200:
            token_info = token_response.json()


def start_server():
    webbrowser.open(auth_url, new=1)
    with socketserver.TCPServer(("", PORT), CallbackHandler) as server:
        print("Serving on port", PORT)
        server.handle_request()
        server.server_close()


state_storage[state] = True


class GitlabOuth:
    def gitlablogin(self):
        global user_data
        start_server()
        access_token = token_info["access_token"]
        user_info_url = "https://git.selfmade.ninja/oauth/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.post(user_info_url, headers=headers)

        if user_response.status_code == 200:
            try:
                user_data = user_response.json()
                gitlabdata = [
                        "[bold green1]:small_blue_diamond:Gitlab Authentication Successfull :dog_face:[/bold green1]",
                        f"[bold green1]:small_blue_diamond:Name : {user_data['name']}[/bold green1]",
                        f"[bold green1]:small_blue_diamond:Email : {user_data['email']}[/bold green1]"
                ]
                gitlabp = Panel("\n".join(gitlabdata),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style='bold orchid')
                console.print(gitlabp)
            except json.JSONDecodeError as e:
                print(f"Error : {e}")
        else:
            print("Login in git")
        lab_auth = "https://labs.selfmade.ninja/api/app/authorize"
        payload = {
            "access_token": token_info["access_token"],
            "token_type": token_info["token_type"],
            "refresh_token": token_info["refresh_token"],
            "scope": token_info["scope"],
            "id_token": token_info["id_token"],
            "created_at": token_info["created_at"],
        }
        files = []
        lab_response = requests.request("POST", lab_auth, data=payload, files=files)
        labsession = lab_response.cookies.get("PHPSESSID")
        # SERVICENAME = "SNALABS"
        # USERNAME = "SNALABS"
        # PASSWORD = str(labsession)
        # keyring.set_password(SERVICENAME,USERNAME,PASSWORD)
        set = Store()
        set.setkey(labsession)
        if lab_response.status_code == 200:
            try:
                lab_data = lab_response.json()
                labaccessmessage = [
                    "[bold green1]:small_blue_diamond: Labs Authentication Successfull :test_tube:[/bold green1]",
                    f"[bold green1]:small_blue_diamond: {lab_data.get('name')} has lab access :Grinning_Face:[/bold green1]",
                ]
                labacesspanel = Panel("\n".join(labaccessmessage),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style='bold orchid')
                console.print(labacesspanel)
            except requests.exceptions.RequestException as l:
                print(f"Error : {l}")
        else:
            noaccessmessage = [
                f":small_blue_diamond: [red1]{user_data['name']}[/red1] [bold green]has no lab access[/bold green]"
            ]
            noaccesspanel = Panel("\n".join(noaccessmessage),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style='bold orchid')
            console.print(noaccesspanel)

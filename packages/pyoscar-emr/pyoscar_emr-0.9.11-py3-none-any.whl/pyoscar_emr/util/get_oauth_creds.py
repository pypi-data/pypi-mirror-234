from rich import print
from rich.prompt import Prompt
from rich.table import Table

from flask import Flask, request
import polling2
from threading import Thread
from werkzeug.serving import make_server

from requests_oauthlib import OAuth1Session
import webbrowser

import logging
from time import sleep
from urllib.parse import parse_qsl

CALLBACK_PORT = 1231
CALLBACK_HOST = f"localhost"
CALLBACK_URL = f"http://{CALLBACK_HOST}:{CALLBACK_PORT}"


class OAuthRedirectServer(Thread):
    """
    A class that retrieves the appropriate OAuth data from the authorization redirect.
    """

    def __init__(self):
        Thread.__init__(self)

        self.oauth_verifier = ""
        self.oauth_token = ""
        self.oauth_redirect_received = False

        self.daemon = True
        self.app = Flask(__name__)

        @self.app.route("/")
        def get_oauth_tokens_from_redirect():
            self.oauth_verifier = request.args["oauth_verifier"]
            self.oauth_token = request.args["oauth_token"]
            self.oauth_redirect_received = True

            # Run this asynchronously so that it returns the webpage to user before shutting it down
            Thread(target=lambda: self.shutdown()).start()

            return "<div><h1>PyOSCAR</h1><p>Authorization was successful. You can close this tab now and go to your terminal.</p></div>"

        self.server = make_server(CALLBACK_HOST, CALLBACK_PORT, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def shutdown(self):
        # Give some time before actually shutting down for stuff to finish up
        sleep(0.3)
        self.server.shutdown()

    def run(self):
        self.server.serve_forever()


def fetch_request_token(consumer_key: str, consumer_secret: str, base_url: str):
    """
    Fetch temporary credentials given the consumer key & secret.

    Returns the request oauth_token and oauth_token_secret.
    """

    oscar_emr_request = OAuth1Session(
        client_key=consumer_key,
        client_secret=consumer_secret,
        callback_uri=CALLBACK_URL,
    )
    request_res = oscar_emr_request.post(f"{base_url}/ws/oauth/initiate")
    assert (
        request_res.status_code == 200
    ), f"Status code of {request_res.status_code}: consumer key / consumer secret / base_url are likely invalid"

    oauth_info = dict(parse_qsl(request_res.text))
    assert (
        "oauth_callback_confirmed" in oauth_info
    ), "OAuth request token fetch response data is invalid"
    assert (
        oauth_info["oauth_callback_confirmed"] == "true"
    ), "OAuth request token fetch response data is invalid"

    return oauth_info["oauth_token"], oauth_info["oauth_token_secret"]


def fetch_access_creds(
    consumer_key: str,
    consumer_secret: str,
    tmp_token: str,
    tmp_secret: str,
    csrf_verifier: str,
    base_url: str,
):
    """
    Fetch long-lived credentials given the consumer key, temporary token, and CSRF verifier.

    Returns the request oauth_token and oauth_token_secret.
    """

    oscar_emr_request = OAuth1Session(
        client_key=consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=tmp_token,
        resource_owner_secret=tmp_secret,
        verifier=csrf_verifier,
    )
    request_res = oscar_emr_request.post(f"{base_url}/ws/oauth/token")
    assert (
        request_res.status_code == 200
    ), f"Status code of {request_res.status_code}, authorization step likely failed"

    # oauth_info = {key_val.split("=")[0]: key_val.split("=")[1] for key_val in request_res.text.split("&")}
    oauth_info = dict(parse_qsl(request_res.text))
    assert (
        "oauth_token" in oauth_info
    ), "OAuth access creds fetch response data is invalid"
    assert (
        "oauth_token_secret" in oauth_info
    ), "OAuth access creds fetch response data is invalid"

    return oauth_info["oauth_token"], oauth_info["oauth_token_secret"]


def main():
    logging.getLogger("werkzeug").disabled = True

    print("[u bold red]PyOSCAR[/]: OAuth1 Credential Retriever\n")
    print(
        "The OSCAR EMR uses the [bold u]OAuth1 protocol[/bold u] to allow apps to connect to their API on behalf of a provider account."
    )
    print("As such, four keys are required to authenticate to use the API:")

    table = Table(show_header=True, header_style="bold green")
    table.add_column("Name", justify="center")
    table.add_column("Credential Type", justify="center")
    table.add_column("Source", justify="center")
    table.add_row("Consumer Key", "Client / App", "OSCAR EMR: settings page")
    table.add_row("Consumer Secret", "Client / App", "OSCAR EMR: settings page")
    table.add_row("Access Token", "Token / User", "this tool")
    table.add_row("Access Secret", "Token / User", "this tool")
    print(table)
    print()

    print(
        "To use this tool, you will first need to register a [bold blue u]REST Client[/] in your OSCAR EMR instance, and get its [bold green u]consumer key[/] and a [bold green u]consumer secret[/]."
    )
    print(
        f"[bold u]Please use this as the callback URL[/]: {CALLBACK_URL} (a web server will be temporarily hosted by this tool to run the OAuth process)"
    )
    print(
        "You can learn more about registering an app and getting the necessary credentials here: https://oscaremr.atlassian.net/wiki/spaces/OS/pages/79855638/Connecting+to+OSCAR+s+REST+API"
    )
    print()

    print("-----------------------------")
    print("[u green bold]Input your OSCAR EMR instance info[/]")
    base_url = Prompt.ask(
        "Base URL (ex. https://test-instance.kai-oscar.com/oscar, without /)"
    )
    base_url = base_url.removesuffix(
        "/"
    )  # Remove ending / in case if user accidently adds it

    print("\n-----------------------------")
    print("[u green bold]Input your Consumer Credentials[/]")
    consumer_key = Prompt.ask("Consumer Key")
    consumer_secret = Prompt.ask("Consumer Secret")

    # Fetch temporary token and secret, and prepare for auth step
    temp_token, temp_token_secret = fetch_request_token(
        consumer_key=consumer_key, consumer_secret=consumer_secret, base_url=base_url
    )
    authorize_link = f"{base_url}/ws/oauth/authorize?oauth_token={temp_token}"

    # Open link and start redirect server
    print("[green]Opening [bold]app authorization[/bold] in browser...[/green]")
    webbrowser.open(authorize_link)
    print(
        f"If it doesn't open, put this link into your browser: [u orange bold]{authorize_link}[/]"
    )
    # app.run(CALLBACK_HOST, CALLBACK_PORT, False)

    server = OAuthRedirectServer()
    server.start()

    print("[orange]Waiting for redirect...[/]")
    # app.

    # Wait for server to get redirect request
    polling2.poll(lambda: server.oauth_redirect_received, step=0.25, timeout=360)
    assert server.oauth_token != "", "OAuth temporary token was not returned"
    assert server.oauth_verifier != "", "OAuth verifier token was not returned"

    # Get the access credentials
    access_token, access_token_secret = fetch_access_creds(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        tmp_token=temp_token,
        tmp_secret=temp_token_secret,
        csrf_verifier=server.oauth_verifier,
        base_url=base_url,
    )

    print(
        "[green bold u]Your OAuth1 credentials have been successfully fetched![/]\nThese should be stored in a .env file for use with PyOSCAR."
    )
    creds_table = Table(
        show_header=True, header_style="bold green", title_justify="center"
    )
    creds_table.add_column("Name")
    creds_table.add_column("Credential")
    creds_table.add_row("Consumer Key", consumer_key)
    creds_table.add_row("Consumer Secret", consumer_secret)
    creds_table.add_row("Access Token", access_token)
    creds_table.add_row("Access Secret", access_token_secret)
    print(creds_table)


if __name__ == "__main__":
    main()

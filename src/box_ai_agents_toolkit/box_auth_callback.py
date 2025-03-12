"""Handles the call back request from Box OAuth2.0
---
This is a simple HTTP server that listens for a request from Box OAuth2.0.
picking up the code and csrf_token from the query string.
"""

import logging
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from box_sdk_gen import BoxOAuth

CSRF_TOKEN_ORIG = ""
AUTH = None


class CallbackServer(BaseHTTPRequestHandler):
    """
    Creates a mini http request handler to handle a single callback request"""

    def do_GET(self):  # pylint: disable=invalid-name
        """
        Gets the redirect call back from Box OAuth2.0
        capturing the code and csrf_token from the query string
        and calls for the completion of the OAuth2.0 process.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        code = " ".join(params.get("code")) if params.get("code") else None
        state = " ".join(params.get("state")) if params.get("state") else None
        error = " ".join(params.get("error")) if params.get("error") else None
        error_description = (
            " ".join(params.get("error_description"))
            if params.get("error_description")
            else None
        )

        logging.info("code: %s", code)
        logging.info("state: %s", state)
        logging.info("error: %s", error)
        logging.info("error_description: %s", error_description)

        if state != CSRF_TOKEN_ORIG:
            error = "Invalid State token"
            error_description = (
                "The unique state token send is not the same one received."
            )

        if error:
            html_response = f"""
            <html>
                <head>
                    <title>Box Authentication Error</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding-top: 50px;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f9f9f9;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        }}
                        h1 {{
                            color: #c82124;
                        }}
                        p {{
                            font-size: 16px;
                            line-height: 1.5;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Box authorization error</h1>
                        <p>An error occurred during authorization.</p>
                        <p>Error: {error}</p>
                        <p>Error Description: {error_description}</p>
                    </div>
                </body>
            </html>
            """

        if code:
            AUTH.get_tokens_authorization_code_grant(code)
            html_response = """
            <html>
                <head>
                    <title>Box Authentication Successful</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding-top: 50px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f9f9f9;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        }
                        h1 {
                            color: #0061d5;
                        }
                        p {
                            font-size: 16px;
                            line-height: 1.5;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Success!</h1>
                        <p>Authorization completed successfully.</p> 
                        <p>You can now close this window and return to the application.</p>
                    </div>
                </body>
            </html>
            """

        self.wfile.write(
            bytes(html_response, "utf-8"),
        )


def callback_handle_request(auth: BoxOAuth, hostname, port, csrf_token: str):
    """
    Handles the call back request from Box OAuth2.0
    Creates a simple HTTP server that listens for a request from Box OAuth2.0.
    """
    global CSRF_TOKEN_ORIG  # pylint: disable=global-statement
    CSRF_TOKEN_ORIG = csrf_token
    global AUTH  # pylint: disable=global-statement
    AUTH = auth

    web_server = HTTPServer((hostname, port), CallbackServer)

    logging.info(
        "Server started http://%s:%s",
        hostname,
        port,
    )

    try:
        web_server.handle_request()
    finally:
        web_server.server_close()

    logging.info("Server stopped.")


def open_browser(auth_url: str):
    """
    Opens a browser to the auth_url
    """
    webbrowser.open(auth_url)

# config/fullautomatedtoken.py
import praw
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import webbrowser
import json
import os

CLIENT_ID = "5TwM5fD6Cr-Xe1wzT410Uw"
REDIRECT_URI = "http://localhost:8080"
USER_AGENT = "CarbonTrackerDesktop by u/TooGlamToGiveADamn_"
SCOPES = ["identity", "read", "history", "vote"]
STATE = "carbonapp_state"

TOKEN_FILE = "token.json"


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse.urlparse(self.path).query
        params = urlparse.parse_qs(query)
        code = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"You can close this tab now.")
        self.server.code = code


def get_code_from_redirect():
    httpd = HTTPServer(("localhost", 8080), RedirectHandler)
    print("🌐 Waiting for Reddit login redirect...")
    httpd.handle_request()
    return httpd.code


def save_refresh_token(token):
    data = {"refresh_token": token}
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print("💾 Refresh token saved to", TOKEN_FILE)


def load_refresh_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("refresh_token")
    return None


def get_authenticated_reddit():
    """Returns an authenticated Reddit instance, logging in only if necessary."""
    refresh_token = load_refresh_token()

    if not refresh_token:
        print("🔐 No refresh token found — starting login flow...")
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=None,
            redirect_uri=REDIRECT_URI,
            user_agent=USER_AGENT,
        )
        auth_url = reddit.auth.url(SCOPES, STATE, "permanent")
        print("🔗 Open this URL in your browser:", auth_url)
        webbrowser.open(auth_url)

        code = get_code_from_redirect()
        refresh_token = reddit.auth.authorize(code)
        save_refresh_token(refresh_token)
        print("✅ Refresh token obtained and stored!")

    # Always return a logged-in Reddit instance
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        refresh_token=refresh_token,
        user_agent=USER_AGENT,
    )
    print("✅ Logged in as:", reddit.user.me())
    return reddit


if __name__ == "__main__":
    # Just test authentication when run directly
    reddit = get_authenticated_reddit()

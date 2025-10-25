import praw
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import webbrowser

# ====== CONFIGURATION ======
CLIENT_ID = "5TwM5fD6Cr-Xe1wzT410Uw"
REDIRECT_URI = "http://localhost:8080"  # use local server for testing
USER_AGENT = "CarbonTrackerDesktop by u/TooGlamToGiveADamn_"
SCOPES = ["identity", "read", "history", "vote"]
STATE = "carbonapp_state"
# ============================

def get_authorization_url():
    """
    Generates a Reddit OAuth URL for user login.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,  # installed apps don't use secrets
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT
    )

    auth_url = reddit.auth.url(SCOPES, STATE, "permanent")
    return auth_url


class RedirectHandler(BaseHTTPRequestHandler):
    """
    Handles the OAuth redirect from Reddit and extracts the code.
    """
    def do_GET(self):
        query = urlparse.urlparse(self.path).query
        params = urlparse.parse_qs(query)
        code = params.get("code", [None])[0]
        print("\n✅ Authorization code received:", code)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"You can close this browser tab now.")
        self.server.code = code  # save code to server object


def get_code_from_redirect():
    """
    Starts a local HTTP server to capture the redirect from Reddit login.
    """
    httpd = HTTPServer(("localhost", 8080), RedirectHandler)
    print("\n🌐 Waiting for Reddit redirect on http://localhost:8080 ...")
    httpd.handle_request()  # Wait for one redirect
    return httpd.code


def get_refresh_token(code: str):
    """
    Exchanges the authorization code for a refresh token.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT
    )
    refresh_token = reddit.auth.authorize(code)
    print("\n✅ Refresh token generated:", refresh_token)
    return refresh_token


def get_reddit_instance(refresh_token: str):
    """
    Returns an authenticated Reddit instance using a saved refresh token.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        refresh_token=refresh_token,
        user_agent=USER_AGENT
    )
    print("\n🔐 Reddit instance authenticated successfully.")
    return reddit


if __name__ == "__main__":
    print("=== Reddit OAuth Setup (Desktop Test) ===")

    # Step 1: Generate auth URL
    auth_url = get_authorization_url()
    print("\n🔗 Open this URL in your browser to log in:")
    print(auth_url)

    # Optional: automatically open in default browser
    webbrowser.open(auth_url)

    # Step 2: Start local server to capture redirect
    code = get_code_from_redirect()

    # Step 3: Exchange code for refresh token
    refresh_token = get_refresh_token(code)

    # Step 4: Get authenticated Reddit instance
    reddit = get_reddit_instance(refresh_token)
    print("Logged in as:", reddit.user.me())

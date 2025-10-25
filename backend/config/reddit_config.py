import praw
import urllib.parse as urlparse

# ====== CONFIGURATION ======
CLIENT_ID = "5TwM5fD6Cr-Xe1wzT410Uw"
REDIRECT_URI = "com.user.carbonapp://auth"
USER_AGENT = "CarbonTrackerMobile by u/TooGlamToGiveADamn_"
SCOPES = ["identity", "read", "history", "vote"]

# ============================

def get_authorization_url():
    """
    Generates a Reddit OAuth URL that the user needs to visit to grant permissions.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,  # Installed apps don't use secrets
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT
    )

    auth_url = reddit.auth.url(SCOPES, "carbonapp_state", "permanent")
    print("\n🔗 Open this URL in your browser or WebView to log in:")
    print(auth_url)
    return auth_url


def get_refresh_token(redirect_response_url: str):
    """
    Extracts the 'code' from the redirect URI and exchanges it for a refresh token.
    Example redirect_response_url:
      com.user.carbonapp://auth?state=carbonapp_state&code=XYZ
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT
    )

    parsed = urlparse.urlparse(redirect_response_url)
    code = urlparse.parse_qs(parsed.query).get("code", [None])[0]

    if not code:
        raise ValueError("No authorization code found in redirect URL.")

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
    print("=== Reddit OAuth Setup for Installed App ===")

    # Step 1: Get the authorization URL
    url = get_authorization_url()

    # Step 2: After the user logs in and Reddit redirects to your app,
    # paste the full redirect URI (from your app or browser)
    redirect_url = input("\nPaste the full redirect URL here: ").strip()

    # Step 3: Exchange for a refresh token
    token = get_refresh_token(redirect_url)

    # Step 4: Test Reddit connection
    reddit = get_reddit_instance(token)
    print("Logged in as:", reddit.user.me())

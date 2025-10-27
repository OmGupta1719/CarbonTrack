import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ✅ ensure parent folder is importable

from config.fullautomatedtoken import get_authenticated_reddit as get_reddit_instance


def get_reddit_client():
    """Create an authenticated Reddit client using saved credentials."""
    reddit = get_reddit_instance()  # Automatically loads or refreshes token
    return reddit


def estimate_votes(submission):
    """
    Estimate upvotes and downvotes using Reddit's upvote_ratio and score.
    Formula:
        upvotes = (ratio * score) / (2 * ratio - 1)
        downvotes = upvotes - score
    """
    ratio = submission.upvote_ratio
    score = submission.score

    if ratio in (0.5, 0, 1):
        upvotes = max(0, score if score > 0 else 0)
        downvotes = 0
    else:
        try:
            upvotes = (ratio * score) / (2 * ratio - 1)
            downvotes = upvotes - score
        except ZeroDivisionError:
            upvotes, downvotes = score, 0

    return {
        "upvotes": round(max(0, upvotes)),
        "downvotes": round(max(0, downvotes))
    }


def fetch_user_metadata(reddit):
    """Fetch basic user info for summary metrics."""
    user = reddit.user.me()
    created_utc = datetime.utcfromtimestamp(user.created_utc)
    account_age_days = (datetime.utcnow() - created_utc).days

    return {
        "username": str(user.name),
        "account_age_days": account_age_days,
        "comment_karma": user.comment_karma,
        "link_karma": user.link_karma
    }


def fetch_user_submissions(limit=50):
    """Fetch user submissions with engagement and vote info."""
    reddit = get_reddit_client()
    data = []

    for submission in reddit.user.me().submissions.new(limit=limit):
        votes = estimate_votes(submission)
        data.append({
            "id": submission.id,
            "title": submission.title,
            "selftext": getattr(submission, "selftext", ""),
            "score": submission.score,
            "num_comments": submission.num_comments,
            "upvote_ratio": submission.upvote_ratio,
            "subreddit": str(submission.subreddit),
            "is_video": submission.is_video,
            "is_self": submission.is_self,
            "url": submission.url,
            "upvotes": votes["upvotes"],
            "downvotes": votes["downvotes"]
        })
    return data


def fetch_user_comments(limit=50):
    """Fetch latest user comments."""
    reddit = get_reddit_client()
    data = []
    for comment in reddit.user.me().comments.new(limit=limit):
        data.append({
            "id": comment.id,
            "body": comment.body,
            "score": comment.score,
            "is_submitter": comment.is_submitter
        })
    return data

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ✅ ensure parent folder is importable

from config.fullautomatedtoken import get_authenticated_reddit as get_reddit_instance

def get_reddit_client():
    """Create an authenticated Reddit client using saved credentials."""
    reddit = get_reddit_instance()   # Automatically loads or refreshes token
    return reddit


def fetch_user_submissions(limit=50):
    reddit = get_reddit_client()
    data = []
    for submission in reddit.user.me().submissions.new(limit=limit):
        data.append({
            "id": submission.id,
            "title": submission.title,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "upvote_ratio": submission.upvote_ratio,
            "url": submission.url
        })
    return data


def fetch_user_comments(limit=50):
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

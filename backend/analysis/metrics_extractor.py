# analysis/metrics_extractor.py

def extract_submission_metrics(submission):
    """
    Extracts numerical and text-based metrics from a submission dictionary.
    """
    metrics = {}

    # Text-based
    metrics["title_length"] = len(submission.get("title", ""))
    metrics["selftext_length"] = len(submission.get("selftext", ""))

    # Numerical
    metrics["score"] = submission.get("score", 0)
    metrics["upvote_ratio"] = submission.get("upvote_ratio", 0.0)
    metrics["num_comments"] = submission.get("num_comments", 0)
    metrics["upvotes"] = submission.get("upvotes", 0)
    metrics["downvotes"] = submission.get("downvotes", 0)
    metrics["subreddit"] = submission.get("subreddit", "")
    metrics["is_video"] = submission.get("is_video", False)
    metrics["is_self"] = submission.get("is_self", False)

    # Derived metrics
    metrics["engagement"] = metrics["score"] + metrics["num_comments"]
    metrics["media_intensity"] = 1 if metrics["is_video"] else (0.5 if not metrics["is_self"] else 0)

    return metrics


def extract_comment_metrics(comment):
    """Extracts simple metrics from a comment dictionary."""
    metrics = {}
    metrics["body_length"] = len(comment.get("body", ""))
    metrics["score"] = comment.get("score", 0)
    metrics["is_submitter"] = comment.get("is_submitter", False)
    return metrics

import math

def extract_submission_metrics(submission):
    """
    Extracts simple numerical and text-based metrics from a submission dictionary.
    """
    metrics = {}

    # Text-based metrics
    metrics["title_length"] = len(submission.get("title", ""))

    # Numerical metrics
    metrics["score"] = submission.get("score", 0)
    metrics["upvote_ratio"] = submission.get("upvote_ratio", 0.0)
    metrics["num_comments"] = submission.get("num_comments", 0)

    # Optional: you can add more computed metrics here
    # For example, engagement level
    metrics["engagement"] = submission.get("score", 0) + submission.get("num_comments", 0)

    return metrics


def extract_comment_metrics(comment):
    """
    Extracts simple metrics from a comment dictionary.
    """
    metrics = {}
    metrics["body_length"] = len(comment.get("body", ""))
    metrics["score"] = comment.get("score", 0)
    metrics["is_submitter"] = comment.get("is_submitter", False)
    return metrics

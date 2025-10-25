def get_comment_type(body):
    text = body.lower()
    if any(x in text for x in ["i.redd.it", "imgur.com", "giphy.com", ".gif"]):
        return "image/gif"
    elif "http://" in text or "https://" in text:
        return "link"
    elif "/r/" in text and "/comments/" in text:
        return "crosspost"
    else:
        return "text"

def process_comment(comment, depth=0):
    """
    Recursively extracts data for a comment and its nested replies.
    """
    data = {
        "id": comment.id,
        "body_length": len(comment.body),
        "type": get_comment_type(comment.body),
        "ups": comment.ups,
        "downs": getattr(comment, "downs", 0),
        "score": comment.score,
        "depth": depth,
        "replies_count": len(comment.replies),
        "awards": comment.gilded,
    }

    replies_data = []
    if hasattr(comment, "replies"):
        for reply in comment.replies:
            replies_data.append(process_comment(reply, depth + 1))
    
    data["replies"] = replies_data
    return data

def estimate_post_carbon(metrics):
    """
    Estimate carbon emission for a single post using its extracted metrics.
    Simplified model using engagement and content-based features.
    """

    # Safely get values with defaults to avoid KeyErrors
    score = metrics.get("score", 0)
    num_comments = metrics.get("num_comments", 0)
    title_length = metrics.get("title_length", 0)
    upvote_ratio = metrics.get("upvote_ratio", 1.0)

    # Basic constants (gCO2e = grams of CO2 equivalent)
    base_post = 0.05                     # Base storage & indexing footprint
    per_comment = 0.02 * num_comments    # Comment activity impact
    per_score = 0.005 * score            # Approximate upvote/visibility impact
    text_impact = 0.0001 * title_length  # Title text size impact
    visibility_factor = 1 + (upvote_ratio - 0.5)  # Scale by visibility/popularity

    # Total estimated carbon for this post
    estimated_carbon = (base_post + per_comment + per_score + text_impact) * visibility_factor
    return round(estimated_carbon, 4)


def estimate_comment_carbon(comment_data):
    """
    Recursively calculate carbon impact for nested comments (dictionary-based).
    """

    score = comment_data.get("score", 0)
    body_length = comment_data.get("body_length", 0)
    replies_count = comment_data.get("replies_count", 0)
    replies = comment_data.get("replies", [])

    base = 0.01                               # Base storage cost per comment
    upvote_impact = 0.005 * score             # Upvote/interaction cost
    text_impact = 0.00005 * body_length       # Based on text length
    replies_impact = 0.01 * replies_count     # Additional cost for reply depth

    total = base + upvote_impact + text_impact + replies_impact

    # Recursively include replies
    for reply in replies:
        total += estimate_comment_carbon(reply)

    return round(total, 4)

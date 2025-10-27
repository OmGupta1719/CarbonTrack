# analysis/carbon_estimator.py

def estimate_daily_carbon(summary):
    """
    Estimate total carbon footprint (gCO₂e) for a Reddit user based on
    scientifically derived constants.
    Formula:
    CFP = (A × 0.001 / 365)
         + (0.0323 × Pself)
         + (0.503 × Pvideo)
         + (0.0152 × C)
         + (0.00736 × (U + D))
    """

    A = summary.get("account_age_days", 0)
    Pself = summary.get("total_self_posts", 0)
    Pvideo = summary.get("total_video_posts", 0)
    C = summary.get("total_comments", 0)
    U = summary.get("total_upvotes_posts", 0)
    D = summary.get("total_downvotes_posts", 0)

    cfp = (A * 0.001 / 365) + (0.0323 * Pself) + (0.503 * Pvideo) + (0.0152 * C) + (0.00736 * (U + D))
    return round(cfp, 3)


def estimate_post_carbon(metrics):
    """Estimate carbon per post (for breakdown view)."""
    if metrics.get("is_video"):
        return 0.503
    elif metrics.get("is_self"):
        return 0.0323
    else:
        # link or image type post (approximate to text)
        return 0.0323 * 0.5


def estimate_comment_carbon(_comment):
    """Each comment ≈ 0.0152 gCO₂e."""
    return 0.0152

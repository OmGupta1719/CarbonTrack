# server.py
from flask import Flask, jsonify, request
from reddit_api.fetch_user_data import (
    fetch_user_submissions,
    fetch_user_comments,
    fetch_user_metadata,
    get_reddit_client,
)
from analysis.metrics_extractor import extract_submission_metrics
from analysis.carbon_estimator import (
    estimate_post_carbon,
    estimate_comment_carbon,
    estimate_daily_carbon,
)

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "✅ CarbonTrack API is running"})


@app.route("/calculate", methods=["GET"])
def calculate_footprint():
    """
    Endpoint to fetch Reddit user data and calculate carbon footprint.
    """
    try:
        print("🔐 Authenticating Reddit user...")
        reddit = get_reddit_client()
        user_info = fetch_user_metadata(reddit)
        submissions = fetch_user_submissions(limit=50)
        comments = fetch_user_comments(limit=50)

        print(f"✅ Logged in as: {user_info['username']}")
        print("📊 Processing posts and comments...")

        results = []
        total_upvotes_posts = 0
        total_downvotes_posts = 0
        total_media_intensity = 0
        total_self_posts = 0
        total_video_posts = 0

        for s in submissions:
            s_metrics = extract_submission_metrics(s)
            post_carbon = estimate_post_carbon(s_metrics)
            s_metrics["post_carbon_gCO2e"] = round(post_carbon, 3)
            results.append(s_metrics)

            total_upvotes_posts += s_metrics.get("upvotes", 0)
            total_downvotes_posts += s_metrics.get("downvotes", 0)
            total_media_intensity += s_metrics.get("media_intensity", 0)
            if s_metrics.get("is_video"):
                total_video_posts += 1
            if s_metrics.get("is_self"):
                total_self_posts += 1

        avg_media_intensity = total_media_intensity / len(submissions) if submissions else 0
        comments_carbon_total = sum(estimate_comment_carbon(c) for c in comments)

        summary = {
            "username": user_info["username"],
            "account_age_days": user_info["account_age_days"],
            "comment_karma": user_info["comment_karma"],
            "link_karma": user_info["link_karma"],
            "total_posts": len(submissions),
            "total_comments": len(comments),
            "total_self_posts": total_self_posts,
            "total_video_posts": total_video_posts,
            "total_upvotes_posts": total_upvotes_posts,
            "total_downvotes_posts": total_downvotes_posts,
            "media_intensity": round(avg_media_intensity, 3),
        }

        total_carbon = estimate_daily_carbon(summary)
        summary["total_carbon_gCO2e"] = total_carbon

        output = {"summary": summary, "detailed": results}

        print("✅ Done! Returning JSON response.")
        return jsonify(output)

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run on all interfaces so your phone/emulator can access
    app.run(host="0.0.0.0", port=5000)

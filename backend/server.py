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
import os
import requests # Import requests for making HTTP calls

app = Flask(__name__)

# Note: Removed genai import and configuration as we'll use requests

@app.route("/")
def home():
    return jsonify({"message": "✅ CarbonTrack API is running"})

@app.route("/calculate", methods=["GET"])
def calculate_footprint():
    try:
        reddit = get_reddit_client()
        user_info = fetch_user_metadata(reddit)
        submissions = fetch_user_submissions(limit=50)
        comments = fetch_user_comments(limit=50)

        total_upvotes_posts = 0
        total_downvotes_posts = 0
        total_media_intensity = 0
        total_self_posts = 0
        total_video_posts = 0
        results = []

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

        avg_media_intensity = (total_media_intensity / len(submissions)) if submissions else 0
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
        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def generate_recommendation():
    try:
        data = request.json or {}
        summary = data.get("summary", {})
        total_carbon = estimate_daily_carbon(summary)
        summary["total_carbon_gCO2e"] = total_carbon

        username = summary.get("username", "User")
        carbon = summary.get("total_carbon_gCO2e", 0.0)
        posts = summary.get("total_posts", 0)
        comments = summary.get("total_comments", 0)
        media_intensity = summary.get("media_intensity", 0.0)
        videos = summary.get("total_video_posts", 0)
        age = summary.get("account_age_days", 0)

        # Separate System Instruction and User Query as per instructions
        system_prompt = """
        You are CarbonTrack, an eco-awareness assistant.
        Generate a friendly, unique recommendation in half sentence for how this user
        can reduce their digital carbon footprint or act more sustainably online.
        eg: 1.Great job! You’re keeping emissions super low — stay consistent!
        2.Try turning off background data or reduce streaming quality.
        3.Moderate emissions — consider taking short digital breaks daily.
        4.High footprint! Time to cut down usage and enable dark mode.
        5.Extremely high! You’d need x trees to offset this. Time for serious change!
        """
        
        user_query = f"""
        User: {username}
        Account age: {age} days
        Total posts: {posts}, Comments: {comments}, Video posts: {videos}, Media intensity: {media_intensity}
        Daily digital carbon footprint: {carbon} gCO₂e
        """
        
        # API key is left empty as per instructions (will be provided by environment)
        api_key = "" 
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=AIzaSyCjdGvs39K8wXmxSajFjCV281YflgIuiqE"

        # Construct the payload
        payload = {
            "contents": [{ "parts": [{ "text": user_query }] }],
            "systemInstruction": {
                "parts": [{ "text": system_prompt }]
            },
        }

        # Make the POST request to the Gemini API
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            json=payload
        )

        # Check for HTTP errors
        response.raise_for_status() 

        # Parse the JSON response
        result = response.json()

        # Safely extract the generated text
        try:
            recommendation = result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError):
            recommendation = "No recommendation could be generated at this time."

        return jsonify({
            "username": username,
            "carbon_footprint_gCO2e": carbon,
            "recommendation": recommendation.strip()
        })

    except requests.exceptions.RequestException as re:
        # Handle network or API errors
        return jsonify({
            "error": "API request failed",
            "details": str(re)
        }), 500
    except Exception as e:
        # Handle other errors (e.g., JSON parsing)
        return jsonify({
            "error": "Recommendation generation failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
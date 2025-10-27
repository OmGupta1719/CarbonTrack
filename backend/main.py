import json
from reddit_api.fetch_user_data import fetch_user_submissions, fetch_user_comments
from analysis.metrics_extractor import extract_submission_metrics
from analysis.carbon_estimator import estimate_post_carbon, estimate_comment_carbon


def main():
    print("🔐 Fetching your Reddit account data...")

    # Fetch data
    submissions = fetch_user_submissions(limit=50)
    comments = fetch_user_comments(limit=50)

    print("✅ Logged in and fetched data successfully.")
    print("📊 Processing posts and comments...")

    results = []

    # Process posts
    for s in submissions:
        s_metrics = extract_submission_metrics(s)
        post_carbon = estimate_post_carbon(s_metrics)
        s_metrics["post_carbon_gCO2e"] = round(post_carbon, 3)
        results.append(s_metrics)

    # Process comments separately
    comments_carbon_total = 0
    for c in comments:
        comments_carbon_total += estimate_comment_carbon(c)

    print(f"✅ Processed {len(submissions)} posts and {len(comments)} comments.")

    # Combine total carbon
    total_carbon = sum(r["post_carbon_gCO2e"] for r in results) + comments_carbon_total
    summary = {
        "total_posts": len(submissions),
        "total_comments": len(comments),
        "total_carbon_gCO2e": round(total_carbon, 3),
    }

    # Save both detailed and summary results
    output = {
        "summary": summary,
        "detailed": results
    }

    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("📁 Results saved to output/results.json")
    print("🌍 Total estimated footprint:", round(total_carbon, 3), "gCO2e")


if __name__ == "__main__":
    main()

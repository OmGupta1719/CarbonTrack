import json
from reddit_api.fetch_user_data import fetch_user_submissions, fetch_user_comments
from analysis.metrics_extractor import extract_submission_metrics
from analysis.carbon_estimator import estimate_post_carbon, estimate_comment_carbon

def main():
    print("🔐 Fetching your Reddit account data...")
    submissions = fetch_user_submissions(limit=50)
    comments = fetch_user_comments(limit=50)
    
    print("📊 Processing posts and comments...")
    results = []

    for s in submissions:
        s_metrics = extract_submission_metrics(s)
        post_carbon = estimate_post_carbon(s_metrics)
        comments_carbon = sum(
            estimate_comment_carbon(c) for c in s_metrics["comments_data"]
        )

        total_carbon = post_carbon + comments_carbon
        s_metrics["total_carbon_gCO2e"] = round(total_carbon, 3)
        results.append(s_metrics)

    print(f"✅ Processed {len(results)} posts. Saving results...")

    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("📁 Results saved to output/results.json")

if __name__ == "__main__":
    main()

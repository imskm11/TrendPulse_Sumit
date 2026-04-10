import pandas as pd
import os

# Input file from Task 2
INPUT_FILE = "data/trends_cleaned.csv"


def main():
    # Check file exists
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    # Load data
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("\n===== TrendPulse Analysis =====\n")

    # -----------------------------
    # 1. Total posts per category
    # -----------------------------
    print("1. Total posts per category:")
    print(df["category"].value_counts(), "\n")

    # -----------------------------
    # 2. Average score per category
    # -----------------------------
    print("2. Average score per category:")
    print(df.groupby("category")["score"].mean().round(2), "\n")

    # -----------------------------
    # 3. Average comments per category
    # -----------------------------
    print("3. Average comments per category:")
    print(df.groupby("category")["num_comments"].mean().round(2), "\n")

    # -----------------------------
    # 4. Top 5 highest scored posts
    # -----------------------------
    print("4. Top 5 highest scored posts:")
    top_posts = df.sort_values(by="score", ascending=False).head(5)
    print(top_posts[["title", "category", "score"]], "\n")

    # -----------------------------
    # 5. Most active authors
    # -----------------------------
    print("5. Most active authors:")
    print(df["author"].value_counts().head(5), "\n")

    # -----------------------------
    # 6. Category with highest engagement
    # Engagement = score + comments
    # -----------------------------
    df["engagement"] = df["score"] + df["num_comments"]

    engagement_by_category = df.groupby("category")["engagement"].mean()
    best_category = engagement_by_category.idxmax()

    print("6. Category with highest engagement:")
    print(engagement_by_category.round(2))
    print(f"\n🔥 Highest engagement category: {best_category}")


if __name__ == "__main__":
    main()
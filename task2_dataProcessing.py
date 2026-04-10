import pandas as pd
import json
import os

# Input JSON file (update date if needed)
INPUT_FILE = "data/trends_20240115.json"

# Output CSV file
OUTPUT_FILE = "data/trends_clean.csv"


def main():
    
    # 1. Load JSON file
    
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    df = pd.DataFrame(data)

    print(f"Loaded {len(df)} stories from {INPUT_FILE}\n")

    
    # 2. Clean the Data
    

    # Remove duplicates based on post_id
    before = len(df)
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # Remove missing values (post_id, title, score)
    before = len(df)
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Convert data types
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

    # Fill NaN in num_comments with 0
    df["num_comments"] = df["num_comments"].fillna(0)

    # Convert to integer
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Remove low-quality stories (score < 5)
    before = len(df)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}\n")

    # Clean whitespace in title
    df["title"] = df["title"].str.strip()

    
    # 3. Save to CSV
    
    try:
        df.to_csv(OUTPUT_FILE, index=False)
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return

    print(f"Saved {len(df)} rows to {OUTPUT_FILE}\n")

    print("Stories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()
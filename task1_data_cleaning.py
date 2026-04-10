import json
import os
import pandas as pd

# File path (update if needed)
INPUT_FILE = "data/trends_20240115.json"  # change date accordingly
OUTPUT_FILE = "data/trends_cleaned.csv"


def main():
    # Check if file exists
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    # Load JSON data
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    print(f"Original records: {len(df)}")


    # 1. Drop rows with missing essential fields
    df.dropna(subset=["post_id", "title", "category"], inplace=True)

    # 2. Remove duplicate posts (based on post_id)
    df.drop_duplicates(subset=["post_id"], inplace=True)

    # 3. Clean text (remove extra spaces)
    df["title"] = df["title"].str.strip()
    df["author"] = df["author"].astype(str).str.strip()

    # 4. Fix data types
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # 5. Ensure category is lowercase (consistency)
    df["category"] = df["category"].str.lower()

    
    print(f"Cleaned records: {len(df)}")

    # Save to CSV
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Cleaned data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving CSV: {e}")


if __name__ == "__main__":
    main()
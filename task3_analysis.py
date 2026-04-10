import pandas as pd
import numpy as np
import os

# Input file from Task 2
INPUT_FILE = "data/trends_clean.csv"

# Output file for Task 4
OUTPUT_FILE = "data/trends_analysed.csv"


def main():
    
    # 1. Load and Explore Data
    
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    print(f"Loaded data: {df.shape}\n")

    print("First 5 rows:")
    print(df.head(), "\n")

    # Average score and comments
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"Average score   : {round(avg_score, 2)}")
    print(f"Average comments: {round(avg_comments, 2)}\n")

    
    # 2. NumPy Analysis
    
    scores = df["score"].values
    comments = df["num_comments"].values

    print("--- NumPy Stats ---")

    # Mean, Median, Std
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)

    print(f"Mean score   : {round(mean_score, 2)}")
    print(f"Median score : {round(median_score, 2)}")
    print(f"Std deviation: {round(std_score, 2)}")

    # Max and Min
    max_score = np.max(scores)
    min_score = np.min(scores)

    print(f"Max score    : {max_score}")
    print(f"Min score    : {min_score}\n")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_count = category_counts.max()

    print(f"Most stories in: {top_category} ({top_count} stories)\n")

    # Most commented story
    max_comments_index = np.argmax(comments)
    top_story = df.iloc[max_comments_index]

    print(f'Most commented story: "{top_story["title"]}" — {top_story["num_comments"]} comments\n')

    
    # 3. Add New Columns
    

    # Engagement = comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = score > average score
    df["is_popular"] = df["score"] > avg_score

    
    # 4. Save Result
    
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()
import pandas as pd
import matplotlib.pyplot as plt
import os

# Input file from Task 3
INPUT_FILE = "data/trends_analysed.csv"

# Output folder
OUTPUT_FOLDER = "outputs"


def shorten_title(title, max_length=50):
    """
    Shortens long titles to keep charts readable
    """
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title


def main():
    
    # 1. Setup
    
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    # Load data
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Created outputs folder if not exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print("Data loaded. Creating charts...\n")

    
    # 2. Chart 1: Top 10 Stories
    
    top10 = df.sort_values(by="score", ascending=False).head(10)

    titles = [shorten_title(t) for t in top10["title"]]
    scores = top10["score"]

    plt.figure()
    plt.barh(titles, scores)
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()  # highest on top
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_FOLDER}/chart1_top_stories.png")
    plt.show()

    
    # 3. Chart 2: Stories per Category
    
    category_counts = df["category"].value_counts()

    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_FOLDER}/chart2_categories.png")
    plt.show()

    
    # 4. Chart 3: Scatter Plot
    
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_FOLDER}/chart3_scatter.png")
    plt.show()

    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1 in dashboard
    axes[0].barh(titles, scores)
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2 in dashboard
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")
    axes[1].tick_params(axis='x', rotation=45)

    # Chart 3 in dashboard
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    plt.suptitle("TrendPulse Dashboard")
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_FOLDER}/dashboard.png")
    plt.show()

    print("All charts saved in 'outputs/' folder ✅")


if __name__ == "__main__":
    main()
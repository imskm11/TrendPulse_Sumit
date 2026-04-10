import requests
import json
import os
import time
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Headers (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and their keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to categorize story based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  


def main():
    print("Fetching top stories...")

    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]  
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    collected_data = []
    category_count = {cat: 0 for cat in CATEGORIES}

    for story_id in story_ids:
        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            res.raise_for_status()
            story = res.json()
        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

        # Skip if no title
        if not story or "title" not in story:
            continue

        category = get_category(story["title"])

        # Skip if no category match
        if not category:
            continue

        # Limit 25 stories per category
        if category_count[category] >= 25:
            continue

        # Extract required fields
        data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(data)
        category_count[category] += 1

        # Stop if all categories filled
        if all(count >= 25 for count in category_count.values()):
            break

    # Sleep once per category loop (as required)
    for _ in CATEGORIES:
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
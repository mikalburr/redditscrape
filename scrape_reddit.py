import praw
import json
import os

# Get credentials from environment variables
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "default_reddit_bot")

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=USER_AGENT
)

def scrape_comments(post_url):
    """Scrape comments from a Reddit post."""
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)

    comments = []
    for comment in submission.comments:
        comments.append({
            "username": comment.author.name if comment.author else "[deleted]",
            "text": comment.body,
            "score": comment.score,
            "timestamp": comment.created_utc
        })

    # Save to JSON file
    with open("reddit_comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=4)

    print(f"✅ Scraped {len(comments)} comments from {post_url}")

# Example Post URL
post_url = "https://www.reddit.com/r/technology/comments/abcd123/"  # Replace with your URL
scrape_comments(post_url)

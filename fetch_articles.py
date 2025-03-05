# This script fetches news articles from NewsAPI and RSS feeds.
# It loads sources from sources.json and retrieves only new articles.
# NewsAPI requests use the "from" parameter to avoid fetching duplicates.
# RSS feeds are checked using common feed patterns.
# Existing articles are tracked to prevent duplicates.
# All fetched articles are saved to articles.json and accumulate over time.
# The last fetch date is stored in last_fetch.json to optimize API usage.

import requests
import re
import feedparser
import json
import os
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

# Configurations
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"
LAST_FETCH_FILE = "last_fetch.json"
ARTICLES_FILE = "articles.json"

# Load sources.json 
with open("sources.json", "r") as f:
    sources_data = json.load(f)

newsapi_sources = sources_data.get("newsapi", [])
rss_sources = sources_data.get("rss", [])

# Load last fetch date
if os.path.exists(LAST_FETCH_FILE):
    with open(LAST_FETCH_FILE, "r") as f:
        last_fetch_data = json.load(f)
        last_fetch_date = last_fetch_data.get("last_fetch_date", None)
else:
    last_fetch_date = None

# Set fetch date range
if last_fetch_date:
    from_date = datetime.strptime(last_fetch_date, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)
else:
    from_date = datetime.now(timezone.utc) - timedelta(days=30)  # Default is last 30 days

# Update last fetch date
current_fetch_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
with open(LAST_FETCH_FILE, "w") as f:
    json.dump({"last_fetch_date": current_fetch_date}, f)

# Load existing articles
if os.path.exists(ARTICLES_FILE):
    with open(ARTICLES_FILE, "r") as f:
        articles = json.load(f)
else:
    articles = []

# Function to check for duplicate articles
def is_duplicate(article_url):
    return any(article["url"] == article_url for article in articles)

# Function to clean HTML content and limit description to 2 periods at most for RSS fetches
def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text().strip()  
    sentences = re.split(r'(?<=\.)\s+', text) 
    return " ".join(sentences[:2])  

# Fetch articles from NewsAPI
for outlet in newsapi_sources:
    params = {
        "domains": outlet,
        "apiKey": NEWS_API_KEY,
        "from": from_date.strftime("%Y-%m-%d"),
    }
    response = requests.get(NEWS_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for article in data.get("articles", []):
            if not is_duplicate(article["url"]):
                articles.append({
                    "source": {
                        "id": article["source"].get("id"),
                        "name": article["source"].get("name")
                    },
                    "author": article.get("author"),
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "publishedAt": article["publishedAt"],
                })

# Common RSS feed patterns
RSS_PATTERNS = [
    "/feed", "/rss", "/feed/", "/rss/",
    "/atom", "/atom/", "/feeds/posts/default",
    "/index.xml", "/rss.xml", "/feed.xml", "/news/feed"
]

# Fetch articles from RSS feeds
for outlet in rss_sources:
    for pattern in RSS_PATTERNS:
        rss_feed_url = f"https://{outlet}{pattern}"
        feed = feedparser.parse(rss_feed_url)
        
        if feed.bozo == 0 and feed.entries:
            for entry in feed.entries[:100]:  # Limit to first 100 articles per source
                article_url = entry.link
                if not is_duplicate(article_url):
                    articles.append({
                        "source": {
                            "id": None,
                            "name": outlet  # Using the outlet name as the source
                        },
                        "author": entry.get("author", None),  # Some feeds provide author names
                        "title": clean_text(entry.title),
                        "description": clean_text(entry.get("summary", "")),  # Clean RSS descriptions
                        "url": article_url,
                        "publishedAt": entry.get("published", ""),  # Use published date if available
                    })
            break  # Stop checking patterns once a valid feed is found

# Save articles
with open(ARTICLES_FILE, "w") as f:
    json.dump(articles, f, indent=4)

print("Fetching complete. Articles saved.")
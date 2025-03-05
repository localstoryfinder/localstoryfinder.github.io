# This script classifies local journalism outlets based on their accessibility through NewsAPI or RSS feeds. 
# It first checks whether an outlet is available via NewsAPI using its domain. 
# If the outlet is not found, it searches for a valid RSS feed by iterating through common feed patterns. 
# The results are saved to sources.json, categorizing outlets under "newsapi" or "rss." 
# This process needs to be run only once per local region to determine which sources are accessible.

import requests
import feedparser
import json
import os

NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# List of local SF news outlet websites
OUTLETS = [
    "ebar.com", "sfexaminer.com", "sfchronicle.com", "inglesidelight.com", "westsideobserver.com",
    "catchlight.io", "missionlocal.org", "calhealthreport.org", "thefrisc.com", "sfpublicpress.org",
    "sfgate.com", "brokeassstuart.com", "sfstandard.com", "patch.com/san-francisco",
    "axios.com/local/san-francisco", "sf.streetsblog.org", "kpoo.com", "sfbayview.com",
    "eltecolote.org", "boldlatina.com", "thesunreporter.com", "elreportero.com", "univision.com/san-francisco",
    "windnewspaper.com", "kiqi1010.com", "russianlife.com", "jweekly.com", "kalw.org", "kqed.org"
]

# Common RSS feed patterns
RSS_PATTERNS = [
    "/feed", "/rss", "/feed/", "/rss/",
    "/atom", "/atom/", "/feeds/posts/default",
    "/index.xml", "/rss.xml", "/feed.xml", "/news/feed"
]

newsapi_sources = []
rss_sources = []

for outlet in OUTLETS:
    params = {
        "domains": outlet,
        "apiKey": NEWS_API_KEY,
        "pageSize": 1
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200 and response.json().get("articles"):
        newsapi_sources.append(outlet)
    else:
        for pattern in RSS_PATTERNS:
            rss_feed_url = f"https://{outlet}{pattern}"
            feed = feedparser.parse(rss_feed_url)
            if feed.bozo == 0 and feed.entries:
                rss_sources.append(outlet)
                break

# Save results to a JSON file
sources_data = {"newsapi": newsapi_sources, "rss": rss_sources}
with open("sources.json", "w") as f:
    json.dump(sources_data, f, indent=4)

print("Sources classified. Saved to sources.json")
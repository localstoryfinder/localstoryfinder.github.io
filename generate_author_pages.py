# This script generates author pages from articles.json.
# It extracts unique authors, assigns their articles, and creates HTML pages.
# Each author gets an individual page listing their published articles.
# The pages are saved in the "authors" directory.

import json
import os
from jinja2 import Template

# Create authors directory
os.makedirs("authors", exist_ok=True)
print("Created authors directory")

# Define template as string
AUTHOR_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ author }} - SF Local Story Finder</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        /* Center the results container */
        .results {
            display: flex;
            flex-direction: column;
            align-items: center; /* Centers the cards horizontally */
            width: 100%;
        }

        /* Ensure result items match the main search page */
        .result-item {
            width: 80%; /* Ensure they are not too wide */
            max-width: 600px; /* Keep consistent width */
            text-align: left; /* Left-align text inside */
            padding: 1rem;
            border: 1px solid var(--indigo);
            border-radius: 8px;
            background-color: var(--light-gray);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 1rem;
        }

        /* Hover effect for consistency */
        .result-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Center the title */
        .search-container h1 {
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <button class="menu-btn">☰</button>
        <nav class="dropdown-menu">
            <a href="/index.html">Home</a>
            <a href="/about.html">About</a>
            <a href="/methodology.html">Create Your Own</a>
        </nav>
    </header>
    
    <main>
        <div class="search-container">
            <h2>San Francisco's</h2>
            <h1>{{ author }}</h1>

            <div class="results">  <!-- This ensures all cards are centered -->
                {% for article in articles %}
                <div class="result-item">
                    <h3><a href="{{ article.url }}" target="_blank">{{ article.title }}</a></h3>
                    <p class="source-name">{{ article.source.name if article.source and article.source.name else '' }}</p>
                    <p>{{ article.description if article.description else '' }}</p>
                </div>
                {% endfor %}
            </div>
            
            <p><a href="../index.html">Back to Home</a></p>
        </div>
    </main>

    <script src="../script.js"></script>
</body>
</html>"""

# Load articles.json
try:
    with open("articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Loaded {len(articles)} articles from articles.json")
except Exception as e:
    print(f"Error loading articles.json: {e}")
    exit(1)

# Function to split multiple authors
def split_authors(author_string):
    if not author_string:
        return []
    
    # Common author separators
    separators = [", ", " and ", "; ", " & "]
    
    # Try each separator
    for separator in separators:
        if separator in author_string:
            authors = [a.strip() for a in author_string.split(separator)]
            return [a for a in authors if a and a.lower() != "unknown"]
    
    # No separators found, treat as single author
    return [author_string] if author_string.strip() and author_string.lower() != "unknown" else []

# Process authors and handle multiple authors per article
author_articles = {}

for article in articles:
    author_string = article.get("author")
    if not author_string or author_string.strip() == "" or author_string.lower() == "unknown":
        continue
        
    # Split multiple authors
    authors = split_authors(author_string)
    
    # Add article to each author's list
    for author in authors:
        if author not in author_articles:
            author_articles[author] = []
        author_articles[author].append(article)

print(f"Found {len(author_articles)} unique authors")

# Create author pages
for author, articles_list in author_articles.items():
    try:
        # Create filename
        author_filename = author.replace(" ", "_").replace("/", "_").replace("\\", "_").lower()
        file_path = f"authors/{author_filename}.html"
        
        # Sort articles by date if possible
        try:
            sorted_articles = sorted(articles_list, key=lambda x: x.get("publishedAt", ""), reverse=True)
        except:
            sorted_articles = articles_list
        
        # Render template
        author_template = Template(AUTHOR_TEMPLATE)
        author_content = author_template.render(
            author=author,
            articles=sorted_articles
        )
        
        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(author_content)
        print(f"Created {file_path}")
    except Exception as e:
        print(f"Error creating page for {author}: {e}")

print("Generated author pages.")

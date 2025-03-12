# San Francisco's Local Story Finder

**[Visit the Live Site](https://localstoryfinder.github.io)**

## Overview
The Local Story Finder is a tool designed to help readers discover local stories in the San Francisco Bay Area. By aggregating content from multiple local news sources via NewsAPI and RSS feeds, the platform provides a searchable database of articles that can be filtered by author, publication, or topic.

## Background
People trust local news more than any other kind—and for good reason. Local journalism keeps communities informed, connected, and engaged. In fact, 85% of Americans say local news is at least somewhat important to their community, with nearly half calling it extremely or very important. San Francisco is home to a thriving local news scene, powered by curious, dedicated journalists. We built a tool to make it easier to find them.

By centralizing access to content from local news outlets, this project aims to:
1. Make local journalism more discoverable
2. Highlight the work of smaller news outlets
3. Promote awareness of local news sources

## Features
- **Automatic Content Aggregation**: Daily updates from both NewsAPI and RSS feeds
- **Author Pages**: Dedicated pages for each journalist with their collected works 
- **Search Functionality**: Find articles by author, publication, or topic
- **Responsive Design**: Works on mobile and desktop devices

## Technical Implementation

### Data Collection
- **NewsAPI Integration**: Fetches articles from local SF news outlets
- **RSS Feed Parsing**: Collects articles from outlets not available through NewsAPI
- **Automated Updates**: GitHub Actions workflow runs daily at 6 AM PT
- **Deduplication**: Prevents duplicate articles across sources
- **Date Standardization**: Normalizes publication dates for consistent sorting

### Frontend
- **Search Engine**: Powered by Fuse.js for flexible, fault-tolerant searching
- **Source Name Normalization**: Converts domain names to reader-friendly publication names
- **HTML/CSS/JavaScript**: Simple, fast-loading interface with no dependencies
- **GitHub Pages Hosting**: Free, reliable hosting with automatic deployment

## News Sources
This project currently aggregates content from the following sources:

### Via NewsAPI
- SF Chronicle (sfchronicle.com)
- SF Gate (sfgate.com)
- SF Examiner (sfexaminer.com)
- SF Standard (sfstandard.com)
- Mission Local (missionlocal.org)
- KQED (kqed.org)
- SF Bay View (sfbayview.com)
- El Tecolote (eltecolote.org)
- J Weekly (jweekly.com)
- KALW (kalw.org)

### Via RSS Feeds
- California Health Report (calhealthreport.org)
- Streetsblog SF (sf.streetsblog.org)
- KPOO (kpoo.com)
- Bold Latina (boldlatina.com)
- San Francisco Sun Reporter (thesunreporter.com)

## Setup and Development

### Prerequisites
- Python 3.9+
- GitHub account
- NewsAPI key

### Local Development
1. Clone the repository
   ```
   git clone https://github.com/localjournalistfinder/localjournalistfinder.github.io.git
   ```

2. Install required packages
   ```
   pip install requests feedparser beautifulsoup4 jinja2 
   ```

3. Set up your NewsAPI key as an environment variable
   ```
   export NEWSAPI_KEY=your_api_key_here  # For Mac/Linux
   set NEWSAPI_KEY=your_api_key_here     # For Windows
   ```

4. Run the article fetcher
   ```
   python fetch_articles.py
   ```

5. Generate author pages
   ```
   python generate_author_pages.py
   ```

6. Test the site locally
   ```
   python -m http.server
   ```

7. Visit http://localhost:8000 in your browser

### Deployment
The site automatically deploys to GitHub Pages when changes are pushed to the main branch. The workflow in `.github/workflows/fetch_articles.yml` runs daily to update the content.

## Created By
Enkhjin Munkhbayar and Hannah Woodworth at Stanford University, March 2025.

## Acknowledgments
- All the journalists and news outlets continuing to provide vital local coverage in the San Francisco Bay Area
- Local news outlet list in San Francisco is from Northwestern University's [State of Local News Project](https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/)
- Statistics on local news importance from Pew Research Center's [Americans' Changing Relationship With Local News](https://www.pewresearch.org/journalism/2024/05/07/americans-changing-relationship-with-local-news/)
- NewsAPI for providing access to news outlets

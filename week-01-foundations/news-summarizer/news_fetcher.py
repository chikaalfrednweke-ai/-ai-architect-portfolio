# ============================================
# Fred Baker's Automations
# news_fetcher.py — AI News Summarizer
# Fetches AI, Nigerian Tech & AI Tools news
# ============================================

import feedparser
import json
import requests
from datetime import datetime

# ---- NEWS SOURCES ----
RSS_FEEDS = [
    # AI Automation News
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "category": "AI Automation"
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "category": "AI Automation"
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "category": "AI Automation"
    },

    # Nigerian Tech & Business News
    {
        "name": "TechCabal",
        "url": "https://techcabal.com/feed/",
        "category": "Nigerian Tech"
    },
    {
        "name": "Techpoint Africa",
        "url": "https://techpoint.africa/feed/",
        "category": "Nigerian Tech"
    },
    {
        "name": "Nairametrics",
        "url": "https://nairametrics.com/feed/",
        "category": "Nigerian Business"
    },

    # AI Tools News
    {
        "name": "AI Tools Newsletter",
        "url": "https://www.aitools.fyi/rss",
        "category": "AI Tools"
    },
    {
        "name": "Towards Data Science",
        "url": "https://towardsdatascience.com/feed",
        "category": "AI Tools"
    },
]

# ---- RELEVANCE CLASSIFIER ----
def classify_relevance(title, summary):
    text = (title + " " + summary).lower()

    scores = {
        "LexAI": 0,
        "EstateIQ": 0,
        "OpsGuard": 0
    }

    # LexAI keywords
    lexai_keywords = ["law", "legal", "court", "contract", "compliance",
                      "regulation", "attorney", "lawyer", "litigation"]
    for kw in lexai_keywords:
        if kw in text:
            scores["LexAI"] += 1

    # EstateIQ keywords
    estateiq_keywords = ["real estate", "property", "housing", "mortgage",
                         "rent", "landlord", "construction", "building"]
    for kw in estateiq_keywords:
        if kw in text:
            scores["EstateIQ"] += 1

    # OpsGuard keywords
    opsguard_keywords = ["oil", "gas", "energy", "pipeline", "petroleum",
                         "operations", "industrial", "manufacturing"]
    for kw in opsguard_keywords:
        if kw in text:
            scores["OpsGuard"] += 1

    # Return most relevant product
    max_score = max(scores.values())
    if max_score > 0:
        return max(scores, key=scores.get)
    return "General"

# ---- MOCK SUMMARIZER ----
def mock_summarize(title, content):
    sentences = content.split(".")
    clean = [s.strip() for s in sentences if len(s.strip()) > 30]
    if len(clean) >= 3:
        return ". ".join(clean[:3]) + "."
    elif len(clean) >= 1:
        return clean[0] + "."
    return title + ". No summary available."

# ---- FETCH NEWS ----
def fetch_news(max_per_feed=5):
    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  AI News Summarizer — Fetching...")
    print("=" * 55)

    all_articles = []
    
    for feed_info in RSS_FEEDS:
        try:
            print(f"\n  Fetching: {feed_info['name']}...")
            feed = feedparser.parse(feed_info["url"])
            
            count = 0
            for entry in feed.entries[:max_per_feed]:
                title = entry.get("title", "No title")
                link = entry.get("link", "")
                published = entry.get("published", 
                           datetime.now().strftime("%Y-%m-%d"))
                
                # Get summary/content
                summary = entry.get("summary", "")
                if not summary:
                    summary = entry.get("description", "")
                
                # Clean HTML tags
                import re
                summary = re.sub('<[^<]+?>', '', summary)
                summary = summary[:500]

                # Classify relevance
                relevance = classify_relevance(title, summary)

                # Generate summary
                brief = mock_summarize(title, summary)

                article = {
                    "title": title,
                    "link": link,
                    "published": published,
                    "source": feed_info["name"],
                    "category": feed_info["category"],
                    "relevance": relevance,
                    "summary": brief,
                    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                all_articles.append(article)
                count += 1

            print(f"  Got {count} articles from {feed_info['name']}")

        except Exception as e:
            print(f"  Error fetching {feed_info['name']}: {e}")

    return all_articles

# ---- GENERATE BRIEFING ----
def generate_briefing(articles):
    now = datetime.now().strftime("%B %d, %Y %H:%M")
    
    # Group by category
    by_category = {}
    for a in articles:
        cat = a["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(a)

    # Group by relevance
    by_relevance = {}
    for a in articles:
        rel = a["relevance"]
        if rel not in by_relevance:
            by_relevance[rel] = []
        by_relevance[rel].append(a)

    print("\n" + "=" * 55)
    print(f"  DAILY BRIEFING — {now}")
    print("=" * 55)
    print(f"  Total articles fetched: {len(articles)}")
    
    print("\n  BY CATEGORY:")
    for cat, arts in by_category.items():
        print(f"    {cat:<25} {len(arts)} articles")

    print("\n  BY PRODUCT RELEVANCE:")
    for rel, arts in by_relevance.items():
        print(f"    {rel:<25} {len(arts)} articles")

    print("\n  TOP STORIES:")
    print("-" * 55)
    for article in articles[:10]:
        print(f"\n  📰 {article['title'][:60]}")
        print(f"     Source    : {article['source']}")
        print(f"     Category  : {article['category']}")
        print(f"     Relevance : {article['relevance']}")
        print(f"     Summary   : {article['summary'][:100]}...")
        print(f"     Link      : {article['link'][:60]}")

    return by_category, by_relevance

# ---- SAVE RESULTS ----
def save_results(articles):
    # Save JSON
    filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    print(f"\n  Saved {len(articles)} articles to {filename}")
    return filename

# ---- MAIN ----
articles = fetch_news(max_per_feed=5)
by_category, by_relevance = generate_briefing(articles)
save_results(articles)

print("\n" + "=" * 55)
print("  News fetch complete!")
print("  Next: Add Claude API to generate AI summaries")
print("=" * 55)
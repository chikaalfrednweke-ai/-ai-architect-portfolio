# ============================================
# Fred Baker's Automations
# briefing_generator.py — HTML Daily Briefing
# ============================================

import json
import os
from datetime import datetime

def generate_html_briefing(articles):
    now = datetime.now().strftime("%B %d, %Y — %H:%M")

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

    # Category icons
    cat_icons = {
        "AI Automation": "🤖",
        "Nigerian Tech": "🇳🇬",
        "Nigerian Business": "💼",
        "AI Tools": "⚡"
    }

    # Relevance colors
    rel_colors = {
        "LexAI": "#4A8FC9",
        "EstateIQ": "#4CAF7A",
        "OpsGuard": "#C9A84C",
        "General": "#6A6060"
    }

    # Build category sections
    category_html = ""
    for cat, arts in by_category.items():
        icon = cat_icons.get(cat, "📰")
        articles_html = ""
        for a in arts:
            rel = a.get("relevance", "General")
            color = rel_colors.get(rel, "#6A6060")
            articles_html += f"""
            <div class="article-card">
                <div class="article-header">
                    <span class="relevance-badge" style="background:rgba(255,255,255,0.05);color:{color};border:1px solid {color}40">{rel}</span>
                    <span class="article-source">{a['source']}</span>
                </div>
                <h3 class="article-title">
                    <a href="{a['link']}" target="_blank">{a['title']}</a>
                </h3>
                <p class="article-summary">{a['summary'][:150]}...</p>
                <div class="article-footer">
                    <span class="article-date">{a['published'][:16]}</span>
                    <a href="{a['link']}" target="_blank" class="read-more">Read More →</a>
                </div>
            </div>"""

        category_html += f"""
        <div class="category-section">
            <h2 class="category-title">{icon} {cat}</h2>
            <div class="articles-grid">
                {articles_html}
            </div>
        </div>"""

    # Stats
    total = len(articles)
    lexai_count = len(by_relevance.get("LexAI", []))
    estateiq_count = len(by_relevance.get("EstateIQ", []))
    opsguard_count = len(by_relevance.get("OpsGuard", []))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fred Baker's Daily AI Briefing — {now}</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@300;400;500&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0A0A0A; color: #E8E0D0; font-family: 'Cormorant Garamond', serif; font-size: 16px; line-height: 1.7; }}
  
  .header {{
    background: linear-gradient(135deg, #111111, #0A0A0A);
    border-bottom: 2px solid #C9A84C;
    padding: 3rem;
    text-align: center;
  }}
  .header .eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.3em;
    color: #C9A84C;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }}
  .header h1 {{
    font-family: 'Cinzel', serif;
    font-size: 2.5rem;
    color: #E2C97E;
    margin-bottom: 0.5rem;
  }}
  .header .date {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #7A6330;
  }}

  .stats-bar {{
    display: flex;
    justify-content: center;
    gap: 3rem;
    padding: 1.5rem 3rem;
    background: #111111;
    border-bottom: 1px solid rgba(201,168,76,0.1);
  }}
  .stat {{ text-align: center; }}
  .stat .num {{
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    color: #C9A84C;
    display: block;
  }}
  .stat .lbl {{
    font-size: 11px;
    color: #7A6330;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
  }}

  .container {{ max-width: 1200px; margin: 0 auto; padding: 3rem; }}

  .category-section {{ margin-bottom: 3rem; }}
  .category-title {{
    font-family: 'Cinzel', serif;
    font-size: 1.3rem;
    color: #E2C97E;
    border-bottom: 1px solid rgba(201,168,76,0.2);
    padding-bottom: 0.8rem;
    margin-bottom: 1.5rem;
  }}

  .articles-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.2rem;
  }}

  .article-card {{
    background: #111111;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 1.2rem;
    transition: border-color 0.2s;
  }}
  .article-card:hover {{ border-color: rgba(201,168,76,0.2); }}

  .article-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
  }}
  .relevance-badge {{
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
  }}
  .article-source {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #7A6330;
  }}

  .article-title {{
    font-family: 'Cinzel', serif;
    font-size: 14px;
    margin-bottom: 0.8rem;
    line-height: 1.4;
  }}
  .article-title a {{
    color: #E2C97E;
    text-decoration: none;
  }}
  .article-title a:hover {{ color: #C9A84C; }}

  .article-summary {{
    font-size: 14px;
    color: #7A6370;
    font-style: italic;
    margin-bottom: 1rem;
    line-height: 1.6;
  }}

  .article-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .article-date {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #4A4040;
  }}
  .read-more {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #C9A84C;
    text-decoration: none;
  }}
  .read-more:hover {{ color: #E2C97E; }}

  .footer {{
    text-align: center;
    padding: 2rem;
    border-top: 1px solid rgba(201,168,76,0.1);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #4A4040;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="eyebrow">Fred Baker's Automations — Daily Intelligence</div>
  <h1>AI & Nigeria Tech Briefing</h1>
  <div class="date">{now}</div>
</div>

<div class="stats-bar">
  <div class="stat">
    <span class="num">{total}</span>
    <span class="lbl">Articles</span>
  </div>
  <div class="stat">
    <span class="num" style="color:#4A8FC9">{lexai_count}</span>
    <span class="lbl">LexAI</span>
  </div>
  <div class="stat">
    <span class="num" style="color:#4CAF7A">{estateiq_count}</span>
    <span class="lbl">EstateIQ</span>
  </div>
  <div class="stat">
    <span class="num" style="color:#C9A84C">{opsguard_count}</span>
    <span class="lbl">OpsGuard</span>
  </div>
  <div class="stat">
    <span class="num">{len(by_category)}</span>
    <span class="lbl">Categories</span>
  </div>
</div>

<div class="container">
  {category_html}
</div>

<div class="footer">
  Fred Baker's Automations | Nigeria's Leading AI Automation Company | Abuja, Nigeria<br>
  Generated: {now} | Powered by Python + RSS Feeds + Claude API (coming soon)
</div>

</body>
</html>"""

    filename = f"briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Briefing saved to: {filename}")
    print(f"  Open in browser to view!")
    return filename

# ---- LOAD LATEST NEWS JSON ----
def load_latest_news():
    files = [f for f in os.listdir(".") if f.startswith("news_") and f.endswith(".json")]
    if not files:
        print("No news files found! Run news_fetcher.py first.")
        return []
    latest = sorted(files)[-1]
    print(f"  Loading: {latest}")
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  Daily Briefing Generator")
print("=" * 55)

articles = load_latest_news()
if articles:
    filename = generate_html_briefing(articles)
    print("\n" + "=" * 55)
    print(f"  Briefing generated successfully!")
    print(f"  {len(articles)} articles compiled")
    print("=" * 55)
# ============================================
# Fred Baker's Automations
# pdf_report.py — Database PDF Report
# ============================================

import sqlite3
from datetime import datetime

def get_db():
    conn = sqlite3.connect("nigeria_businesses.db")
    conn.row_factory = sqlite3.Row
    return conn

def generate_html_report():
    conn = get_db()
    cursor = conn.cursor()

    # Stats
    cursor.execute("SELECT COUNT(*) FROM businesses")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM businesses
        GROUP BY city ORDER BY count DESC
    """)
    cities = cursor.fetchall()

    cursor.execute("""
        SELECT prospect_for, COUNT(*) as count
        FROM businesses
        GROUP BY prospect_for ORDER BY count DESC
    """)
    products = cursor.fetchall()

    cursor.execute("""
        SELECT sector, COUNT(*) as count
        FROM businesses
        GROUP BY sector ORDER BY count DESC
    """)
    sectors = cursor.fetchall()

    cursor.execute("""
        SELECT company_name, city, sector, prospect_for, phone, website
        FROM businesses
        WHERE prospect_for = 'LexAI'
        AND contacted = 0
        ORDER BY city
        LIMIT 20
    """)
    top_lexai = cursor.fetchall()

    cursor.execute("""
        SELECT company_name, city, sector, prospect_for, phone, website
        FROM businesses
        WHERE prospect_for = 'EstateIQ'
        AND contacted = 0
        ORDER BY city
        LIMIT 20
    """)
    top_estateiq = cursor.fetchall()

    cursor.execute("""
        SELECT company_name, city, sector, prospect_for, phone, website
        FROM businesses
        WHERE prospect_for = 'OpsGuard'
        AND contacted = 0
        ORDER BY city
        LIMIT 20
    """)
    top_opsguard = cursor.fetchall()
    conn.close()

    now = datetime.now().strftime("%B %d, %Y %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Fred Baker's Automations — Nigeria Business Intelligence Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Cormorant+Garamond:wght@300;400;500&display=swap');
  
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  
  body {{
    font-family: 'Cormorant Garamond', serif;
    background: #0A0A0A;
    color: #E8E0D0;
    padding: 3rem;
    font-size: 16px;
  }}

  .header {{
    text-align: center;
    border-bottom: 2px solid #C9A84C;
    padding-bottom: 2rem;
    margin-bottom: 3rem;
  }}

  .header .eyebrow {{
    font-size: 11px;
    letter-spacing: 0.3em;
    color: #C9A84C;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }}

  .header h1 {{
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    color: #E2C97E;
    margin-bottom: 0.5rem;
  }}

  .header .date {{
    font-size: 13px;
    color: #7A6330;
    margin-top: 0.5rem;
  }}

  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 3rem;
  }}

  .stat-card {{
    background: #111111;
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
  }}

  .stat-card .number {{
    font-family: 'Cinzel', serif;
    font-size: 2.5rem;
    color: #C9A84C;
    display: block;
  }}

  .stat-card .label {{
    font-size: 13px;
    color: #7A6330;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }}

  .section {{
    margin-bottom: 3rem;
  }}

  .section h2 {{
    font-family: 'Cinzel', serif;
    font-size: 1.2rem;
    color: #E2C97E;
    border-bottom: 1px solid rgba(201,168,76,0.2);
    padding-bottom: 0.8rem;
    margin-bottom: 1.5rem;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }}

  th {{
    background: rgba(201,168,76,0.1);
    color: #C9A84C;
    padding: 0.8rem 1rem;
    text-align: left;
    font-family: 'Cinzel', serif;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }}

  td {{
    padding: 0.7rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #E8E0D0;
  }}

  tr:hover td {{ background: rgba(201,168,76,0.03); }}

  .badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: 500;
  }}

  .badge-lexai {{ background: rgba(74,143,201,0.15); color: #4A8FC9; }}
  .badge-estateiq {{ background: rgba(76,175,122,0.15); color: #4CAF7A; }}
  .badge-opsguard {{ background: rgba(201,168,76,0.15); color: #C9A84C; }}

  .footer {{
    text-align: center;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(201,168,76,0.2);
    font-size: 13px;
    color: #7A6330;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="eyebrow">Fred Baker's Automations — Abuja, Nigeria</div>
  <h1>Nigeria Business Intelligence Report</h1>
  <div class="date">Generated: {now}</div>
</div>

<div class="stats-grid">
  <div class="stat-card">
    <span class="number">{total:,}</span>
    <span class="label">Total Records</span>
  </div>
  <div class="stat-card">
    <span class="number">{len(cities)}</span>
    <span class="label">Cities Covered</span>
  </div>
  <div class="stat-card">
    <span class="number">3</span>
    <span class="label">Products</span>
  </div>
</div>

<div class="section">
  <h2>Records by City</h2>
  <table>
    <tr><th>City</th><th>State</th><th>Records</th></tr>
    {"".join(f"<tr><td>{r['city']}</td><td>—</td><td>{r['count']}</td></tr>" for r in cities)}
  </table>
</div>

<div class="section">
  <h2>Records by Product</h2>
  <table>
    <tr><th>Product</th><th>Prospects</th></tr>
    {"".join(f"<tr><td>{r['prospect_for']}</td><td>{r['count']}</td></tr>" for r in products)}
  </table>
</div>

<div class="section">
  <h2>Top LexAI Prospects — Law Firms</h2>
  <table>
    <tr><th>Company</th><th>City</th><th>Phone</th><th>Product</th></tr>
    {"".join(f"<tr><td>{r['company_name']}</td><td>{r['city']}</td><td>{r['phone']}</td><td><span class='badge badge-lexai'>LexAI</span></td></tr>" for r in top_lexai)}
  </table>
</div>

<div class="section">
  <h2>Top EstateIQ Prospects — Real Estate</h2>
  <table>
    <tr><th>Company</th><th>City</th><th>Phone</th><th>Product</th></tr>
    {"".join(f"<tr><td>{r['company_name']}</td><td>{r['city']}</td><td>{r['phone']}</td><td><span class='badge badge-estateiq'>EstateIQ</span></td></tr>" for r in top_estateiq)}
  </table>
</div>

<div class="section">
  <h2>Top OpsGuard Prospects — Oil & Gas</h2>
  <table>
    <tr><th>Company</th><th>City</th><th>Phone</th><th>Product</th></tr>
    {"".join(f"<tr><td>{r['company_name']}</td><td>{r['city']}</td><td>{r['phone']}</td><td><span class='badge badge-opsguard'>OpsGuard</span></td></tr>" for r in top_opsguard)}
  </table>
</div>

<div class="footer">
  Fred Baker's Automations | Nigeria's Leading AI Automation Company | Abuja, Nigeria
</div>

</body>
</html>"""

    filename = f"nigeria_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Nigeria Business Intelligence Report")
    print("=" * 55)
    print(f"\n  Total records  : {total:,}")
    print(f"  Cities covered : {len(cities)}")
    print(f"\n  Report saved to: {filename}")
    print(f"  Open in browser to view!")
    print("=" * 55)

    return filename

# ---- RUN ----
generate_html_report()
# ============================================
# Fred Baker's Automations
# enrich_with_claude.py — AI Enrichment
# Uses Claude API to enrich business records
# ============================================

import sqlite3
import json
from datetime import datetime

# ---- CONFIGURATION ----
API_KEY = "your-api-key-here"  # Replace with sk-ant-...

# ---- DATABASE ----
def get_db():
    conn = sqlite3.connect("nigeria_businesses.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_unenriched(limit=10):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM businesses
        WHERE summary LIKE '%is a%and%located%'
        OR summary = ''
        OR summary IS NULL
        LIMIT ?
    """, (limit,))
    records = cursor.fetchall()
    conn.close()
    return records

def update_summary(record_id, summary, prospect_for):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE businesses
        SET summary = ?, prospect_for = ?
        WHERE id = ?
    """, (summary, prospect_for, record_id))
    conn.commit()
    conn.close()

# ---- CLAUDE ENRICHMENT ----
def enrich_business(company_name, sector, city, state):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=API_KEY)

        prompt = f"""You are a Nigerian business intelligence analyst.

Write a 3-sentence professional summary for this business:
Company: {company_name}
Sector: {sector}
Location: {city}, {state}, Nigeria

Requirements:
- Sentence 1: What the company does
- Sentence 2: Who they serve or their specialty
- Sentence 3: Their market position or size estimate

Also classify which Fred Baker's Automations product fits best:
- LexAI → for law firms and legal services
- EstateIQ → for real estate and property companies  
- OpsGuard → for oil, gas, and energy companies

Respond in JSON format only:
{{
    "summary": "three sentence summary here",
    "prospect_for": "LexAI or EstateIQ or OpsGuard"
}}"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text
        clean = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return data["summary"], data["prospect_for"]

    except Exception as e:
        print(f"    Error enriching {company_name}: {e}")
        return None, None

# ---- MOCK ENRICHMENT (no API key needed) ----
def mock_enrich(company_name, sector, city):
    summaries = {
        "Law Firm": f"{company_name} is a professional law firm providing comprehensive legal services in {city}, Nigeria. The firm specialises in corporate law, litigation, and advisory services for businesses and individuals. With experienced attorneys on staff, they serve clients across multiple practice areas in the Nigerian legal landscape.",
        "Real Estate": f"{company_name} is a dynamic real estate company operating in {city}'s growing property market. The firm provides end-to-end property services including sales, leasing, and investment advisory for residential and commercial clients. They have built a strong reputation for facilitating transparent and efficient property transactions.",
        "Oil & Gas": f"{company_name} is an energy sector company providing specialized services to Nigeria's oil and gas industry. The firm offers technical, operational, and consultancy solutions to upstream and downstream operators. They maintain a skilled workforce dedicated to safe and efficient energy operations across the Niger Delta region."
    }

    product_map = {
        "Law Firm": "LexAI",
        "Real Estate": "EstateIQ",
        "Oil & Gas": "OpsGuard"
    }

    summary = summaries.get(sector, f"{company_name} is a business operating in {city}, Nigeria.")
    prospect = product_map.get(sector, "LexAI")
    return summary, prospect

# ---- MAIN ENRICHMENT PIPELINE ----
def run_enrichment(use_claude=False, limit=5):
    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Claude AI Enrichment Pipeline")
    print("=" * 55)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses LIMIT ?", (limit,))
    records = cursor.fetchall()
    conn.close()

    print(f"\n  Enriching {len(records)} records...")
    print(f"  Mode: {'Claude API' if use_claude else 'Mock (no API key)'}")
    print("-" * 55)

    enriched = 0
    for record in records:
        print(f"\n  Processing: {record['company_name']}")

        if use_claude and API_KEY != "your-api-key-here":
            summary, prospect = enrich_business(
                record["company_name"],
                record["sector"],
                record["city"],
                record["state"]
            )
        else:
            summary, prospect = mock_enrich(
                record["company_name"],
                record["sector"],
                record["city"]
            )

        if summary:
            update_summary(record["id"], summary, prospect)
            print(f"  Sector   : {record['sector']}")
            print(f"  Product  : {prospect}")
            print(f"  Summary  : {summary[:80]}...")
            enriched += 1

    print("\n" + "=" * 55)
    print(f"  Enriched {enriched} records successfully!")
    print("=" * 55)

    # Show final state
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, city, prospect_for,
               substr(summary, 1, 60) as preview
        FROM businesses
        ORDER BY city
    """)
    print("\n  ENRICHED DATABASE PREVIEW:")
    print("-" * 55)
    for row in cursor.fetchall():
        print(f"  {row['company_name'][:25]:<25} | {row['prospect_for']}")
        print(f"    {row['preview']}...")
    conn.close()

# ---- RUN ----
run_enrichment(use_claude=False, limit=16) 
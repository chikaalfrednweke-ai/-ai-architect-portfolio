# ============================================
# Fred Baker's Automations
# bulk_generator.py — Bulk Data Generator
# Uses Claude API to generate Nigerian
# business records at scale
# ============================================

import sqlite3
import json
import time
from datetime import datetime

# ---- CONFIGURATION ----
API_KEY = "your-api-key-here"  # Replace when ready

# ---- TARGET SECTORS & CITIES ----
GENERATION_TARGETS = [
    # LAGOS
    {"city": "Lagos", "state": "Lagos State", "sector": "Law Firm", "prospect": "LexAI", "count": 50},
    {"city": "Lagos", "state": "Lagos State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 50},
    {"city": "Lagos", "state": "Lagos State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 30},
    {"city": "Lagos", "state": "Lagos State", "sector": "Legal Services", "prospect": "LexAI", "count": 30},
    {"city": "Lagos", "state": "Lagos State", "sector": "Property Development", "prospect": "EstateIQ", "count": 30},

    # ABUJA
    {"city": "Abuja", "state": "FCT", "sector": "Law Firm", "prospect": "LexAI", "count": 50},
    {"city": "Abuja", "state": "FCT", "sector": "Real Estate", "prospect": "EstateIQ", "count": 50},
    {"city": "Abuja", "state": "FCT", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 30},
    {"city": "Abuja", "state": "FCT", "sector": "Legal Services", "prospect": "LexAI", "count": 30},
    {"city": "Abuja", "state": "FCT", "sector": "Property Development", "prospect": "EstateIQ", "count": 30},

    # PORT HARCOURT
    {"city": "Port Harcourt", "state": "Rivers State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 60},
    {"city": "Port Harcourt", "state": "Rivers State", "sector": "Law Firm", "prospect": "LexAI", "count": 40},
    {"city": "Port Harcourt", "state": "Rivers State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 30},

    # KANO
    {"city": "Kano", "state": "Kano State", "sector": "Law Firm", "prospect": "LexAI", "count": 40},
    {"city": "Kano", "state": "Kano State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 30},

    # IBADAN
    {"city": "Ibadan", "state": "Oyo State", "sector": "Law Firm", "prospect": "LexAI", "count": 30},
    {"city": "Ibadan", "state": "Oyo State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 30},

    # ENUGU
    {"city": "Enugu", "state": "Enugu State", "sector": "Law Firm", "prospect": "LexAI", "count": 30},
    {"city": "Enugu", "state": "Enugu State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},

    # BENIN CITY
    {"city": "Benin City", "state": "Edo State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 30},
    {"city": "Benin City", "state": "Edo State", "sector": "Law Firm", "prospect": "LexAI", "count": 25},
# WARRI
    {"city": "Warri", "state": "Delta State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 50},
    {"city": "Warri", "state": "Delta State", "sector": "Law Firm", "prospect": "LexAI", "count": 30},
    {"city": "Warri", "state": "Delta State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},

    # CALABAR
    {"city": "Calabar", "state": "Cross River State", "sector": "Law Firm", "prospect": "LexAI", "count": 30},
    {"city": "Calabar", "state": "Cross River State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},

    # KADUNA
    {"city": "Kaduna", "state": "Kaduna State", "sector": "Law Firm", "prospect": "LexAI", "count": 30},
    {"city": "Kaduna", "state": "Kaduna State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},

    # OWERRI
    {"city": "Owerri", "state": "Imo State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 30},
    {"city": "Owerri", "state": "Imo State", "sector": "Law Firm", "prospect": "LexAI", "count": 25},

    # UYO
    {"city": "Uyo", "state": "Akwa Ibom State", "sector": "Oil & Gas", "prospect": "OpsGuard", "count": 40},
    {"city": "Uyo", "state": "Akwa Ibom State", "sector": "Law Firm", "prospect": "LexAI", "count": 25},
    {"city": "Uyo", "state": "Akwa Ibom State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},
# JOS
    {"city": "Jos", "state": "Plateau State", "sector": "Law Firm", "prospect": "LexAI", "count": 25},
    {"city": "Jos", "state": "Plateau State", "sector": "Real Estate", "prospect": "EstateIQ", "count": 20},

    # MAIDUGURI
    {"city": "Maiduguri", "state": "Borno State", "sector": "Law Firm", "prospect": "LexAI", "count": 20}
]

# ---- DATABASE ----
def get_db():
    conn = sqlite3.connect("nigeria_businesses.db")
    conn.row_factory = sqlite3.Row
    return conn

def save_batch(records):
    conn = get_db()
    cursor = conn.cursor()
    saved = 0
    skipped = 0

    for r in records:
        # Check duplicate
        cursor.execute(
            "SELECT id FROM businesses WHERE company_name = ? AND city = ?",
            (r["company_name"], r["city"])
        )
        if cursor.fetchone():
            skipped += 1
            continue

        cursor.execute("""
            INSERT INTO businesses
            (company_name, address, city, state, phone,
             website, sector, summary, prospect_for,
             source, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["company_name"], r["address"], r["city"],
            r["state"], r["phone"], r["website"],
            r["sector"], r["summary"], r["prospect_for"],
            "claude_generated",
            datetime.now().strftime("%Y-%m-%d")
        ))
        saved += 1

    conn.commit()
    conn.close()
    return saved, skipped

# ---- CLAUDE GENERATOR ----
def generate_with_claude(target):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=API_KEY)

        prompt = f"""Generate {target['count']} realistic Nigerian business records for {target['city']}, {target['state']}.

Sector: {target['sector']}
Product fit: {target['prospect']}

For each business generate:
- company_name: realistic Nigerian business name
- address: realistic {target['city']} street address
- phone: Nigerian format +234-8XX-XXX-XXXX
- website: realistic .com.ng or .ng domain
- summary: 3 professional sentences about the business
- sector: "{target['sector']}"
- prospect_for: "{target['prospect']}"
- city: "{target['city']}"
- state: "{target['state']}"

Return ONLY a JSON array. No explanation. No markdown.
Example format:
[
  {{
    "company_name": "Example Law Firm",
    "address": "123 Example Street, {target['city']}",
    "phone": "+234-801-234-5678",
    "website": "www.examplelaw.com.ng",
    "summary": "Sentence one. Sentence two. Sentence three.",
    "sector": "{target['sector']}",
    "prospect_for": "{target['prospect']}",
    "city": "{target['city']}",
    "state": "{target['state']}"
  }}
]"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text
        clean = response.replace("```json", "").replace("```", "").strip()
        records = json.loads(clean)
        return records

    except Exception as e:
        print(f"    Claude error: {e}")
        return []

# ---- MOCK GENERATOR ----
def generate_mock(target):
    nigerian_law_prefixes = [
        "Adeyemi", "Okonkwo", "Ibrahim", "Bello", "Emeka",
        "Adeola", "Chukwu", "Musa", "Abubakar", "Olawale",
        "Nwosu", "Eze", "Danjuma", "Abdullahi", "Okafor",
        "Fashola", "Tinubu", "Aminu", "Yakubu", "Okeke"
    ]

    nigerian_re_prefixes = [
        "Lagos", "Abuja", "Capital", "Prime", "Royal",
        "Golden", "Elite", "Premium", "Heritage", "Crown",
        "Victory", "Prestige", "Sterling", "Diamond", "Pearl"
    ]

    nigerian_og_prefixes = [
        "Niger", "Delta", "Atlantic", "Petroleum", "Energy",
        "Crude", "Pipeline", "Offshore", "Deepwater", "Apex",
        "Continental", "Federal", "National", "United", "Allied"
    ]

    streets = [
        "Marina Street", "Broad Street", "Victoria Island",
        "Ikoyi Road", "Lekki Phase 1", "Wuse Zone 5",
        "Maitama District", "Garki Area 2", "Asokoro",
        "GRA Phase 2", "Trans Amadi", "Rumuola Road",
        "Kano Road", "Zaria Avenue", "Sabon Gari"
    ]

    records = []
    for i in range(target["count"]):
        if target["sector"] in ["Law Firm", "Legal Services"]:
            prefix = nigerian_law_prefixes[i % len(nigerian_law_prefixes)]
            suffix = ["& Associates", "Legal Chambers", "& Co",
                      "Law Firm", "Solicitors", "& Partners",
                      "Legal Practice", "Barristers"][i % 8]
            name = f"{prefix} {suffix}"
            summary = f"{name} is a professional legal services firm based in {target['city']}, Nigeria. The firm specialises in corporate law, litigation, and regulatory compliance for businesses and individuals. With experienced legal practitioners, they provide comprehensive legal solutions across multiple practice areas."

        elif target["sector"] in ["Real Estate", "Property Development"]:
            prefix = nigerian_re_prefixes[i % len(nigerian_re_prefixes)]
            suffix = ["Properties", "Homes", "Realty", "Real Estate",
                      "Development", "Housing", "Estates", "Realtors"][i % 8]
            name = f"{prefix} {suffix}"
            summary = f"{name} is a dynamic property company operating in {target['city']}'s growing real estate market. The firm provides comprehensive property services including sales, leasing, and investment advisory for residential and commercial clients. They have built a strong track record of successful property transactions across prime {target['city']} locations."

        else:
            prefix = nigerian_og_prefixes[i % len(nigerian_og_prefixes)]
            suffix = ["Energy", "Petroleum", "Oil & Gas", "Resources",
                      "Energy Partners", "Petroleum Ltd", "Energy Plc",
                      "Resources Ltd"][i % 8]
            name = f"{prefix} {suffix}"
            summary = f"{name} is an energy sector company providing specialized services to Nigeria's oil and gas industry in {target['city']}. The firm offers technical, operational, and consultancy solutions to upstream and downstream operators across the Niger Delta. They maintain a skilled workforce dedicated to safe and efficient energy operations."

        street = streets[i % len(streets)]
        phone_num = f"+234-8{(i % 9) + 1}{i:02d}-{(i * 7) % 1000:03d}-{(i * 13) % 10000:04d}"
        name_slug = name.lower().replace(" ", "").replace("&", "and")[:20]

        records.append({
            "company_name": name,
            "address": f"No. {i+1} {street}, {target['city']}",
            "phone": phone_num,
            "website": f"www.{name_slug}.com.ng",
            "summary": summary,
            "sector": target["sector"],
            "prospect_for": target["prospect"],
            "city": target["city"],
            "state": target["state"]
        })

    return records

# ---- MAIN ----
def run_bulk_generation(use_claude=False):
    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Nigeria Business DB — Bulk Generator")
    print("=" * 55)

    total_saved = 0
    total_skipped = 0

    for target in GENERATION_TARGETS:
        print(f"\n  Generating: {target['count']} {target['sector']}s")
        print(f"  Location  : {target['city']}, {target['state']}")

        if use_claude and API_KEY != "your-api-key-here":
            records = generate_with_claude(target)
        else:
            records = generate_mock(target)

        saved, skipped = save_batch(records)
        total_saved += saved
        total_skipped += skipped
        print(f"  Saved     : {saved} | Skipped: {skipped}")

    # Final stats
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM businesses")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM businesses
        GROUP BY city
        ORDER BY count DESC
    """)
    cities = cursor.fetchall()

    cursor.execute("""
        SELECT prospect_for, COUNT(*) as count
        FROM businesses
        GROUP BY prospect_for
        ORDER BY count DESC
    """)
    products = cursor.fetchall()
    conn.close()

    print("\n" + "=" * 55)
    print("  BULK GENERATION COMPLETE!")
    print("=" * 55)
    print(f"  New records saved : {total_saved}")
    print(f"  Duplicates skipped: {total_skipped}")
    print(f"  Total in database : {total}")

    print("\n  By City:")
    for row in cities:
        print(f"    {row['city']:<20} {row['count']} records")

    print("\n  By Product:")
    for row in products:
        print(f"    {row['prospect_for']:<20} {row['count']} prospects")
    print("=" * 55)

# ---- RUN ----
run_bulk_generation(use_claude=False)
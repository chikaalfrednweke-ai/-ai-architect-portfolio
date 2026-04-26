# ============================================
# Fred Baker's Automations
# apify_scraper.py — Google Maps Scraper
# Pulls Nigerian businesses into SQLite DB
# ============================================

import json
import sqlite3
from datetime import datetime

# ---- APIFY SETUP ----
# pip install apify-client
try:
    from apify_client import ApifyClient
    APIFY_AVAILABLE = True
except ImportError:
    APIFY_AVAILABLE = False
    print("  apify-client not installed yet")
    print("  Run: pip install apify-client")

# ---- SEARCH TARGETS ----
# These are the searches we'll run on Google Maps
SEARCH_TARGETS = [
    # ABUJA
    {"query": "law firms in Abuja Nigeria", "city": "Abuja", "state": "FCT", "sector": "Law Firm", "prospect": "LexAI"},
    {"query": "real estate companies in Abuja Nigeria", "city": "Abuja", "state": "FCT", "sector": "Real Estate", "prospect": "EstateIQ"},
    {"query": "oil and gas companies in Abuja Nigeria", "city": "Abuja", "state": "FCT", "sector": "Oil & Gas", "prospect": "OpsGuard"},
    {"query": "legal chambers in Abuja Nigeria", "city": "Abuja", "state": "FCT", "sector": "Law Firm", "prospect": "LexAI"},
    {"query": "property developers in Abuja Nigeria", "city": "Abuja", "state": "FCT", "sector": "Real Estate", "prospect": "EstateIQ"},

    # LAGOS
    {"query": "law firms in Lagos Nigeria", "city": "Lagos", "state": "Lagos State", "sector": "Law Firm", "prospect": "LexAI"},
    {"query": "real estate companies in Lagos Nigeria", "city": "Lagos", "state": "Lagos State", "sector": "Real Estate", "prospect": "EstateIQ"},
    {"query": "oil and gas companies in Lagos Nigeria", "city": "Lagos", "state": "Lagos State", "sector": "Oil & Gas", "prospect": "OpsGuard"},
    {"query": "property management Lagos Nigeria", "city": "Lagos", "state": "Lagos State", "sector": "Real Estate", "prospect": "EstateIQ"},
    {"query": "energy companies Lagos Nigeria", "city": "Lagos", "state": "Lagos State", "sector": "Oil & Gas", "prospect": "OpsGuard"},
]

# ---- DATABASE CONNECTION ----
def get_db():
    conn = sqlite3.connect("nigeria_businesses.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---- SAVE TO DATABASE ----
def save_to_db(businesses, city, state, sector, prospect):
    conn = get_db()
    cursor = conn.cursor()
    saved = 0
    skipped = 0

    for biz in businesses:
        name = biz.get("title", "")
        address = biz.get("address", "")
        phone = biz.get("phone", "")
        website = biz.get("website", "")

        if not name:
            continue

        # Check for duplicates
        cursor.execute(
            "SELECT id FROM businesses WHERE company_name = ? AND city = ?",
            (name, city)
        )
        if cursor.fetchone():
            skipped += 1
            continue

        cursor.execute("""
            INSERT INTO businesses
            (company_name, address, city, state, phone, website,
             sector, summary, prospect_for, source, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, address, city, state, phone, website,
            sector, f"{name} is a {sector.lower()} business located in {city}, Nigeria.",
            prospect, "apify_google_maps",
            datetime.now().strftime("%Y-%m-%d")
        ))
        saved += 1

    conn.commit()
    conn.close()
    return saved, skipped

# ---- SCRAPE FUNCTION ----
def scrape_google_maps(api_token, target, max_results=100):
    client = ApifyClient(api_token)

    print(f"\n  Scraping: {target['query']}")
    print(f"  Target  : {max_results} results")

    run_input = {
        "searchStringsArray": [target["query"]],
        "maxCrawledPlacesPerSearch": max_results,
        "language": "en",
        "countryCode": "ng",
    }

    run = client.actor("nwua9Gu5YrADL7ZDj").call(run_input=run_input)

    businesses = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        businesses.append(item)

    saved, skipped = save_to_db(
        businesses,
        target["city"],
        target["state"],
        target["sector"],
        target["prospect"]
    )

    print(f"  Saved   : {saved} new records")
    print(f"  Skipped : {skipped} duplicates")
    return saved

# ---- MOCK SCRAPE (for testing without API key) ----
def mock_scrape():
    print("\n  Running MOCK scrape (no API key needed)")
    print("  This simulates what Apify returns")

    mock_results = [
        {"title": "Banwo & Ighodalo", "address": "98 Awolowo Road, Ikoyi, Lagos", "phone": "+234-801-234-5678", "website": "www.banwo-ighodalo.com"},
        {"title": "Udo Udoma & Belo-Osagie", "address": "St. Nicholas House, Lagos", "phone": "+234-802-345-6789", "website": "www.uubo.org"},
        {"title": "DIPO KEHINDE & CO", "address": "15 Broad Street, Lagos Island", "phone": "+234-803-456-7890", "website": "www.dipokehinde.com"},
        {"title": "Fine & Country West Africa", "address": "3 Anifowoshe Street, Victoria Island", "phone": "+234-804-567-8901", "website": "www.fineandcountry.com/ng"},
        {"title": "Pwan Group", "address": "Plot 1234 Lekki Phase 1, Lagos", "phone": "+234-805-678-9012", "website": "www.pwangroup.com"},
    ]

    target = {
        "city": "Lagos",
        "state": "Lagos State",
        "sector": "Law Firm",
        "prospect": "LexAI"
    }

    saved, skipped = save_to_db(mock_results, **target)
    print(f"  Mock saved  : {saved} records")
    print(f"  Mock skipped: {skipped} duplicates")
    return saved

# ---- FULL PIPELINE ----
def run_full_scrape(api_token, max_per_search=100):
    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Apify Google Maps Scraper")
    print("=" * 55)

    total_saved = 0
    for target in SEARCH_TARGETS:
        saved = scrape_google_maps(api_token, target, max_per_search)
        total_saved += saved

    print("\n" + "=" * 55)
    print(f"  SCRAPE COMPLETE")
    print(f"  Total new records: {total_saved}")
    print("=" * 55)

# ---- STATS ----
def show_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM businesses")
    total = cursor.fetchone()[0]
    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM businesses GROUP BY city
        ORDER BY count DESC
    """)
    cities = cursor.fetchall()
    conn.close()

    print("\n  DATABASE STATS:")
    print(f"  Total records: {total}")
    for row in cities:
        print(f"    {row[0]}: {row[1]} records")

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  Apify Scraper — Ready")
print("=" * 55)

# Install apify client
print("\n  Checking dependencies...")
if not APIFY_AVAILABLE:
    print("  Installing apify-client...")
    import subprocess
    subprocess.run(["pip", "install", "apify-client"], check=True)
    print("  apify-client installed!")

# Run mock scrape to test pipeline
print("\n  Running mock scrape to test pipeline...")
mock_scrape()
show_stats()

print("\n" + "=" * 55)
print
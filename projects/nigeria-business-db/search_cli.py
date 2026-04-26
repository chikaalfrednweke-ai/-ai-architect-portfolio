# ============================================
# Fred Baker's Automations
# search_cli.py — Database Search CLI Tool
# ============================================

import sqlite3
import sys

def get_db():
    conn = sqlite3.connect("nigeria_businesses.db")
    conn.row_factory = sqlite3.Row
    return conn

def print_results(results, title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"  {len(results)} results found")
    print(f"{'=' * 60}")
    for r in results:
        print(f"\n  🏢 {r['company_name']}")
        print(f"     City     : {r['city']}, {r['state']}")
        print(f"     Sector   : {r['sector']}")
        print(f"     Product  : {r['prospect_for']}")
        print(f"     Phone    : {r['phone']}")
        print(f"     Website  : {r['website']}")
        print(f"     Summary  : {r['summary'][:80]}...")
    print(f"{'=' * 60}\n")

def search(query=None, city=None, sector=None, product=None, limit=10):
    conn = get_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM businesses WHERE 1=1"
    params = []

    if query:
        sql += " AND (company_name LIKE ? OR summary LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if city:
        sql += " AND city LIKE ?"
        params.append(f"%{city}%")
    if sector:
        sql += " AND sector LIKE ?"
        params.append(f"%{sector}%")
    if product:
        sql += " AND prospect_for = ?"
        params.append(product)

    sql += f" LIMIT {limit}"
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return results

def interactive_search():
    print("=" * 60)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Nigeria Business Database — Search CLI")
    print("=" * 60)
    print("\n  Commands:")
    print("  search <name>           → search by company name")
    print("  city <city>             → filter by city")
    print("  product <LexAI/EstateIQ/OpsGuard>")
    print("  stats                   → show database stats")
    print("  quit                    → exit")
    print("=" * 60)

    while True:
        try:
            cmd = input("\n  > ").strip().lower()

            if cmd == "quit" or cmd == "exit":
                print("\n  Goodbye! 👋")
                break

            elif cmd == "stats":
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM businesses")
                total = cursor.fetchone()[0]
                cursor.execute("""
                    SELECT city, COUNT(*) as count
                    FROM businesses
                    GROUP BY city ORDER BY count DESC
                """)
                cities = cursor.fetchall()
                conn.close()
                print(f"\n  Total records: {total}")
                for c in cities:
                    print(f"    {c['city']:<20} {c['count']} records")

            elif cmd.startswith("search "):
                query = cmd.replace("search ", "")
                results = search(query=query)
                print_results(results, f"Search: '{query}'")

            elif cmd.startswith("city "):
                city = cmd.replace("city ", "").title()
                results = search(city=city)
                print_results(results, f"City: {city}")

            elif cmd.startswith("product "):
                product = cmd.replace("product ", "").strip()
                product_map = {
                    "lexai": "LexAI",
                    "estateiq": "EstateIQ",
                    "opsguard": "OpsGuard"
                }
                product = product_map.get(product.lower(), product)
                results = search(product=product, limit=20)
                print_results(results, f"Product: {product}")

            else:
                print("  Unknown command. Try: search, city, product, stats, quit")

        except KeyboardInterrupt:
            print("\n\n  Goodbye! 👋")
            break

# ---- RUN ----
interactive_search()
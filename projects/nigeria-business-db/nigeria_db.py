# ============================================
# Fred Baker's Automations
# nigeria_db.py — SQLite Database Engine
# Nigeria Business Intelligence Database
# ============================================

import sqlite3
import csv
import json
from datetime import datetime

# ---- DATABASE SETUP ----
class NigeriaBusinessDB:
    def __init__(self, db_file="nigeria_businesses.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()
        print(f"  Connected to database: {db_file}")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS businesses (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name    TEXT NOT NULL,
                address         TEXT,
                city            TEXT,
                state           TEXT,
                phone           TEXT,
                website         TEXT,
                sector          TEXT,
                summary         TEXT,
                prospect_for    TEXT,
                source          TEXT DEFAULT 'manual',
                date_added      TEXT,
                contacted       INTEGER DEFAULT 0,
                status          TEXT DEFAULT 'new'
            )
        """)
        self.conn.commit()
        print("  Table ready")

    # ---- INSERT ----
    def insert(self, company_name, address, city, state,
               phone, website, sector, summary, prospect_for,
               source="manual"):
        self.cursor.execute("""
            INSERT INTO businesses
            (company_name, address, city, state, phone, website,
             sector, summary, prospect_for, source, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (company_name, address, city, state, phone, website,
              sector, summary, prospect_for, source,
              datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()

    def insert_many(self, records):
        count = 0
        for r in records:
            self.insert(*r)
            count += 1
        print(f"  Inserted {count} records")

    # ---- QUERY ----
    def get_all(self):
        self.cursor.execute("SELECT * FROM businesses")
        return self.cursor.fetchall()

    def search_by_city(self, city):
        self.cursor.execute(
            "SELECT * FROM businesses WHERE city LIKE ?",
            (f"%{city}%",))
        return self.cursor.fetchall()

    def search_by_sector(self, sector):
        self.cursor.execute(
            "SELECT * FROM businesses WHERE sector LIKE ?",
            (f"%{sector}%",))
        return self.cursor.fetchall()

    def search_by_product(self, product):
        self.cursor.execute(
            "SELECT * FROM businesses WHERE prospect_for = ?",
            (product,))
        return self.cursor.fetchall()

    def search_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM businesses WHERE company_name LIKE ?",
            (f"%{name}%",))
        return self.cursor.fetchall()

    def get_hot_prospects(self, product):
        self.cursor.execute("""
            SELECT * FROM businesses
            WHERE prospect_for = ?
            AND contacted = 0
            AND status = 'new'
            ORDER BY company_name
        """, (product,))
        return self.cursor.fetchall()

    # ---- UPDATE ----
    def mark_contacted(self, company_id):
        self.cursor.execute("""
            UPDATE businesses
            SET contacted = 1, status = 'contacted'
            WHERE id = ?
        """, (company_id,))
        self.conn.commit()

    def update_status(self, company_id, status):
        self.cursor.execute("""
            UPDATE businesses
            SET status = ?
            WHERE id = ?
        """, (status, company_id))
        self.conn.commit()

    # ---- STATS ----
    def stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM businesses")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT city, COUNT(*) as count
            FROM businesses
            GROUP BY city
            ORDER BY count DESC
        """)
        cities = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT sector, COUNT(*) as count
            FROM businesses
            GROUP BY sector
            ORDER BY count DESC
        """)
        sectors = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT prospect_for, COUNT(*) as count
            FROM businesses
            GROUP BY prospect_for
            ORDER BY count DESC
        """)
        prospects = self.cursor.fetchall()

        print("\n" + "=" * 55)
        print("  NIGERIA BUSINESS DATABASE — STATS")
        print("=" * 55)
        print(f"  Total Records    : {total}")

        print("\n  By City:")
        for row in cities:
            print(f"    {row['city']:<25} {row['count']} records")

        print("\n  By Sector:")
        for row in sectors:
            print(f"    {row['sector']:<25} {row['count']} records")

        print("\n  By Product Fit:")
        for row in prospects:
            print(f"    {row['prospect_for']:<25} {row['count']} prospects")
        print("=" * 55)

    # ---- EXPORT ----
    def export_csv(self, filename="nigeria_businesses_export.csv"):
        records = self.get_all()
        if not records:
            print("  No records to export!")
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows([dict(r) for r in records])
        print(f"  Exported {len(records)} records to {filename}")

    def export_json(self, filename="nigeria_businesses_export.json"):
        records = self.get_all()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([dict(r) for r in records], f, indent=4)
        print(f"  Exported {len(records)} records to {filename}")

    def close(self):
        self.conn.close()

# ---- SEED DATA ----
seed_records = [
    # ABUJA — Law Firms
    ("Okonkwo & Associates", "Plot 1234 Ademola Adetokunbo Crescent",
     "Abuja", "FCT", "+234-803-123-4567", "www.okonkwolaw.com.ng",
     "Law Firm",
     "Okonkwo & Associates is a leading Abuja-based law firm specialising in corporate and commercial law. The firm serves multinational clients across Nigeria with a team of 25 experienced attorneys. Their practice areas include contract law, real estate transactions, and regulatory compliance.",
     "LexAI", "seed"),

    ("Bello Legal Chambers", "Suite 5, Sahad Stores Complex, Area 1",
     "Abuja", "FCT", "+234-805-234-5678", "www.bellochambers.ng",
     "Law Firm",
     "Bello Legal Chambers provides comprehensive legal services to businesses and individuals in the FCT. Founded in 2005, the firm has built a strong reputation in litigation and dispute resolution. They currently manage over 200 active cases across Nigerian federal courts.",
     "LexAI", "seed"),

    ("Afe Babalola & Co", "No. 8 Diplomatic Drive, Central District",
     "Abuja", "FCT", "+234-806-345-6789", "www.afebabalola.com",
     "Law Firm",
     "Afe Babalola & Co is a distinguished Nigerian law firm with a strong presence in Abuja's legal landscape. The firm specialises in constitutional law, human rights, and commercial litigation. They have successfully argued cases at the Supreme Court of Nigeria for over three decades.",
     "LexAI", "seed"),

    # ABUJA — Real Estate
    ("Abuja Homes & Properties", "No. 15 Gana Street, Maitama",
     "Abuja", "FCT", "+234-807-456-7890", "www.abujahomes.com.ng",
     "Real Estate",
     "Abuja Homes & Properties is a premium real estate firm operating across all Abuja districts. The company specialises in luxury residential and commercial property sales, leasing, and property management. They maintain a portfolio of over 500 properties across Maitama, Asokoro, and Wuse districts.",
     "EstateIQ", "seed"),

    ("Capital City Realtors", "Plot 789 Herbert Macaulay Way, CBD",
     "Abuja", "FCT", "+234-809-567-8901", "www.capitalcityrealtors.ng",
     "Real Estate",
     "Capital City Realtors connects buyers, sellers, and investors in Abuja's competitive property market. The firm offers end-to-end property services including valuation, documentation, and investment advisory. They have facilitated over 1,000 property transactions since their founding in 2010.",
     "EstateIQ", "seed"),

    # ABUJA — Oil & Gas
    ("Niger Delta Energy Partners", "No. 3 Adetokunbo Ademola Crescent, Wuse 2",
     "Abuja", "FCT", "+234-811-678-9012", "www.ndep.com.ng",
     "Oil & Gas",
     "Niger Delta Energy Partners provides upstream oil and gas consultancy services to major operators in Nigeria. The company specialises in field development planning, pipeline integrity management, and HSE compliance. They serve clients across the Niger Delta basin with a team of 80 petroleum engineers.",
     "OpsGuard", "seed"),

    # LAGOS — Law Firms
    ("Templars Law", "The Octagon, 13A A.J. Marinho Drive, Victoria Island",
     "Lagos", "Lagos State", "+234-812-789-0123", "www.templars-law.com",
     "Law Firm",
     "Templars is one of Nigeria's foremost full-service law firms with offices in Lagos and Abuja. The firm advises leading corporates, financial institutions, and government entities on complex transactions. Their practice spans banking, energy, infrastructure, and dispute resolution.",
     "LexAI", "seed"),

    ("Aluko & Oyebode", "1 Murtala Muhammed Drive, Ikoyi",
     "Lagos", "Lagos State", "+234-813-890-1234", "www.aluko-oyebode.com",
     "Law Firm",
     "Aluko & Oyebode is one of Nigeria's largest and most prestigious law firms with over 100 lawyers. The firm has a broad practice covering corporate finance, energy, real estate, and litigation. They have been at the forefront of major Nigerian commercial transactions for over 40 years.",
     "LexAI", "seed"),

    # LAGOS — Real Estate
    ("Propertymart Real Estate", "12 Akin Adesola Street, Victoria Island",
     "Lagos", "Lagos State", "+234-814-901-2345", "www.propertymart.ng",
     "Real Estate",
     "Propertymart is a leading real estate development and marketing company operating across Lagos. The company focuses on affordable and luxury housing developments in high-demand Lagos corridors. They have delivered over 2,000 residential units across Lekki, Ajah, and Ibeju-Lekki.",
     "EstateIQ", "seed"),

    # LAGOS — Oil & Gas
    ("Seplat Energy Plc", "16A Temple Road, Ikoyi",
     "Lagos", "Lagos State", "+234-815-012-3456", "www.seplatenergy.com",
     "Oil & Gas",
     "Seplat Energy is a leading Nigerian independent oil and gas company listed on the Nigerian and London Stock Exchanges. The company operates across onshore and shallow water assets in the Niger Delta. Seplat produces approximately 50,000 barrels of oil equivalent per day.",
     "OpsGuard", "seed"),

    ("Oando PLC", "2 Ajele Street, Lagos Island",
     "Lagos", "Lagos State", "+234-816-123-4567", "www.oandoplc.com",
     "Oil & Gas",
     "Oando PLC is a Nigerian multinational energy company with operations spanning oil and gas exploration, production, and distribution. The company is listed on both the Nigerian Exchange and Johannesburg Stock Exchange. Oando operates one of Nigeria's largest downstream petroleum networks.",
     "OpsGuard", "seed"),
]

# ---- RUN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  Nigeria Business Intelligence Database")
print("  SQLite Engine — Initializing...")
print("=" * 55)

db = NigeriaBusinessDB()

print("\n  Seeding database...")
db.insert_many(seed_records)

db.stats()

# Demo queries
print("\n  DEMO QUERIES:")
print("-" * 55)

print("\n  All LexAI prospects (uncontacted):")
for r in db.get_hot_prospects("LexAI"):
    print(f"    → {r['company_name']} | {r['city']}")

print("\n  All businesses in Abuja:")
for r in db.search_by_city("Abuja"):
    print(f"    → {r['company_name']} | {r['sector']}")

print("\n  Search by name 'Energy':")
for r in db.search_by_name("Energy"):
    print(f"    → {r['company_name']} | {r['city']}")

# Mark first record as contacted
print("\n  Marking record #1 as contacted...")
db.mark_contacted(1)
db.update_status(1, "in-conversation")

# Export
print("\n  Exporting database...")
db.export_csv()
db.export_json()

db.close()
print("\n  Done! nigeria_businesses.db is your SQLite database.")
print("  Open it with DB Browser for SQLite to see it visually!")
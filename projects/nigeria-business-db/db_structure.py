# ============================================
# Fred Baker's Automations
# Nigeria Business Intelligence Database
# db_structure.py — Database Foundation
# ============================================

import json
import csv
import os
from datetime import datetime

# ---- DATABASE SCHEMA ----
def create_business_record(
    company_name,
    address,
    city,
    state,
    phone,
    website,
    sector,
    summary,
    prospect_for,
    source="manual"
):
    return {
        "id": None,  # Auto-assigned
        "company_name": company_name,
        "address": address,
        "city": city,
        "state": state,
        "phone": phone,
        "website": website,
        "sector": sector,
        "summary": summary,
        "prospect_for": prospect_for,  # LexAI, EstateIQ, OpsGuard
        "source": source,
        "date_added": datetime.now().strftime("%Y-%m-%d"),
        "contacted": False,
        "status": "new"
    }

# ---- DATABASE CLASS ----
class NigeriaBusinessDB:
    def __init__(self, db_file="nigeria_businesses.json"):
        self.db_file = db_file
        self.records = []
        self.load()

    def load(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                self.records = json.load(f)
            print(f"  Loaded {len(self.records)} existing records")
        else:
            self.records = []
            print("  Starting fresh database")

    def add(self, record):
        record["id"] = len(self.records) + 1
        self.records.append(record)

    def save(self):
        with open(self.db_file, "w") as f:
            json.dump(self.records, f, indent=4)
        print(f"  Saved {len(self.records)} records to {self.db_file}")

    def export_csv(self, filename="nigeria_businesses.csv"):
        if not self.records:
            print("  No records to export!")
            return
        keys = self.records[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.records)
        print(f"  Exported {len(self.records)} records to {filename}")

    def search(self, field, value):
        results = [r for r in self.records
                   if value.lower() in str(r.get(field, "")).lower()]
        return results

    def filter_by_prospect(self, product):
        return [r for r in self.records if r["prospect_for"] == product]

    def stats(self):
        total = len(self.records)
        cities = {}
        sectors = {}
        prospects = {}

        for r in self.records:
            cities[r["city"]] = cities.get(r["city"], 0) + 1
            sectors[r["sector"]] = sectors.get(r["sector"], 0) + 1
            prospects[r["prospect_for"]] = prospects.get(r["prospect_for"], 0) + 1

        print("\n" + "=" * 55)
        print("  NIGERIA BUSINESS DATABASE — STATS")
        print("=" * 55)
        print(f"  Total Records    : {total}")
        print("\n  By City:")
        for city, count in sorted(cities.items(),
                                   key=lambda x: x[1], reverse=True):
            print(f"    {city:<20} {count} records")
        print("\n  By Sector:")
        for sector, count in sorted(sectors.items(),
                                     key=lambda x: x[1], reverse=True)[:10]:
            print(f"    {sector:<20} {count} records")
        print("\n  By Product Fit:")
        for product, count in prospects.items():
            print(f"    {product:<20} {count} prospects")
        print("=" * 55)

# ---- SEED DATA — Lagos + Abuja Samples ----
seed_data = [
    # ABUJA — Law Firms
    ("Okonkwo & Associates", "Plot 1234 Ademola Adetokunbo Crescent",
     "Abuja", "FCT", "+234-803-123-4567", "www.okonkwolaw.com.ng",
     "Law Firm",
     "Okonkwo & Associates is a leading Abuja-based law firm specialising in corporate and commercial law. The firm serves multinational clients across Nigeria with a team of 25 experienced attorneys. Their practice areas include contract law, real estate transactions, and regulatory compliance.",
     "LexAI"),

    ("Bello Legal Chambers", "Suite 5, Sahad Stores Complex, Area 1",
     "Abuja", "FCT", "+234-805-234-5678", "www.bellochambers.ng",
     "Law Firm",
     "Bello Legal Chambers provides comprehensive legal services to businesses and individuals in the FCT. Founded in 2005, the firm has built a strong reputation in litigation and dispute resolution. They currently manage over 200 active cases across Nigerian federal courts.",
     "LexAI"),

    # ABUJA — Real Estate
    ("Abuja Homes & Properties", "No. 15 Gana Street, Maitama",
     "Abuja", "FCT", "+234-807-345-6789", "www.abujahomes.com.ng",
     "Real Estate",
     "Abuja Homes & Properties is a premium real estate firm operating across all Abuja districts. The company specialises in luxury residential and commercial property sales, leasing, and property management. They maintain a portfolio of over 500 properties across Maitama, Asokoro, and Wuse districts.",
     "EstateIQ"),

    ("Capital City Realtors", "Plot 789 Herbert Macaulay Way, Central Business District",
     "Abuja", "FCT", "+234-809-456-7890", "www.capitalcityrealtors.ng",
     "Real Estate",
     "Capital City Realtors connects buyers, sellers, and investors in Abuja's competitive property market. The firm offers end-to-end property services including valuation, documentation, and investment advisory. They have facilitated over 1,000 property transactions since their founding in 2010.",
     "EstateIQ"),

    # ABUJA — Oil & Gas
    ("Niger Delta Energy Partners", "No. 3 Adetokunbo Ademola Crescent, Wuse 2",
     "Abuja", "FCT", "+234-811-567-8901", "www.ndep.com.ng",
     "Oil & Gas",
     "Niger Delta Energy Partners provides upstream oil and gas consultancy services to major operators in Nigeria. The company specialises in field development planning, pipeline integrity management, and HSE compliance. They serve clients across the Niger Delta basin with a team of 80 petroleum engineers.",
     "OpsGuard"),

    # LAGOS — Law Firms
    ("Templars Law", "The Octagon, 13A, A.J. Marinho Drive, Victoria Island",
     "Lagos", "Lagos State", "+234-812-678-9012", "www.templars-law.com",
     "Law Firm",
     "Templars is one of Nigeria's foremost full-service law firms with offices in Lagos and Abuja. The firm advises leading corporates, financial institutions, and government entities on complex transactions. Their practice spans banking, energy, infrastructure, and dispute resolution.",
     "LexAI"),

    ("Aluko & Oyebode", "1 Murtala Muhammed Drive, Ikoyi",
     "Lagos", "Lagos State", "+234-813-789-0123", "www.aluko-oyebode.com",
     "Law Firm",
     "Aluko & Oyebode is one of Nigeria's largest and most prestigious law firms with over 100 lawyers. The firm has a broad practice covering corporate finance, energy, real estate, and litigation. They have been at the forefront of major Nigerian commercial transactions for over 40 years.",
     "LexAI"),

    # LAGOS — Real Estate
    ("Propertymart Real Estate", "12 Akin Adesola Street, Victoria Island",
     "Lagos", "Lagos State", "+234-814-890-1234", "www.propertymart.ng",
     "Real Estate",
     "Propertymart is a leading real estate development and marketing company operating across Lagos. The company focuses on affordable and luxury housing developments in high-demand Lagos corridors. They have delivered over 2,000 residential units across Lekki, Ajah, and Ibeju-Lekki.",
     "EstateIQ"),

    # LAGOS — Oil & Gas
    ("Seplat Energy Plc", "16A Temple Road, Ikoyi",
     "Lagos", "Lagos State", "+234-815-901-2345", "www.seplatenergy.com",
     "Oil & Gas",
     "Seplat Energy is a leading Nigerian independent oil and gas company listed on the Nigerian and London Stock Exchanges. The company operates across onshore and shallow water assets in the Niger Delta. Seplat produces approximately 50,000 barrels of oil equivalent per day.",
     "OpsGuard"),

    ("Oando PLC", "2 Ajele Street, off Broad Street, Lagos Island",
     "Lagos", "Lagos State", "+234-816-012-3456", "www.oandoplc.com",
     "Oil & Gas",
     "Oando PLC is a Nigerian multinational energy company with operations spanning oil and gas exploration, production, and distribution. The company is listed on both the Nigerian Exchange and Johannesburg Stock Exchange. Oando operates one of Nigeria's largest downstream petroleum networks.",
     "OpsGuard"),
]

# ---- RUN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  Nigeria Business Intelligence Database")
print("  Initializing...")
print("=" * 55)

db = NigeriaBusinessDB()

print("\n  Adding seed records...")
for data in seed_data:
    record = create_business_record(*data)
    db.add(record)

db.save()
db.export_csv()
db.stats()

print("\n  Database initialized successfully!")
print(f"  JSON: nigeria_businesses.json")
print(f"  CSV:  nigeria_businesses.csv")
print("\n  Next: Connect Apify scraper to add 100,000+ records!")
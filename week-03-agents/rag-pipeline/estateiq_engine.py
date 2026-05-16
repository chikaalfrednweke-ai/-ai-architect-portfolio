# ============================================
# Fred Baker's Automations
# estateiq_engine.py — EstateIQ RAG + Claude
# Nigerian Real Estate AI Knowledge Base
# ============================================

import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---- CONFIGURATION ----
COLLECTION_NAME = "estateiq_nigeria_realestate"
DB_PATH = "./chroma_db"

# ---- REAL ESTATE DOCUMENTS ----
REAL_ESTATE_DOCS = [
    {
        "id": "abuja_market_001",
        "title": "Abuja Property Market Overview 2024",
        "content": """
        Abuja is Nigeria's Federal Capital Territory and one of Africa's fastest
        growing real estate markets. Property values have appreciated 15-20% annually.
        Prime Districts and Average Prices (2024):
        1. Maitama: Residential plots N150M-N500M, 4-bedroom N250M-N800M
        2. Asokoro: Residential plots N100M-N400M, embassy district
        3. Wuse 2: Commercial hub, office spaces N2M-N5M per sqm
        4. Gwarinpa: More affordable N30M-N80M for 3-bedroom
        5. Jahi: Emerging premium, plots N50M-N150M
        6. Life Camp: Growing residential, 3-bedroom N25M-N60M
        Market trends: Shortage of quality properties driving prices up.
        """,
        "category": "Market Data",
        "source": "Fred Baker's Automations Research 2024"
    },
    {
        "id": "lagos_market_001",
        "title": "Lagos Property Market Overview 2024",
        "content": """
        Lagos is Nigeria's commercial capital and largest real estate market.
        Key Districts and Prices (2024):
        1. Victoria Island: Apartments N150M-N500M, offices N3M-N8M per sqm
        2. Ikoyi: Ultra-premium, luxury apartments N200M-N1B+
        3. Lekki Phase 1: 3-bedroom apartment N50M-N150M
        4. Ajah: More affordable N20M-N60M, good appreciation
        5. Ibeju-Lekki: Future growth, land N2M-N15M per plot
        6. Mainland (Ikeja): 3-bedroom N15M-N40M, 8-12% rental yields
        Investment: Lekki-Epe corridor showing strongest growth.
        Short-let apartments yielding 15-25% annually.
        """,
        "category": "Market Data",
        "source": "Fred Baker's Automations Research 2024"
    },
    {
        "id": "cof_process_001",
        "title": "Certificate of Occupancy (C of O) Complete Guide",
        "content": """
        A Certificate of Occupancy (C of O) is the most important title document
        for land and property in Nigeria, issued by State Governors.
        Types of title documents:
        1. Certificate of Occupancy (C of O) - Strongest title
        2. Right of Occupancy (R of O) - Government allocation
        3. Deed of Assignment - Transfer between private parties
        4. Governor's Consent - Required for property transfers
        How to obtain C of O in Abuja:
        Step 1: Land allocation from FCDA or purchase from owner
        Step 2: Survey the land - hire licensed surveyor (N200,000-N500,000)
        Step 3: Apply at AGIS
        Step 4: Pay processing fees
        Step 5: Physical inspection by government officials
        Step 6: Approval and issuance (6-18 months)
        Red flags: Sellers reluctant to verify at Land Registry,
        C of O with corrections, properties in acquisition areas.
        """,
        "category": "Property Documentation",
        "source": "Land Use Act 1978, AGIS Guidelines"
    },
    {
        "id": "investment_001",
        "title": "Real Estate Investment Strategies in Nigeria",
        "content": """
        Real estate investment strategies ranked by returns:
        1. Short-Let/Airbnb (20-35% annually):
           Furnish apartment, list on Airbnb. Best near airports.
        2. Student Housing (15-25% annually):
           Near UNILAG, UI, ABU, UNIABUJA. High consistent demand.
        3. Commercial Properties (12-18% annually):
           Office spaces, retail, warehouses. Longer leases.
        4. Buy and Hold Residential (8-15% annually):
           Long-term rental income. Lower management intensity.
        5. Land Banking (capital appreciation):
           Buy in growth corridors. Best: Ibeju-Lekki, Lugbe.
        Key metrics: Gross Rental Yield = Annual Rent / Price x 100.
        Target minimum 8% gross yield for residential.
        Financing: Federal Mortgage Bank rates 6-9%.
        """,
        "category": "Investment Strategy",
        "source": "Nigerian Real Estate Market Analysis"
    },
    {
        "id": "due_diligence_001",
        "title": "Property Due Diligence Checklist Nigeria",
        "content": """
        Essential due diligence before purchasing property in Nigeria:
        Title Verification:
        - Obtain official search at Land Registry
        - Verify C of O authenticity
        - Check for existing mortgages or charges
        - Verify no government acquisition notice
        Physical Inspection:
        - Visit property multiple times
        - Hire structural engineer
        - Verify property matches survey plan
        - Check for flooding history (especially Lagos)
        Documentation Review:
        - Survey plan from licensed surveyor
        - Building approval/development permit
        - Tax clearance certificate of seller
        - Deed of Assignment (properly stamped)
        Financial Verification:
        - Legal fees: 5-10% of purchase price
        - Agency fees: 5-10%
        - Government fees: 1-3%
        Red Flags: Multiple ownership claims, priced below market,
        seller pressuring for quick payment.
        """,
        "category": "Due Diligence",
        "source": "Nigerian Real Estate Best Practices"
    },
    {
        "id": "rental_001",
        "title": "Rental Market and Landlord-Tenant Law Nigeria",
        "content": """
        Lagos Tenancy Law 2011 Key Provisions:
        1. Maximum advance rent: Residential 1 year, Commercial 2 years
        2. Notice to quit: Weekly=1 week, Monthly=1 month, Yearly=6 months
        3. Rent increases: Must give 6 months notice
        4. Self-help eviction (changing locks) is illegal
        Current rental yields:
        - Maitama Abuja: 5-8% annually
        - Wuse 2 Abuja: 7-10% annually
        - Victoria Island Lagos: 6-9% annually
        - Lekki Phase 1: 8-12% annually
        - Ikeja Lagos: 10-15% annually
        Short-let rates per night (2024):
        - Maitama/Asokoro: N80,000-N300,000
        - VI/Ikoyi Lagos: N100,000-N500,000
        Property management fees: 10% of annual rent standard.
        """,
        "category": "Rental Market",
        "source": "Lagos Tenancy Law 2011"
    },
    {
        "id": "reit_001",
        "title": "Real Estate Investment Trusts (REITs) in Nigeria",
        "content": """
        REITs allow Nigerians to invest in real estate from N5,000 via NGX.
        Listed REITs: UPDC REIT (8-12% yield), Skye Shelter Fund, Union Homes REIT.
        REIT Regulations: Regulated by SEC Nigeria.
        Must distribute minimum 90% of income as dividends.
        Advantages: Low entry point, professional management, liquidity.
        How to invest: Open stockbroker account, fund it, buy REIT units on NGX.
        """,
        "category": "Investment Vehicles",
        "source": "SEC Nigeria, NGX Guidelines"
    },
    {
        "id": "valuation_001",
        "title": "Property Valuation Methods in Nigeria",
        "content": """
        Valuation methods used by licensed Estate Surveyors (NIESV):
        1. Comparative Method: Compare with recent sales of similar properties.
        2. Investment Method: Value = Annual Rent / Capitalization Rate.
           Cap rates in Nigeria: 6-12% depending on location.
        3. Cost Method: Land value + depreciated building cost.
        4. Residual Method: For development land.
        Key factors: Location, Title (C of O commands 20-30% premium),
        Infrastructure, Security, Construction quality.
        Valuation fees: 0.25-0.5% of property value for residential.
        When needed: Mortgage application, insurance, legal disputes.
        """,
        "category": "Property Valuation",
        "source": "NIESV Guidelines"
    },
    {
        "id": "mortgage_001",
        "title": "Mortgage and Property Financing in Nigeria",
        "content": """
        Mortgage options in Nigeria:
        1. Federal Mortgage Bank (FMBN): 6% interest, max N15M loan.
           Eligibility: Must contribute to NHF for 6+ months.
        2. Primary Mortgage Banks: 15-22% interest, up to 20 years.
        3. Commercial Banks: 20-28% interest, stricter requirements.
        4. Developer Financing: 30% upfront, balance in installments.
        5. Cooperative Society Loans: Lower interest, members only.
        Qualification requirements:
        - Minimum 3 years employment history
        - Monthly repayment max 33% of income
        - Clean credit history (CRC check)
        - Property must have C of O
        Costs: Legal fees 1-2%, valuation 0.25-0.5%, insurance 0.35%.
        """,
        "category": "Property Financing",
        "source": "FMBN Guidelines, CBN Mortgage Regulations"
    },
    {
        "id": "proptech_001",
        "title": "PropTech and Digital Real Estate in Nigeria",
        "content": """
        Leading Nigerian PropTech platforms:
        1. PropertyPro.ng: Largest listing platform, 300,000+ listings
        2. Private Property Nigeria: Strong in Lagos and Abuja
        3. Tolet.com.ng: Focus on rentals, tenant verification
        4. Spleet: Flexible monthly rent payment
        5. Seso Global: Blockchain-based property transactions
        Digital trends: Virtual tours, AI property recommendations,
        digital mortgages, blockchain title registry.
        EstateIQ positioning: AI-powered matching, WhatsApp-first,
        naira-denominated, NDPR compliant.
        Market opportunity: Nigerian real estate $1.1 trillion,
        PropTech penetration less than 5%.
        """,
        "category": "PropTech",
        "source": "Nigerian PropTech Report 2024"
    }
]

# ---- ESTATEIQ RAG ENGINE ----
class EstateIQRAGEngine:
    def __init__(self):
        print("  Initializing EstateIQ RAG Engine...")
        self.client_db = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client_db.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Nigerian Real Estate Knowledge Base"}
        )
        self.claude = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        print(f"  Documents in DB: {self.collection.count()}")

    def load_documents(self, documents):
        print(f"\n  Loading {len(documents)} documents...")
        ids = []
        texts = []
        metadatas = []

        for doc in documents:
            ids.append(doc["id"])
            texts.append(f"{doc['title']}\n\n{doc['content']}")
            metadatas.append({
                "title": doc["title"],
                "category": doc["category"],
                "source": doc["source"]
            })

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        print(f"  Loaded {len(documents)} documents!")
        print(f"  Total in DB: {self.collection.count()}")

    def search(self, query, n_results=3):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def answer(self, question):
        print(f"\n  ❓ {question}")
        results = self.search(question)

        context = ""
        for i, (doc, meta) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0]
        )):
            context += f"\n--- Source {i+1}: {meta['title']} ---\n"
            context += f"Category: {meta['category']}\n"
            context += f"Source: {meta['source']}\n"
            context += f"Content: {doc[:600]}\n"

        print("  Sources found:")
        for i, meta in enumerate(results["metadatas"][0]):
            print(f"    {i+1}. {meta['title']}")

        prompt = f"""You are EstateIQ, an AI real estate assistant specializing
in the Nigerian property market. Use the following market data to answer accurately.

REAL ESTATE KNOWLEDGE BASE:
{context}

QUESTION: {question}

Provide a clear, data-driven answer about Nigerian real estate.
Include specific prices, yields, and practical recommendations.
Be professional and concise."""

        message = self.claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  EstateIQ — RAG + Claude API = FULL POWER!")
print("=" * 55)

engine = EstateIQRAGEngine()
engine.load_documents(REAL_ESTATE_DOCS)

test_questions = [
    "What are property prices in Maitama Abuja?",
    "What is the best real estate investment strategy?",
    "How do I verify a property title in Nigeria?",
]

print("\n" + "=" * 55)
print("  ESTATEIQ REAL AI RESPONSES")
print("=" * 55)

for question in test_questions:
    answer = engine.answer(question)
    print("\n" + "-" * 55)
    print(answer)
    print()

print("=" * 55)
print("  EstateIQ RAG + Claude = FULLY OPERATIONAL!")
print("=" * 55)
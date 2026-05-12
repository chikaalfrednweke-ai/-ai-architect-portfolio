# ============================================
# Fred Baker's Automations
# estateiq_engine.py — EstateIQ RAG Pipeline
# Nigerian Real Estate AI Knowledge Base
# ============================================

import chromadb
from datetime import datetime

# ---- CONFIGURATION ----
COLLECTION_NAME = "estateiq_nigeria_realestate"
DB_PATH = "./chroma_db"

# ---- NIGERIAN REAL ESTATE DOCUMENTS ----
REAL_ESTATE_DOCS = [
    {
        "id": "abuja_market_001",
        "title": "Abuja Property Market Overview 2024",
        "content": """
        Abuja is Nigeria's Federal Capital Territory and one of Africa's fastest 
        growing real estate markets. Property values have appreciated 15-20% annually
        in prime districts over the last 5 years.
        
        Prime Districts and Average Prices (2024):
        1. Maitama:
           - Residential plots: N150M - N500M per plot
           - 4-bedroom detached: N250M - N800M
           - Commercial properties: N500M - N2B
           
        2. Asokoro:
           - Residential plots: N100M - N400M
           - 4-bedroom detached: N200M - N600M
           - Embassy district, high security
           
        3. Wuse 2:
           - Commercial hub of Abuja
           - Office spaces: N2M - N5M per sqm
           - Retail spaces highly sought after
           
        4. Gwarinpa:
           - Largest housing estate in West Africa
           - More affordable: N30M - N80M for 3-bedroom
           - Good for middle-income investment
           
        5. Jahi:
           - Emerging premium district
           - Plots: N50M - N150M
           - High appreciation potential
           
        6. Life Camp:
           - Growing residential area
           - 3-bedroom: N25M - N60M
           - Popular with young professionals
           
        Market trends:
        - Shortage of quality properties driving prices up
        - Expat demand keeping Maitama/Asokoro premium
        - Infrastructure development boosting emerging areas
        - Dollar-denominated properties gaining popularity
        """,
        "category": "Market Data",
        "source": "Fred Baker's Automations Research 2024"
    },
    {
        "id": "lagos_market_001",
        "title": "Lagos Property Market Overview 2024",
        "content": """
        Lagos is Nigeria's commercial capital and largest real estate market,
        with over 20 million residents creating massive housing demand.
        
        Key Districts and Prices (2024):
        1. Victoria Island (VI):
           - Premium commercial and residential
           - Apartments: N150M - N500M
           - Office spaces: N3M - N8M per sqm
           - Most expensive area in Nigeria
           
        2. Ikoyi:
           - Ultra-premium residential
           - Luxury apartments: N200M - N1B+
           - Waterfront properties command premium
           
        3. Lekki Phase 1:
           - Most popular middle-upper market
           - 3-bedroom apartment: N50M - N150M
           - High rental demand from professionals
           
        4. Ajah:
           - Fast growing corridor
           - More affordable: N20M - N60M
           - Good appreciation potential
           
        5. Ibeju-Lekki:
           - Future growth corridor
           - Land: N2M - N15M per plot
           - Dangote Refinery driving development
           
        6. Mainland (Ikeja, Surulere):
           - Commercial and residential mix
           - 3-bedroom: N15M - N40M
           - Good rental yields 8-12% annually
           
        Investment insights:
        - Lekki-Epe corridor showing strongest growth
        - Short-let apartments yielding 15-25% annually
        - Student housing near universities high demand
        - Warehousing/logistics properties scarce
        """,
        "category": "Market Data",
        "source": "Fred Baker's Automations Research 2024"
    },
    {
        "id": "cof_process_001",
        "title": "Certificate of Occupancy (C of O) — Complete Guide",
        "content": """
        A Certificate of Occupancy (C of O) is the most important title document
        for land and property in Nigeria, issued by State Governors under the Land Use Act.
        
        Types of title documents in Nigeria:
        1. Certificate of Occupancy (C of O) — Strongest title
        2. Right of Occupancy (R of O) — Government allocation
        3. Deed of Assignment — Transfer between private parties
        4. Governor's Consent — Required for property transfers
        5. Deed of Lease — For leasehold properties
        6. Survey Plan — Boundary description (not a title)
        
        How to obtain a C of O in Abuja (FCT):
        Step 1: Land allocation from FCDA or purchase from existing owner
        Step 2: Survey the land — hire a licensed surveyor (N200,000-N500,000)
        Step 3: Apply at AGIS (Abuja Geographic Information Systems)
        Step 4: Pay processing fees (varies by land size and use)
        Step 5: Physical inspection by government officials
        Step 6: Approval and issuance (6-18 months typically)
        
        How to obtain a C of O in Lagos:
        Step 1: Purchase property with Deed of Assignment
        Step 2: Apply at Lagos Land Bureau
        Step 3: Submit: Survey plan, Deed, Tax clearance
        Step 4: Pay fees (1.5-3% of property value)
        Step 5: Processing takes 3-12 months
        
        Verifying a C of O:
        - Visit the Land Registry in person
        - Request official search (N5,000-N20,000)
        - Verify plot number, owner name, encumbrances
        - Check for government acquisition notices
        
        Red flags to watch for:
        - Sellers reluctant to verify at Land Registry
        - C of O with multiple names or corrections
        - Properties in government acquisition areas
        - No survey plan available
        - Family land disputes unresolved
        """,
        "category": "Property Documentation",
        "source": "Land Use Act 1978, AGIS Guidelines"
    },
    {
        "id": "investment_001",
        "title": "Real Estate Investment Strategies in Nigeria",
        "content": """
        Real estate remains one of the best investment vehicles in Nigeria,
        offering protection against inflation and naira devaluation.
        
        Investment strategies ranked by returns:
        
        1. Short-Let/Airbnb Properties (Highest returns: 20-35% annually)
           - Furnish apartment in VI, Lekki, or Maitama
           - List on Airbnb, Booking.com, shortlet platforms
           - Requires management (self or property manager)
           - Best locations: Near airports, business districts
           
        2. Student Housing (15-25% annually)
           - Near UNILAG, UI, ABU, UNIBEN, UNIABUJA
           - High and consistent demand
           - Lower maintenance than luxury properties
           - Consider buying multiple rooms in hostels
           
        3. Commercial Properties (12-18% annually)
           - Office spaces, retail shops, warehouses
           - Longer leases (2-5 years) = stable income
           - Dollar-denominated rents in premium areas
           
        4. Buy and Hold Residential (8-15% annually)
           - Long-term rental income
           - Capital appreciation over time
           - Lower management intensity
           
        5. Land Banking (Capital appreciation focus)
           - Buy land in growth corridors
           - Hold 3-7 years for 200-500% returns
           - Best areas: Ibeju-Lekki, Lugbe, Gwagwalada
           
        Key metrics to evaluate:
        - Gross Rental Yield = Annual Rent / Property Price x 100
        - Net Yield = (Annual Rent - Expenses) / Price x 100
        - Target: Minimum 8% gross yield for residential
        - Capital Appreciation: Target 15%+ annually
        
        Financing options:
        - Mortgage: Federal Mortgage Bank (FMB) rates 6-9%
        - Commercial banks: 20-25% interest (expensive)
        - Developer payment plans: 12-36 months installments
        - REITs: Listed on NGX, accessible from N5,000
        """,
        "category": "Investment Strategy",
        "source": "Nigerian Real Estate Market Analysis"
    },
    {
        "id": "due_diligence_001",
        "title": "Property Due Diligence Checklist Nigeria",
        "content": """
        Before purchasing any property in Nigeria, conduct thorough due diligence
        to avoid fraud, disputes, and financial loss.
        
        ESSENTIAL DUE DILIGENCE CHECKLIST:
        
        Title Verification:
        ☐ Obtain official search at Land Registry
        ☐ Verify C of O or title document authenticity
        ☐ Confirm owner matches seller identity
        ☐ Check for existing mortgages or charges
        ☐ Verify no government acquisition notice
        ☐ Check court records for pending litigation
        
        Physical Inspection:
        ☐ Visit property multiple times (day and night)
        ☐ Hire structural engineer for building inspection
        ☐ Verify property matches survey plan dimensions
        ☐ Check for flooding history (especially Lagos)
        ☐ Inspect all electrical, plumbing, roof
        ☐ Verify all fittings and fixtures included
        
        Documentation Review:
        ☐ Survey plan from licensed surveyor
        ☐ Building approval/development permit
        ☐ Environmental Impact Assessment (if applicable)
        ☐ Tax clearance certificate of seller
        ☐ Deed of Assignment (properly stamped)
        ☐ Governor's Consent (for transfers)
        
        Neighborhood Research:
        ☐ Check proximity to amenities (schools, hospitals)
        ☐ Verify road access and infrastructure
        ☐ Research planned government developments
        ☐ Talk to neighbors about the area
        ☐ Check security situation
        
        Financial Verification:
        ☐ Confirm asking price vs market value
        ☐ Verify rental income if tenanted property
        ☐ Calculate all transaction costs:
           - Legal fees: 5-10% of purchase price
           - Agency fees: 5-10%
           - Government fees: 1-3%
           - C of O processing: N200,000-N2M
        
        Red Flags — Walk Away If:
        ✗ Seller cannot produce original title documents
        ✗ Multiple people claiming ownership
        ✗ Priced significantly below market value
        ✗ Seller pressuring for quick payment
        ✗ Property in obvious government acquisition zone
        ✗ No physical access for inspection
        """,
        "category": "Due Diligence",
        "source": "Nigerian Real Estate Best Practices"
    },
    {
        "id": "rental_001",
        "title": "Rental Market and Landlord-Tenant Law Nigeria",
        "content": """
        The Nigerian rental market is governed by state tenancy laws,
        with Lagos and Abuja having specific regulations.
        
        Lagos Tenancy Law 2011 — Key Provisions:
        1. Maximum advance rent:
           - Residential: 1 year maximum
           - Commercial: 2 years maximum
           - Landlords cannot demand more
           
        2. Notice to quit periods:
           - Weekly tenancy: 1 week notice
           - Monthly tenancy: 1 month notice
           - Yearly tenancy: 6 months notice
           
        3. Rent increases:
           - Must give 6 months notice before increase
           - Cannot increase arbitrarily mid-tenancy
           
        4. Recovery of premises:
           - Must go through court process
           - Self-help eviction (changing locks) is illegal
           - Tenancy Tribunal handles disputes
           
        Current rental yields by location:
        - Maitama Abuja: 5-8% annually
        - Wuse 2 Abuja: 7-10% annually
        - Victoria Island Lagos: 6-9% annually
        - Lekki Phase 1: 8-12% annually
        - Ikeja Lagos: 10-15% annually
        
        Short-let rental rates (per night, 2024):
        - Maitama/Asokoro: N80,000-N300,000
        - VI/Ikoyi Lagos: N100,000-N500,000
        - Lekki: N50,000-N200,000
        
        Property management fees:
        - Standard: 10% of annual rent
        - Short-let management: 20-30% of revenue
        - Full facility management: 15-20%
        
        Tenant screening best practices:
        - Verify employment/income (3x monthly rent minimum)
        - Check references from previous landlords
        - Conduct ID verification
        - Sign comprehensive tenancy agreement
        - Collect security deposit (1-3 months rent)
        """,
        "category": "Rental Market",
        "source": "Lagos Tenancy Law 2011, FCT Tenancy Regulations"
    },
    {
        "id": "reit_001",
        "title": "Real Estate Investment Trusts (REITs) in Nigeria",
        "content": """
        Real Estate Investment Trusts (REITs) allow Nigerians to invest in 
        real estate with as little as N5,000 through the Nigerian Exchange (NGX).
        
        Listed REITs on Nigerian Exchange (2024):
        1. UPDC REIT:
           - Focus: Commercial properties in Lagos
           - Dividend yield: 8-12% annually
           - Units tradeable on NGX
           
        2. Skye Shelter Fund:
           - Focus: Residential properties
           - Regular dividend distributions
           
        3. Union Homes REIT:
           - Diversified property portfolio
           - Regulated by SEC Nigeria
           
        REIT Regulations in Nigeria:
        - Regulated by Securities and Exchange Commission (SEC)
        - Must distribute minimum 90% of income as dividends
        - Maximum 35% development projects (must be 65% income-generating)
        - Annual financial reporting to SEC mandatory
        - Minimum 100 unit holders required
        
        Advantages of REITs:
        ✅ Low entry point (from N5,000)
        ✅ Professional management
        ✅ Liquidity (tradeable on stock exchange)
        ✅ Diversification across multiple properties
        ✅ Regular dividend income
        ✅ No property management hassle
        
        Disadvantages:
        ❌ Lower returns than direct ownership
        ❌ Market price volatility
        ❌ Management fees reduce returns
        ❌ Limited control over investment decisions
        
        How to invest in Nigerian REITs:
        1. Open account with stockbroker
        2. Fund account
        3. Buy REIT units on NGX
        4. Receive quarterly/annual dividends
        5. Sell units anytime market is open
        """,
        "category": "Investment Vehicles",
        "source": "SEC Nigeria, NGX Guidelines"
    },
    {
        "id": "valuation_001",
        "title": "Property Valuation Methods in Nigeria",
        "content": """
        Property valuation in Nigeria is conducted by licensed Estate Surveyors
        and Valuers, regulated by the Nigerian Institution of Estate Surveyors 
        and Valuers (NIESV).
        
        Main valuation methods used in Nigeria:
        
        1. Comparative Method (Sales Comparison):
           - Most common for residential properties
           - Compare with recent sales of similar properties
           - Adjust for differences in size, location, condition
           - Best when there are many comparable transactions
           
        2. Investment/Income Method:
           - Used for commercial and rental properties
           - Formula: Value = Annual Rent / Capitalization Rate
           - Example: Annual rent N5M / 8% cap rate = N62.5M value
           - Cap rates in Nigeria: 6-12% depending on location
           
        3. Cost Method (Depreciated Replacement Cost):
           - Used for special purpose properties
           - Calculate land value + depreciated building cost
           - Used for insurance valuations
           
        4. Residual Method:
           - For development land
           - Value = GDV - Development Costs - Profit
           - Used by developers to assess viability
           
        Key factors affecting property values in Nigeria:
        - Location and accessibility
        - Title (C of O commands 20-30% premium over no title)
        - Infrastructure (electricity, water, road)
        - Security of the neighborhood
        - Proximity to business districts
        - Quality of construction
        
        Valuation fees in Nigeria:
        - 0.25-0.5% of property value for residential
        - 0.5-1% for commercial properties
        - Minimum fee: N50,000-N100,000
        
        When you need a valuation:
        - Mortgage application
        - Insurance purposes
        - Legal disputes
        - Sale/purchase negotiation
        - Probate and estate administration
        - Company asset reporting
        """,
        "category": "Property Valuation",
        "source": "NIESV Guidelines, Nigerian Property Standards"
    },
    {
        "id": "mortgage_001",
        "title": "Mortgage and Property Financing in Nigeria",
        "content": """
        Property financing in Nigeria remains challenging due to high interest rates,
        but several options exist for buyers and investors.
        
        Mortgage options in Nigeria:
        
        1. Federal Mortgage Bank of Nigeria (FMBN):
           - National Housing Fund (NHF) loans
           - Interest rate: 6% per annum (subsidized)
           - Maximum loan: N15 million (contributors)
           - Eligibility: Must contribute to NHF for 6+ months
           - Employee deduction: 2.5% of basic salary monthly
           
        2. Primary Mortgage Banks (PMBs):
           - Interest rates: 15-22% per annum
           - Loan-to-value ratio: 60-70%
           - Tenure: Up to 20 years
           - Examples: Abbey Mortgage, ASO Savings
           
        3. Commercial Banks:
           - Most expensive option: 20-28% per annum
           - Shorter tenure: 5-15 years
           - Stricter qualification requirements
           - Better for investment properties
           
        4. Developer Financing:
           - Off-plan payment plans: 12-48 months
           - Usually 30% upfront, balance in installments
           - No interest if completed within plan period
           - Risk: Developer may not complete project
           
        5. Cooperative Society Loans:
           - Lower interest than commercial banks
           - Available to members only
           - Good for civil servants
           
        Mortgage qualification requirements:
        - Minimum 3 years employment history
        - Salary: Monthly repayment max 33% of income
        - Clean credit history (CRC credit check)
        - Valid means of identification
        - Tax clearance certificate
        - Property must have C of O
        
        Cost of obtaining a mortgage:
        - Legal fees: 1-2% of loan amount
        - Valuation fee: 0.25-0.5% of property value
        - Insurance: 0.35% annually (MOPI)
        - Processing fee: 1-2% of loan amount
        """,
        "category": "Property Financing",
        "source": "FMBN Guidelines, CBN Mortgage Regulations"
    },
    {
        "id": "proptech_001",
        "title": "PropTech and Digital Real Estate in Nigeria",
        "content": """
        Property technology (PropTech) is transforming Nigeria's real estate sector,
        making transactions more transparent and accessible.
        
        Leading Nigerian PropTech platforms:
        
        1. PropertyPro.ng:
           - Largest property listing platform
           - Over 300,000 listings nationwide
           - Verified agent program
           
        2. Private Property Nigeria:
           - Strong in Lagos and Abuja
           - Agent and developer listings
           
        3. Tolet.com.ng:
           - Focus on rentals
           - Tenant verification services
           
        4. Spleet:
           - Flexible rent payment (monthly instead of annual)
           - Targeting young professionals
           
        5. Seso Global:
           - Blockchain-based property transactions
           - Digital title registry
           
        Digital transformation trends:
        1. Virtual property tours (360° views)
        2. AI-powered property recommendations
        3. Digital mortgage applications
        4. Blockchain title registry (pilot in Lagos)
        5. Automated rental payment systems
        6. Property management software adoption
        
        EstateIQ competitive positioning:
        - AI-powered property matching for Nigerian market
        - Integration with local MLS databases
        - WhatsApp-first communication (Nigerian preference)
        - Naira-denominated transactions
        - Local market knowledge built into AI
        - NDPR compliant data handling
        
        Market opportunity:
        - Nigerian real estate market: $1.1 trillion
        - PropTech penetration still less than 5%
        - Growing middle class driving demand
        - Diaspora remittances funding property purchases
        - Government affordable housing deficit: 20 million units
        """,
        "category": "PropTech",
        "source": "Nigerian PropTech Report 2024"
    }
]

# ---- ESTATEIQ RAG ENGINE ----
class EstateIQRAGEngine:
    def __init__(self):
        print("  Initializing EstateIQ RAG Engine...")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Nigerian Real Estate Knowledge Base for EstateIQ"}
        )
        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Documents in DB: {self.collection.count()}")

    def load_documents(self, documents):
        print(f"\n  Loading {len(documents)} documents into ChromaDB...")
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
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def answer(self, question):
        print(f"\n  Question: {question}")
        results = self.search(question)

        print("  Context retrieved:")
        for i, meta in enumerate(results["metadatas"][0]):
            print(f"    {i+1}. {meta['title']} ({meta['category']})")

        return results

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  EstateIQ RAG Pipeline — Nigerian Real Estate AI")
print("=" * 55)

engine = EstateIQRAGEngine()
engine.load_documents(REAL_ESTATE_DOCS)

# Test queries
test_questions = [
    "What are property prices in Maitama Abuja?",
    "How do I get a Certificate of Occupancy?",
    "What is the best real estate investment strategy?",
    "How do I verify a property title?",
    "What are rental yields in Lagos?",
    "How does a Nigerian mortgage work?",
    "What is an REIT in Nigeria?",
    "How is property valued in Nigeria?"
]

print("\n" + "=" * 55)
print("  TESTING ESTATEIQ SEARCH")
print("=" * 55)

for question in test_questions:
    results = engine.answer(question)
    print(f"  Top match: {results['metadatas'][0][0]['title']}")
    print()

print("=" * 55)
print("  EstateIQ RAG Engine ready!")
print("  10 Nigerian real estate documents loaded")
print("  Next: Build EstateIQ chat interface")
print("=" * 55)
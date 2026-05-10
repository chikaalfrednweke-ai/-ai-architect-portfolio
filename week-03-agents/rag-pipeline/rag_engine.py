# ============================================
# Fred Baker's Automations
# rag_engine.py — RAG Pipeline Engine
# Powers LexAI Nigerian Legal Knowledge Base
# ============================================

import chromadb
import json
import os
from datetime import datetime

# ---- CONFIGURATION ----
COLLECTION_NAME = "lexai_nigeria_legal"
DB_PATH = "./chroma_db"

# ---- SAMPLE NIGERIAN LEGAL DOCUMENTS ----
# These simulate real Nigerian legal content
# Real version will load actual PDF documents
NIGERIAN_LEGAL_DOCS = [
    {
        "id": "cac_001",
        "title": "CAC Company Registration Requirements",
        "content": """
        To register a company in Nigeria with the Corporate Affairs Commission (CAC), 
        you need the following requirements:
        1. Minimum of two shareholders for a private limited company
        2. Minimum share capital of N100,000 for private companies
        3. At least one director who must be a natural person
        4. A registered office address in Nigeria
        5. Memorandum and Articles of Association
        6. Form CAC 1.1 (Application for Registration)
        7. Valid means of identification for directors and shareholders
        8. Tax Identification Number (TIN) for corporate shareholders
        The registration process takes 1-2 weeks and costs approximately N10,000-N50,000 
        depending on share capital. Post-registration, companies must file annual returns 
        with the CAC within 42 days of each anniversary of incorporation.
        """,
        "category": "Company Law",
        "source": "CAC Act 2020"
        
    },
    {
        "id": "contract_001",
        "title": "Contract Formation Under Nigerian Law",
        "content": """
        Under Nigerian law, a valid contract requires the following essential elements:
        1. Offer: A clear proposal made by one party to another
        2. Acceptance: Unconditional agreement to the terms of the offer
        3. Consideration: Something of value exchanged between parties
        4. Capacity: Both parties must be of legal age (18+) and sound mind
        5. Intention: Both parties must intend to create legal relations
        6. Legality: The contract must not be for an illegal purpose
        
        Nigerian courts follow the common law tradition inherited from English law.
        Written contracts are preferred but oral contracts are also enforceable.
        The Statute of Frauds requires certain contracts to be in writing, including:
        - Contracts for sale of land
        - Contracts that cannot be performed within one year
        - Guarantees and indemnities
        Breach of contract remedies include damages, specific performance, and injunction.
        """,
        "category": "Contract Law",
        "source": "Nigerian Contract Law"
    },
    {
        "id": "property_001",
        "title": "Land Ownership and Title in Nigeria",
        "content": """
        Land ownership in Nigeria is governed by the Land Use Act 1978, which vests 
        all land in each state in the Governor, who holds it in trust for the people.
        
        Types of land tenure in Nigeria:
        1. Statutory Right of Occupancy - granted by State Governor for urban land
        2. Customary Right of Occupancy - granted by Local Government for rural land
        3. Leasehold - right to use land for a specified period
        4. Certificate of Occupancy (C of O) - the primary title document in Nigeria
        
        To obtain a Certificate of Occupancy:
        - Apply to the State Government Land Bureau
        - Survey the land and obtain a survey plan
        - Pay prescribed fees
        - Process takes 3-12 months depending on the state
        
        Due diligence for property purchase:
        - Verify C of O authenticity at the Land Registry
        - Check for existing encumbrances or mortgages
        - Confirm Governor's consent for assignments
        - Verify survey plan with the Surveyor General's office
        """,
        "category": "Property Law",
        "source": "Land Use Act 1978"
    },
    {
        "id": "employment_001",
        "title": "Employment Law in Nigeria",
        "content": """
        Nigerian employment law is governed primarily by the Labour Act Cap L1 LFN 2004.
        
        Key provisions:
        1. Minimum wage: Currently N70,000 per month (2024)
        2. Working hours: Maximum 8 hours per day, 40 hours per week
        3. Annual leave: Minimum 6 working days after 12 months of service
        4. Notice period: Minimum 1 month for monthly-paid employees
        5. Termination: Must follow due process to avoid wrongful dismissal claims
        
        Employee rights in Nigeria:
        - Right to written contract of employment
        - Right to safe working conditions
        - Right to join trade unions
        - Protection against discrimination
        - Right to maternity leave (12 weeks minimum)
        
        Wrongful dismissal:
        Courts may award reinstatement or compensation
        Compensation typically calculated as salary for notice period plus damages
        Industrial Arbitration Panel handles labour disputes
        """,
        "category": "Employment Law",
        "source": "Labour Act Cap L1 LFN 2004"
    },
    {
        "id": "ndpr_001",
        "title": "NDPR Data Protection Compliance",
        "content": """
        The Nigeria Data Protection Regulation (NDPR) 2019 governs data protection 
        in Nigeria, administered by the National Information Technology Development 
        Agency (NITDA).
        
        Key NDPR requirements for businesses:
        1. Lawful basis for processing personal data
        2. Data Subject Rights:
           - Right to access personal data
           - Right to rectification
           - Right to erasure (right to be forgotten)
           - Right to data portability
        3. Privacy Policy: Must be clearly displayed and accessible
        4. Data Protection Officer: Required for organizations processing large volumes
        5. Data Audit: Annual data protection audit required
        6. Breach Notification: Must notify NITDA within 72 hours of data breach
        
        Penalties for non-compliance:
        - 2% of annual gross revenue or N10 million (whichever is greater)
        - Criminal liability for directors in serious cases
        
        Businesses must register with NITDA if they process personal data of 
        more than 1,000 data subjects annually.
        """,
        "category": "Data Protection",
        "source": "NDPR 2019"
    },
    {
        "id": "tax_001",
        "title": "Corporate Tax Obligations in Nigeria",
        "content": """
        Nigerian companies are subject to several taxes administered by the 
        Federal Inland Revenue Service (FIRS) and State Internal Revenue Services.
        
        Key corporate taxes:
        1. Companies Income Tax (CIT): 30% for large companies, 20% for medium,
           0% for small companies (turnover below N25 million)
        2. Value Added Tax (VAT): 7.5% on goods and services
        3. Withholding Tax (WHT): Varies by transaction type (5-10%)
        4. Capital Gains Tax (CGT): 10% on disposal of assets
        5. Stamp Duties: On legal instruments and documents
        
        Tax filing deadlines:
        - CIT returns: 6 months after financial year end
        - VAT returns: 21st of following month
        - WHT remittance: 21st of following month
        
        Tax incentives available:
        - Pioneer status: 3-5 years tax holiday for qualifying industries
        - Export expansion grant for export-oriented businesses
        - Investment allowances for capital expenditure
        """,
        "category": "Tax Law",
        "source": "CITA Cap C21 LFN 2004"
    },
    {
        "id": "dispute_001",
        "title": "Commercial Dispute Resolution in Nigeria",
        "content": """
        Nigeria offers several mechanisms for resolving commercial disputes:
        
        1. Nigerian Courts:
           - Federal High Court: Commercial matters above N25 million
           - State High Courts: General civil matters
           - Court of Appeal and Supreme Court for appeals
        
        2. Arbitration:
           - Lagos Court of Arbitration (LCA)
           - Nigerian Institute of Chartered Arbitrators
           - International Chamber of Commerce (ICC)
           - Arbitration Act Cap A18 LFN 2004 governs arbitration
        
        3. Mediation:
           - Lagos Multi-Door Courthouse
           - Nigerian Bar Association mediation services
           - Generally faster and cheaper than litigation
        
        4. Alternative Dispute Resolution (ADR):
           - Preferred for commercial disputes
           - Courts may refer matters to ADR
           - Settlements are binding and enforceable
        
        Statute of Limitations:
        - Contract disputes: 6 years
        - Tort claims: 3 years
        - Land disputes: 12 years
        - Recovery of land: 12 years
        """,
        "category": "Dispute Resolution",
        "source": "Arbitration Act Cap A18 LFN 2004"
    },
    {
        "id": "ip_001",
        "title": "Intellectual Property Rights in Nigeria",
        "content": """
        Intellectual property protection in Nigeria is governed by several laws:
        
        1. Copyright:
           - Automatic protection upon creation
           - Duration: Life of author + 70 years
           - Administered by Nigerian Copyright Commission (NCC)
           - Protects literary, musical, artistic works, films, broadcasts
        
        2. Trademarks:
           - Registration required for full protection
           - Duration: 7 years, renewable indefinitely
           - Administered by Trademarks, Patents and Designs Registry
           - Must be distinctive and not descriptive
        
        3. Patents:
           - Protects inventions for 20 years
           - Must be new, inventive, and industrially applicable
           - Not available for mathematical methods, mental acts
        
        4. Industrial Designs:
           - Protects aesthetic features of products
           - Duration: 5 years, renewable up to 15 years
        
        Enforcement:
        - Federal High Court has exclusive jurisdiction
        - Customs Service can seize counterfeit goods at borders
        - Criminal penalties for infringement
        """,
        "category": "Intellectual Property",
        "source": "Copyright Act 2022"
    },
{
        "id": "cama_001",
        "title": "CAMA 2020 — Companies and Allied Matters Act",
        "content": """
        The Companies and Allied Matters Act (CAMA) 2020 is the principal legislation 
        governing companies in Nigeria, replacing the 1990 Act with significant reforms.
        
        Key reforms in CAMA 2020:
        1. Single Member Companies: One person can now incorporate a private company
        2. Electronic Filing: CAC filings can now be done electronically
        3. Reduction of Share Capital: Simplified process without court approval
        4. Mergers and Acquisitions: Streamlined process for business combinations
        5. Minority Shareholder Protection: Enhanced rights for minority shareholders
        6. Company Secretary: Small companies no longer required to have one
        7. Micro Companies: Special provisions for micro businesses
        
        Director responsibilities under CAMA 2020:
        - Duty to act in good faith in best interests of company
        - Duty to avoid conflicts of interest
        - Duty not to accept benefits from third parties
        - Duty to declare interest in proposed transactions
        
        Penalties for non-compliance:
        - Failure to file annual returns: N100,000 plus N5,000 per day
        - Late filing of financial statements: N500,000 fine
        - Directors can be personally liable for company debts in fraud cases
        """,
        "category": "Company Law",
        "source": "CAMA 2020"
    },
    {
        "id": "constitution_001",
        "title": "Fundamental Rights Under Nigerian Constitution",
        "content": """
        Chapter IV of the 1999 Constitution (as amended) guarantees fundamental rights 
        to all persons in Nigeria.
        
        Guaranteed fundamental rights:
        1. Right to Life (Section 33): No one shall be deprived of life intentionally
        2. Right to Dignity (Section 34): Freedom from torture and inhuman treatment
        3. Right to Personal Liberty (Section 35): Protection from unlawful detention
        4. Right to Fair Hearing (Section 36): Fair trial within reasonable time
        5. Right to Private and Family Life (Section 37): Privacy of home and correspondence
        6. Right to Freedom of Thought (Section 38): Freedom of conscience and religion
        7. Right to Freedom of Expression (Section 39): Freedom of the press
        8. Right to Peaceful Assembly (Section 40): Freedom of association
        9. Right to Freedom of Movement (Section 41): Right to move freely in Nigeria
        10. Right to Freedom from Discrimination (Section 42)
        11. Right to Own Property (Section 44): No compulsory acquisition without compensation
        
        Enforcement:
        - Apply to Federal High Court or State High Court
        - Fundamental Rights Enforcement Procedure Rules 2009
        - Can claim damages for violation of rights
        - Attorney General can enforce rights on behalf of public
        """,
        "category": "Constitutional Law",
        "source": "Constitution of Nigeria 1999"
    },
    {
        "id": "fintech_001",
        "title": "CBN Regulations for Fintech and Digital Banking",
        "content": """
        The Central Bank of Nigeria (CBN) regulates financial technology companies 
        and digital banking services in Nigeria.
        
        Key CBN regulations for fintechs:
        1. Payment Service Bank (PSB) License:
           - Minimum capital: N5 billion
           - Can accept deposits, facilitate payments
           - Cannot grant loans or issue credit cards
        
        2. Mobile Money Operator License:
           - Minimum capital: N2 billion
           - Must partner with licensed bank
           - Subject to KYC requirements
        
        3. USSD Banking Guidelines:
           - Charges regulated by CBN
           - Maximum charge: N6.98 per transaction
        
        4. Open Banking Framework:
           - Data sharing between banks and fintechs
           - Customer consent required
           - API standards prescribed by CBN
        
        5. Cryptocurrency Regulations:
           - CBN prohibited banks from crypto transactions in 2021
           - SEC regulates digital assets separately
           - eNaira (CBDC) is the official digital currency
        
        Compliance requirements:
        - Anti-Money Laundering (AML) policies
        - Know Your Customer (KYC) verification
        - Transaction monitoring systems
        - Suspicious Transaction Reports to NFIU
        """,
        "category": "Financial Regulation",
        "source": "CBN Act and Guidelines"
    },
    {
        "id": "petroleum_001",
        "title": "Petroleum Industry Act 2021 — Oil and Gas Law",
        "content": """
        The Petroleum Industry Act (PIA) 2021 fundamentally restructured Nigeria's 
        oil and gas industry, replacing several existing laws.
        
        Key provisions of PIA 2021:
        1. New Regulatory Agencies:
           - Nigerian Upstream Petroleum Regulatory Commission (NUPRC)
           - Nigerian Midstream and Downstream Petroleum Regulatory Authority (NMDPRA)
        
        2. Fiscal Framework:
           - Royalty rates revised for upstream operations
           - Hydrocarbon tax introduced
           - Companies Income Tax still applies
        
        3. Host Community Development:
           - 3% of operating expenditure to host communities
           - Host Community Development Trust mandatory
        
        4. Nigerian National Petroleum Company (NNPC) Limited:
           - Commercialized and corporatized
           - Operates on commercial principles
           - No longer a government department
        
        5. Petroleum Prospecting License (PPL):
           - Replaces Oil Prospecting License (OPL)
           - Maximum 4 years for offshore, 3 years onshore
        
        6. Petroleum Mining Lease (PML):
           - Replaces Oil Mining Lease (OML)
           - Maximum 20 years, renewable
        
        Environmental obligations:
        - Gas flaring penalties increased significantly
        - Mandatory environmental impact assessments
        - Decommissioning funds required
        """,
        "category": "Oil and Gas Law",
        "source": "Petroleum Industry Act 2021"
    },
    {
        "id": "cybercrime_001",
        "title": "Cybercrime Act 2015 — Digital Offences in Nigeria",
        "content": """
        The Cybercrimes (Prohibition, Prevention) Act 2015 is Nigeria's primary 
        legislation on cybercrime and digital offences.
        
        Key offences under the Cybercrime Act:
        1. Unauthorized Access: 
           - Penalty: 3 years imprisonment or N7 million fine
        2. System Interference:
           - Penalty: 3 years or N7 million fine
        3. Identity Theft:
           - Penalty: 7 years imprisonment or N5 million fine
        4. Cyberstalking:
           - Penalty: 3 years or N7 million fine
        5. Sending offensive messages:
           - Penalty: 3 years or N7 million fine
        6. Online fraud (Yahoo Yahoo):
           - Penalty: 7 years minimum, asset forfeiture
        7. ATM/Card fraud:
           - Penalty: 7 years and N5 million fine
        
        Business obligations under Cybercrime Act:
        - Financial institutions must report suspicious transactions
        - Service providers must retain customer data for 2 years
        - Must cooperate with law enforcement investigations
        - Must implement cybersecurity measures
        
        Enforcement:
        - Nigerian Police Force Cybercrime Unit
        - Economic and Financial Crimes Commission (EFCC)
        - Office of the National Security Adviser
        """,
        "category": "Cybercrime Law",
        "source": "Cybercrimes Act 2015"
    },
    {
        "id": "consumer_001",
        "title": "Consumer Protection Laws in Nigeria",
        "content": """
        Consumer protection in Nigeria is governed by the Federal Competition and 
        Consumer Protection Act (FCCPA) 2018, administered by the Federal Competition 
        and Consumer Protection Commission (FCCPC).
        
        Consumer rights under FCCPA 2018:
        1. Right to quality goods and services
        2. Right to accurate product information
        3. Right to fair pricing (no price gouging)
        4. Right to return defective products
        5. Right to compensation for damages
        6. Right to privacy of consumer information
        7. Right to be heard (make complaints)
        
        Business obligations:
        - Display prices clearly in Nigerian currency
        - Provide accurate product descriptions
        - Honor warranties and guarantees
        - Cannot engage in misleading advertising
        - Must have complaint handling mechanism
        
        Prohibited practices:
        - Price fixing with competitors
        - Market allocation agreements
        - Abuse of dominant market position
        - Deceptive trade practices
        
        Penalties:
        - Up to 10% of annual turnover for anti-competitive practices
        - Criminal prosecution for directors
        - Disgorgement of profits from violations
        
        Filing complaints:
        - FCCPC website: www.fccpc.gov.ng
        - Can seek damages in court
        - Class action suits permitted
        """,
        "category": "Consumer Protection",
        "source": "FCCPA 2018"
    },
    {
        "id": "immigration_001",
        "title": "Immigration and Work Permits in Nigeria",
        "content": """
        Immigration in Nigeria is governed by the Immigration Act 2015, 
        administered by the Nigeria Immigration Service (NIS).
        
        Types of visas and permits:
        1. Subject to Regularization (STR) Visa:
           - For foreigners seeking employment in Nigeria
           - Must be converted to CERPAC within 90 days
        
        2. Combined Expatriate Residence Permit and Aliens Card (CERPAC):
           - Main work and residence permit
           - Valid for 2 years, renewable
           - Cost: $2,000 for initial, $1,000 for renewal
        
        3. Business Visa:
           - Short-term business visits
           - Maximum 90 days
           - Cannot be used for employment
        
        Expatriate quota:
        - Companies must apply for expatriate quota positions
        - Maximum ratio: 1 expatriate to 5 Nigerians
        - Specific positions must be justified
        - Succession plan required (training Nigerian replacement)
        
        Employer obligations:
        - Must obtain expatriate quota approval before hiring foreigners
        - Must register expatriates with NIS
        - Penalties for employing illegal immigrants: N250,000 per person
        - Deportation of illegal workers
        
        Nigerians in diaspora:
        - Nigerian passport valid for 5 years (adult), 3 years (minor)
        - Dual citizenship permitted since 1999 Constitution
        """,
        "category": "Immigration Law",
        "source": "Immigration Act 2015"
    },
    {
        "id": "real_estate_001",
        "title": "Real Estate Investment and Regulation in Nigeria",
        "content": """
        Real estate investment in Nigeria is regulated by various federal and 
        state laws, with significant variations between states.
        
        Key regulations:
        1. Land Use Act 1978:
           - All land vested in State Governors
           - Certificate of Occupancy (C of O) is primary title
           - Governor's consent required for transfers
        
        2. Lagos State Property Protection Law 2016:
           - Protects property owners from illegal occupants
           - Fast-track eviction process
           - Penalties for illegal occupation
        
        3. Real Estate Developers:
           - Must register with Corporate Affairs Commission
           - Lagos requires registration with Real Estate Developers Association
           - Must obtain building permits before construction
        
        Investment structures:
        1. Direct ownership: Buy land/property outright
        2. Joint venture with landowner
        3. Real Estate Investment Trust (REIT):
           - Listed on Nigerian Stock Exchange
           - Regulated by SEC
           - Minimum distribution: 90% of income
        
        Due diligence checklist:
        - Verify title at Land Registry
        - Check for government acquisition notices
        - Confirm survey plan authenticity
        - Check building approval/permit
        - Verify no pending litigation
        - Check for existing tenants/occupants
        
        Rental regulations:
        - Lagos Tenancy Law 2011 governs landlord-tenant relations
        - Maximum advance rent: 1 year for residential, 2 years commercial
        - Notice to quit: Minimum 7-30 days depending on tenancy type
        """,
        "category": "Real Estate Law",
        "source": "Land Use Act 1978, Lagos Tenancy Law 2011"
    },
    {
        "id": "family_001",
        "title": "Family Law and Marriage in Nigeria",
        "content": """
        Family law in Nigeria operates under a dual system of statutory and 
        customary law, with significant regional variations.
        
        Types of marriage in Nigeria:
        1. Statutory Marriage (Marriage Act):
           - Conducted at Marriage Registry
           - Monogamous by law
           - Minimum age: 21 (or 18 with parental consent)
           - Legally recognized across Nigeria
        
        2. Customary Marriage:
           - Governed by local customs and traditions
           - May permit polygamy
           - Recognition varies by state
           - Payment of bride price required in most cultures
        
        3. Islamic Marriage (Nikah):
           - Governed by Islamic law (Sharia)
           - Applicable in northern states
           - Permits up to 4 wives with conditions
        
        Divorce:
        - Statutory marriage: File in High Court
           Grounds: Irretrievable breakdown of marriage
           Process: Minimum 2 years separation
        - Customary marriage: Return bride price
           Governed by applicable customary law
        
        Children and custody:
        - Best interests of child is primary consideration
        - Both parents have equal rights to custody
        - Child maintenance is mandatory for non-custodial parent
        - Child Rights Act 2003 protects children's rights
        
        Inheritance:
        - Statutory: Governed by Administration of Estates Law
        - Customary: Governed by local customs (often excludes women)
        - Islamic: Governed by Sharia inheritance rules
        - A valid Will can override customary inheritance rules
        """,
        "category": "Family Law",
        "source": "Marriage Act, Child Rights Act 2003"
    },
    {
        "id": "criminal_001",
        "title": "Criminal Law and Procedure in Nigeria",
        "content": """
        Criminal law in Nigeria is primarily governed by the Criminal Code Act 
        (southern Nigeria) and the Penal Code (northern Nigeria).
        
        Key criminal offences and penalties:
        1. Corruption and Bribery:
           - ICPC Act: Up to 7 years imprisonment
           - EFCC Act: Up to 5 years for economic crimes
           - Asset forfeiture mandatory
        
        2. Fraud:
           - Advance fee fraud (419): Up to 20 years
           - Bank fraud: Up to 10 years
           - Insurance fraud: Up to 5 years
        
        3. Theft and Robbery:
           - Simple theft: Up to 3 years
           - Armed robbery: Life imprisonment or death
           - Burglary: Up to 14 years
        
        4. Drug offences:
           - NDLEA Act governs drug offences
           - Trafficking: Up to 25 years
           - Possession: Up to 15 years
        
        Criminal procedure:
        1. Arrest: Police can arrest with or without warrant
        2. Charge: Must be charged within 24-48 hours
        3. Bail: Constitutional right, may be denied for capital offences
        4. Trial: Magistrate Court (minor) or High Court (serious)
        5. Appeal: Court of Appeal, then Supreme Court
        
        Rights of accused:
        - Right to know charges
        - Right to legal representation
        - Right to silence (cannot be compelled to testify)
        - Right to fair hearing within reasonable time
        - Presumption of innocence
        """,
        "category": "Criminal Law",
        "source": "Criminal Code Act, Administration of Criminal Justice Act 2015"
    }
]


# ---- RAG ENGINE CLASS ----
class LexAIRAGEngine:
    def __init__(self):
        print("  Initializing LexAI RAG Engine...")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Nigerian Legal Knowledge Base for LexAI"}
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

        # Add to ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )

        print(f"  Loaded {len(documents)} documents successfully!")
        print(f"  Total documents in DB: {self.collection.count()}")

    def search(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def format_context(self, results):
        context = ""
        docs = results["documents"][0]
        metas = results["metadatas"][0]

        for i, (doc, meta) in enumerate(zip(docs, metas)):
            context += f"\n--- Source {i+1}: {meta['title']} ---\n"
            context += f"Category: {meta['category']}\n"
            context += f"Source: {meta['source']}\n"
            context += f"Content: {doc[:500]}...\n"

        return context

    def answer(self, question):
        print(f"\n  Question: {question}")
        print("  Searching knowledge base...")

        # Search for relevant documents
        results = self.search(question)
        context = self.format_context(results)

        # Build prompt
        prompt = f"""You are LexAI, an AI legal assistant specializing in Nigerian law.
Use the following legal documents to answer the question accurately.

LEGAL DOCUMENTS:
{context}

QUESTION: {question}

Provide a clear, accurate answer based on Nigerian law. 
Reference the specific laws and sources provided.
Keep your answer practical and actionable."""

        print("\n  Context retrieved:")
        for i, meta in enumerate(results["metadatas"][0]):
            print(f"    {i+1}. {meta['title']} ({meta['category']})")

        print("\n  📋 GENERATED PROMPT FOR CLAUDE:")
        print("-" * 50)
        print(prompt[:300] + "...")
        print("-" * 50)

        return prompt, results

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  LexAI RAG Pipeline — Week 3")
print("=" * 55)

# Initialize engine
engine = LexAIRAGEngine()

# Load Nigerian legal documents
engine.load_documents(NIGERIAN_LEGAL_DOCS)

# Test queries
test_questions = [
    "How do I register a company in Nigeria?",
    "What are my rights as an employee in Nigeria?",
    "How does NDPR affect my business?",
    "What taxes does my company need to pay?",
    "How can I protect my trademark in Nigeria?"
]

print("\n" + "=" * 55)
print("  TESTING RAG SEARCH")
print("=" * 55)

for question in test_questions:
    prompt, results = engine.answer(question)
    print(f"\n  Top match: {results['metadatas'][0][0]['title']}")
    print(f"  Distance: {results['distances'][0][0]:.4f}")
    print()

print("=" * 55)
print("  RAG Engine ready!")
print("  Next: Connect Claude API for full answers")
print("=" * 55)
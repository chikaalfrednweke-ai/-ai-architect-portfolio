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
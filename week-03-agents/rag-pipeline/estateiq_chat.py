# ============================================
# Fred Baker's Automations
# estateiq_chat.py — EstateIQ Chat + Claude
# Nigerian Real Estate AI Assistant
# ============================================

import streamlit as st
import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="EstateIQ — Nigerian Real Estate AI",
    page_icon="🏢",
    layout="wide"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .stApp { background-color: #0A0A0A; color: #E8E0D0; }
    .stChatMessage { background-color: #111111; border-radius: 8px; }
    h1, h2, h3 { color: #E2C97E; }
    .source-card {
        background: #111111;
        border: 1px solid rgba(76,175,122,0.2);
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 13px;
    }
    .stButton button {
        background: rgba(76,175,122,0.1);
        border: 1px solid rgba(76,175,122,0.3);
        color: #4CAF7A;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
col1, col2 = st.columns([3,1])
with col1:
    st.title("🏢 EstateIQ")
    st.markdown("*Nigerian Real Estate AI Assistant — Powered by Claude + RAG*")
with col2:
    st.markdown("###")
    st.markdown("📍 **Abuja & Lagos**")
    st.markdown("🤖 **Claude AI Powered**")

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.title("🏢 EstateIQ")
st.sidebar.markdown("**Nigerian Real Estate AI**")
st.sidebar.markdown("*Powered by Fred Baker's Automations*")
st.sidebar.markdown("---")

st.sidebar.markdown("**Knowledge Base:**")
areas = [
    "Abuja property prices 2024",
    "Lagos property prices 2024",
    "Certificate of Occupancy (C of O)",
    "Investment strategies & yields",
    "Due diligence checklist",
    "Rental market & laws",
    "Mortgage & financing",
    "REIT investing",
    "Property valuation",
    "PropTech platforms",
]
for area in areas:
    st.sidebar.markdown(f"✅ {area}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Questions:**")
sample_questions = [
    "Property prices in Maitama?",
    "Best investment strategy?",
    "How to get a C of O?",
    "Rental yields in Lekki?",
    "How to verify a title?",
    "How does mortgage work?",
    "What is a REIT?",
    "Short-let vs long-term rental?",
]
for q in sample_questions:
    if st.sidebar.button(q, key=f"btn_{q}"):
        st.session_state.pending_question = q

st.sidebar.markdown("---")
st.sidebar.success("🤖 Claude AI Connected!")

# ---- DATABASE + CLAUDE ----
DB_PATH = "./chroma_db"
COLLECTION_NAME = "estateiq_nigeria_realestate"

@st.cache_resource
def get_collection():
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        if collection.count() == 0:
            load_realestate_docs(collection)
        return collection
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def load_realestate_docs(collection):
    docs = [
        ("abuja_001", "Abuja Property Market Overview 2024",
         "Abuja prime districts 2024: Maitama residential plots N150M-N500M, 4-bedroom N250M-N800M, rental yield 5-8%. Asokoro plots N100M-N400M, embassy district. Wuse 2 commercial offices N2M-N5M per sqm. Gwarinpa 3-bedroom N30M-N80M. Jahi plots N50M-N150M emerging premium. Life Camp 3-bedroom N25M-N60M. Market appreciation 15-20% annually.",
         "Market Data", "Fred Baker's Automations Research 2024"),
        ("lagos_001", "Lagos Property Market Overview 2024",
         "Lagos districts 2024: Victoria Island apartments N150M-N500M, offices N3M-N8M per sqm. Ikoyi luxury N200M-N1B+. Lekki Phase 1 3-bedroom N50M-N150M. Ajah N20M-N60M good appreciation. Ibeju-Lekki land N2M-N15M future growth near Dangote Refinery. Mainland Ikeja 3-bedroom N15M-N40M, 8-12% rental yields. Short-let yields 15-25% annually.",
         "Market Data", "Fred Baker's Automations Research 2024"),
        ("cof_001", "Certificate of Occupancy C of O Complete Guide",
         "C of O is strongest title document in Nigeria. Types: C of O, Right of Occupancy, Deed of Assignment, Governor's Consent. Abuja process: land allocation, survey N200,000-N500,000, apply at AGIS, pay fees, inspection, 6-18 months. Lagos: apply at Land Bureau, submit survey and deed, pay 1.5-3% of property value, 3-12 months. Red flags: reluctant to verify at registry, multiple corrections on C of O, government acquisition areas.",
         "Property Documentation", "Land Use Act 1978"),
        ("investment_001", "Real Estate Investment Strategies Nigeria",
         "Strategies by returns: Short-let Airbnb 20-35% annually best near airports, Student housing 15-25% near universities, Commercial properties 12-18% longer leases, Buy and hold residential 8-15%, Land banking capital appreciation in Ibeju-Lekki and Lugbe. Key metric: Gross Rental Yield equals Annual Rent divided by Price times 100. Target minimum 8% gross yield. Federal Mortgage Bank rates 6-9%.",
         "Investment Strategy", "Nigerian Real Estate Analysis"),
        ("due_diligence_001", "Property Due Diligence Checklist Nigeria",
         "Title verification: official Land Registry search, verify C of O authenticity, check mortgages and charges, government acquisition notices, court records. Physical inspection: multiple visits, structural engineer, verify survey plan dimensions, flooding history. Documents: survey plan, building permit, tax clearance, stamped Deed of Assignment, Governor's Consent. Costs: legal fees 5-10%, agency fees 5-10%, government fees 1-3%. Red flags: multiple ownership claims, priced below market, pressure for quick payment.",
         "Due Diligence", "Nigerian Real Estate Best Practices"),
        ("rental_001", "Rental Market and Landlord Tenant Law Nigeria",
         "Lagos Tenancy Law 2011: maximum advance rent residential 1 year, commercial 2 years. Notice periods: weekly 1 week, monthly 1 month, yearly 6 months. Rent increases need 6 months notice. Self-help eviction illegal. Yields: Maitama 5-8%, Wuse 2 7-10%, Victoria Island 6-9%, Lekki 8-12%, Ikeja 10-15%. Short-let rates: Maitama N80,000-N300,000 per night, VI N100,000-N500,000. Property management 10% of annual rent.",
         "Rental Market", "Lagos Tenancy Law 2011"),
        ("reit_001", "Real Estate Investment Trusts REITs Nigeria",
         "REITs listed on Nigerian Exchange NGX from N5,000 minimum. UPDC REIT yields 8-12%, Skye Shelter Fund, Union Homes REIT. Regulated by SEC Nigeria, must distribute 90% of income as dividends. Advantages: low entry, professional management, liquidity, diversification, regular dividends. How to invest: open stockbroker account, fund it, buy REIT units on NGX, receive dividends.",
         "Investment Vehicles", "SEC Nigeria NGX Guidelines"),
        ("valuation_001", "Property Valuation Methods Nigeria",
         "Methods by licensed Estate Surveyors NIESV: Comparative method comparing similar sales, Investment method Value equals Annual Rent divided by Cap Rate (6-12% in Nigeria), Cost method land plus depreciated building, Residual method for development land. C of O commands 20-30% premium over undocumented properties. Fees: 0.25-0.5% of property value residential. Needed for mortgage, insurance, legal disputes, probate.",
         "Property Valuation", "NIESV Guidelines"),
        ("mortgage_001", "Mortgage and Property Financing Nigeria",
         "Options: Federal Mortgage Bank FMBN 6% interest maximum N15M loan requires NHF contribution 6+ months. Primary Mortgage Banks 15-22% up to 20 years. Commercial banks 20-28% stricter requirements. Developer financing 30% upfront balance installments. Cooperative society loans lower interest members only. Requirements: 3 years employment, repayment max 33% income, clean CRC credit check, property must have C of O. Costs: legal 1-2%, valuation 0.25-0.5%, insurance 0.35%.",
         "Property Financing", "FMBN Guidelines CBN Regulations"),
        ("proptech_001", "PropTech and Digital Real Estate Nigeria",
         "Leading platforms: PropertyPro.ng largest 300,000+ listings, Private Property Nigeria, Tolet.com.ng rentals, Spleet monthly rent, Seso Global blockchain titles. Digital trends: virtual tours, AI recommendations, digital mortgages, blockchain registry. EstateIQ advantages: AI-powered matching, WhatsApp-first, naira-denominated, NDPR compliant. Market: Nigerian real estate 1.1 trillion dollars, PropTech penetration under 5%, 20 million unit housing deficit.",
         "PropTech", "Nigerian PropTech Report 2024"),
    ]

    ids = [d[0] for d in docs]
    texts = [f"{d[1]}\n\n{d[2]}" for d in docs]
    metadatas = [{"title": d[1], "category": d[3], "source": d[4]} for d in docs]
    collection.upsert(ids=ids, documents=texts, metadatas=metadatas)

@st.cache_resource
def get_claude():
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except:
        api_key = os.getenv("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=api_key)

def search_docs(query, n_results=3):
    collection = get_collection()
    if not collection:
        return None
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )

def ask_estateiq(question, results):
    context = ""
    for i, (doc, meta) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0]
    )):
        context += f"\n--- Source {i+1}: {meta['title']} ---\n"
        context += f"Category: {meta['category']}\n"
        context += f"Content: {doc[:700]}\n"

    claude = get_claude()
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="""You are EstateIQ, an expert AI real estate assistant 
specializing in the Nigerian property market. You work for Fred Baker's Automations,
a Nigerian AI company based in Abuja.

Your personality:
- Professional but friendly
- Data-driven with specific Nigerian prices and yields
- Always practical and actionable
- Reference specific Nigerian laws and regulations
- Use ₦ for naira amounts
- Format responses with clear headers and tables where helpful""",
        messages=[
            {
                "role": "user",
                "content": f"""Use this Nigerian real estate knowledge base to answer:

{context}

Question: {question}

Provide a comprehensive, accurate answer about the Nigerian property market.
Include specific prices, yields, and actionable recommendations."""
            }
        ]
    )
    return message.content[0].text

# ---- CHAT INTERFACE ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """Hello! I'm **EstateIQ** 🏢 — your Nigerian real estate AI assistant, powered by Claude AI.

I have deep knowledge of the Nigerian property market including:
- 📍 **Abuja & Lagos** property prices by district
- 📋 **C of O** process and title verification
- 💰 **Investment strategies** with real yield data
- 🏦 **Mortgage options** including Federal Mortgage Bank rates
- 📊 **Rental yields** across major Nigerian cities
- 🏗️ **Due diligence** checklists for safe property purchase

I'm powered by **real Nigerian market data** and **Claude AI** for comprehensive analysis.

**What real estate question can I help you with today?**"""
        }
    ]

# Handle pending question from sidebar
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    results = search_docs(question)
    if results:
        with st.spinner("EstateIQ is analyzing Nigerian market data..."):
            answer = ask_estateiq(question, results)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": results["metadatas"][0]
        })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Sources Used"):
                for meta in message["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>🏢 {meta['title']}</strong><br>
                        <small>{meta['category']} | {meta['source']}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about Nigerian real estate..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🏢 EstateIQ analyzing Nigerian market data..."):
            results = search_docs(prompt)
            if results:
                answer = ask_estateiq(prompt, results)
                st.markdown(answer)

                with st.expander("📚 Sources Used"):
                    for meta in results["metadatas"][0]:
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>🏢 {meta['title']}</strong><br>
                            <small>{meta['category']} | {meta['source']}</small>
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": results["metadatas"][0]
                })
            else:
                answer = "I couldn't find relevant information. Please try rephrasing your question."
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
# ============================================
# Fred Baker's Automations
# lexai_chat.py — LexAI Chat + Claude AI
# Nigerian Legal AI Assistant
# ============================================

import streamlit as st
import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="LexAI — Nigerian Legal AI",
    page_icon="⚖️",
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
        border: 1px solid rgba(74,143,201,0.2);
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 13px;
    }
    .stButton button {
        background: rgba(74,143,201,0.1);
        border: 1px solid rgba(74,143,201,0.3);
        color: #4A8FC9;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
col1, col2 = st.columns([3,1])
with col1:
    st.title("⚖️ LexAI")
    st.markdown("*Nigerian Legal AI Assistant — Powered by Claude + RAG*")
with col2:
    st.markdown("###")
    st.markdown("📍 **Abuja, Nigeria**")
    st.markdown("🤖 **Claude AI Powered**")

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.title("⚖️ LexAI")
st.sidebar.markdown("**Nigerian Legal AI**")
st.sidebar.markdown("*Powered by Fred Baker's Automations*")
st.sidebar.markdown("---")

st.sidebar.markdown("**Legal Knowledge Base:**")
areas = [
    "Company Law (CAC, CAMA 2020)",
    "Contract Law",
    "Property & Land Law",
    "Employment Law",
    "Data Protection (NDPR)",
    "Tax Law (FIRS)",
    "Oil & Gas (PIA 2021)",
    "Cybercrime Law",
    "Consumer Protection",
    "Immigration Law",
    "Family Law",
    "Criminal Law",
    "Constitutional Rights",
    "IP & Trademark Law",
    "Financial Regulation",
    "Real Estate Law",
    "Dispute Resolution",
]
for area in areas:
    st.sidebar.markdown(f"✅ {area}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Questions:**")
sample_questions = [
    "How do I register a company?",
    "What are employee rights?",
    "How does NDPR affect me?",
    "What taxes must I pay?",
    "How to protect my trademark?",
    "How to handle contract dispute?",
    "What is the Cybercrime Act?",
    "How to get a work permit?",
]
for q in sample_questions:
    if st.sidebar.button(q, key=f"btn_{q}"):
        st.session_state.pending_question = q

st.sidebar.markdown("---")
st.sidebar.success("🤖 Claude AI Connected!")

# ---- DATABASE + CLAUDE ----
DB_PATH = "./chroma_db"
COLLECTION_NAME = "lexai_nigeria_legal"

@st.cache_resource
@st.cache_resource
def get_collection():
    try:
        # Try loading existing collection
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        
        # If empty, load documents
        if collection.count() == 0:
            load_legal_docs(collection)
        return collection
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def load_legal_docs(collection):
    docs = [
        ("cac_001", "CAC Company Registration Requirements",
         "To register a company in Nigeria with CAC: minimum two shareholders, share capital N100,000, at least one director, registered office address in Nigeria, Memorandum and Articles of Association, Form CAC 1.1, valid ID for directors and shareholders, TIN for corporate shareholders. Registration takes 1-2 weeks, costs N10,000-N50,000. Annual returns must be filed within 42 days of incorporation anniversary.",
         "Company Law", "CAC Act 2020"),
        ("contract_001", "Contract Formation Under Nigerian Law",
         "Valid Nigerian contract requires: Offer, Acceptance, Consideration, Capacity (18+, sound mind), Intention to create legal relations, Legality. Written contracts preferred but oral enforceable. Statute of Frauds requires writing for: land contracts, contracts over one year, guarantees. Remedies: damages, specific performance, injunction.",
         "Contract Law", "Nigerian Contract Law"),
        ("employment_001", "Employment Law in Nigeria",
         "Labour Act Cap L1 LFN 2004: Minimum wage N70,000/month (2024), 8 hours/day max, 6 days annual leave after 12 months, 1 month notice period. Rights: written contract, safe conditions, union membership, anti-discrimination, 12 weeks maternity leave. Wrongful dismissal: reinstatement or compensation available.",
         "Employment Law", "Labour Act Cap L1 LFN 2004"),
        ("ndpr_001", "NDPR Data Protection Compliance",
         "NDPR 2019 administered by NITDA. Requirements: lawful basis for processing, data subject rights (access, rectification, erasure, portability), privacy policy, Data Protection Officer, annual audit, breach notification within 72 hours. Penalties: 2% annual revenue or N10 million. Register with NITDA if processing 1000+ data subjects annually.",
         "Data Protection", "NDPR 2019"),
        ("tax_001", "Corporate Tax Obligations in Nigeria",
         "FIRS taxes: Companies Income Tax 30% large, 20% medium, 0% small (under N25M turnover), VAT 7.5%, Withholding Tax 5-10%, Capital Gains Tax 10%, Stamp Duties. Deadlines: CIT 6 months after year end, VAT 21st of following month. Incentives: Pioneer status 3-5 year holiday, export grants, investment allowances.",
         "Tax Law", "CITA Cap C21 LFN 2004"),
        ("cama_001", "CAMA 2020 Companies and Allied Matters Act",
         "CAMA 2020 reforms: Single member companies allowed, electronic CAC filing, simplified share capital reduction, enhanced minority shareholder protection, small companies no longer need company secretary. Director duties: good faith, avoid conflicts, declare interests. Penalties: N100,000 plus N5,000 per day for late annual returns.",
         "Company Law", "CAMA 2020"),
        ("ip_001", "Intellectual Property Rights in Nigeria",
         "Copyright: automatic protection, life plus 70 years, Nigerian Copyright Commission. Trademarks: registration required, 7 years renewable, Trademarks Registry. Patents: 20 years, must be new and inventive. Industrial Designs: 5 years renewable to 15 years. Enforcement: Federal High Court exclusive jurisdiction.",
         "Intellectual Property", "Copyright Act 2022"),
        ("dispute_001", "Commercial Dispute Resolution in Nigeria",
         "Options: Federal High Court (above N25M), State High Courts, Lagos Court of Arbitration, mediation via Lagos Multi-Door Courthouse. Arbitration Act Cap A18 LFN 2004. Limitation periods: contracts 6 years, torts 3 years, land 12 years. ADR preferred for commercial disputes, settlements binding and enforceable.",
         "Dispute Resolution", "Arbitration Act Cap A18 LFN 2004"),
        ("cybercrime_001", "Cybercrime Act 2015 Digital Offences Nigeria",
         "Cybercrimes Act 2015 offences: Unauthorized access 3 years or N7M, Identity theft 7 years or N5M, Online fraud 7 years minimum with asset forfeiture, ATM fraud 7 years and N5M. Business obligations: report suspicious transactions, retain customer data 2 years, implement cybersecurity measures, cooperate with law enforcement.",
         "Cybercrime Law", "Cybercrimes Act 2015"),
        ("property_001", "Land Ownership and Title in Nigeria",
         "Land Use Act 1978: all land vested in State Governors. Types: Statutory Right of Occupancy, Customary Right of Occupancy, Certificate of Occupancy (C of O). C of O process: survey land, apply at Land Bureau, pay fees, 3-12 months. Due diligence: verify at Land Registry, check encumbrances, confirm Governor's consent for transfers.",
         "Property Law", "Land Use Act 1978"),
    ]
    
    ids = [d[0] for d in docs]
    texts = [f"{d[1]}\n\n{d[2]}" for d in docs]
    metadatas = [{"title": d[1], "category": d[3], "source": d[4]} for d in docs]
    
    collection.upsert(ids=ids, documents=texts, metadatas=metadatas)    


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

def ask_lexai(question, results):
    context = ""
    for i, (doc, meta) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0]
    )):
        context += f"\n--- Source {i+1}: {meta['title']} ---\n"
        context += f"Category: {meta['category']}\n"
        context += f"Source: {meta['source']}\n"
        context += f"Content: {doc[:700]}\n"

    claude = get_claude()
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="""You are LexAI, an expert AI legal assistant
specializing in Nigerian law. You work for Fred Baker's Automations,
a Nigerian AI company based in Abuja.

Your personality:
- Professional and authoritative
- Reference specific Nigerian laws and sections
- Always practical and actionable
- Add appropriate legal disclaimers
- Format responses with clear headers and tables
- Use Nigerian legal terminology correctly
- Cite specific acts, sections and cases where relevant""",
        messages=[
            {
                "role": "user",
                "content": f"""Use this Nigerian legal knowledge base to answer:

{context}

Question: {question}

Provide a comprehensive, accurate answer based on Nigerian law.
Reference specific laws, sections and practical steps."""
            }
        ]
    )
    return message.content[0].text

# ---- CHAT INTERFACE ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """Hello! I'm **LexAI** ⚖️ — your Nigerian legal AI assistant, powered by Claude AI.

I have deep knowledge of Nigerian law including:
- 🏢 **Company Law** — CAC registration, CAMA 2020
- 📋 **Contract Law** — Formation, breach, remedies
- 🏘️ **Property Law** — Land Use Act, C of O
- 👷 **Employment Law** — Labour Act, employee rights
- 🔒 **Data Protection** — NDPR 2019 compliance
- 💰 **Tax Law** — CIT, VAT, WHT obligations
- ⛽ **Oil & Gas Law** — PIA 2021
- 💻 **Cybercrime Law** — Digital offences
- And **17 more areas** of Nigerian law!

I'm powered by **real Nigerian legal documents** and **Claude AI** for comprehensive analysis.

⚠️ *Note: LexAI provides legal information, not legal advice. Consult a qualified Nigerian lawyer for specific legal matters.*

**What legal question can I help you with today?**"""
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
        with st.spinner("⚖️ LexAI is analyzing Nigerian law..."):
            answer = ask_lexai(question, results)
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
            with st.expander("📚 Legal Sources"):
                for meta in message["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>⚖️ {meta['title']}</strong><br>
                        <small>{meta['category']} | {meta['source']}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a Nigerian legal question..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚖️ LexAI analyzing Nigerian law..."):
            results = search_docs(prompt)
            if results:
                answer = ask_lexai(prompt, results)
                st.markdown(answer)

                with st.expander("📚 Legal Sources"):
                    for meta in results["metadatas"][0]:
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>⚖️ {meta['title']}</strong><br>
                            <small>{meta['category']} | {meta['source']}</small>
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": results["metadatas"][0]
                })
            else:
                answer = "I couldn't find relevant information. Please try rephrasing."
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
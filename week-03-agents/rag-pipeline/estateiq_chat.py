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
        return client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

@st.cache_resource
def get_claude():
    return anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

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
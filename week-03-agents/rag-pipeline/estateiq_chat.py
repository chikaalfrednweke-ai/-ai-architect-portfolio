# ============================================
# Fred Baker's Automations
# estateiq_chat.py — EstateIQ Chat Interface
# Nigerian Real Estate AI Assistant
# ============================================

import streamlit as st
import chromadb
import os

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
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
col1, col2 = st.columns([3,1])
with col1:
    st.title("🏢 EstateIQ")
    st.markdown("*Nigerian Real Estate AI Assistant — Powered by Fred Baker's Automations*")
with col2:
    st.markdown("###")
    st.markdown("📍 **Abuja & Lagos, Nigeria**")
    st.markdown("🏢 **Fred Baker's Automations**")

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.title("🏢 EstateIQ")
st.sidebar.markdown("**Nigerian Real Estate Knowledge Base**")
st.sidebar.markdown("---")
st.sidebar.markdown("**I Can Help With:**")
areas = [
    "Abuja property prices",
    "Lagos property prices",
    "Certificate of Occupancy (C of O)",
    "Investment strategies",
    "Due diligence checklist",
    "Rental market & yields",
    "Mortgage options",
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
    "How to get a C of O?",
    "Best investment strategy?",
    "How to verify a title?",
    "Rental yields in Lekki?",
    "How does mortgage work?",
    "What is a REIT?",
    "How is property valued?",
]
for q in sample_questions:
    if st.sidebar.button(q, key=q):
        st.session_state.selected_question = q

st.sidebar.markdown("---")
st.sidebar.info("🔑 Connect Claude API for full AI analysis")

# ---- DATABASE ----
DB_PATH = "./chroma_db"
COLLECTION_NAME = "estateiq_nigeria_realestate"

@st.cache_resource
def get_rag_engine():
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
        return collection
    except Exception as e:
        st.error(f"RAG Engine error: {e}")
        return None

def search_docs(query, n_results=3):
    collection = get_rag_engine()
    if not collection:
        return None
    return collection.query(query_texts=[query], n_results=n_results)

def generate_answer(query, results):
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    answer = f"Here's what I found about **'{query}'** in the Nigerian real estate market:\n\n"

    for i, (doc, meta) in enumerate(zip(docs, metas)):
        answer += f"**{meta['title']}** ({meta['category']})\n"
        answer += f"*Source: {meta['source']}*\n\n"
        content = doc.replace(meta['title'], '').strip()[:400]
        answer += f"{content}...\n\n"
        if i < len(docs) - 1:
            answer += "---\n\n"

    answer += "\n\n⚠️ *Preview response. Connect Claude API for comprehensive AI-powered real estate analysis.*"
    return answer

# ---- CHAT ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """Hello! I'm **EstateIQ**, your Nigerian real estate AI assistant! 🏢

I can help you with:
- 📍 Property prices in Abuja and Lagos
- 📋 Certificate of Occupancy (C of O) process
- 💰 Investment strategies and rental yields
- ✅ Due diligence and title verification
- 🏦 Mortgage options and financing
- 📊 Property valuation methods
- 🏗️ PropTech platforms in Nigeria

**What real estate question can I help you with today?**"""
        }
    ]

# Handle sidebar question
if "selected_question" in st.session_state:
    question = st.session_state.selected_question
    del st.session_state.selected_question
    st.session_state.messages.append({"role": "user", "content": question})
    results = search_docs(question)
    if results:
        answer = generate_answer(question, results)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a Nigerian real estate question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Nigerian real estate database..."):
            results = search_docs(prompt)
            if results:
                answer = generate_answer(prompt, results)
                st.markdown(answer)

                with st.expander("📚 Sources Used"):
                    for meta in results["metadatas"][0]:
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>🏢 {meta['title']}</strong><br>
                            Category: {meta['category']}<br>
                            Source: {meta['source']}
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                answer = "I couldn't find relevant information. Please try rephrasing."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
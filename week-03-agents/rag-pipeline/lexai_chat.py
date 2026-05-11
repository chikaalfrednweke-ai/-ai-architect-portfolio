# ============================================
# Fred Baker's Automations
# lexai_chat.py — LexAI Chat Interface
# Nigerian Legal AI Assistant
# ============================================

import streamlit as st
import chromadb
import os

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="LexAI — Nigerian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .stApp { background-color: #0A0A0A; color: #E8E0D0; }
    .stChatMessage { background-color: #111111; border-radius: 8px; }
    h1, h2, h3 { color: #E2C97E; }
    .stTextInput input { background-color: #111111; color: #E8E0D0; }
    .source-card {
        background: #111111;
        border: 1px solid rgba(201,168,76,0.2);
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
    st.title("⚖️ LexAI")
    st.markdown("*Nigerian Legal AI Assistant — Powered by Fred Baker's Automations*")
with col2:
    st.markdown("###")
    st.markdown("📍 **Abuja, Nigeria**")
    st.markdown("🏢 **Fred Baker's Automations**")

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.title("⚖️ LexAI")
st.sidebar.markdown("**Nigerian Legal Knowledge Base**")
st.sidebar.markdown("---")
st.sidebar.markdown("**Coverage Areas:**")
areas = [
    "Company Law (CAC, CAMA)",
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
    "Financial Regulation (CBN)",
    "Real Estate Law",
    "Dispute Resolution",
]
for area in areas:
    st.sidebar.markdown(f"✅ {area}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Sample Questions:**")
sample_questions = [
    "How do I register a company?",
    "What are employee rights?",
    "How does NDPR affect me?",
    "What taxes must I pay?",
    "How to protect my trademark?",
    "What is a C of O?",
    "How to handle contract disputes?",
    "What is the Cybercrime Act?",
]
for q in sample_questions:
    if st.sidebar.button(q, key=q):
        st.session_state.selected_question = q

st.sidebar.markdown("---")
st.sidebar.info("🔑 Connect Claude API key for full AI answers")

# ---- DATABASE ----
DB_PATH = "./chroma_db"
COLLECTION_NAME = "lexai_nigeria_legal"

@st.cache_resource
def get_rag_engine():
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
        return collection
    except Exception as e:
        st.error(f"RAG Engine error: {e}")
        return None

def search_legal_docs(query, n_results=3):
    collection = get_rag_engine()
    if not collection:
        return None
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def generate_mock_answer(query, results):
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # Build answer from retrieved docs
    answer = f"Based on Nigerian law, here is what I found regarding **'{query}'**:\n\n"

    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
        relevance = "High" if dist < 0.7 else "Medium" if dist < 1.0 else "Low"
        answer += f"**{meta['title']}** ({meta['category']})\n"
        answer += f"*Source: {meta['source']}*\n\n"
        # Get first 300 chars of content
        content = doc.replace(meta['title'], '').strip()[:400]
        answer += f"{content}...\n\n"
        if i < len(docs) - 1:
            answer += "---\n\n"

    answer += "\n\n⚠️ *This is a preview response. Connect Claude API key for comprehensive AI-powered legal analysis.*"
    return answer

# ---- CHAT INTERFACE ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """Hello! I'm **LexAI**, your Nigerian legal AI assistant.

I can help you with questions about:
- Company registration and CAMA 2020
- Contract law and dispute resolution  
- Employment rights and obligations
- Property law and land titles
- Tax obligations and FIRS compliance
- NDPR data protection requirements
- Oil & gas regulations (PIA 2021)
- And much more Nigerian law topics!

**How can I help you today?** Ask me any legal question about Nigerian law."""
        }
    ]

# Handle sample question selection
if "selected_question" in st.session_state:
    question = st.session_state.selected_question
    del st.session_state.selected_question
    st.session_state.messages.append({"role": "user", "content": question})

    # Search and answer
    results = search_legal_docs(question)
    if results:
        answer = generate_mock_answer(question, results)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Legal Sources"):
                for source in message["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>{source['title']}</strong><br>
                        Category: {source['category']}<br>
                        Source: {source['source']}
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a Nigerian legal question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search RAG
    with st.chat_message("assistant"):
        with st.spinner("Searching Nigerian legal database..."):
            results = search_legal_docs(prompt)

            if results:
                answer = generate_mock_answer(prompt, results)
                st.markdown(answer)

                # Show sources
                with st.expander("📚 Legal Sources Used"):
                    for meta in results["metadatas"][0]:
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>⚖️ {meta['title']}</strong><br>
                            Category: {meta['category']}<br>
                            Source: {meta['source']}
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
                st.session_state.messages.append({"role": "assistant", "content": answer})
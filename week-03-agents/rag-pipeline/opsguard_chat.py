# ============================================
# Fred Baker's Automations
# opsguard_chat.py — OpsGuard Chat + Claude
# Nigerian Oil & Gas AI Assistant
# ============================================

import streamlit as st
import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="OpsGuard — Nigerian Oil & Gas AI",
    page_icon="⚙️",
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
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 13px;
    }
    .stButton button {
        background: rgba(201,168,76,0.1);
        border: 1px solid rgba(201,168,76,0.3);
        color: #C9A84C;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
col1, col2 = st.columns([3,1])
with col1:
    st.title("⚙️ OpsGuard")
    st.markdown("*Nigerian Oil & Gas AI Assistant — Powered by Claude + RAG*")
with col2:
    st.markdown("###")
    st.markdown("📍 **Nigeria**")
    st.markdown("🤖 **Claude AI Powered**")

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.title("⚙️ OpsGuard")
st.sidebar.markdown("**Nigerian Oil & Gas AI**")
st.sidebar.markdown("*Powered by Fred Baker's Automations*")
st.sidebar.markdown("---")

st.sidebar.markdown("**Knowledge Base:**")
areas = [
    "Petroleum Industry Act 2021",
    "HSE Management Systems",
    "Pipeline Integrity Management",
    "Environmental Compliance",
    "Incident Reporting & Management",
    "Maintenance Management",
    "Production Operations",
    "Host Community Relations",
    "Local Content (NCDMB)",
    "SCADA & Digital Operations",
]
for area in areas:
    st.sidebar.markdown(f"✅ {area}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Questions:**")
sample_questions = [
    "What are HSE requirements?",
    "How to report an oil spill?",
    "What is PIA 2021?",
    "Local content requirements?",
    "How to manage pipeline integrity?",
    "How does SCADA help operations?",
    "Host community obligations?",
    "How to handle major incident?",
]
for q in sample_questions:
    if st.sidebar.button(q, key=f"btn_{q}"):
        st.session_state.pending_question = q

st.sidebar.markdown("---")
st.sidebar.success("🤖 Claude AI Connected!")

# ---- DATABASE + CLAUDE ----
DB_PATH = "./chroma_db"
COLLECTION_NAME = "opsguard_nigeria_oilgas"

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

def ask_opsguard(question, results):
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
        system="""You are OpsGuard, an expert AI operations assistant
specializing in Nigerian oil and gas operations. You work for 
Fred Baker's Automations, a Nigerian AI company based in Abuja.

Your personality:
- Safety-focused and precise
- Reference specific Nigerian regulations (NUPRC, NOSDRA, PIA 2021)
- Always practical with actionable checklists
- Use industry terminology correctly
- Format responses with clear headers and tables
- Include risk ratings where relevant
- Cite specific acts and regulatory guidelines""",
        messages=[
            {
                "role": "user",
                "content": f"""Use this Nigerian oil & gas knowledge base to answer:

{context}

Question: {question}

Provide a comprehensive, safety-focused answer about Nigerian oil & gas operations.
Reference specific regulations, standards and practical steps."""
            }
        ]
    )
    return message.content[0].text

# ---- CHAT INTERFACE ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """Hello! I'm **OpsGuard** ⚙️ — your Nigerian oil & gas AI assistant, powered by Claude AI.

I have deep knowledge of Nigerian oil & gas operations including:
- 📋 **HSE Management** — Safety systems, permits, incident reporting
- 🛢️ **Pipeline Integrity** — Monitoring, vandalism prevention, repairs
- 🌿 **Environmental Compliance** — NOSDRA, gas flaring, spill response
- ⚠️ **Incident Management** — Classification, reporting, investigation
- 🔧 **Maintenance Management** — Preventive, predictive, corrective
- ⛽ **Production Operations** — Monitoring, optimization, reporting
- 👥 **Host Community** — HCDT, grievance management, CSR
- 🇳🇬 **Local Content** — NCDMB compliance, NCP preparation
- 💻 **SCADA & Digital** — Monitoring, automation, cybersecurity
- 📜 **PIA 2021** — Licensing, fiscal terms, regulatory compliance

I'm powered by **real Nigerian oil & gas regulations** and **Claude AI**.

**What operational question can I help you with today?**"""
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
        with st.spinner("⚙️ OpsGuard analyzing Nigerian oil & gas regulations..."):
            answer = ask_opsguard(question, results)
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
            with st.expander("📚 Regulatory Sources"):
                for meta in message["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>⚙️ {meta['title']}</strong><br>
                        <small>{meta['category']} | {meta['source']}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about Nigerian oil & gas operations..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚙️ OpsGuard analyzing regulations..."):
            results = search_docs(prompt)
            if results:
                answer = ask_opsguard(prompt, results)
                st.markdown(answer)

                with st.expander("📚 Regulatory Sources"):
                    for meta in results["metadatas"][0]:
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>⚙️ {meta['title']}</strong><br>
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
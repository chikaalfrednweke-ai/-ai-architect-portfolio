# ============================================
# Fred Baker's Automations
# app.py — Streamlit Business Intelligence App
# Nigeria Business Database Dashboard
# ============================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Fred Baker's Automations",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .main { background-color: #0A0A0A; }
    .stApp { background-color: #0A0A0A; color: #E8E0D0; }
    h1, h2, h3 { color: #E2C97E; font-family: 'Georgia', serif; }
    .metric-card {
        background: #111111;
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stSelectbox label { color: #C9A84C; }
    .stTextInput label { color: #C9A84C; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
DB_PATH = "projects/nigeria-business-db/nigeria_businesses.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM businesses", conn)
    conn.close()
    return df

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM businesses")
    total = cursor.fetchone()[0]
    conn.close()
    return total

# ---- SIDEBAR ----
st.sidebar.image("https://img.shields.io/badge/Fred%20Baker's-Automations-C9A84C?style=for-the-badge", width='stretch')
st.sidebar.title("🤖 Fred Baker's")
st.sidebar.markdown("**Nigeria Business Intelligence**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🔍 Search Database", "📈 Analytics", "⚖️ LexAI Prospects", "🏢 EstateIQ Prospects", "⚙️ OpsGuard Prospects"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Products**")
st.sidebar.markdown("⚖️ LexAI — Law Firms")
st.sidebar.markdown("🏢 EstateIQ — Real Estate")
st.sidebar.markdown("⚙️ OpsGuard — Oil & Gas")
st.sidebar.markdown("---")
st.sidebar.markdown("📍 Abuja, Nigeria")

# ---- LOAD DATA ----
try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Database error: {e}")
    data_loaded = False

# ---- PAGES ----

# PAGE 1 — DASHBOARD
if page == "📊 Dashboard":
    st.title("🤖 Fred Baker's Automations")
    st.markdown("### Nigeria Business Intelligence Dashboard")
    st.markdown("---")

    if data_loaded:
        # Stats
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("LexAI Prospects", len(df[df['prospect_for'] == 'LexAI']))
        with col3:
            st.metric("EstateIQ Prospects", len(df[df['prospect_for'] == 'EstateIQ']))
        with col4:
            st.metric("OpsGuard Prospects", len(df[df['prospect_for'] == 'OpsGuard']))
        with col5:
            st.metric("Cities", df['city'].nunique())

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Records by City")
            city_counts = df['city'].value_counts().reset_index()
            city_counts.columns = ['City', 'Count']
            fig = px.bar(
                city_counts,
                x='City', y='Count',
                color='Count',
                color_continuous_scale=[[0, '#1A1A1A'], [1, '#C9A84C']],
                template='plotly_dark'
            )
            fig.update_layout(
                paper_bgcolor='#111111',
                plot_bgcolor='#111111',
                font_color='#E8E0D0'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Product Distribution")
            product_counts = df['prospect_for'].value_counts()
            fig2 = px.pie(
                values=product_counts.values,
                names=product_counts.index,
                color_discrete_sequence=['#4A8FC9', '#4CAF7A', '#C9A84C'],
                template='plotly_dark'
            )
            fig2.update_layout(
                paper_bgcolor='#111111',
                plot_bgcolor='#111111',
                font_color='#E8E0D0'
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Recent records
        st.subheader("Latest Records")
        st.dataframe(
            df[['company_name', 'city', 'sector', 'prospect_for', 'phone', 'website']].head(20),
            use_container_width=True
        )

# PAGE 2 — SEARCH
elif page == "🔍 Search Database":
    st.title("🔍 Search Nigeria Business Database")
    st.markdown("---")

    if data_loaded:
        col1, col2, col3 = st.columns(3)

        with col1:
            search_term = st.text_input("Search company name", placeholder="e.g. Okonkwo")
        with col2:
            city_filter = st.selectbox("Filter by city", ["All"] + sorted(df['city'].unique().tolist()))
        with col3:
            product_filter = st.selectbox("Filter by product", ["All", "LexAI", "EstateIQ", "OpsGuard"])

        # Apply filters
        filtered = df.copy()
        if search_term:
            filtered = filtered[filtered['company_name'].str.contains(search_term, case=False, na=False)]
        if city_filter != "All":
            filtered = filtered[filtered['city'] == city_filter]
        if product_filter != "All":
            filtered = filtered[filtered['prospect_for'] == product_filter]

        st.markdown(f"**{len(filtered)} results found**")
        st.dataframe(
            filtered[['company_name', 'city', 'state', 'sector', 'prospect_for', 'phone', 'website', 'summary']],
            use_container_width=True
        )

        # Download
        csv = filtered.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name=f"nigeria_businesses_{city_filter}_{product_filter}.csv",
            mime="text/csv"
        )

# PAGE 3 — ANALYTICS
elif page == "📈 Analytics":
    st.title("📈 Business Intelligence Analytics")
    st.markdown("---")

    if data_loaded:
        # City x Product heatmap
        st.subheader("City × Product Matrix")
        pivot = df.groupby(['city', 'prospect_for']).size().unstack(fill_value=0)
        fig = px.imshow(
            pivot,
            color_continuous_scale=[[0, '#0A0A0A'], [1, '#C9A84C']],
            template='plotly_dark',
            aspect='auto'
        )
        fig.update_layout(paper_bgcolor='#111111', font_color='#E8E0D0')
        st.plotly_chart(fig, use_container_width=True)

        # Sector breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sectors")
            sector_counts = df['sector'].value_counts().head(10)
            fig3 = px.bar(
                x=sector_counts.values,
                y=sector_counts.index,
                orientation='h',
                color=sector_counts.values,
                color_continuous_scale=[[0, '#1A1A1A'], [1, '#C9A84C']],
                template='plotly_dark'
            )
            fig3.update_layout(paper_bgcolor='#111111', font_color='#E8E0D0')
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            st.subheader("Contact Status")
            contact_counts = df['contacted'].value_counts()
            contact_labels = ['Not Contacted', 'Contacted']
            fig4 = px.pie(
                values=contact_counts.values,
                names=contact_labels[:len(contact_counts)],
                color_discrete_sequence=['#C9A84C', '#4CAF7A'],
                template='plotly_dark'
            )
            fig4.update_layout(paper_bgcolor='#111111', font_color='#E8E0D0')
            st.plotly_chart(fig4, use_container_width=True)

# PAGE 4 — LEXAI
elif page == "⚖️ LexAI Prospects":
    st.title("⚖️ LexAI — Law Firm Prospects")
    st.markdown("*AI automation for Nigerian law firms*")
    st.markdown("---")

    if data_loaded:
        lexai_df = df[df['prospect_for'] == 'LexAI']
        st.metric("Total LexAI Prospects", len(lexai_df))

        city_filter = st.selectbox("Filter by city", ["All"] + sorted(lexai_df['city'].unique().tolist()))
        if city_filter != "All":
            lexai_df = lexai_df[lexai_df['city'] == city_filter]

        for _, row in lexai_df.head(20).iterrows():
            with st.expander(f"⚖️ {row['company_name']} — {row['city']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**City:** {row['city']}, {row['state']}")
                    st.write(f"**Sector:** {row['sector']}")
                    st.write(f"**Phone:** {row['phone']}")
                with col2:
                    st.write(f"**Website:** {row['website']}")
                    st.write(f"**Status:** {row['status']}")
                st.write(f"**Summary:** {row['summary']}")

# PAGE 5 — ESTATEIQ
elif page == "🏢 EstateIQ Prospects":
    st.title("🏢 EstateIQ — Real Estate Prospects")
    st.markdown("*AI intelligence for Nigerian real estate companies*")
    st.markdown("---")

    if data_loaded:
        estate_df = df[df['prospect_for'] == 'EstateIQ']
        st.metric("Total EstateIQ Prospects", len(estate_df))

        city_filter = st.selectbox("Filter by city", ["All"] + sorted(estate_df['city'].unique().tolist()))
        if city_filter != "All":
            estate_df = estate_df[estate_df['city'] == city_filter]

        for _, row in estate_df.head(20).iterrows():
            with st.expander(f"🏢 {row['company_name']} — {row['city']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**City:** {row['city']}, {row['state']}")
                    st.write(f"**Sector:** {row['sector']}")
                    st.write(f"**Phone:** {row['phone']}")
                with col2:
                    st.write(f"**Website:** {row['website']}")
                    st.write(f"**Status:** {row['status']}")
                st.write(f"**Summary:** {row['summary']}")

# PAGE 6 — OPSGUARD
elif page == "⚙️ OpsGuard Prospects":
    st.title("⚙️ OpsGuard — Oil & Gas Prospects")
    st.markdown("*AI operations management for Nigerian oil & gas companies*")
    st.markdown("---")

    if data_loaded:
        ops_df = df[df['prospect_for'] == 'OpsGuard']
        st.metric("Total OpsGuard Prospects", len(ops_df))

        city_filter = st.selectbox("Filter by city", ["All"] + sorted(ops_df['city'].unique().tolist()))
        if city_filter != "All":
            ops_df = ops_df[ops_df['city'] == city_filter]

        for _, row in ops_df.head(20).iterrows():
            with st.expander(f"⚙️ {row['company_name']} — {row['city']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**City:** {row['city']}, {row['state']}")
                    st.write(f"**Sector:** {row['sector']}")
                    st.write(f"**Phone:** {row['phone']}")
                with col2:
                    st.write(f"**Website:** {row['website']}")
                    st.write(f"**Status:** {row['status']}")
                st.write(f"**Summary:** {row['summary']}")
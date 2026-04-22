import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0d1117; }
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.stButton>button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🏏 Cricbuzz LiveStats")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📺 Live Matches", "🏆 Player Stats", "📊 SQL Analytics", "⚙️ CRUD Operations"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("Built with Streamlit + MySQL + Cricbuzz API")

# Page Routing
if page == "🏠 Home":
    from pages.home import show
    show()

elif page == "📺 Live Matches":
    from pages.live_matches import show
    show()

elif page == "🏆 Player Stats":
    from pages.player_stats import show
    show()

elif page == "📊 SQL Analytics":
    from pages.sql_analytics import show
    show()

elif page == "⚙️ CRUD Operations":
    from pages.crud_operations import show
    show()

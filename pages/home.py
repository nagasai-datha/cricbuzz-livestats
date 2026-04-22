import streamlit as st

def show():
    st.markdown("""
    <style>
    .hero { background: linear-gradient(135deg, #1a472a, #2d6a4f); padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
    .hero h1 { color: white; font-size: 2.8em; margin: 0; }
    .hero p  { color: #a8d5b5; font-size: 1.2em; }
    .card    { background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 20px; margin: 10px 0; }
    .tech-badge { display: inline-block; background: #2d6a4f; color: white; padding: 4px 12px; border-radius: 20px; margin: 4px; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>🏏 Cricbuzz LiveStats</h1>
        <p>Real-Time Cricket Insights & SQL-Based Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📺 Live Matches", "Via API", "Real-time")
    with col2:
        st.metric("👤 Players", "20+", "In Database")
    with col3:
        st.metric("📊 SQL Queries", "25", "Practice Sets")
    with col4:
        st.metric("🗄️ DB Tables", "9", "MySQL")

    st.markdown("---")
    st.subheader("📌 Navigate the App")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h4>📺 Live Matches</h4>
            <p>View ongoing cricket matches with live scorecards, batsman & bowler details fetched directly from Cricbuzz API.</p>
        </div>
        <div class="card">
            <h4>🏆 Top Player Stats</h4>
            <p>ICC rankings for batting & bowling across Test, ODI, and T20I formats with visual charts.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h4>📊 SQL Analytics</h4>
            <p>25 SQL queries from beginner to advanced level. Run them live and see results in a table format.</p>
        </div>
        <div class="card">
            <h4>⚙️ CRUD Operations</h4>
            <p>Add, update, and delete player & match records from the database using a simple form interface.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛠️ Tech Stack")
    st.markdown("""
    <span class="tech-badge">Python 3.10+</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">MySQL</span>
    <span class="tech-badge">Cricbuzz REST API</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">Plotly</span>
    <span class="tech-badge">Requests</span>
    <span class="tech-badge">python-dotenv</span>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📁 Project Folder Structure")
    st.code("""
project 7/
│
├── main.py                  ← App entry point
├── requirements.txt         ← Python dependencies
├── .env                     ← API key & DB credentials
│
├── utils/
│   ├── db_connection.py     ← MySQL connection helper
│   └── api_helper.py        ← Cricbuzz API functions
│
└── pages/
    ├── home.py              ← This page
    ├── live_matches.py      ← Live match scores
    ├── player_stats.py      ← Top stats & rankings
    ├── sql_analytics.py     ← 25 SQL queries
    └── crud_operations.py   ← Add/Edit/Delete records
    """, language="text")

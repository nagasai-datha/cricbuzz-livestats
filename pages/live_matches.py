import streamlit as st
import pandas as pd
from utils.api_helper import get_live_matches, get_recent_matches, get_upcoming_matches

def show():
    st.title("📺 Live Cricket Matches")
    st.markdown("*Powered by Cricbuzz API — updates every refresh*")

    tab1, tab2, tab3 = st.tabs(["🔴 Live Now", "✅ Recent", "📅 Upcoming"])

    # ── LIVE ──────────────────────────────────────────────
    with tab1:
        with st.spinner("Fetching live matches..."):
            matches = get_live_matches()

        if not matches:
            st.info("No live matches right now. Check back during match hours!")
        else:
            for m in matches:
                with st.container():
                    st.markdown(f"""
                    <div style="background:#1e1e2e;border-left:4px solid #e63946;
                                border-radius:10px;padding:15px;margin:10px 0;">
                        <span style="background:#e63946;color:white;padding:2px 8px;
                                     border-radius:4px;font-size:0.75em;">🔴 LIVE</span>
                        <h4 style="color:white;margin:8px 0 4px 0;">{m['team1']} vs {m['team2']}</h4>
                        <p style="color:#aaa;margin:0;">{m['series']} | {m['match_format']} | {m['venue']}, {m['city']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(m['team1'],
                                  f"{m['team1_score']}/{m['team1_wkts']}",
                                  f"Overs: {m['team1_overs']}")
                    with col2:
                        st.metric(m['team2'],
                                  f"{m['team2_score']}/{m['team2_wkts']}",
                                  f"Overs: {m['team2_overs']}")

                    st.caption(f"📊 Status: {m['status']}")
                    st.divider()

    # ── RECENT ────────────────────────────────────────────
    with tab2:
        with st.spinner("Fetching recent matches..."):
            recent = get_recent_matches()

        if not recent:
            st.info("No recent matches found.")
        else:
            df = pd.DataFrame(recent)
            cols_to_show = ["description", "series", "team1", "team2", "match_format", "venue", "status"]
            df = df[[c for c in cols_to_show if c in df.columns]]
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True)

    # ── UPCOMING ──────────────────────────────────────────
    with tab3:
        with st.spinner("Fetching upcoming matches..."):
            upcoming = get_upcoming_matches()

        if not upcoming:
            st.info("No upcoming matches scheduled.")
        else:
            df = pd.DataFrame(upcoming)
            cols_to_show = ["description", "series", "team1", "team2", "match_format", "venue", "start_date"]
            df = df[[c for c in cols_to_show if c in df.columns]]
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True)

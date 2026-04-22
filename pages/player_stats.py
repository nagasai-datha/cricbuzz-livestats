import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_helper import get_batting_stats, get_bowling_stats
from utils.db_connection import run_query

def show():
    st.title("🏆 Top Player Statistics")

    tab1, tab2, tab3 = st.tabs(["🏏 ICC Batting Rankings", "🎳 ICC Bowling Rankings", "📊 DB Career Stats"])

    # ── ICC BATTING RANKINGS ──────────────────────────────
    with tab1:
        format_ = st.selectbox("Select Format", ["odi", "test", "t20"], key="bat_format")
        with st.spinner("Fetching batting rankings..."):
            players = get_batting_stats(format_=format_)

        if not players:
            st.warning("Could not fetch data. Check your API key in .env file.")
        else:
            df = pd.DataFrame(players)
            df["rank"] = df["rank"].astype(str)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader(f"Top Batsmen — {format_.upper()}")
                st.dataframe(df, use_container_width=True, hide_index=True)
            with col2:
                fig = px.bar(df.head(10), x="name", y="rating",
                             color="rating", color_continuous_scale="Greens",
                             title=f"Top 10 Batsmen Rating ({format_.upper()})",
                             labels={"name": "Player", "rating": "Rating"})
                fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── ICC BOWLING RANKINGS ──────────────────────────────
    with tab2:
        format_b = st.selectbox("Select Format", ["odi", "test", "t20"], key="bowl_format")
        with st.spinner("Fetching bowling rankings..."):
            bowlers = get_bowling_stats(format_=format_b)

        if not bowlers:
            st.warning("Could not fetch data. Check your API key in .env file.")
        else:
            df = pd.DataFrame(bowlers)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader(f"Top Bowlers — {format_b.upper()}")
                st.dataframe(df, use_container_width=True, hide_index=True)
            with col2:
                fig = px.bar(df.head(10), x="name", y="rating",
                             color="rating", color_continuous_scale="Blues",
                             title=f"Top 10 Bowlers Rating ({format_b.upper()})",
                             labels={"name": "Player", "rating": "Rating"})
                fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── DATABASE CAREER STATS ─────────────────────────────
    with tab3:
        st.subheader("Career Stats from Database")

        format_db = st.selectbox("Select Format", ["ODI", "Test", "T20I"], key="db_format")
        rows = run_query(f"""
            SELECT p.full_name AS Player, p.country AS Country,
                   p.playing_role AS Role,
                   cs.matches_played AS Matches,
                   cs.total_runs AS Runs,
                   cs.highest_score AS `High Score`,
                   cs.batting_average AS `Bat Avg`,
                   cs.total_centuries AS `100s`,
                   cs.total_fifties AS `50s`,
                   cs.total_wickets AS Wickets,
                   cs.bowling_average AS `Bowl Avg`
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            WHERE cs.match_type = '{format_db}'
            ORDER BY cs.total_runs DESC
        """)

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Top run scorers chart
            fig = px.bar(df.head(10), x="Player", y="Runs",
                         color="Country", title=f"Top Run Scorers — {format_db}",
                         text="Runs")
            fig.update_traces(textposition="outside")
            fig.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for this format in the database.")

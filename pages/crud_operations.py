import streamlit as st
import pandas as pd
from utils.db_connection import run_query, run_write

def show():
    st.title("⚙️ CRUD Operations")
    st.markdown("Add, update, and delete records in your database.")

    tab1, tab2 = st.tabs(["👤 Players", "🏟️ Matches"])

    # ── PLAYERS CRUD ──────────────────────────────────────
    with tab1:
        st.subheader("📋 All Players")
        players = run_query("SELECT player_id, full_name, country, playing_role, batting_style FROM players ORDER BY player_id")
        if players:
            st.dataframe(pd.DataFrame(players), use_container_width=True, hide_index=True)

        st.divider()
        action = st.radio("Action", ["➕ Add Player", "✏️ Update Player", "🗑️ Delete Player"], horizontal=True)

        # ── ADD ──
        if action == "➕ Add Player":
            st.subheader("Add New Player")
            teams = run_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
            team_map = {t["team_name"]: t["team_id"] for t in teams}

            with st.form("add_player"):
                col1, col2 = st.columns(2)
                with col1:
                    name       = st.text_input("Full Name*")
                    country    = st.text_input("Country*")
                    dob        = st.date_input("Date of Birth")
                    role       = st.selectbox("Playing Role", ["Batsman","Bowler","All-rounder","Wicket-keeper"])
                with col2:
                    bat_style  = st.selectbox("Batting Style", ["Right-hand bat","Left-hand bat"])
                    bowl_style = st.text_input("Bowling Style", placeholder="e.g. Right-arm fast")
                    team_name  = st.selectbox("Team", list(team_map.keys()))

                submitted = st.form_submit_button("Add Player", type="primary")
                if submitted:
                    if not name or not country:
                        st.error("Name and Country are required.")
                    else:
                        run_write("""
                            INSERT INTO players (full_name, country, date_of_birth, playing_role,
                                                 batting_style, bowling_style, team_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (name, country, dob, role, bat_style,
                              bowl_style or None, team_map[team_name]))
                        st.success(f"✅ Player '{name}' added successfully!")
                        st.rerun()

        # ── UPDATE ──
        elif action == "✏️ Update Player":
            st.subheader("Update Player")
            player_map = {f"{p['player_id']} — {p['full_name']}": p["player_id"] for p in players}
            selected   = st.selectbox("Select Player to Update", list(player_map.keys()))
            pid        = player_map[selected]
            p_data     = run_query("SELECT * FROM players WHERE player_id = %s", (pid,))[0]

            with st.form("update_player"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name    = st.text_input("Full Name", value=p_data["full_name"])
                    new_country = st.text_input("Country",   value=p_data["country"])
                    new_role    = st.selectbox("Playing Role",
                                               ["Batsman","Bowler","All-rounder","Wicket-keeper"],
                                               index=["Batsman","Bowler","All-rounder","Wicket-keeper"].index(p_data["playing_role"]))
                with col2:
                    new_bat  = st.selectbox("Batting Style",
                                            ["Right-hand bat","Left-hand bat"],
                                            index=["Right-hand bat","Left-hand bat"].index(p_data["batting_style"]))
                    new_bowl = st.text_input("Bowling Style", value=p_data["bowling_style"] or "")

                submitted = st.form_submit_button("Update Player", type="primary")
                if submitted:
                    run_write("""
                        UPDATE players
                        SET full_name=%s, country=%s, playing_role=%s, batting_style=%s, bowling_style=%s
                        WHERE player_id=%s
                    """, (new_name, new_country, new_role, new_bat, new_bowl or None, pid))
                    st.success(f"✅ Player updated successfully!")
                    st.rerun()

        # ── DELETE ──
        else:
            st.subheader("Delete Player")
            player_map = {f"{p['player_id']} — {p['full_name']}": p["player_id"] for p in players}
            selected   = st.selectbox("Select Player to Delete", list(player_map.keys()))
            pid        = player_map[selected]

            st.warning(f"⚠️ This will permanently delete the selected player record.")
            if st.button("🗑️ Confirm Delete", type="primary"):
                try:
                    run_write("DELETE FROM players WHERE player_id = %s", (pid,))
                    st.success("✅ Player deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Cannot delete: {e}")

    # ── MATCHES CRUD ──────────────────────────────────────
    with tab2:
        st.subheader("📋 All Matches")
        matches = run_query("""
            SELECT m.match_id, m.match_description,
                   t1.team_name AS team1, t2.team_name AS team2,
                   m.match_type, m.status, m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            ORDER BY m.match_date DESC
        """)
        if matches:
            st.dataframe(pd.DataFrame(matches), use_container_width=True, hide_index=True)

        st.divider()
        m_action = st.radio("Action", ["➕ Add Match", "🗑️ Delete Match"], horizontal=True, key="m_action")

        teams   = run_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
        venues  = run_query("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
        series  = run_query("SELECT series_id, series_name FROM series ORDER BY series_name")
        team_map   = {t["team_name"]: t["team_id"] for t in teams}
        venue_map  = {v["venue_name"]: v["venue_id"] for v in venues}
        series_map = {s["series_name"]: s["series_id"] for s in series}

        if m_action == "➕ Add Match":
            st.subheader("Add New Match")
            with st.form("add_match"):
                col1, col2 = st.columns(2)
                with col1:
                    desc        = st.text_input("Match Description*")
                    team1_name  = st.selectbox("Team 1", list(team_map.keys()), key="t1")
                    team2_name  = st.selectbox("Team 2", list(team_map.keys()), key="t2")
                    series_name = st.selectbox("Series", list(series_map.keys()))
                with col2:
                    venue_name  = st.selectbox("Venue", list(venue_map.keys()))
                    match_type  = st.selectbox("Match Type", ["ODI","Test","T20I","T20","Other"])
                    match_date  = st.date_input("Match Date")
                    status      = st.selectbox("Status", ["upcoming","live","completed"])

                submitted = st.form_submit_button("Add Match", type="primary")
                if submitted:
                    if not desc:
                        st.error("Description is required.")
                    elif team1_name == team2_name:
                        st.error("Team 1 and Team 2 must be different.")
                    else:
                        run_write("""
                            INSERT INTO matches (series_id, match_description, team1_id, team2_id,
                                                 venue_id, match_date, match_type, status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (series_map[series_name], desc, team_map[team1_name],
                              team_map[team2_name], venue_map[venue_name],
                              match_date, match_type, status))
                        st.success("✅ Match added successfully!")
                        st.rerun()

        else:
            st.subheader("Delete Match")
            if matches:
                match_map = {f"{m['match_id']} — {m['match_description']}": m["match_id"] for m in matches}
                sel_match  = st.selectbox("Select Match to Delete", list(match_map.keys()))
                mid        = match_map[sel_match]
                st.warning("⚠️ This will permanently delete this match record.")
                if st.button("🗑️ Confirm Delete Match", type="primary"):
                    try:
                        run_write("DELETE FROM matches WHERE match_id = %s", (mid,))
                        st.success("✅ Match deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Cannot delete: {e}")

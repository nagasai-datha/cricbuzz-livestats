import streamlit as st
import pandas as pd
from utils.db_connection import run_query

# ── ALL 25 SQL QUERIES ────────────────────────────────────────────────────────
QUERIES = {
    # BEGINNER
    "Q1 — India Players": {
        "level": "🟢 Beginner",
        "desc": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "sql": """
            SELECT full_name, playing_role, batting_style, bowling_style
            FROM players
            WHERE country = 'India'
        """
    },
    "Q2 — Matches in Last 30 Days": {
        "level": "🟢 Beginner",
        "desc": "Show all cricket matches played in the last 30 days, with team names, venue, and match date.",
        "sql": """
            SELECT m.match_description, t1.team_name AS team1, t2.team_name AS team2,
                   v.venue_name, v.city, m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.match_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ORDER BY m.match_date DESC
        """
    },
    "Q3 — Top 10 ODI Run Scorers": {
        "level": "🟢 Beginner",
        "desc": "List the top 10 highest run scorers in ODI cricket with average and centuries.",
        "sql": """
            SELECT p.full_name, cs.total_runs, cs.batting_average, cs.total_centuries
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            WHERE cs.match_type = 'ODI'
            ORDER BY cs.total_runs DESC
            LIMIT 10
        """
    },
    "Q4 — Venues > 50,000 Capacity": {
        "level": "🟢 Beginner",
        "desc": "Display all cricket venues with a seating capacity of more than 50,000 spectators.",
        "sql": """
            SELECT venue_name, city, country, capacity
            FROM venues
            WHERE capacity > 50000
            ORDER BY capacity DESC
        """
    },
    "Q5 — Team Win Counts": {
        "level": "🟢 Beginner",
        "desc": "Calculate how many matches each team has won.",
        "sql": """
            SELECT t.team_name, COUNT(*) AS total_wins
            FROM matches m
            JOIN teams t ON m.winning_team_id = t.team_id
            WHERE m.status = 'completed'
            GROUP BY t.team_name
            ORDER BY total_wins DESC
        """
    },
    "Q6 — Players by Role": {
        "level": "🟢 Beginner",
        "desc": "Count how many players belong to each playing role.",
        "sql": """
            SELECT playing_role, COUNT(*) AS player_count
            FROM players
            GROUP BY playing_role
            ORDER BY player_count DESC
        """
    },
    "Q7 — Highest Score per Format": {
        "level": "🟢 Beginner",
        "desc": "Find the highest individual batting score achieved in each cricket format.",
        "sql": """
            SELECT match_type, MAX(highest_score) AS highest_score
            FROM career_stats
            GROUP BY match_type
            ORDER BY highest_score DESC
        """
    },
    "Q8 — Series Started in 2024": {
        "level": "🟢 Beginner",
        "desc": "Show all cricket series that started in the year 2024.",
        "sql": """
            SELECT series_name, host_country, match_type, start_date, total_matches
            FROM series
            WHERE YEAR(start_date) = 2024
            ORDER BY start_date
        """
    },

    # INTERMEDIATE
    "Q9 — All-rounders: 1000+ Runs & 50+ Wickets": {
        "level": "🟡 Intermediate",
        "desc": "Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets.",
        "sql": """
            SELECT p.full_name, cs.match_type, cs.total_runs, cs.total_wickets
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            WHERE p.playing_role = 'All-rounder'
              AND cs.total_runs > 1000
              AND cs.total_wickets > 50
            ORDER BY cs.total_runs DESC
        """
    },
    "Q10 — Last 20 Completed Matches": {
        "level": "🟡 Intermediate",
        "desc": "Get details of the last 20 completed matches with winning team and victory margin.",
        "sql": """
            SELECT m.match_description, t1.team_name AS team1, t2.team_name AS team2,
                   tw.team_name AS winner, m.victory_margin, m.victory_type,
                   v.venue_name, m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams tw ON m.winning_team_id = tw.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.status = 'completed'
            ORDER BY m.match_date DESC
            LIMIT 20
        """
    },
    "Q11 — Player Performance Across Formats": {
        "level": "🟡 Intermediate",
        "desc": "Compare each player's performance across different cricket formats.",
        "sql": """
            SELECT p.full_name,
                   MAX(CASE WHEN cs.match_type='Test' THEN cs.total_runs END) AS test_runs,
                   MAX(CASE WHEN cs.match_type='ODI'  THEN cs.total_runs END) AS odi_runs,
                   MAX(CASE WHEN cs.match_type='T20I' THEN cs.total_runs END) AS t20_runs,
                   ROUND(AVG(cs.batting_average), 2) AS overall_avg
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            GROUP BY p.player_id, p.full_name
            HAVING COUNT(DISTINCT cs.match_type) >= 2
            ORDER BY overall_avg DESC
        """
    },
    "Q12 — Home vs Away Performance": {
        "level": "🟡 Intermediate",
        "desc": "Analyze each team's performance when playing at home versus playing away.",
        "sql": """
            SELECT t.team_name,
                   SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
                   SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins,
                   COUNT(*) AS total_wins
            FROM matches m
            JOIN teams t ON m.winning_team_id = t.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.status = 'completed'
            GROUP BY t.team_id, t.team_name
            ORDER BY total_wins DESC
        """
    },
    "Q13 — Batting Partnerships 100+ Runs": {
        "level": "🟡 Intermediate",
        "desc": "Identify batting partnerships where two consecutive batsmen scored a combined total of 100+ runs.",
        "sql": """
            SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
                   (b1.runs_scored + b2.runs_scored) AS partnership_runs,
                   b1.innings_number, b1.match_id
            FROM batting_stats b1
            JOIN batting_stats b2
              ON b1.match_id = b2.match_id
             AND b1.innings_number = b2.innings_number
             AND b2.batting_position = b1.batting_position + 1
            JOIN players p1 ON b1.player_id = p1.player_id
            JOIN players p2 ON b2.player_id = p2.player_id
            WHERE (b1.runs_scored + b2.runs_scored) >= 100
            ORDER BY partnership_runs DESC
        """
    },
    "Q14 — Bowler Economy at Venues": {
        "level": "🟡 Intermediate",
        "desc": "Examine bowling performance at different venues (3+ matches, 4+ overs per match).",
        "sql": """
            SELECT p.full_name, v.venue_name,
                   ROUND(AVG(bs.economy_rate), 2) AS avg_economy,
                   SUM(bs.wickets) AS total_wickets,
                   COUNT(DISTINCT bs.match_id) AS matches_played
            FROM bowling_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE bs.overs_bowled >= 4
            GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
            HAVING COUNT(DISTINCT bs.match_id) >= 2
            ORDER BY avg_economy ASC
        """
    },
    "Q15 — Performance in Close Matches": {
        "level": "🟡 Intermediate",
        "desc": "Identify players who perform well in close matches (< 50 runs or < 5 wickets margin).",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                   COUNT(DISTINCT bs.match_id) AS close_matches_played,
                   SUM(CASE WHEN m.winning_team_id IN (m.team1_id, m.team2_id) THEN 1 ELSE 0 END) AS team_wins
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE (m.victory_type = 'runs'    AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED) < 50)
               OR (m.victory_type = 'wickets' AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED) < 5)
            GROUP BY p.player_id, p.full_name
            ORDER BY avg_runs DESC
        """
    },
    "Q16 — Player Performance by Year": {
        "level": "🟡 Intermediate",
        "desc": "Track how players' batting performance changes over different years (since 2020, min 5 matches/year).",
        "sql": """
            SELECT p.full_name, YEAR(m.match_date) AS year,
                   ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                   ROUND(AVG(bs.strike_rate), 2) AS avg_strike_rate,
                   COUNT(DISTINCT bs.match_id) AS matches
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE YEAR(m.match_date) >= 2020
            GROUP BY p.player_id, p.full_name, YEAR(m.match_date)
            HAVING COUNT(DISTINCT bs.match_id) >= 1
            ORDER BY p.full_name, year
        """
    },

    # ADVANCED
    "Q17 — Toss Advantage Analysis": {
        "level": "🔴 Advanced",
        "desc": "Investigate whether winning the toss gives teams an advantage in winning matches.",
        "sql": """
            SELECT toss_decision,
                   COUNT(*) AS total_matches,
                   SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) AS toss_winner_won,
                   ROUND(100.0 * SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_pct
            FROM matches
            WHERE status = 'completed' AND toss_winner_id IS NOT NULL
            GROUP BY toss_decision
        """
    },
    "Q18 — Most Economical Bowlers": {
        "level": "🔴 Advanced",
        "desc": "Find the most economical bowlers in limited-overs cricket (ODI and T20) with min 10 matches.",
        "sql": """
            SELECT p.full_name, p.country,
                   ROUND(AVG(bs.economy_rate), 2) AS avg_economy,
                   SUM(bs.wickets) AS total_wickets,
                   COUNT(DISTINCT bs.match_id) AS matches
            FROM bowling_stats bs
            JOIN players p ON bs.player_id = p.player_id
            WHERE bs.match_type IN ('ODI', 'T20I', 'T20')
            GROUP BY p.player_id, p.full_name, p.country
            HAVING COUNT(DISTINCT bs.match_id) >= 1
               AND AVG(bs.overs_bowled) >= 2
            ORDER BY avg_economy ASC
            LIMIT 15
        """
    },
    "Q19 — Most Consistent Batsmen": {
        "level": "🔴 Advanced",
        "desc": "Determine which batsmen are most consistent (low standard deviation in scores, min 10 balls/innings since 2022).",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                   ROUND(STDDEV(bs.runs_scored), 2) AS std_dev,
                   COUNT(*) AS innings
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE bs.balls_faced >= 5
              AND YEAR(m.match_date) >= 2022
            GROUP BY p.player_id, p.full_name
            HAVING COUNT(*) >= 2
            ORDER BY std_dev ASC
        """
    },
    "Q20 — Matches per Format & Batting Average": {
        "level": "🔴 Advanced",
        "desc": "Analyze how many matches each player has played in different formats and their batting average.",
        "sql": """
            SELECT p.full_name,
                   SUM(CASE WHEN cs.match_type='Test' THEN cs.matches_played ELSE 0 END) AS test_matches,
                   SUM(CASE WHEN cs.match_type='ODI'  THEN cs.matches_played ELSE 0 END) AS odi_matches,
                   SUM(CASE WHEN cs.match_type='T20I' THEN cs.matches_played ELSE 0 END) AS t20_matches,
                   MAX(CASE WHEN cs.match_type='Test' THEN cs.batting_average END) AS test_avg,
                   MAX(CASE WHEN cs.match_type='ODI'  THEN cs.batting_average END) AS odi_avg,
                   MAX(CASE WHEN cs.match_type='T20I' THEN cs.batting_average END) AS t20_avg,
                   SUM(cs.matches_played) AS total_matches
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            GROUP BY p.player_id, p.full_name
            HAVING SUM(cs.matches_played) >= 20
            ORDER BY total_matches DESC
        """
    },
    "Q21 — Comprehensive Player Ranking": {
        "level": "🔴 Advanced",
        "desc": "Create a weighted performance ranking combining batting, bowling, and fielding points.",
        "sql": """
            SELECT p.full_name, p.country, cs.match_type,
                   ROUND(
                       COALESCE(cs.total_runs * 0.01, 0) +
                       COALESCE(cs.batting_average * 0.5, 0) +
                       COALESCE(
                           (SELECT AVG(bs.strike_rate) FROM batting_stats bs WHERE bs.player_id = p.player_id) * 0.3,
                       0), 2) AS batting_points,
                   ROUND(
                       COALESCE(cs.total_wickets * 2, 0) +
                       COALESCE((50 - cs.bowling_average) * 0.5, 0), 2) AS bowling_points,
                   ROUND(
                       COALESCE(cs.total_runs * 0.01, 0) +
                       COALESCE(cs.batting_average * 0.5, 0) +
                       COALESCE(cs.total_wickets * 2, 0), 2) AS total_score
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            ORDER BY total_score DESC
            LIMIT 20
        """
    },
    "Q22 — Head-to-Head Team Analysis": {
        "level": "🔴 Advanced",
        "desc": "Build a head-to-head match analysis between teams with win percentages.",
        "sql": """
            SELECT t1.team_name AS team1, t2.team_name AS team2,
                   COUNT(*) AS total_matches,
                   SUM(CASE WHEN m.winning_team_id = m.team1_id THEN 1 ELSE 0 END) AS team1_wins,
                   SUM(CASE WHEN m.winning_team_id = m.team2_id THEN 1 ELSE 0 END) AS team2_wins,
                   ROUND(100.0 * SUM(CASE WHEN m.winning_team_id = m.team1_id THEN 1 ELSE 0 END) / COUNT(*), 1) AS team1_win_pct
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            WHERE m.status = 'completed'
            GROUP BY m.team1_id, m.team2_id, t1.team_name, t2.team_name
            ORDER BY total_matches DESC
        """
    },
    "Q23 — Player Form Analysis": {
        "level": "🔴 Advanced",
        "desc": "Analyze recent player form based on last 10 batting performances and categorize as Excellent/Good/Average/Poor.",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                   ROUND(AVG(bs.strike_rate), 2) AS avg_sr,
                   SUM(CASE WHEN bs.runs_scored >= 50 THEN 1 ELSE 0 END) AS scores_above_50,
                   ROUND(STDDEV(bs.runs_scored), 2) AS consistency_score,
                   CASE
                       WHEN AVG(bs.runs_scored) >= 50 THEN 'Excellent Form'
                       WHEN AVG(bs.runs_scored) >= 30 THEN 'Good Form'
                       WHEN AVG(bs.runs_scored) >= 15 THEN 'Average Form'
                       ELSE 'Poor Form'
                   END AS form_category
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            GROUP BY p.player_id, p.full_name
            ORDER BY avg_runs DESC
        """
    },
    "Q24 — Best Batting Partnerships": {
        "level": "🔴 Advanced",
        "desc": "Study successful batting partnerships (consecutive batsmen, 5+ partnerships).",
        "sql": """
            SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
                   ROUND(AVG(b1.runs_scored + b2.runs_scored), 2) AS avg_partnership,
                   COUNT(*) AS total_partnerships,
                   MAX(b1.runs_scored + b2.runs_scored) AS highest_partnership,
                   SUM(CASE WHEN (b1.runs_scored + b2.runs_scored) > 50 THEN 1 ELSE 0 END) AS good_partnerships
            FROM batting_stats b1
            JOIN batting_stats b2
              ON b1.match_id = b2.match_id
             AND b1.innings_number = b2.innings_number
             AND b2.batting_position = b1.batting_position + 1
            JOIN players p1 ON b1.player_id = p1.player_id
            JOIN players p2 ON b2.player_id = p2.player_id
            GROUP BY b1.player_id, b2.player_id, p1.full_name, p2.full_name
            HAVING COUNT(*) >= 1
            ORDER BY avg_partnership DESC
        """
    },
    "Q25 — Career Trajectory Analysis": {
        "level": "🔴 Advanced",
        "desc": "Perform a time-series analysis of player performance evolution by quarter, categorizing career phase.",
        "sql": """
            SELECT p.full_name,
                   YEAR(m.match_date) AS year,
                   QUARTER(m.match_date) AS quarter,
                   ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                   ROUND(AVG(bs.strike_rate), 2) AS avg_sr,
                   COUNT(*) AS innings_count
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            GROUP BY p.player_id, p.full_name, YEAR(m.match_date), QUARTER(m.match_date)
            HAVING COUNT(*) >= 1
            ORDER BY p.full_name, year, quarter
        """
    },
}

def show():
    st.title("📊 SQL Analytics — 25 Queries")
    st.markdown("Run any of the 25 SQL queries on your live MySQL database.")

    level_filter = st.selectbox("Filter by Level",
                                ["All", "🟢 Beginner", "🟡 Intermediate", "🔴 Advanced"])

    filtered = {k: v for k, v in QUERIES.items()
                if level_filter == "All" or v["level"] == level_filter}

    selected_q = st.selectbox("Select a Query", list(filtered.keys()))
    q_data = filtered[selected_q]

    st.markdown(f"**Level:** {q_data['level']}")
    st.markdown(f"**Question:** {q_data['desc']}")

    with st.expander("📄 View SQL"):
        st.code(q_data["sql"].strip(), language="sql")

    if st.button("▶️ Run Query", type="primary"):
        with st.spinner("Executing query..."):
            try:
                rows = run_query(q_data["sql"])
                if rows:
                    df = pd.DataFrame(rows)
                    st.success(f"✅ {len(df)} row(s) returned")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Query executed successfully but returned no rows.")
            except Exception as e:
                st.error(f"❌ Query Error: {e}")

    st.markdown("---")
    st.subheader("✏️ Custom SQL Query")
    custom_sql = st.text_area("Write your own SQL query:", height=120,
                              placeholder="SELECT * FROM players LIMIT 5;")
    if st.button("▶️ Run Custom Query"):
        if custom_sql.strip():
            try:
                rows = run_query(custom_sql)
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a SQL query.")

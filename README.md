# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Domain](https://img.shields.io/badge/Domain-Sports%20Analytics-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

**Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard built as part of an internship project at **Labmentrix**. It integrates:

- 🔴 **Live match data** from the Cricbuzz REST API (via RapidAPI)
- 🗄️ **MySQL database** with 9 normalized tables
- 📊 **Interactive visualizations** using Plotly charts
- ⚙️ **Full CRUD operations** for data management
- 🧮 **25 SQL practice queries** from beginner to advanced level

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| Streamlit | Web application framework |
| MySQL 8.0 | Relational database |
| Cricbuzz REST API | Live cricket data via RapidAPI |
| Pandas | Data manipulation & analysis |
| Plotly | Interactive charts & visualizations |
| mysql-connector-python | Database connectivity |
| python-dotenv | Secure environment variable management |
| Requests | HTTP API calls |

---

## 💼 Business Use Cases

1. **📺 Sports Media & Broadcasting** — Real-time match updates for commentary teams
2. **🎮 Fantasy Cricket Platforms** — Player form analysis and performance tracking
3. **📈 Cricket Analytics Firms** — Advanced statistical modeling and evaluation
4. **🎓 Educational Institutions** — SQL practice with real-world cricket datasets
5. **🎲 Sports Betting & Prediction** — Historical performance analysis for odds

---

## 📁 Project Structure

```
project 7/
│
├── main.py                    ← App entry point (run this)
├── requirements.txt           ← Python dependencies
├── .env                       ← API key & DB credentials (not committed)
├── cricbuzz_schema.sql        ← Full database schema + sample data
├── README.md                  ← Project documentation
├── .gitignore                 ← Git ignore rules
│
├── .streamlit/
│   └── config.toml            ← Streamlit UI configuration
│
├── utils/
│   ├── __init__.py
│   ├── db_connection.py       ← MySQL connection & query helper
│   └── api_helper.py          ← Cricbuzz API functions
│
└── pages/
    ├── home.py                ← Home & project overview page
    ├── live_matches.py        ← Live/Recent/Upcoming matches
    ├── player_stats.py        ← ICC rankings & career stats
    ├── sql_analytics.py       ← 25 SQL queries interface
    └── crud_operations.py     ← Add/Update/Delete records
```

---

## 🗄️ Database Schema

The project uses **9 MySQL tables**:

| Table | Description |
|---|---|
| `teams` | International cricket teams |
| `venues` | Cricket stadiums with capacity |
| `players` | Player profiles with roles & styles |
| `series` | Cricket series information |
| `matches` | Match results and details |
| `batting_stats` | Match-level batting scores |
| `bowling_stats` | Match-level bowling figures |
| `fielding_stats` | Catches, stumpings, run-outs |
| `career_stats` | Aggregated career statistics |

---

## ⚙️ Setup Instructions

### ✅ Prerequisites
- Python 3.10 or above
- MySQL 8.0 installed and running
- RapidAPI account (free tier) for live data

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/cricbuzz-livestats.git
cd cricbuzz-livestats
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables
Create a `.env` file in the root folder:
```
RAPIDAPI_KEY=your_rapidapi_key_here

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=cricbuzz_db
```

### Step 4 — Set Up the Database
Open **MySQL Workbench** and run:
```
File → Open SQL Script → select cricbuzz_schema.sql → Ctrl+Shift+Enter
```

### Step 5 — Run the App
```bash
streamlit run main.py
```

Open your browser at: **http://localhost:8501** 🚀

---

## 📊 App Pages & Features

### 🏠 Home Page
- Project overview and feature highlights
- Tech stack display and navigation guide

### 📺 Live Matches Page
- 🔴 Live Now — Real-time scorecards with runs, wickets, overs
- ✅ Recent — Recently completed matches
- 📅 Upcoming — Scheduled future matches

### 🏆 Player Stats Page
- ICC Batting & Bowling Rankings (ODI / Test / T20I)
- Interactive Plotly bar charts
- Database career statistics

### 📊 SQL Analytics Page
- 25 SQL queries (Beginner → Intermediate → Advanced)
- Run queries live on MySQL database
- Custom SQL editor for your own queries

### ⚙️ CRUD Operations Page
- Players: Add, Update, Delete records
- Matches: Add, Delete records
- Form-based UI connected to live MySQL

---

## 🧮 SQL Practice Questions (25 Queries)

### 🟢 Beginner (Q1–Q8)
Q1 - India players | Q2 - Recent matches | Q3 - Top ODI scorers
Q4 - Large venues | Q5 - Team wins | Q6 - Players by role
Q7 - Highest score per format | Q8 - 2024 series

### 🟡 Intermediate (Q9–Q16)
Q9 - All-rounders | Q10 - Completed matches | Q11 - Cross-format stats
Q12 - Home vs Away | Q13 - Partnerships | Q14 - Venue bowling
Q15 - Close matches | Q16 - Performance by year

### 🔴 Advanced (Q17–Q25)
Q17 - Toss advantage | Q18 - Economical bowlers | Q19 - Consistency
Q20 - Format averages | Q21 - Player ranking | Q22 - Head-to-head
Q23 - Form analysis | Q24 - Best partnerships | Q25 - Career trajectory

---

## 👨‍💻 Author

**Gangarapu Datha Naga Sai**
- 🎓 Data / Business Analyst Intern at **Labmentrix**
- 💼 LinkedIn: [gangarapu-datha-naga-sai](https://www.linkedin.com/in/gangarapu-datha-naga-sai)
- 🐙 GitHub: [nagasai-datha](https://github.com/nagasai-datha)
- 📧 Email: nagasaigangarapu@gmail.com
- 🎬 Demo Video: [Watch on Google Drive](https://drive.google.com/file/d/1sqTO6HyN6TADgJDO1VbT-eOa5tz2fMBf/view?usp=sharing)

---

## 🙏 Acknowledgements

- [Cricbuzz Cricket API](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/) via RapidAPI
- [Streamlit](https://streamlit.io/) — Web framework
- **Labmentrix** — For the internship project assignment

---

## 📄 License
MIT License — free to use and modify!

import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", ""),
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

def api_get(endpoint):
    """Generic GET request to Cricbuzz API."""
    try:
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_live_matches():
    """Fetch all live/recent matches."""
    data = api_get("matches/v1/live")
    matches = []
    if "typeMatches" in data:
        for type_match in data["typeMatches"]:
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})
                    matches.append({
                        "match_id": info.get("matchId"),
                        "description": info.get("matchDesc", ""),
                        "series": series_wrapper.get("seriesName", ""),
                        "team1": info.get("team1", {}).get("teamName", ""),
                        "team2": info.get("team2", {}).get("teamName", ""),
                        "status": info.get("status", ""),
                        "venue": info.get("venueInfo", {}).get("ground", ""),
                        "city": info.get("venueInfo", {}).get("city", ""),
                        "match_format": info.get("matchFormat", ""),
                        "team1_score": score.get("team1Score", {}).get("inngs1", {}).get("runs", "-"),
                        "team1_wkts": score.get("team1Score", {}).get("inngs1", {}).get("wickets", "-"),
                        "team1_overs": score.get("team1Score", {}).get("inngs1", {}).get("overs", "-"),
                        "team2_score": score.get("team2Score", {}).get("inngs1", {}).get("runs", "-"),
                        "team2_wkts": score.get("team2Score", {}).get("inngs1", {}).get("wickets", "-"),
                        "team2_overs": score.get("team2Score", {}).get("inngs1", {}).get("overs", "-"),
                    })
    return matches

def get_recent_matches():
    """Fetch recently completed matches."""
    data = api_get("matches/v1/recent")
    matches = []
    if "typeMatches" in data:
        for type_match in data["typeMatches"]:
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    matches.append({
                        "match_id": info.get("matchId"),
                        "description": info.get("matchDesc", ""),
                        "series": series_wrapper.get("seriesName", ""),
                        "team1": info.get("team1", {}).get("teamName", ""),
                        "team2": info.get("team2", {}).get("teamName", ""),
                        "status": info.get("status", ""),
                        "venue": info.get("venueInfo", {}).get("ground", ""),
                        "match_format": info.get("matchFormat", ""),
                    })
    return matches

def get_upcoming_matches():
    """Fetch upcoming matches."""
    data = api_get("matches/v1/upcoming")
    matches = []
    if "typeMatches" in data:
        for type_match in data["typeMatches"]:
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    matches.append({
                        "match_id": info.get("matchId"),
                        "description": info.get("matchDesc", ""),
                        "series": series_wrapper.get("seriesName", ""),
                        "team1": info.get("team1", {}).get("teamName", ""),
                        "team2": info.get("team2", {}).get("teamName", ""),
                        "start_date": info.get("startDate", ""),
                        "venue": info.get("venueInfo", {}).get("ground", ""),
                        "match_format": info.get("matchFormat", ""),
                    })
    return matches

def get_batting_stats(type_="icc-rankings", format_="odi"):
    """Fetch top batting stats / ICC rankings."""
    data = api_get(f"stats/v1/rankings/batsmen?formatType={format_}")
    players = []
    if "rank" in data:
        for p in data["rank"][:20]:
            players.append({
                "rank": p.get("rank"),
                "name": p.get("name"),
                "country": p.get("country"),
                "rating": p.get("rating"),
                "points": p.get("points"),
            })
    return players

def get_bowling_stats(format_="odi"):
    """Fetch top bowling stats / ICC rankings."""
    data = api_get(f"stats/v1/rankings/bowlers?formatType={format_}")
    players = []
    if "rank" in data:
        for p in data["rank"][:20]:
            players.append({
                "rank": p.get("rank"),
                "name": p.get("name"),
                "country": p.get("country"),
                "rating": p.get("rating"),
                "points": p.get("points"),
            })
    return players

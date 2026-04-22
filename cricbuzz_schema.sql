-- ============================================================
-- CRICBUZZ LIVESTATS - DATABASE SCHEMA
-- Run this in MySQL Workbench
-- ============================================================

CREATE DATABASE IF NOT EXISTS cricbuzz_db;
USE cricbuzz_db;

-- ============================================================
-- TABLE 1: teams
-- ============================================================
CREATE TABLE IF NOT EXISTS teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(10),
    country VARCHAR(100),
    team_type ENUM('international', 'domestic', 'ipl') DEFAULT 'international',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE 2: venues
-- ============================================================
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE 3: players
-- ============================================================
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    date_of_birth DATE,
    playing_role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper') DEFAULT 'Batsman',
    batting_style ENUM('Right-hand bat', 'Left-hand bat') DEFAULT 'Right-hand bat',
    bowling_style VARCHAR(100),
    team_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- ============================================================
-- TABLE 4: series
-- ============================================================
CREATE TABLE IF NOT EXISTS series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other') DEFAULT 'ODI',
    start_date DATE,
    end_date DATE,
    total_matches INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE 5: matches
-- ============================================================
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    series_id INT,
    match_description VARCHAR(200),
    team1_id INT,
    team2_id INT,
    venue_id INT,
    match_date DATETIME,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other') DEFAULT 'ODI',
    status ENUM('upcoming', 'live', 'completed') DEFAULT 'upcoming',
    toss_winner_id INT,
    toss_decision ENUM('bat', 'bowl'),
    winning_team_id INT,
    victory_margin VARCHAR(50),
    victory_type ENUM('runs', 'wickets', 'draw', 'tie', 'no result'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id)
);

-- ============================================================
-- TABLE 6: batting_stats
-- ============================================================
CREATE TABLE IF NOT EXISTS batting_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    innings_number INT DEFAULT 1,
    batting_position INT,
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate DECIMAL(6,2),
    dismissal_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- ============================================================
-- TABLE 7: bowling_stats
-- ============================================================
CREATE TABLE IF NOT EXISTS bowling_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    innings_number INT DEFAULT 1,
    overs_bowled DECIMAL(4,1),
    maidens INT DEFAULT 0,
    runs_given INT DEFAULT 0,
    wickets INT DEFAULT 0,
    economy_rate DECIMAL(5,2),
    bowling_average DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- ============================================================
-- TABLE 8: fielding_stats
-- ============================================================
CREATE TABLE IF NOT EXISTS fielding_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    run_outs INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- ============================================================
-- TABLE 9: career_stats (aggregated per player per format)
-- ============================================================
CREATE TABLE IF NOT EXISTS career_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    matches_played INT DEFAULT 0,
    total_runs INT DEFAULT 0,
    highest_score INT DEFAULT 0,
    batting_average DECIMAL(6,2),
    total_centuries INT DEFAULT 0,
    total_fifties INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    bowling_average DECIMAL(6,2),
    best_bowling VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- ============================================================
-- SAMPLE DATA INSERT
-- ============================================================

-- Teams
INSERT INTO teams (team_name, short_name, country, team_type) VALUES
('India', 'IND', 'India', 'international'),
('Australia', 'AUS', 'Australia', 'international'),
('England', 'ENG', 'England', 'international'),
('Pakistan', 'PAK', 'Pakistan', 'international'),
('South Africa', 'SA', 'South Africa', 'international'),
('New Zealand', 'NZ', 'New Zealand', 'international'),
('West Indies', 'WI', 'West Indies', 'international'),
('Sri Lanka', 'SL', 'Sri Lanka', 'international'),
('Bangladesh', 'BAN', 'Bangladesh', 'international'),
('Afghanistan', 'AFG', 'Afghanistan', 'international');

-- Venues
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Eden Gardens', 'Kolkata', 'India', 66000),
('Lords Cricket Ground', 'London', 'England', 30000),
('Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
('Wankhede Stadium', 'Mumbai', 'India', 33108),
('The Oval', 'London', 'England', 25500),
('Headingley', 'Leeds', 'England', 17000),
('M. Chinnaswamy Stadium', 'Bengaluru', 'India', 40000),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
('SuperSport Park', 'Centurion', 'South Africa', 22000),
('Arun Jaitley Stadium', 'Delhi', 'India', 41820);

-- Players
INSERT INTO players (full_name, country, date_of_birth, playing_role, batting_style, bowling_style, team_id) VALUES
('Virat Kohli', 'India', '1988-11-05', 'Batsman', 'Right-hand bat', 'Right-arm medium', 1),
('Rohit Sharma', 'India', '1987-04-30', 'Batsman', 'Right-hand bat', 'Right-arm off break', 1),
('Jasprit Bumrah', 'India', '1993-12-06', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
('Ravindra Jadeja', 'India', '1988-12-06', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
('KL Rahul', 'India', '1992-04-18', 'Wicket-keeper', 'Right-hand bat', 'Right-arm off break', 1),
('Steve Smith', 'Australia', '1989-06-02', 'Batsman', 'Right-hand bat', 'Right-arm leg break', 2),
('Pat Cummins', 'Australia', '1993-05-08', 'Bowler', 'Right-hand bat', 'Right-arm fast', 2),
('David Warner', 'Australia', '1986-10-27', 'Batsman', 'Left-hand bat', 'Right-arm off break', 2),
('Joe Root', 'England', '1990-12-30', 'Batsman', 'Right-hand bat', 'Right-arm off break', 3),
('Ben Stokes', 'England', '1991-06-04', 'All-rounder', 'Left-hand bat', 'Right-arm fast medium', 3),
('Babar Azam', 'Pakistan', '1994-10-15', 'Batsman', 'Right-hand bat', 'Right-arm off break', 4),
('Shaheen Afridi', 'Pakistan', '2000-04-06', 'Bowler', 'Left-hand bat', 'Left-arm fast', 4),
('Kagiso Rabada', 'South Africa', '1995-05-25', 'Bowler', 'Right-hand bat', 'Right-arm fast', 5),
('Quinton de Kock', 'South Africa', '1992-12-17', 'Wicket-keeper', 'Left-hand bat', NULL, 5),
('Kane Williamson', 'New Zealand', '1990-08-08', 'Batsman', 'Right-hand bat', 'Right-arm off break', 6),
('Trent Boult', 'New Zealand', '1989-07-22', 'Bowler', 'Right-hand bat', 'Left-arm fast medium', 6),
('Chris Gayle', 'West Indies', '1979-09-21', 'Batsman', 'Left-hand bat', 'Right-arm off break', 7),
('Kusal Mendis', 'Sri Lanka', '1995-02-02', 'Wicket-keeper', 'Right-hand bat', NULL, 8),
('Shakib Al Hasan', 'Bangladesh', '1987-03-24', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 9),
('Rashid Khan', 'Afghanistan', '1998-09-20', 'All-rounder', 'Right-hand bat', 'Right-arm leg break', 10);

-- Series
INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
('ICC Cricket World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
('Border-Gavaskar Trophy 2024', 'Australia', 'Test', '2024-11-22', '2025-01-07', 5),
('ICC T20 World Cup 2024', 'West Indies', 'T20I', '2024-06-01', '2024-06-29', 55),
('India vs England ODI Series 2024', 'India', 'ODI', '2024-02-01', '2024-02-10', 3),
('India vs Australia T20 Series 2024', 'India', 'T20I', '2024-11-22', '2024-12-01', 5),
('Pakistan vs New Zealand Test 2024', 'Pakistan', 'Test', '2024-12-16', '2025-01-03', 3),
('SA20 League 2024', 'South Africa', 'T20', '2024-01-10', '2024-02-10', 33),
('India vs Sri Lanka ODI 2024', 'Sri Lanka', 'ODI', '2024-07-27', '2024-08-07', 3);

-- Matches
INSERT INTO matches (series_id, match_description, team1_id, team2_id, venue_id, match_date, match_type, status, toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type) VALUES
(1, 'IND vs AUS - Match 1, ICC WC 2023', 1, 2, 1, '2023-10-08 14:00:00', 'ODI', 'completed', 1, 'bat', 1, '6 wickets', 'wickets'),
(1, 'IND vs PAK - Match 12, ICC WC 2023', 1, 4, 1, '2023-10-14 14:00:00', 'ODI', 'completed', 4, 'bowl', 1, '7 wickets', 'wickets'),
(1, 'ENG vs AUS - Match 15, ICC WC 2023', 3, 2, 9, '2023-10-17 14:00:00', 'ODI', 'completed', 2, 'bat', 2, '33 runs', 'runs'),
(2, 'AUS vs IND - 1st Test, BGT 2024', 2, 1, 5, '2024-11-22 04:00:00', 'Test', 'completed', 2, 'bat', 2, '295 runs', 'runs'),
(2, 'AUS vs IND - 2nd Test, BGT 2024', 2, 1, 3, '2024-12-06 04:00:00', 'Test', 'completed', 1, 'bowl', 1, '295 runs', 'runs'),
(3, 'IND vs PAK - T20 WC 2024', 1, 4, NULL, '2024-06-09 20:00:00', 'T20I', 'completed', 1, 'bat', 1, '6 runs', 'runs'),
(4, 'IND vs ENG - 1st ODI 2024', 1, 3, 6, '2024-02-01 13:30:00', 'ODI', 'completed', 3, 'bowl', 1, '8 wickets', 'wickets'),
(5, 'IND vs AUS - 1st T20I 2024', 1, 2, 12, '2024-11-22 19:00:00', 'T20I', 'completed', 2, 'bowl', 2, '7 wickets', 'wickets'),
(8, 'SL vs IND - 1st ODI 2024', 8, 1, NULL, '2024-07-27 14:30:00', 'ODI', 'completed', 1, 'bat', 1, '3 wickets', 'wickets'),
(1, 'NZ vs SA - Match 20, ICC WC 2023', 6, 5, 9, '2023-10-19 14:00:00', 'ODI', 'completed', 6, 'bat', 5, '190 runs', 'runs');

-- Career Stats
INSERT INTO career_stats (player_id, match_type, matches_played, total_runs, highest_score, batting_average, total_centuries, total_fifties, total_wickets, bowling_average, best_bowling) VALUES
(1, 'Test', 113, 8848, 254, 49.95, 29, 31, 0, NULL, NULL),
(1, 'ODI', 295, 13906, 183, 57.32, 50, 72, 4, 166.0, '1/15'),
(1, 'T20I', 125, 4188, 122, 52.35, 1, 38, 0, NULL, NULL),
(2, 'Test', 67, 4301, 212, 39.64, 12, 17, 8, 97.0, '2/10'),
(2, 'ODI', 264, 10709, 264, 48.96, 31, 56, 8, 83.0, '2/27'),
(2, 'T20I', 159, 4231, 118, 32.05, 5, 32, 10, 57.2, '2/9'),
(6, 'Test', 108, 9390, 239, 55.27, 32, 40, 17, 81.5, '3/18'),
(6, 'ODI', 170, 7227, 164, 43.53, 13, 46, 25, 63.8, '3/26'),
(9, 'Test', 145, 12272, 254, 54.30, 34, 61, 57, 51.2, '5/8'),
(9, 'ODI', 185, 7658, 180, 53.90, 22, 46, 21, 72.3, '4/66'),
(11, 'Test', 55, 4088, 196, 48.15, 11, 25, 5, 120.0, '1/30'),
(11, 'ODI', 104, 5187, 158, 56.38, 19, 27, 3, 95.0, '1/20'),
(11, 'T20I', 124, 4026, 122, 44.72, 4, 31, 4, 88.0, '1/14'),
(19, 'Test', 68, 4526, 217, 38.35, 12, 23, 240, 30.5, '7/36'),
(19, 'ODI', 247, 7624, 134, 37.56, 9, 55, 323, 29.8, '6/55'),
(19, 'T20I', 122, 2335, 84, 23.58, 0, 15, 131, 28.4, '5/20'),
(20, 'ODI', 85, 1232, 60, 16.85, 0, 5, 172, 17.5, '7/18'),
(20, 'T20I', 94, 893, 48, 13.71, 0, 1, 149, 13.6, '5/3'),
(3, 'Test', 42, 630, 55, 11.25, 0, 1, 182, 20.4, '6/27'),
(3, 'ODI', 90, 545, 35, 8.08, 0, 0, 149, 24.3, '6/19'),
(3, 'T20I', 75, 204, 15, 5.10, 0, 0, 89, 18.6, '4/14');

-- Batting Stats (match level)
INSERT INTO batting_stats (player_id, match_id, match_type, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, dismissal_type) VALUES
(1, 1, 'ODI', 2, 3, 85, 78, 8, 2, 108.97, 'caught'),
(2, 1, 'ODI', 2, 1, 92, 101, 9, 1, 91.08, 'not out'),
(6, 1, 'ODI', 1, 3, 46, 55, 4, 1, 83.63, 'bowled'),
(1, 2, 'ODI', 2, 3, 16, 29, 1, 0, 55.17, 'lbw'),
(11, 2, 'ODI', 1, 1, 42, 49, 5, 0, 85.71, 'caught'),
(9, 3, 'ODI', 1, 3, 71, 83, 7, 1, 85.54, 'run out'),
(10, 3, 'ODI', 2, 5, 43, 38, 4, 2, 113.15, 'caught'),
(6, 4, 'Test', 1, 3, 31, 62, 4, 0, 50.00, 'caught'),
(1, 4, 'Test', 2, 3, 17, 44, 2, 0, 38.63, 'bowled'),
(2, 5, 'Test', 1, 1, 56, 121, 7, 0, 46.28, 'caught'),
(1, 6, 'T20I', 1, 3, 76, 59, 6, 4, 128.81, 'not out'),
(11, 6, 'T20I', 2, 1, 53, 41, 5, 2, 129.26, 'run out'),
(1, 7, 'ODI', 2, 3, 0, 1, 0, 0, 0.00, 'caught'),
(2, 7, 'ODI', 2, 1, 40, 32, 4, 2, 125.00, 'not out'),
(1, 8, 'T20I', 1, 3, 11, 13, 1, 0, 84.61, 'bowled');

-- Bowling Stats
INSERT INTO bowling_stats (player_id, match_id, match_type, innings_number, overs_bowled, maidens, runs_given, wickets, economy_rate, bowling_average) VALUES
(3, 1, 'ODI', 1, 10.0, 1, 42, 2, 4.20, 21.00),
(4, 1, 'ODI', 1, 10.0, 0, 55, 1, 5.50, 55.00),
(7, 1, 'ODI', 2, 9.0, 0, 48, 0, 5.33, NULL),
(12, 2, 'ODI', 2, 10.0, 2, 28, 3, 2.80, 9.33),
(3, 4, 'Test', 2, 22.0, 4, 67, 5, 3.04, 13.40),
(7, 4, 'Test', 1, 19.0, 3, 65, 3, 3.42, 21.66),
(13, 10, 'ODI', 2, 10.0, 1, 38, 4, 3.80, 9.50),
(20, 6, 'T20I', 1, 4.0, 0, 22, 2, 5.50, 11.00),
(12, 6, 'T20I', 1, 4.0, 0, 14, 1, 3.50, 14.00),
(16, 1, 'ODI', 1, 10.0, 0, 58, 2, 5.80, 29.00);

-- Fielding Stats
INSERT INTO fielding_stats (player_id, match_id, catches, stumpings, run_outs) VALUES
(5, 1, 2, 0, 1),
(5, 2, 1, 1, 0),
(14, 10, 3, 0, 0),
(4, 1, 1, 0, 0),
(10, 3, 2, 0, 0),
(15, 10, 1, 0, 1),
(5, 7, 1, 0, 0),
(18, 9, 2, 1, 0);

-- ============================================================
-- VERIFY DATA
-- ============================================================
SELECT 'Teams' AS table_name, COUNT(*) AS row_count FROM teams
UNION ALL SELECT 'Venues', COUNT(*) FROM venues
UNION ALL SELECT 'Players', COUNT(*) FROM players
UNION ALL SELECT 'Series', COUNT(*) FROM series
UNION ALL SELECT 'Matches', COUNT(*) FROM matches
UNION ALL SELECT 'Career Stats', COUNT(*) FROM career_stats
UNION ALL SELECT 'Batting Stats', COUNT(*) FROM batting_stats
UNION ALL SELECT 'Bowling Stats', COUNT(*) FROM bowling_stats
UNION ALL SELECT 'Fielding Stats', COUNT(*) FROM fielding_stats;

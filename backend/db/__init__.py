import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.get_db_url())
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create teams table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            team_name VARCHAR(100) NOT NULL,
            captain_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            players_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create matches table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            team1_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
            team2_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
            match_date DATE NOT NULL,
            match_time TIME NOT NULL,
            location VARCHAR(200) NOT NULL,
            score_team1 INTEGER DEFAULT 0,
            score_team2 INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.close()
    conn.close()
    print("Database initialized successfully!")
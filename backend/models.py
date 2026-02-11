from db import get_db_connection

class Team:
    @staticmethod
    def create(team_name, captain_name, email, phone, players_count):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO teams (team_name, captain_name, email, phone, players_count) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (team_name, captain_name, email, phone, players_count)
        )
        team_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return team_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM teams ORDER BY created_at DESC')
        columns = [desc[0] for desc in cur.description]
        teams = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return teams

    @staticmethod
    def get_by_id(team_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM teams WHERE id = %s', (team_id,))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            team = dict(zip(columns, row))
        else:
            team = None
        cur.close()
        conn.close()
        return team

    @staticmethod
    def delete(team_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM teams WHERE id = %s', (team_id,))
        cur.close()
        conn.close()


class Match:
    @staticmethod
    def create(team1_id, team2_id, match_date, match_time, location):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO matches (team1_id, team2_id, match_date, match_time, location) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (team1_id, team2_id, match_date, match_time, location)
        )
        match_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return match_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT m.id, m.match_date, m.match_time, m.location, 
                   m.score_team1, m.score_team2, m.status,
                   t1.team_name as team1_name, t2.team_name as team2_name,
                   m.team1_id, m.team2_id, m.created_at
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.id
            JOIN teams t2 ON m.team2_id = t2.id
            ORDER BY m.match_date, m.match_time
        ''')
        columns = [desc[0] for desc in cur.description]
        matches = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return matches

    @staticmethod
    def update_score(match_id, score_team1, score_team2, status):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''UPDATE matches SET score_team1 = %s, score_team2 = %s, status = %s 
               WHERE id = %s''',
            (score_team1, score_team2, status, match_id)
        )
        cur.close()
        conn.close()

    @staticmethod
    def delete(match_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM matches WHERE id = %s', (match_id,))
        cur.close()
        conn.close()
from flask import Blueprint, request, jsonify
from models import Match

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/api/matches', methods=['GET'])
def get_matches():
    try:
        matches = Match.get_all()
        for match in matches:
            if match.get('match_date'):
                match['match_date'] = str(match['match_date'])
            if match.get('match_time'):
                match['match_time'] = str(match['match_time'])
            if match.get('created_at'):
                match['created_at'] = str(match['created_at'])
        return jsonify(matches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/api/matches', methods=['POST'])
def create_match():
    try:
        data = request.get_json()
        team1_id = data.get('team1_id')
        team2_id = data.get('team2_id')
        match_date = data.get('match_date')
        match_time = data.get('match_time')
        location = data.get('location')

        if not all([team1_id, team2_id, match_date, match_time, location]):
            return jsonify({'error': 'All fields are required'}), 400

        if team1_id == team2_id:
            return jsonify({'error': 'A team cannot play against itself'}), 400

        match_id = Match.create(team1_id, team2_id, match_date, match_time, location)
        return jsonify({'message': 'Match scheduled successfully', 'id': match_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/api/matches/<int:match_id>/score', methods=['PUT'])
def update_score(match_id):
    try:
        data = request.get_json()
        score_team1 = data.get('score_team1', 0)
        score_team2 = data.get('score_team2', 0)
        status = data.get('status', 'completed')

        Match.update_score(match_id, score_team1, score_team2, status)
        return jsonify({'message': 'Score updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/api/matches/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    try:
        Match.delete(match_id)
        return jsonify({'message': 'Match deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import Blueprint, request, jsonify
from models import Team

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        teams = Team.get_all()
        # Convert datetime objects to strings
        for team in teams:
            if team.get('created_at'):
                team['created_at'] = str(team['created_at'])
        return jsonify(teams), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/api/teams', methods=['POST'])
def create_team():
    try:
        data = request.get_json()
        team_name = data.get('team_name')
        captain_name = data.get('captain_name')
        email = data.get('email')
        phone = data.get('phone')
        players_count = data.get('players_count')

        if not all([team_name, captain_name, email, phone, players_count]):
            return jsonify({'error': 'All fields are required'}), 400

        team_id = Team.create(team_name, captain_name, email, phone, players_count)
        return jsonify({'message': 'Team registered successfully', 'id': team_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    try:
        team = Team.get_by_id(team_id)
        if team:
            if team.get('created_at'):
                team['created_at'] = str(team['created_at'])
            return jsonify(team), 200
        return jsonify({'error': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/api/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    try:
        Team.delete(team_id)
        return jsonify({'message': 'Team deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
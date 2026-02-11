from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from db import init_db
from routes.teams import teams_bp
from routes.matches import matches_bp
import time

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(teams_bp)
app.register_blueprint(matches_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'volleyball-backend'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Volleyball Tournament API', 'version': '1.0'}), 200

def start_app():
    max_retries = 10
    for i in range(max_retries):
        try:
            init_db()
            print("Database connected and initialized!")
            break
        except Exception as e:
            print(f"Database connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                time.sleep(5)
            else:
                print("Could not connect to database. Starting anyway...")

if __name__ == '__main__':
    start_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
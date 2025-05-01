from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "SHL Assessment Backend API is running"
    })

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        query = data.get('query')
        # Process query and return recommendations
        return jsonify({
            "status": "success",
            "recommendations": [
                {"title": "Sample Assessment 1", "description": "Description 1"},
                {"title": "Sample Assessment 2", "description": "Description 2"}
            ]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))

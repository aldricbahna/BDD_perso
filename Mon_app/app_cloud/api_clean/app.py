# api/app.py

from flask import Flask, request, jsonify
from predict import make_prediction
import logging
import os

os.makedirs('logs', exist_ok=True)

# Configuration des logs
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)

@app.before_request
def log_request_info():
    app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route('/')
def home():
    return jsonify({'message': 'API de prédiction opérationnelle 🚀'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        prediction = make_prediction(data)
        return jsonify({'prediction': round(prediction, 2)})
    except Exception as e:
        app.logger.error(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

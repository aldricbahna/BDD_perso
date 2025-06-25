# api/app.py

from flask import Flask, request, jsonify
from predict import make_prediction

app = Flask(__name__)

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
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

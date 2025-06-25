# api/model_loader.py

import joblib
import os

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'mon_modele', 'model.joblib')
    model = joblib.load(model_path)
    return model

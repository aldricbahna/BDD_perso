# api/predict.py

import pandas as pd
from model_loader import load_model
from sklearn.preprocessing import StandardScaler
import joblib
import os
import numpy as np
from sklearn.model_selection import train_test_split
from preprocessing_predict import nettoyage_predict

model = load_model()

def prepare_input(data: dict) -> pd.DataFrame:
    """
    Transforme le JSON reçu en DataFrame + applique les mêmes transformations
    que celles utilisées pour l'entraînement du modèle.
    """
    X_predict = pd.DataFrame([data])
    X_predict=nettoyage_predict(X_predict)
    
    
    return X_predict

def make_prediction(data: dict) -> float:
    """
    Prend un dictionnaire (venant de l'API), retourne la prédiction du modèle.
    """
    df = prepare_input(data)
    prediction = model.predict(df)

    return float(prediction[0])

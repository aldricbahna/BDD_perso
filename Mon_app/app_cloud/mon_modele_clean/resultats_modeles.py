from preprocessing import choix_features, nettoyage
from model_training import get_models, split_data
from evaluation import evaluate_model, lazy_prediction
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import KFold, train_test_split
import pandas as pd
import os
import joblib

path = 'data/BILAN_JOURNEE_mai25.csv'
df = choix_features(path)
df=nettoyage(df)

X=df.drop('Note',axis=1)
y=df['Note']
fold = KFold(n_splits=5, shuffle=True, random_state=42)

def resultat_modeles(X,y,fold):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    resultat_tableau_modeles=lazy_prediction(X,y,fold)
    print(resultat_tableau_modeles)

resultat_modeles(X,y,fold)
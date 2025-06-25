from preprocessing import choix_features, nettoyage, lazy_regressor_preprocessor
from model_training import get_models, split_data
from evaluation import evaluate_model, lazy_prediction, evaluation_metriques
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = lazy_regressor_preprocessor(X)
dict_models=get_models()
evaluation_metriques(dict_models, preprocessor,X_train,y_train,X_test,y_test,fold)
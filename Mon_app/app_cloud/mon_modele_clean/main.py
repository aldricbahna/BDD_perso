from preprocessing import choix_features, nettoyage, lazy_regressor_preprocessor
from model_training import get_models, split_data
from evaluation import evaluate_model
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pandas as pd
import os
import joblib

def main():
    path = 'data/BILAN_JOURNEE_mai25.csv'
    df = choix_features(path)
    df=nettoyage(df)

    X=df.drop('Note',axis=1)
    y=df['Note']
    preprocessor=lazy_regressor_preprocessor(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor",LinearRegression())
    ])
    model.fit(X_train,y_train)
  
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    joblib.dump(model, model_path)
    print(f"✅ Modèle sauvegardé dans {model_path}")

if __name__ == "__main__":
    main()




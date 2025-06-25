import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
import os
import dateparser

#scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
#scaler = joblib.load(scaler_path)

def choix_features(path):
    df = pd.read_csv(path, sep=';', decimal=',')
    df=df.set_index('Jour')
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df=df.iloc[:-1,:]

    
    df['Somme réseaux']=df['Snap']+df['Insta']+df['Twitter']+df['BeReal']
    df['Jour semaine'] = df.index.strftime('%A')
    
    cols_continues=['Somme réseaux','Lecture']
    
    cols_binaires_ML=["A l'étranger",'Parents',
     'Eugé',
     'Sport',
     'Ciné',
     'Film',
     'Docu',
     'Restau',
     'Fast food',
     'Café/bar solo',
     'Lecture dehors',
     'Café/bar avec copains',
     'Repas copains',
     'Vois copains',
     'Soirée chill',
     'Soirée',
     'Dodo avec Eugé',
    'Messe']
    
    cols_presque_binaires_ML=['Copains','Activité','Transport','Match de sport','Footing']
    
    cols_cat=['Jour semaine','Type']
    
    df=df[cols_cat+cols_binaires_ML+cols_presque_binaires_ML+cols_continues+['Note']]
    return df
 
def nettoyage(df):
    jours = {
        'Monday': 'lundi',
        'Tuesday': 'mardi',
        'Wednesday': 'mercredi',
        'Thursday': 'jeudi',
        'Friday': 'vendredi',
        'Saturday': 'samedi',
        'Sunday': 'dimanche'
        }
    df['Jour semaine']=df['Jour semaine'].map(jours)
    df['Copains']=df['Copains'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Activité']=df['Activité'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Transport']=df['Transport'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Match de sport']=df['Match de sport'].map(lambda x: 0 if x==0 else 1)
    df['Footing']=df['Footing'].map(lambda x: 0 if x==0 else 1)
    df["A l'étranger"].fillna('non',inplace=True)
    df["A l'étranger"]=df["A l'étranger"].apply(lambda x: 1 if x == 'oui' else (0 if x == 'non' else np.nan))
    df['Sport']=df['Sport'].map(lambda x:0 if x==0 else 1)
    df['Messe']=df['Messe'].map(lambda x:1 if x==1 else 0)
    df.dropna(inplace=True)
    return df

def nettoyage_predict(df):
    df['Copains']=df['Copains'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Activité']=df['Activité'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Transport']=df['Transport'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Match de sport']=df['Match de sport'].map(lambda x: 0 if x==0 else 1)
    df['Footing']=df['Footing'].map(lambda x: 0 if x==0 else 1)
    df["A l'étranger"]=df["A l'étranger"].apply(lambda x: 1 if x == 'oui' else (0 if x == 'non' else np.nan))
    return df


def lazy_regressor_preprocessor(X):
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
        ],
        remainder="passthrough"  # conserve les colonnes numériques telles quelles
    )
    
    return preprocessor
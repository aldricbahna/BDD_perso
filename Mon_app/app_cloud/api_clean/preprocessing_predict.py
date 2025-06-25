import pandas as pd

def nettoyage_predict(df):
    df['Copains']=df['Copains'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Activité']=df['Activité'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Transport']=df['Transport'].map(lambda x: 1 if pd.notna(x) and x != '' else 0)
    df['Match de sport']=df['Match de sport'].map(lambda x: 0 if x==0 else 1)
    df['Footing']=df['Footing'].map(lambda x: 0 if x==0 else 1)
    df["A l'étranger"]=df["A l'étranger"].apply(lambda x: 1 if x == 'oui' else (0 if x == 'non' else np.nan))
    return df
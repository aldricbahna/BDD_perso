import pandas as pd

data=pd.read_csv('BILAN_JOURNEE_mai25.csv',sep=';')
print(data)
df_4_colonnes=data[['Jour', 'Note', 'Type', 'Lecture']]
df_4_colonnes['Note'] = df_4_colonnes['Note'].astype(str).str.replace(',', '.', regex=False).astype(float)
df_4_colonnes.to_csv('BILAN_JOURNEE_4cols.csv',index=False,sep=';')
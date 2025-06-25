import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import datetime as dt
from datetime import timedelta, datetime    
import itertools
import multiprocessing
import time

from auth import check_password
check_password()


jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']



df, couleur,couleur_box=load_data()
hier = datetime.now() - timedelta(days=1)
hier = hier.replace(hour=0, minute=0, second=0, microsecond=0) # Important que les paramètres du temps soient à 0 pour les sliders !!
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)

cols_presque_binaires=['Activité', 'Transport']

df['Sport']=df['Sport'].map(lambda x:0 if x==0 else 1)
cols_binaires=["Sport","Ciné","Film","Restau","Fast food",
               "Café/bar solo","Café/bar avec copains","Repas copains","Vois copains","Soirée chill","Soirée","Eugé","Messe","QPUC"]

#"Lecture au petit-déj","Lecture dehors","Café/bar Eugé"
df[cols_presque_binaires] = df[cols_presque_binaires].apply(lambda col: col.notna().astype('int8'))
df['Match de sport'] = df['Match de sport'].apply(lambda col: 0 if col==0 else 1)
cols_binaires=cols_binaires+['Match de sport']+cols_presque_binaires

df[cols_binaires]=df[cols_binaires].map(lambda x:1 if x>=1 else 0) #map car Series je crois



df[cols_binaires]=df[cols_binaires].astype('int8')
start = time.time()


df_bin = df[cols_binaires]

# 2. Trouver la combinaison exacte de colonnes à 1 pour chaque ligne
df['Combinaison'] = df_bin.apply(lambda row: tuple(col for col in row.index if row[col] == 1), axis=1)

# 3. Grouper par combinaison exacte
df_combi = df.groupby('Combinaison').agg(
    Moyenne=('Note', 'mean'),
    Nombre=('Note', 'count')
).reset_index()

# 4. Trier et afficher
df_combi.sort_values(by='Moyenne', ascending=False, inplace=True)
st.dataframe(df_combi)

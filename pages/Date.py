import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import datetime as dt
from datetime import timedelta, datetime    

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']



df, couleur,couleur_box=load_data()
hier = datetime.now() - timedelta(days=1)
hier = hier.replace(hour=0, minute=0, second=0, microsecond=0) # Important que les paramètres du temps soient à 0 pour les sliders !!
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)

d = st.date_input("Choisir une date :", value=hier)
jour=pd.to_datetime(d)
st.dataframe(df[df.index==jour])
st.metric('Journée',df.loc[jour,'Type'])
st.metric('Lieu',df.loc[jour,'Lieu'])
st.metric('Note',df.loc[jour,'Note'])
#heure_reveil=datetime.strptime(df.loc[jour,'Heure réveil'],"%Y-%m-%d %H:%M:%S")
if pd.isna(df.loc[jour, 'Heure réveil']):
    heure_reveil="-"
else:
    heure_reveil=df.loc[jour, 'Heure réveil'].strftime('%H:%M')


if pd.isna(df.loc[jour, 'Heure lever']):
    heure_lever="-"
else:
    heure_lever=df.loc[jour, 'Heure lever'].strftime('%H:%M')


if pd.isna(df.loc[jour, 'Heure dodo']):
    heure_dodo="-"
else:
    heure_dodo=df.loc[jour, 'Heure dodo'].strftime('%H:%M')

if pd.isna(df.loc[jour, 'Début travail']):
    debut_travail="-"
else:
    debut_travail=df.loc[jour, 'Début travail'].strftime('%H:%M')

st.metric('⏰ Heure réveil', heure_reveil)
st.metric('🌅 Heure lever', heure_lever)
st.metric('🌙 Heure dodo', heure_dodo)
st.metric('💼 Début travail', debut_travail)
st.metric('😴 Fatigue', df.loc[jour, 'Fatigue'])
st.metric('🛌 Sieste', f"{int(df.loc[jour, 'Sieste'])} mn")
st.metric('😓 Stress', df.loc[jour, 'Stress'])
st.metric('🚶 Nombre de pas', int(df.loc[jour, 'Nombre de pas']))
st.metric('🚴 Vélo', f"{int(df.loc[jour, 'Vélo'])} mn")
st.metric('🍽️ Alimentation', df.loc[jour, 'Alimentation'])
st.metric('🍬 Sucre', df.loc[jour, 'Sucre'])
st.metric('🍷 Alcool', df.loc[jour, 'Alcool'])
st.metric('📖 Lecture', f"{int(df.loc[jour, 'Lecture'])} mn")
st.metric('⏳ Temps perdu', f"{int(df.loc[jour, 'Temps perdu'])} mn")

colonnes_binaires=['Parents','Laëtitia','Famille','Eugé','Cuisine','Sport','Football','Footing','Ciné','Film','Docu','Restau','Restau Eugé','Fast food','Café/bar solo','Lecture dehors','Café/bar avec copains','Café/bar Eugé','Repas copains','Vois copains','QPUC','Soirée chill','Soirée','Dodo avec Eugé','Dodo chez moi','Dodo en lisant','Dodo sans tel','Messe']

#st.write(df.loc[jour, 'Résumé'])
#text=st.text_area("Résumé",df.loc[jour, 'Résumé'])
#st.plotly_chart(text)
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import datetime as dt
from datetime import timedelta, datetime, date  
from PIL import Image

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']



df, couleur,couleur_box=load_data()
hier = datetime.now() - timedelta(days=1)
hier = hier.replace(hour=0, minute=0, second=0, microsecond=0) # Important que les paramètres du temps soient à 0 pour les sliders !!
min_date = df[df.index == '2023-08-01'].index[0].to_pydatetime()
#min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)

periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY-MM-DD"  
        )

options = ["Tout","Entreprise","Week-end - Vacances", "Cours", "Projet/Mission Sciencéthic"]
selection = st.sidebar.selectbox(
    "Choix type de journée", options,index=0)

travail=[type for type in df['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
df_entreprise=df[(df['Type'].str.contains('Stage', na=False))|(df['Type'].str.contains('Alternance', na=False))]
df_cours=df[df['Type'].str.contains('Cours', na=False)]
df_projet=df[(df['Type'].str.contains('Projet', na=False))|(df['Type'].str.contains('Mission Sciencéthic', na=False))]
df_non_travail=df[~df['Type'].isin(travail)]
my_dict={"Tout":df,
        "Entreprise":df_entreprise,
        "Projet/Mission Sciencéthic":df_projet,
        "Cours":df_cours,
        "Week-end - Vacances":df_non_travail}

on = st.sidebar.toggle("Télétravail")
if on:
        df=my_dict[selection]
        df=df[df['Télétravail?']=='oui']
else:
        df=my_dict[selection]

dfs = df[(df.index >= periode[0]) & (df.index <= periode[1])]


dfs_mois=dfs['Météo num'].resample('M').mean()
fig_line_meteo_mois=px.line(dfs_mois)
tickvals = dfs_mois.index[::2]
fig_line_meteo_mois.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=tickvals.strftime('%b %y'),    
        ),
        title="Météo mensuelle sur 10"
    )
st.plotly_chart(fig_line_meteo_mois)

dfs_mois_pluie=dfs['Cumul pluie (mm)'].resample('M').mean()
fig_line_meteo_mois=px.line(dfs_mois_pluie)
tickvals = dfs_mois.index[::2]
fig_line_meteo_mois.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=tickvals.strftime('%b %y'),    
        ),
        title="Cumul pluie mensuel (en mm)"
    )
st.plotly_chart(fig_line_meteo_mois)



df_points=dfs.groupby(['Météo num','Note']).size().reset_index(name='count')

fig_scatter_meteo_note=px.scatter(df_points,x='Note',y='Météo num',size='count',height=500,title=f"Corrélation entre la météo et le bonheur : {dfs['Météo num'].corr(dfs['Note']):.2f}")
st.plotly_chart(fig_scatter_meteo_note)

fig_scatter_meteo_lecture=px.scatter(dfs,x='Lecture',y='Météo num',height=500,title=f"Corrélation entre la météo et le temps de lecture : {dfs['Météo num'].corr(dfs['Lecture']):.2f}")
st.plotly_chart(fig_scatter_meteo_lecture)
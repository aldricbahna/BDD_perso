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

df_points_sucre_forme=df.groupby(['Sucre num','Forme']).size().reset_index(name='count')
fig_sucre_forme=px.scatter(df_points_sucre_forme,x='Sucre num',y='Forme',size='count')
st.plotly_chart(fig_sucre_forme)


coef=df['Sucre num'].corr(df['Note'])
df_points_sucre_note=df.groupby(['Sucre num','Note']).size().reset_index(name='count')
fig_sucre_note=px.scatter(df_points_sucre_note,x='Sucre num',y='Note',size='count',title=f"{coef}")
st.plotly_chart(fig_sucre_note)
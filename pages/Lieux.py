import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from datetime import timedelta
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

st.set_page_config(page_title="Réseaux sociaux",layout="wide")
df, couleur,couleur_box=load_data()
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)


df['Lieu principal']=df['Lieu'].str.split('/').str[0].str.strip()
df_note_lieu=df.groupby('Lieu principal').agg(
    Note_moyenne=('Note','mean'),
    Nombre=('Note','count')
).reset_index()



data_lieux=pd.read_excel("loc_villes.xlsx")
dfl=data_lieux.copy()
dfl.rename(columns={'Lieu':'Lieu principal'},inplace=True)
df_note_lieu=pd.merge(df_note_lieu,dfl,on='Lieu principal',how='left')

fig = px.scatter_mapbox(
    df_note_lieu,
    lat="latitude",
    lon="longitude",
    size="Note_moyenne",
    size_max=30,
    color="Note_moyenne",
    color_continuous_scale="RdYlGn",
    hover_name="Lieu principal",
    hover_data={"Note_moyenne": True},
    zoom=5,
    height=500
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Streamlit
st.title("Carte des villes visitées avec notes moyennes")
st.plotly_chart(fig)

fig2 = px.scatter_mapbox(
    df_note_lieu,
    lat="latitude",
    lon="longitude",
    hover_name="Lieu principal",
    hover_data={"Note_moyenne": True, "Nombre": True,"longitude":False,"latitude":False},
    zoom=5,
    height=500
)
fig2.update_traces(marker=dict(size=14))
fig2.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig2)
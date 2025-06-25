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
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)



def resize_image(image_path, size=(130, 160)):  
    img = Image.open(image_path)
    return img.resize(size)

euge = resize_image("Copains/euge.png")

fig_occurence=px.bar(data_frame=df,x=df.index,y='Eugé',height=210,hover_name=df.index)
fig_occurence.update_xaxes(range=[df.index.min(), date.today()],title_text='')
fig_occurence.update_yaxes(dtick=1,title_text=None, tickvals=[])
fig_occurence.update_traces(width=0.5, marker=dict(line=dict(width=1, color='black'), opacity=0.8))
fig_occurence.update_layout(margin=dict(l=0, r=0, t=0, b=0))

df_euge=df[df['Eugé']==1]

def plus_grande_serie_de_1(colonne):
    # Diviser la colonne en séries de 1 consécutifs
    series = colonne.groupby(colonne.diff().ne(0).cumsum()).sum()
    # Retourner la plus grande longueur de série de 1
    return series.max()

plus_grande_serie = plus_grande_serie_de_1(df['Eugé'])
ratio_euge=round(df_euge.shape[0]/df.shape[0],1)*100

a,b=st.columns([7,2])
with a:
    c,d=st.columns([1,7])
    with c:
        st.image(euge)
    with d:
        st.plotly_chart(fig_occurence, use_container_width=True)
with b:
    c,d=st.columns(2)
    with c:
        st.metric("Nombre de jours vu",df_euge.shape[0])
        st.metric("Ratio",f"{ratio_euge} %")
    with d:
        st.metric("Nb jours sans se voir",(date.today()-df_euge.index.max().date()).days)
        st.metric("Plus grande série",int(plus_grande_serie))
       
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from datetime import timedelta, datetime, date
from wordcloud import WordCloud
from PIL import Image

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

st.set_page_config(page_title="Lecture",layout="wide")
data=pd.read_excel("BILAN_JOURNEE_V2.xlsx", sheet_name="Livres")
df_livres=data.copy()
df, couleur,couleur_box=load_data()
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64
from PIL import Image
import streamlit as st
import datetime

def resize_image(image_path, size=(60, 90)):  # Ajuste la taille selon tes besoins
    img = Image.open(image_path)
    return img.resize(size)

elliot = resize_image("Copains/elliot.png")
flo = resize_image("Copains/flo.png")
hugo=resize_image("Copains/hugo.png")

df['Copains'] = df['Copains'].str.split(', ')
df_exploded = df.explode('Copains')
st.dataframe(df_exploded['Copains'])

df_elliot=df_exploded[df_exploded['Copains']=='Elliot']
fig_occurence=px.bar(data_frame=df_elliot,x=df_elliot.index,height=120,hover_name=df_elliot.index)
fig_occurence.update_xaxes(range=[df.index.min(), date.today()],title_text='')
fig_occurence.update_yaxes(dtick=1,title_text=None, tickvals=[])
fig_occurence.update_traces(width=0.5, marker=dict(line=dict(width=1, color='black'), opacity=0.8))
fig_occurence.update_layout(margin=dict(l=0, r=0, t=0, b=0))

df_hugo=df_exploded[df_exploded['Copains']=='Hugo']
fig_occurence4=px.bar(data_frame=df_hugo,x=df_hugo.index,height=120,hover_name=df_hugo.index)
fig_occurence4.update_xaxes(range=[df.index.min(), date.today()],title_text='')
fig_occurence4.update_yaxes(dtick=1,title_text=None, tickvals=[])
fig_occurence4.update_traces(width=0.5, marker=dict(line=dict(width=1, color='black'), opacity=0.8))
fig_occurence4.update_layout(margin=dict(l=0, r=0, t=0, b=0))


df_flo=df_exploded[df_exploded['Copains']=='Flo']
fig_occurence2=px.bar(data_frame=df_flo,x=df_flo.index,height=120,hover_name=df_flo.index)
fig_occurence2.update_xaxes(range=[df.index.min(), date.today()],title_text='')
fig_occurence2.update_yaxes(dtick=1,title_text=None, tickvals=[])
fig_occurence2.update_traces(width=0.5, marker=dict(line=dict(width=1, color='black'), opacity=0.8))
fig_occurence2.update_layout(margin=dict(l=0, r=0, t=0, b=0))


fig_occurence.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig_occurence2.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig_occurence4.update_layout(margin=dict(l=0, r=0, t=0, b=0))

a,b=st.columns([1,9])
with a:
    st.image(elliot)
    st.image(flo)
    st.image(hugo)
with b:
    c,d=st.columns([7,1])
    with c:
        st.plotly_chart(fig_occurence, use_container_width=True)
        st.plotly_chart(fig_occurence2, use_container_width=True)
        st.plotly_chart(fig_occurence4, use_container_width=True)
    with d:
        st.metric("Nb jours sans se voir",(date.today()-df_elliot.index.max().date()).days)
        st.metric("Nb jours sans se voir",(date.today()-df_flo.index.max().date()).days)
        st.metric("Nb jours sans se voir",(date.today()-df_hugo.index.max().date()).days)
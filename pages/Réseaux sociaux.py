import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from datetime import timedelta

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

st.set_page_config(page_title="Réseaux sociaux",layout="wide")
df, couleur,couleur_box=load_data()
min_date = df.index.min().to_pydatetime()
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
#dfs_reseaux=dfs[dfs[['Snap','Insta']]]
## Par mois
dfs_mois=dfs.select_dtypes(include=['number']).resample('M').mean()
fig1=px.line(dfs_mois,x=dfs_mois.index,y=dfs_mois['Somme réseaux'])
tickvals = dfs_mois.index[::2]      
fig1.update_layout(xaxis=dict(
        tickmode='array',  
        tickvals=tickvals,  
        ticktext=tickvals.strftime('%b %y'),    
    ),
)


## Tous les réseaux
colors = ['#FFD700', '#800080', '#1DA1F2', '#333333']
dfs_mois_reseaux=dfs_mois[['Snap', 'Insta','Twitter','BeReal']]
fig2 = px.bar(dfs_mois_reseaux, 
              x=dfs_mois_reseaux.index, 
              y=['Snap', 'Insta','Twitter','BeReal'],
              color_discrete_sequence=colors,title="Répartition mensuelle des 3 types de journée ")
fig2.update_layout(xaxis=dict(
        tickmode='array',  
        tickvals=tickvals,  
        ticktext=tickvals.strftime('%b %y'),    
    )
)

##

fig3 = px.histogram(dfs, x="Somme réseaux", color="Catégorie note", marginal="box",
                   hover_data=df.columns,color_discrete_map=couleur)


dfs_jour_semaine=dfs.groupby('Jour semaine')[['Snap','Insta','Twitter','BeReal','Somme réseaux']].mean()
fig4= px.bar(dfs_jour_semaine, 
              x=dfs_jour_semaine.index, 
              y=['Snap', 'Insta','Twitter','BeReal'],
              color_discrete_sequence=colors,category_orders={'Jour semaine':jours_semaine_ordre})

fig_box_dodo_lisant=px.box(dfs,x='Somme réseaux lendemain',y='Dodo en lisant?',color='Dodo en lisant?',color_discrete_map=couleur_box,
                           category_orders={'Dodo en lisant veille?': ['oui', 'non']})
col1,col2=st.columns(2)
with col1:
    a,b=st.columns([10,1])
    with a:
        st.plotly_chart(fig1)
    with b:
        st.metric("Snap",int(dfs['Snap'].mean()))
        st.metric("Insta",int(dfs['Insta'].mean()))
        st.metric("Twitter",int(dfs['Twitter'].mean()))
        st.metric("BeReal",int(dfs['BeReal'].mean()))
    st.plotly_chart(fig2)
with col2:
    st.plotly_chart(fig3)
    st.plotly_chart(fig_box_dodo_lisant)
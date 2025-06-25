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
df['Catégorie note lendemain']=df['Catégorie note'].shift(-1)
df['Note lendemain']=df['Note'].shift(-1)
hier = datetime.now() - timedelta(days=1)
hier = hier.replace(hour=0, minute=0, second=0, microsecond=0) # Important que les paramètres du temps soient à 0 pour les sliders !!
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()
j_365=max_date-timedelta(days=365)

def decimal_to_time(x):
    hours = int(x)
    minutes = int((x - hours) * 60)
    return f"{hours}h{minutes:02d}"

travail=[type for type in df['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
df_entreprise=df[(df['Type'].str.contains('Stage', na=False))|(df['Type'].str.contains('Alternance', na=False))]
df_cours=df[df['Type'].str.contains('Cours', na=False)]
df_projet=df[(df['Type'].str.contains('Projet', na=False))|(df['Type'].str.contains('Mission Sciencéthic', na=False))]
df_non_travail=df[~df['Type'].isin(travail)]

## Selectbox et toggle
options = ["Tout","Entreprise","Week-end - Vacances", "Cours", "Projet/Mission Sciencéthic"]
selection = st.sidebar.selectbox(
    "Choix type de journée", options)

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

debut_date=pd.to_datetime('2024-05-02')
periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(debut_date.to_pydatetime(), max_date),
                format="YYYY-MM-DD"  
        )
        
dfs = df[(df.index >= periode[0]) & (df.index <= periode[1])]


## Réveil
df_reveil=dfs[dfs.index>='2024-05-02']

df_reveil['Minutes réveil']=df_reveil['Heure réveil'].dt.hour * 60 +df_reveil['Heure réveil'].dt.minute 
df_reveil['Heure réveil décimal']=df_reveil['Minutes réveil']/60
df_reveil['Heure dodo minutes']=df_reveil['Heure dodo'].dt.hour * 60 + df_reveil['Heure dodo'].dt.minute
df_reveil['Heure dodo minutes']=df_reveil['Heure dodo minutes'].map(lambda x:x-1440 if (x<1440) & (x>=1020) else x)
df_reveil['Heure dodo minutes veille']=df_reveil['Heure dodo minutes'].shift(1)

df_reveil['Minutes lever']=df_reveil['Heure lever'].dt.hour * 60 +df_reveil['Heure lever'].dt.minute 
df_reveil['Heure lever décimal']=df_reveil['Minutes lever']/60

def minutes_to_time(x):
    x = x % 1440  # remet l'écart dans la plage d'une journée
    hours = x // 60
    minutes = x % 60
    hours = int(hours)
    minutes = int(minutes)
    return f"{hours:02d}h{minutes:02d}"

df_dodo=dfs[dfs.index>='2023-07-22']
df_dodo['Heure dodo minutes']=df_dodo['Heure dodo'].dt.hour * 60 + df_dodo['Heure dodo'].dt.minute
df_dodo['Heure dodo minutes']=df_dodo['Heure dodo minutes'].map(lambda x:x-1440 if (x<1440) & (x>=1020) else x)
df_dodo['Heure dodo minutes veille']=df_dodo['Heure dodo minutes'].shift(1)

df_dodo['Minutes réveil']=df_dodo['Heure réveil'].dt.hour * 60 +df_dodo['Heure réveil'].dt.minute

## Durée journée

df_dodo['Durée journée']=(df_dodo['Heure dodo minutes']+1440-df_dodo['Minutes réveil'])/60
df_dodo['Durée journée en ôtant la sieste']=(df_dodo['Heure dodo minutes']+1440-df_dodo['Minutes réveil']-df_dodo['Sieste'])/60

df_reveil['Durée journée après lever']=(df_reveil['Heure dodo minutes']+1440-df_reveil['Minutes lever'])/60
df_reveil['Durée journée après lever et en ôtant sieste']=(df_reveil['Heure dodo minutes']+1440-df_reveil['Minutes lever']-df_reveil['Sieste'])/60

df_duree_journee_mois=df_reveil['Durée journée après lever et en ôtant sieste'].resample('M').mean().reset_index()
tickvals_duree_journee_mois=df_duree_journee_mois['Jour'][::2]

y_min=df_duree_journee_mois['Durée journée après lever et en ôtant sieste'].min()
y_max=df_duree_journee_mois['Durée journée après lever et en ôtant sieste'].max()

tickvals_y = [y_min + i * (y_max - y_min) / 4 for i in range(5)]
ticktext_y=[decimal_to_time(val) for val in tickvals_y]

fig_line_duree_journee_mois=px.line(data_frame=df_duree_journee_mois,x='Jour',y='Durée journée après lever et en ôtant sieste')
fig_line_duree_journee_mois.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_duree_journee_mois,
        ticktext=tickvals_duree_journee_mois.dt.strftime('%b %y'),    
        ),
    yaxis=dict(
        tickmode='array',
        tickvals=tickvals_y,
        ticktext=ticktext_y,
    ),
    title="Durée journée mensuelle"
)

fig_hist_duree_lever_sieste=px.histogram(data_frame=df_reveil,x='Durée journée après lever et en ôtant sieste',color='Catégorie note',marginal='box',color_discrete_map=couleur)



duree_journee_heures=decimal_to_time(df_dodo['Durée journée'].mean())
duree_journee_heures_sieste=decimal_to_time(df_dodo['Durée journée en ôtant la sieste'].mean())

duree_journee_heures_apres_lever=decimal_to_time(df_reveil['Durée journée après lever'].mean())
duree_journee_heures_apres_lever_sieste=decimal_to_time(df_reveil['Durée journée après lever et en ôtant sieste'].mean())


## Temps lever
df_reveil['Minutes pour se réveiller']=df_reveil['Minutes lever']-df_reveil['Minutes réveil']
fig_hist_minutes_pour_se_reveiller=px.histogram(data_frame=df_reveil,x='Minutes pour se réveiller',color='Catégorie note',color_discrete_map=couleur,marginal="box")


df_reveil_temps_lever_mensuellement=df_reveil['Minutes pour se réveiller'].resample('M').mean().reset_index()
tickvals=df_reveil_temps_lever_mensuellement['Jour'][::2]
fig_line_temps_lever_mois=px.line(data_frame=df_reveil_temps_lever_mensuellement,x='Jour',y='Minutes pour se réveiller')
fig_line_temps_lever_mois.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals,
        ticktext=tickvals.dt.strftime('%b %y'),    
        ),
        title="Temps lever mensuel"
)

a,b,c,d,e=st.columns(5)
with a:
    st.metric("Durée journée",duree_journee_heures)
with b:
    st.metric("Durée journée (sieste ôtée)",duree_journee_heures_sieste)
with c:
    st.metric("Durée journée après lever",duree_journee_heures_apres_lever)
with d:
    st.metric("Durée journée après lever (sieste ôtée)",duree_journee_heures_apres_lever_sieste)
with e:
    st.metric("Temps lever moyen",f"{int(df_reveil['Temps lever'].mean().round(0))} mn")
e,f=st.columns(2)
with e:
    st.plotly_chart(fig_line_duree_journee_mois)
    st.plotly_chart(fig_line_temps_lever_mois)
with f:
    st.plotly_chart(fig_hist_duree_lever_sieste)
    st.plotly_chart(fig_hist_minutes_pour_se_reveiller)


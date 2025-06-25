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

st.set_page_config(page_title="Lecture",layout="wide")
data=pd.read_excel("BILAN_JOURNEE_mars25.xlsx", sheet_name="Livres")
df_livres=data.copy()
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

sous_onglet = st.sidebar.radio(
    "Sous-onglets Lecture",
    options=["Statistiques globales", "Livres"],
    index=0,  # Sous-onglet par défaut
)

#dfs_livres = df_livres[(df_livres.index >= periode[0]) & (df_livres.index <= periode[1])]

if sous_onglet=='Statistiques globales':
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
    dfs_mois=dfs.select_dtypes(include=['number']).resample('M').mean()

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=dfs_mois.index,
            y=dfs_mois['Lecture'],
            mode='lines',
            name='Lecture',  
            line=dict(color='blue')  
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=dfs_mois.index,
            y=dfs_mois['Somme réseaux'],
            mode='lines',
            name='Somme réseaux',  
            line=dict(color='red')  
        )
    )
    tickvals = dfs_mois.index[::2]
    fig1.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=tickvals.strftime('%b %y'),    
        ),
        title="Comparaison mensuelle entre le temps de lecture et celui de réseaux sociaux"
    )

    fig2 = px.histogram(dfs, x="Lecture", color="Catégorie note", marginal="box",
                    hover_data=df.columns,color_discrete_map=couleur)


    fig3=px.box(dfs,x='Lecture', y='Dodo en lisant veille?',color='Dodo en lisant veille?',color_discrete_map=couleur_box,
                category_orders={'Dodo en lisant veille?': ['oui', 'non']})

    dfs_jour_semaine=dfs.groupby('Jour semaine')['Lecture'].mean()
    dfs_jour_semaine=dfs_jour_semaine.reindex(jours_semaine_ordre)
    fig_line_jour_semaine=px.line(dfs_jour_semaine,x=dfs_jour_semaine.index,y='Lecture')
    fig_line_jour_semaine.update_layout(yaxis=dict(range=[0,60]))

    ## Jour semaine box
    fig_box_lecture_semaine=px.box(dfs,x='Jour semaine',y='Lecture',color="Catégorie note",category_orders={'Jour semaine':jours_semaine_ordre},color_discrete_map=couleur)

    moyenne_30_derniers_jours=int((dfs.iloc[-30:,:]['Lecture'].mean()).round(0))
    std_30_derniers_jours=int((dfs.iloc[-30:,:]['Lecture'].std()).round(0))
    moyenne_avant_30_jours=int((dfs.iloc[-60:-30,:]['Lecture'].mean()).round(0))
    std_avant_30_jours=int((dfs.iloc[-60:-30,:]['Lecture'].std()).round(0))
    evolution_moyenne=moyenne_30_derniers_jours-moyenne_avant_30_jours
    evolution_std=std_30_derniers_jours-std_avant_30_jours

    moyenne_2023=int(df[df.index<"2024-01-01"]['Lecture'].mean().round(0))
    moyenne_2024=int(df[(df.index>="2024-01-01") & (df.index<"2025-01-01")]['Lecture'].mean().round(0))
    moyenne_2025=int(df[df.index>="2025-01-01"]['Lecture'].mean().round(0))
    a,b,c,d,e,f,g,h,i=st.columns(9)
    with a:
        st.metric("Moyenne sur la période",int(dfs['Lecture'].mean().round(0)))
    with b:
        st.metric("Ecart-type sur la période",int(dfs['Lecture'].std().round(0)))
    with d:
        st.metric("Mean 30 derniers jours",moyenne_30_derniers_jours,evolution_moyenne)
    with e:
        st.metric("Std 30 derniers jours",std_30_derniers_jours,evolution_std,delta_color="inverse")
    with g:
        st.metric("Moyenne 2023",moyenne_2023)
    with h:
        st.metric("Moyenne 2024",moyenne_2024)
    with i:
        st.metric("Moyenne 2025",moyenne_2025)
    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(fig1)
        st.plotly_chart(fig3)
        st.plotly_chart(fig_box_lecture_semaine)
    with col2:
        st.plotly_chart(fig2)
        st.plotly_chart(fig_line_jour_semaine)

    fig_line_lecture=px.line(dfs,x=dfs.index,y='Lecture')
    st.plotly_chart(fig_line_lecture)







elif sous_onglet=='Livres':
    df_livres=df_livres[~df_livres['Fin'].isna()]
    dfs_livres=df_livres[(df_livres['Début'] >= periode[0]) & (df_livres['Fin'] <= max_date)]

    dfs_livres = dfs_livres.sort_values(by="Début", ascending=False)
    dfs_livres["Nom"] = dfs_livres["Nom"].astype(str)
    fig = px.timeline(
        dfs_livres,
        x_start="Début",
        x_end="Fin",
        y="Nom",  
        title="Frise chronologique des films",
        height=700
    )
    genre_colors = {
        "Politique": "royalblue",
        "Roman": "#FFD1DC",
        "Histoire":"orange",
        "Société":"#87CEEB",
        "Politique/Histoire":"mediumpurple",
        "Santé":"#77DD77",
        "Ecologie":"green",
        "Dév perso":"yellow",
        "Philosophie":"salmon",
        "Nouvelles":"#FFB6C1"
    }
    fig.update_traces(marker=dict(color=[genre_colors.get(g, "gray") for g in dfs_livres["Genre"]]))
    legend_trace = []
    for genre, color in genre_colors.items():
        legend_trace.append(
            dict(
                name=genre,
                marker=dict(color=color),
                mode="markers",
                type="scatter",
                x=[None],  # Permet d'afficher la légende sans point visible
                y=[None],
            )
        )
    fig.update_layout(legend=dict(font=dict(size=14)))
    fig.add_traces(legend_trace)

    st.plotly_chart(fig)

    
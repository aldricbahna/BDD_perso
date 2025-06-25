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

sous_onglet = st.sidebar.radio(
    "Sous-onglets",
    options=["Dodo sans tel","Dodo en lisant"],
    index=0,  # Sous-onglet par défaut
)


if sous_onglet=="Dodo sans tel":
    dft=df[~df['Dodo sans tel'].isna()]
    periode_tel = st.sidebar.slider(
                "Période:",
                min_value=dft.index.min().to_pydatetime(),
                max_value=dft.index.max().to_pydatetime(),
                value=(dft.index.min().to_pydatetime(), dft.index.max().to_pydatetime()),
                format="YYYY-MM-DD"  
        )
    dfs = dft[(dft.index >= periode_tel[0]) & (dft.index <= periode_tel[1])]

    fig_barre_tel = go.Figure()
    fig_barre_tel.add_trace(go.Bar(
        x=dfs.index,
        y=dfs['Dodo sans tel'],
        name="Dodo sans tel"
    ))

    st.plotly_chart(fig_barre_tel)
    fig_pie_tel=px.pie(dfs,names='Dodo sans tel?',title='Dodo sans tel ?',
                       color='Dodo sans tel?',
                       color_discrete_map=couleur_box,
                       category_orders={'Dodo sans tel?': ['oui', 'non']})
    st.plotly_chart(fig_pie_tel)

    fig_tel_box=px.box(dfs,x='Note', y='Dodo sans tel veille?',color='Dodo sans tel veille?',color_discrete_map=couleur_box,
            category_orders={'Dodo sans tel veille?': ['oui', 'non']})
    st.plotly_chart(fig_tel_box)

else:
    options = ["Global", "Mensuellement", "Jour semaine", "Eugé"]
    selection_dashboard = st.pills("Dashboard", options)
    dfl=df[(df.index>"2024-01-06") & (df.index<=hier)]

    periode_lisant = st.sidebar.slider(
                "Période:",
                min_value=pd.to_datetime("2024-01-06").to_pydatetime(),
                max_value=hier,
                value=(pd.to_datetime("2024-01-06").to_pydatetime(), hier),
                format="YYYY-MM-DD"  
        )
    dfs = dfl[(dfl.index >= periode_lisant[0]) & (dfl.index <= periode_lisant[1])]

    travail=[type for type in dfs['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
    dfs_entreprise=dfs[(dfs['Type'].str.contains('Stage', na=False))|(dfs['Type'].str.contains('Alternance', na=False))]
    dfs_cours=dfs[dfs['Type'].str.contains('Cours', na=False)]
    dfs_projet=dfs[(dfs['Type'].str.contains('Projet', na=False))|(dfs['Type'].str.contains('Mission Sciencéthic', na=False))]
    dfs_non_travail=dfs[~dfs['Type'].isin(travail)]

    my_dict={"Entreprise":dfs_entreprise,
      "Projet/Mission Sciencéthic":dfs_projet,
      "Cours":dfs_cours,
      "Week-end - Vacances":dfs_non_travail,
      "Tout":dfs}

    options = ["Tout","Entreprise","Week-end - Vacances", "Cours", "Projet/Mission Sciencéthic"]
    selection = st.sidebar.selectbox(
    "Choix type de journée", options)

    df_selection=my_dict[selection]

    if selection_dashboard=='Global':

        fig_barre_lis = go.Figure()
        fig_barre_lis.add_trace(go.Bar(
            x=df_selection.index,
            y=df_selection['Dodo en lisant'],
            name="Dodo en lisant",
        ))

        st.plotly_chart(fig_barre_lis, use_container_width=True, height=50)
        
        fig_lis_pie=px.pie(df_selection,names='Dodo en lisant?',title='Dodo en lisant ?',
                        color='Dodo en lisant?',
                        color_discrete_map=couleur_box,
                        category_orders={'Dodo en lisant?': ['oui', 'non']})
        
        fig_lis_box=px.box(dfs,x='Note', y='Dodo en lisant veille?',color='Dodo en lisant veille?',color_discrete_map=couleur_box,
                category_orders={'Dodo en lisant veille?': ['oui', 'non']})

        a,b=st.columns(2)
        with a:
            st.plotly_chart(fig_lis_pie)
        with b:
            st.plotly_chart(fig_lis_box)

        dates=dfs.index.tolist()
        '''serie_max=0
        for date in dates:
            nombre=df.loc[date,'Dodo en lisant']
            if nombre==1:
                serie_cours=0
                serie_cours+=1
            else:'''
        
    elif selection_dashboard=='Mensuellement':
        df_selection_mensuellement=df_selection['Dodo en lisant'].resample('M').mean().reset_index()
        df_selection_mensuellement['Dodo en lisant']=df_selection_mensuellement['Dodo en lisant']*100
        tickvals = df_selection_mensuellement['Jour'][::2]
        fig_line_dodo_lisant_mois=px.line(data_frame=df_selection_mensuellement,x='Jour',y='Dodo en lisant')
        fig_line_dodo_lisant_mois.update_layout(
        xaxis=dict(
        tickmode='array',
        tickvals=tickvals,
        ticktext=tickvals.dt.strftime('%b %y'),    
        ),
        title="Taux de dodo en lisant (%)"
        )
        fig_line_dodo_lisant_mois.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_line_dodo_lisant_mois)
    elif selection_dashboard=='Jour semaine':
        df_selection_jour_semaine=df_selection.groupby('Jour semaine')['Dodo en lisant'].mean()
        df_selection_jour_semaine=df_selection_jour_semaine*100
        df_selection_jour_semaine=df_selection_jour_semaine.reindex(jours_semaine_ordre)
        fig_line_dodo_lisant_jour_semaine=px.line(data_frame=df_selection_jour_semaine,x=df_selection_jour_semaine.index,y='Dodo en lisant')
        fig_line_dodo_lisant_jour_semaine.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_line_dodo_lisant_jour_semaine)
    else:
        st.write(2)
    



        



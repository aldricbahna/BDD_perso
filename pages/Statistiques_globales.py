import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

from auth import check_password
check_password()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
dict_mois={'Janvier':1,
               'Février':2,
               'Mars':3,
               'Avril':4,
               'Mai':5,
               'Juin':6,
               'Jullet':7,
               'Août':8,
               'Septembre':9,
               'Octobre':10,
               'Novembre':11,
               'Décembre':12}

dict_mois_chiffre_lettre={1:'Janvier',
               2:'Février',
               3:'Mars',
               4:'Avril',
               5:'Mai',
               6:'Juin',
               7:'Jullet',
               8:'Août',
               9:'Septembre',
               10:'Octobre',
               11:'Novembre',
               12:'Décembre'}

st.set_page_config(page_title="Statistiques globales",layout="wide")
df,couleur,couleur_box=load_data()

def minutes_to_hours(x):
    hours = int(x//60)
    minutes = round(x%60)
    return f"{hours}h{minutes:02d}"

df['Mois lettre']=df['Mois'].map(dict_mois_chiffre_lettre)
min_date=df.index.min()
max_date=df.index.max()

travail=[type for type in df['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
df_entreprise=df[(df['Type'].str.contains('Stage', na=False))|(df['Type'].str.contains('Alternance', na=False))]
df_cours=df[df['Type'].str.contains('Cours', na=False)]
df_projet=df[(df['Type'].str.contains('Projet', na=False))|(df['Type'].str.contains('Mission Sciencéthic', na=False))]
df_non_travail=df[~df['Type'].isin(travail)]


sous_onglet = st.sidebar.radio(
    "Sous-onglets Commandes",
    options=["Vue globale", "Comparaison années", "Semaine, mois","Mois", "Mois actuel"],
    index=0,  # Sous-onglet par défaut
)

if sous_onglet == "Vue globale":
    min_date = df.index.min().to_pydatetime()
    max_date = df.index.max().to_pydatetime()


    periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY-MM-DD"  
        )
        
    df_filtre = df[(df.index >= periode[0]) & (df.index <= periode[1])]
    travail=[type for type in df_filtre['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
    df_entreprise=df_filtre[(df_filtre['Type'].str.contains('Stage', na=False))|(df_filtre['Type'].str.contains('Alternance', na=False))]
    df_cours=df_filtre[df_filtre['Type'].str.contains('Cours', na=False)]
    df_projet=df_filtre[(df_filtre['Type'].str.contains('Projet', na=False))|(df_filtre['Type'].str.contains('Mission Sciencéthic', na=False))]
    df_non_travail=df_filtre[~df_filtre['Type'].isin(travail)]
    df_travail=df_filtre[df_filtre['Type'].isin(travail)]


    fig1=px.histogram(data_frame=df_filtre, x='Note',nbins=100,title='Distribution des notes journalières',range_x=[0,10])
    fig1.update_layout(
    xaxis=dict(
        tickmode='linear',  
        tick0=0,            
        dtick=1             
    )
    )


## Par mois
    df_filtre_mois=df_filtre.select_dtypes(include=['number']).resample('M').mean()
    tickvals = df_filtre_mois.index[::2]      
    fig2=px.line(data_frame=df_filtre_mois,x=df_filtre_mois.index,y=df_filtre_mois['Note'],title="Moyenne mensuelle des notes")
    fig2.update_layout(xaxis=dict(
            tickmode='array',  
            tickvals=tickvals,  
            ticktext=tickvals.strftime('%b %y'),    
        ),
    )



### 3 catégories

    df_bien=df_filtre[df_filtre['Note']>=7]
    df_bien_mois=df_bien.resample('M').size()
    df_bien_mois.index = df_bien_mois.index.strftime('%b %Y')
    df_bien_mois=pd.DataFrame(data=df_bien_mois,index=df_bien_mois.index,columns=['Bien (7-10)'])

    df_correct=df_filtre[(df_filtre['Note']<7) & (df_filtre['Note']>=6)]
    df_correct_mois=df_correct.resample('M').size()
    df_correct_mois.index = df_correct_mois.index.strftime('%b %Y')
    df_correct_mois=pd.DataFrame(data=df_correct_mois,index=df_correct_mois.index,columns=['Correct (6-6,5)'])

    df_mauvais=df_filtre[df_filtre['Note']<6]
    df_mauvais_mois=df_mauvais.resample('M').size()
    df_mauvais_mois.index = df_mauvais_mois.index.strftime('%b %Y')
    df_mauvais_mois=pd.DataFrame(data=df_mauvais_mois,index=df_mauvais_mois.index,columns=['Mauvais (0-5,5)'])

    shape1 = df_bien.shape[0]  
    shape2 = df_correct.shape[0]  
    shape3 = df_mauvais.shape[0]  

    sizes = [shape1, shape2, shape3]
    labels = ["Bien (7-10)", "Correct (6-6,5)", "Mauvais (0-5,5)"]
    colors=['#66CDAA', '#FFD700', '#FF7F7F']
    fig3 = px.pie(
    names=labels, 
    values=sizes, 
    color_discrete_sequence=colors,
    )
    fig3.update_traces(textfont_size=20)
    fig3.update_layout(legend=dict(font=dict(size=16)))

    df_bien_mois.index=pd.DatetimeIndex(df_bien_mois.index)
    df_correct_mois.index=pd.DatetimeIndex(df_correct_mois.index)
    df_mauvais_mois.index=pd.DatetimeIndex(df_mauvais_mois.index)
    df_categories_note=pd.merge(df_bien_mois,df_correct_mois,how='outer', left_index=True, right_index=True)
    df_categories_note=pd.merge(df_categories_note,df_mauvais_mois,how='outer', left_index=True, right_index=True)
    jours_dans_mois = df_categories_note.index.to_period('M').days_in_month
    df_categories_note_pourcentage = df_categories_note.div(jours_dans_mois, axis=0).mul(100).round(2)
    df_categories_note_pourcentage.index=df_categories_note_pourcentage.index.strftime('%b %Y')


    fig4 = px.bar(df_categories_note_pourcentage, 
              x=df_categories_note_pourcentage.index, 
              y=["Bien (7-10)", "Correct (6-6,5)", "Mauvais (0-5,5)"],
              color_discrete_sequence=colors,title="Répartition mensuelle des 3 types de journée ")
    fig4.update_layout(showlegend=False)

    col1, col2=st.columns(2)
    with col1:
        a,b=st.columns([4,1])
        with a:
            st.plotly_chart(fig1)
        with b:
            st.metric("Moyenne note",df_filtre['Note'].mean().round(2))
            st.metric("Ecart-type",df_filtre['Note'].std().round(2))
    with col2:
        st.plotly_chart(fig2)


    col01,col02=st.columns([2,5])
    with col01:
        st.plotly_chart(fig3)
    with col02:
        st.plotly_chart(fig4)

    df_non_travail_mois=df_non_travail['Note'].resample('M').mean().reset_index()
    df_travail_mois=df_travail['Note'].resample('M').mean().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_non_travail_mois['Jour'],
        y=df_non_travail_mois['Note'],
        mode='lines',
        name='Week-end, vacances...',
        line=dict(color='blue')
    ))

    # Ajouter la ligne pour les jours travaillés
    fig.add_trace(go.Scatter(
        x=df_travail_mois['Jour'],
        y=df_travail_mois['Note'],
        mode='lines',
        name='Travail',
        line=dict(color='orange')
    ))

    # Personnaliser les ticks de l'axe x
    fig.update_layout(
        title="Moyenne mensuelle des notes",
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=tickvals.strftime('%b %y')
        ),
        yaxis_title='Note',
        legend_title="Type de jour"
    )
    st.plotly_chart(fig)

elif sous_onglet=="Comparaison années":
    df_2023=df[df.index<='2023-12-31']
    df_2024=df[(df.index>'2023-12-31')&(df.index<='2024-12-31')]
    df_2025=df[(df.index>'2024-12-31')&(df.index<='2025-12-31')]
    options=st.multiselect(
        'Choisis 2 années',
        [2023,2024,2025],
        [2023,2024]
    )

    st.dataframe(df_2023)
    annee1, annee2=st.columns(2)


    
elif sous_onglet == "Semaine, mois":
    st.dataframe(df)
    df_numero_jour=df.groupby('Numéro jour').agg(
        Note_moyenne=('Note','mean'),
        Note_std=('Note','std')
    ).reset_index()

    df_jour_semaine=df.groupby('Jour semaine').agg(
        Note_moyenne=('Note','mean'),
        Note_std=('Note','std')
    )

    df_numero_semaine=df.groupby('Numéro semaine').agg(
        Note_moyenne=('Note','mean'),
        Note_std=('Note','std')
    )

    fig_line_numero_jour=px.line(data_frame=df_numero_jour,x='Numéro jour',y='Note_moyenne',
                                 hover_data={"Note_moyenne": ":.2f", "Note_std": ":.2f"})

    fig_line_numero_jour.add_scatter(
    x=df_numero_jour['Numéro jour'],
    y=df_numero_jour['Note_moyenne'] + df_numero_jour['Note_std'],
    mode='lines',
    line=dict(width=0),
    showlegend=False
    )

    fig_line_numero_jour.add_scatter(
        x=df_numero_jour['Numéro jour'],
        y=df_numero_jour['Note_moyenne'] - df_numero_jour['Note_std'],
        mode='lines',
        fill='tonexty',
        line=dict(width=0),
        fillcolor='rgba(0,176,246,0.2)',
        showlegend=False
    )
    st.plotly_chart(fig_line_numero_jour)

    df_jour_semaine=df_jour_semaine.reindex(jours_semaine_ordre)
    fig_line_jour_semaine=px.line(data_frame=df_jour_semaine,x=df_jour_semaine.index,y='Note_moyenne')
    st.plotly_chart(fig_line_jour_semaine)

    
    fig_line_numero_semaine=px.line(data_frame=df_numero_semaine,x=df_numero_semaine.index,y='Note_moyenne',hover_data={"Note_moyenne": ":.2f", "Note_std": ":.2f"})
    st.plotly_chart(fig_line_numero_semaine)

    df_historique_mois=df.groupby('Mois lettre')['Note'].mean().reset_index()


    mois_ordre = list(dict_mois_chiffre_lettre.values()) 
    df["Mois lettre"] = pd.Categorical(df["Mois lettre"], categories=mois_ordre, ordered=True)


    df_historique_mois=df.groupby('Mois lettre')['Note'].mean().reset_index()
    fig_line_historique_mois=px.line(df_historique_mois,x='Mois lettre',y='Note')
    st.plotly_chart(fig_line_historique_mois)

elif sous_onglet=="Mois":
    choix_annee = st.radio(
    "Chosir une année",
    options=["2023", "2024", "2025"],
    index=2,  # Sous-onglet par défaut
)
    choix_mois_litteral=st.selectbox("Chosir un mois",options=dict_mois.keys())
    choix_moix=dict_mois[choix_mois_litteral]
    dfs=df[(df['Année']==int(choix_annee)) & (df['Mois']==int(choix_moix))]

    travail=[type for type in dfs['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
    df_entreprise=dfs[(dfs['Type'].str.contains('Stage', na=False))|(dfs['Type'].str.contains('Alternance', na=False))]
    df_cours=dfs[dfs['Type'].str.contains('Cours', na=False)]
    df_projet=dfs[(dfs['Type'].str.contains('Projet', na=False))|(dfs['Type'].str.contains('Mission Sciencéthic', na=False))]
    df_non_travail=dfs[~dfs['Type'].isin(travail)]
    dfs_travail=dfs[dfs['Type'].isin(travail)]

    fig_hist_mois=px.bar(dfs,x='Numéro jour',y='Note',color_discrete_sequence=['#FF69B4'])
    fig_hist_mois.update_yaxes(range=[0,10])
    fig_hist_mois.add_hline(y=df['Note'].mean(), line_dash="dash", line_color="black")
    st.plotly_chart(fig_hist_mois)

    st.dataframe(dfs)
    st.metric("Moyenne lecture",int(dfs['Lecture'].mean().round()))
    st.metric("Somme réseaux",int(dfs['Somme réseaux'].mean().round()))
    st.metric("Météo",dfs['Météo num'].mean().round(1))
    st.metric("Footing",f"{dfs['Footing'].sum().round(1)} km")

    st.metric("Moyenne note",dfs['Note'].mean().round(2))
    st.metric("Ecart-type",dfs['Note'].std().round(2))

    travail=[type for type in dfs['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
    df_entreprise=dfs[(dfs['Type'].str.contains('Stage', na=False))|(dfs['Type'].str.contains('Alternance', na=False))]
    df_cours=dfs[dfs['Type'].str.contains('Cours', na=False)]
    df_projet=dfs[(dfs['Type'].str.contains('Projet', na=False))|(dfs['Type'].str.contains('Mission Sciencéthic', na=False))]
    df_non_travail=dfs[~dfs['Type'].isin(travail)]

    st.metric("Moyenne week-ends",df_non_travail['Note'].mean().round(2))
    st.metric("Moyenne entreprise",df_entreprise['Note'].mean().round(2))

    st.metric("Moyenne temps perdu",minutes_to_hours(dfs['Temps perdu'].mean()))

    st.metric("Travail moyen (tout jour)", minutes_to_hours(dfs['Travail'].mean()))
    st.metric("Travail moyen", minutes_to_hours(dfs_travail['Travail'].mean()))

    #cols_presques_binaires=['Activité','Transport','Match de sport']
    colonne_debut=dfs.columns.get_loc('Parents')
    colonne_fin=dfs.columns.get_loc('Dodo sans tel')
    cols_binaires=dfs.columns[colonne_debut:colonne_fin+1].tolist()
    cols_binaires.remove('Match de sport')
    st.write(cols_binaires)

    moyennes={}
    for col in cols_binaires:
        moyenne = dfs[col].mean()

        # Créer un nom de variable dynamique et stocker la moyenne dans le dictionnaire
        nom_variable = f"{col} moyenne"
        moyennes[nom_variable] = moyenne
    st.write(moyennes)
    dfs_cols_binaires = pd.DataFrame(moyennes.values(), index=moyennes.keys(), columns=["Moyenne"])
    st.dataframe(dfs_cols_binaires)

    #st.bar_chart(data=dfs_cols_binaires,x=dfs_cols_binaires.index,y='Moyenne')
    fig_bar_cols_binaires=px.bar(data_frame=dfs_cols_binaires,x=dfs_cols_binaires.index,y='Moyenne')
    st.plotly_chart(fig_bar_cols_binaires)
    

elif sous_onglet=="Mois actuel":
    maintenant = datetime.now()
    #maintenant=datetime(year=2024, month=8, day=15)
    mois_actuel = maintenant.month
    annee_actuelle = maintenant.year

    if mois_actuel>1:
        mois_precedent=mois_actuel-1
        annee_mois_precedent=annee_actuelle
    else:
        mois_precedent=12 
        annee_mois_precedent=annee_actuelle-1
    
    dfs=df[(df['Année']==annee_actuelle) & (df['Mois']==mois_actuel)]
    travail=[type for type in dfs['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
    df_entreprise=dfs[(dfs['Type'].str.contains('Stage', na=False))|(dfs['Type'].str.contains('Alternance', na=False))]
    df_cours=dfs[dfs['Type'].str.contains('Cours', na=False)]
    df_projet=dfs[(dfs['Type'].str.contains('Projet', na=False))|(dfs['Type'].str.contains('Mission Sciencéthic', na=False))]
    df_non_travail=dfs[~dfs['Type'].isin(travail)]

    df_mois_precedent=df[(df['Année']==annee_mois_precedent) & (df['Mois']==mois_precedent)]

    fig_hist_notes=px.histogram(data_frame=dfs, x='Note',nbins=100,title='Distribution des notes journalières',range_x=[0,10])
    fig_hist_notes.update_layout(
    xaxis=dict(
        tickmode='linear',  
        tick0=0,            
        dtick=1             
    ))


    st.plotly_chart(fig_hist_notes)

    dfs_type=dfs.groupby('Type').count()
    fig_pie=px.pie(dfs_type,names=dfs_type.index,values='Note')
    fig_pie.update_layout(legend=dict(font=dict(size=16)))
    st.plotly_chart(fig_pie)

    ecart_note=(dfs['Note'].mean()-df_mois_precedent['Note'].mean()).round(2)
    ecart_std=(dfs['Note'].std()-df_mois_precedent['Note'].std()).round(2)
    ecart_lecture=int((dfs['Lecture'].mean()-df_mois_precedent['Lecture'].mean()).round(0))
    ecart_reseaux=int((dfs['Somme réseaux'].mean()-df_mois_precedent['Somme réseaux'].mean()).round(0))
    ecart_meteo=(dfs['Météo num'].mean()-df_mois_precedent['Météo num'].mean()).round(1)
    ecart_footing=(dfs['Footing'].sum()-df_mois_precedent['Footing'].sum()).round(1)
    ecart_sport=int(dfs['Sport'].sum()-df_mois_precedent['Sport'].sum())
    

    st.metric("Moyenne note",dfs['Note'].mean().round(2),ecart_note)
    st.metric("Ecart-type",dfs['Note'].std().round(2),ecart_std,delta_color='inverse')

    st.metric("Moyenne week-ends",df_non_travail['Note'].mean())
    st.metric("Moyenne entreprise",df_entreprise['Note'].mean())

    
    fig_hist_mois=px.bar(dfs,x='Numéro jour',y='Note',color_discrete_sequence=['#FF69B4'])
    fig_hist_mois.update_yaxes(range=[0,10])
    fig_hist_mois.add_hline(y=df['Note'].mean(), line_dash="dash", line_color="black")
    st.plotly_chart(fig_hist_mois)

    st.dataframe(dfs)
    st.metric("Moyenne lecture",int(dfs['Lecture'].mean().round()),ecart_lecture)
    st.metric("Somme réseaux",int(dfs['Somme réseaux'].mean().round()),ecart_reseaux,delta_color='inverse')
    st.metric("Météo",dfs['Météo num'].mean().round(1),ecart_meteo)
    st.metric("Footing",f"{dfs['Footing'].sum().round(1)} km",ecart_footing)
    st.metric("Nb séances sport",int(dfs['Sport'].sum()),ecart_sport)



  
    choix_annee = st.radio(
    "Chosir une année",
    options=["2023", "2024", "2025"],
    index=2,  # Sous-onglet par défaut
)
    
    
































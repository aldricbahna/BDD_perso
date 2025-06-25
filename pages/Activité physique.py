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
max_date = df.index.max().to_pydatetime()- timedelta(days=1)
j_365=max_date-timedelta(days=365)


periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY-MM-DD"  
        )
dfs = df[(df.index >= periode[0]) & (df.index <= periode[1])]        

## Footing
df_footing=dfs[dfs['Footing']>0]
df_foot=dfs[dfs['Sport']=='Foot']
fig_hist_footing=px.histogram(df_footing,x='Footing',color='Catégorie note',marginal='box',color_discrete_map=couleur)


df_footing_mois=dfs['Footing'].resample('M').sum().reset_index()
tickvals_footing_mois=df_footing_mois['Jour'][::2]

## Sport
dfs['Sport']=dfs['Sport'].map(lambda x:0 if x==0 else 1)
dfs_sport_mois=dfs['Sport'].resample('M').mean().reset_index()
dfs_sport_mois['Sport']=(dfs_sport_mois['Sport']*100).round(1)


moyenne_activite_physique=(dfs['Sport'].mean()*100).round(1)


nb_jours_footing=dfs[dfs['Footing']>0].shape[0]
ratio_footing=nb_jours_footing/dfs.shape[0]*100



fig = go.Figure()

# Ajouter la trace pour Footing
fig.add_trace(
    go.Scatter(
        x=df_footing_mois['Jour'],
        y=df_footing_mois['Footing'],
        name='Footing',
        mode='lines',
        yaxis='y1',
        line=dict(color='orange')
    )
)

# Ajouter la trace pour Sport
fig.add_trace(
    go.Scatter(
        x=dfs_sport_mois['Jour'],
        y=dfs_sport_mois['Sport'],
        name='Sport',
        mode='lines',
        yaxis='y2',
        line=dict(color='blue')
    )
)

# Mettre à jour la mise en page pour inclure l'axe Y secondaire
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_footing_mois,
        ticktext=tickvals_footing_mois.dt.strftime('%b %y')
    ),
    yaxis=dict(
        title='Nombre de kms mensuels (Footing)',
        side='left',
        range=[0,180]
    ),
    yaxis2=dict(
        title='Sport (%)',
        side='right',
        overlaying='y',
        showgrid=False
    ),
    title="Activité physique mensuelle"
)

#fig4=px.box(dfs,x='Note', y='Sport?',color='Sport?',color_discrete_map=couleur_box,
            #category_orders={'Sport?': ['oui', 'non']})
#st.plotly_chart(fig4)

#fig5=px.box(dfs,x='Note lendemain', y='Sport?',color='Sport?',color_discrete_map=couleur_box,
            #category_orders={'Sport?': ['oui', 'non']})
#st.plotly_chart(fig5)


fig_hist_pas=px.histogram(dfs,x='Nombre de pas',color='Catégorie note',marginal='box',color_discrete_map=couleur,title="Répartition des nombre de pas")



dfs_sans_sport=dfs[dfs['Sport']==0]
dfs_sport=dfs[dfs['Sport']==1]

## Retrancher le nombre de pas

dfs['Nb pas sport'] = (dfs['Footing'] * 1000 / dfs['Longueur foulée']).where(dfs['Footing'] > 0, None)
dfs.loc[dfs['Sport'] == 'Foot', 'Nb pas sport'] = 6300
dfs.loc[dfs.index=='2024-10-09', 'Nb pas sport']=3000
dfs.loc[dfs.index=='2024-10-23', 'Nb pas sport']=3000
dfs.loc[dfs.index=='2025-01-29', 'Nb pas sport']=3000


dfs['Nb pas en enlevant le sport']=dfs['Nombre de pas']-dfs['Nb pas sport']



fig_hist_pas_en_enlevant_sport=px.histogram(dfs,x='Nb pas en enlevant le sport',color='Catégorie note',marginal='box',color_discrete_map=couleur,
                                            title='Nombre de pas en enlevant les pas du sport')


## Heure footing
def decimal_to_time(x):
    if isinstance(x, (int, float)) and np.isnan(x): 
        return None  
    hours = int(x)
    minutes = int((x - hours) * 60)
    return f"{hours}h{minutes:02d}"

dfs['Heure footing minutes']=dfs['Heure footing'].dt.hour * 60 +dfs['Heure footing'].dt.minute 
dfs['Heure footing décimal']=dfs['Heure footing minutes']/60

fig_hist_heure_footing=px.histogram(data_frame=dfs,x='Heure footing décimal',color="Catégorie note", 
                           marginal="box",
                            color_discrete_map=couleur)
y_min = dfs['Heure footing décimal'].min()
y_max = dfs['Heure footing décimal'].max()

tickvals_x = [y_min + i * (y_max - y_min) / 8 for i in range(9)]
ticktext_x=[decimal_to_time(val) for val in tickvals_x]
fig_hist_heure_footing.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_x,
        ticktext=ticktext_x,    
    ),
    title="Distribution des heures de footing"
)



#st.metric("Niveau de forme",f"{dfs['Forme'].mean():.1f}")

#fig_box_sport_forme=px.box(dfs,x='Forme',y='Sport?')
#st.plotly_chart(fig_box_sport_forme)

#fig_box_sport_forme=px.box(dfs,x='Forme lendemain',y='Sport?')
#st.plotly_chart(fig_box_sport_forme)

#st.metric("Forme avec sport :", dfs_sport['Forme'].mean())
#st.metric("Forme sans sport :", dfs_sans_sport['Forme'].mean())

#st.metric("Forme lendemain avec sport :", dfs_sport['Forme lendemain'].mean())
#st.metric("Forme lendemain sans sport :", dfs_sans_sport['Forme lendemain'].mean())


a0,b0,c0,d0,g0,h0=st.columns(6)
with a0:
    st.metric("Ratio d'activité physique",f"{moyenne_activite_physique} %")
with b0:
    st.metric("Ratio de footing",f"{ratio_footing:.1f} %")
with g0:
    st.metric("Nb de pas moyen (depuis fin juin 24)", int(dfs['Nombre de pas'].mean()))
with h0:
    st.metric("Sans sport (depuis fin juin 24)", int(dfs['Nb pas en enlevant le sport'].mean()))


a,b=st.columns(2)
with a:
    st.plotly_chart(fig)
    st.plotly_chart(fig_hist_heure_footing)
with b:
    st.plotly_chart(fig_hist_pas)
    st.plotly_chart(fig_hist_pas_en_enlevant_sport)




fig_box_vfc_sport=px.box(dfs,x='VFC',y='Sport?')
st.plotly_chart(fig_box_vfc_sport)

fig_box_bpm_sport=px.box(dfs,x='BPM max',y='Sport?')
st.plotly_chart(fig_box_bpm_sport)
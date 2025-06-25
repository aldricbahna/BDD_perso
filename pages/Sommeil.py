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


travail=[type for type in df['Type'].unique() if type not in ['Week-end','Vacances','Malade']]
df_entreprise=df[(df['Type'].str.contains('Stage', na=False))|(df['Type'].str.contains('Alternance', na=False))]
df_cours=df[df['Type'].str.contains('Cours', na=False)]
df_projet=df[(df['Type'].str.contains('Projet', na=False))|(df['Type'].str.contains('Mission Sciencéthic', na=False))]
df_non_travail=df[~df['Type'].isin(travail)]

## Selectbox et toggle

periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(j_365, max_date),
                format="YYYY-MM-DD"  
        )

options = ["Tout","Entreprise", "Projet/Mission Sciencéthic", "Cours", "Week-end - Vacances"]
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
        
dfs = df[(df.index >= periode[0]) & (df.index <= periode[1])]






## Réveil
df_reveil=dfs[dfs.index>='2024-05-02']
df_reveil['Minutes réveil']=df_reveil['Heure réveil'].dt.hour * 60 +df_reveil['Heure réveil'].dt.minute 
df_reveil['Heure réveil décimal']=df_reveil['Minutes réveil']/60
df_reveil['Heure dodo minutes']=df_reveil['Heure dodo'].dt.hour * 60 + df_reveil['Heure dodo'].dt.minute
df_reveil['Heure dodo minutes']=df_reveil['Heure dodo minutes'].map(lambda x:x-1440 if (x<1440) & (x>=1020) else x)
df_reveil['Heure dodo minutes veille']=df_reveil['Heure dodo minutes'].shift(1)

moyenne_heure_str = (datetime(1900, 1, 1) + timedelta(minutes=df_reveil['Minutes réveil'].mean())).strftime('%H:%M')

## Lever
df_reveil['Minutes lever']=df_reveil['Heure lever'].dt.hour * 60 +df_reveil['Heure lever'].dt.minute 
df_reveil['Heure lever décimal']=df_reveil['Minutes lever']/60

moyenne_lever_str = (datetime(1900, 1, 1) + timedelta(minutes=df_reveil['Minutes lever'].mean())).strftime('%H:%M')

fig_line_lever=px.line(df_reveil['Heure lever décimal'].resample('M').mean())
fig_line_reveil= px.line(df_reveil['Heure réveil décimal'].resample('M').mean())
fig_line_reveil.data[0].name = 'Heure réveil'

fig_line_reveil.add_trace(
    go.Scatter(
        x=fig_line_lever.data[0].x,
        y=fig_line_lever.data[0].y,
        mode='lines',
        name='Heure lever',
        line=dict(color='orange')  # Définissez la couleur à orange
    )
)

def decimal_to_time(x):
    if isinstance(x, (int, float)) and np.isnan(x): 
        return None  
    hours = int(x)
    minutes = int((x - hours) * 60)
    return f"{hours}h{minutes:02d}"

y_min = df_reveil['Heure réveil décimal'].resample('M').mean().min()
y_max = df_reveil['Heure lever décimal'].resample('M').mean().max()

# Génération des valeurs pour l'axe Y
tickvals_x = df_reveil['Heure réveil décimal'].resample('M').mean().index[::2]
tickvals = [y_min + i * (y_max - y_min) / 4 for i in range(5)]
ticktext = [decimal_to_time(val) for val in tickvals]

fig_line_reveil.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        tickfont=dict(size=14)
    ),
    xaxis=dict(
        tickvals=tickvals_x,
        ticktext=tickvals_x.strftime('%b %y'),
        tickfont=dict(size=14)  
    ),
    title="Heures de réveil et lever mensuels",
    showlegend=False
)


## Dodo
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
moyenne_dodo_minutes=df_dodo['Heure dodo minutes'].mean()
moyenne_heure_dodo_str = (datetime(1900, 1, 1) + timedelta(minutes=moyenne_dodo_minutes)).strftime('%H:%M')

df_dodo_mensuel=df_dodo['Heure dodo minutes'].resample('M').mean()
fig_line_dodo_mensuel=px.line(df_dodo_mensuel)
tickvals_x = df_dodo_mensuel.index[::2]

y_min = df_dodo['Heure dodo minutes'].resample('M').mean().min()
y_max = df_dodo['Heure dodo minutes'].resample('M').mean().max()

tickvals_y = [y_min + i * (y_max - y_min) / 4 for i in range(5)]
ticktext=[minutes_to_time(val) for val in tickvals_y]

fig_line_dodo_mensuel.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_x,
        ticktext=tickvals_x.strftime('%b %y'),    
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=tickvals_y,
        ticktext=ticktext,
    ),
    title="Heure de coucher moyen",
    showlegend=False
)


df_reveil_jour_semaine=df_reveil.groupby('Jour semaine')[['Heure réveil décimal','Heure lever décimal']].mean().reset_index()

#df_reveil_jour_semaine=dfs[['Heure réveil','Heure lever','Heure dodo']].groupby('Jour semaine').mean()
#fig_hist_jour_semaine=px.line(data_frame=df_reveil_jour_semaine,x='Jour semaine',y='Heure réveil décimal')
#st.plotly_chart(fig_hist_jour_semaine)

## Temps sommeil

df_dodo['Minutes réveil']=df_dodo['Heure réveil'].dt.hour * 60 +df_dodo['Heure réveil'].dt.minute
df_dodo['Temps sommeil théorique']=(df_dodo['Minutes réveil']-df_dodo['Heure dodo minutes veille'])/60
df_dodo['Temps sommeil théorique veille']=df_dodo['Temps sommeil théorique'].shift(1)
df_dodo['Total sommeil montre']=(df_dodo['Sommeil profond']+df_dodo['Sommeil léger']+df_dodo['Sommeil paradoxal'])/60 #Attention !!
df_dodo_mois=df_dodo.resample('M')[['Temps sommeil théorique','Total sommeil montre']].mean()


fig_line_sommeil_2_courbes = go.Figure()
fig_line_sommeil_2_courbes.add_trace(
    go.Scatter(
        x=df_dodo_mois.index,
        y=df_dodo_mois['Temps sommeil théorique'],
        name='Sommeil théorique',
        mode='lines',
        line=dict(color='blue'),
        hovertemplate='%{x}<br>Temps sommeil théorique: %{customdata}',
        customdata=[decimal_to_time(val) for val in df_dodo_mois['Temps sommeil théorique']]
    )
)
fig_line_sommeil_2_courbes.add_trace(
    go.Scatter(
        x=df_dodo_mois.index,
        y=df_dodo_mois['Total sommeil montre'],
        name='Montre',
        mode='lines',
        line=dict(color='red'),
        hovertemplate='%{x}<br>Temps sommeil montre: %{customdata}',
        customdata=[decimal_to_time(val) for val in df_dodo_mois['Total sommeil montre']]
    )
)

fig_line_sommeil_2_courbes.update_layout(
    yaxis=dict(title='Temps de sommeil (heures)'),
    xaxis=dict(title='Date')
    
)

y_min = df_dodo_mois[df_dodo_mois.columns[1]].min()
y_max = df_dodo_mois['Temps sommeil théorique'].max()

tickvals_x=df_dodo_mois.index[::2]
tickvals_y = [y_min + i * (y_max - y_min) / 4 for i in range(5)]
ticktext_y = [decimal_to_time(val) for val in tickvals_y]
fig_line_sommeil_2_courbes.update_layout(
    xaxis=dict(
        title='Mois',
        tickmode='array',
        tickvals=tickvals_x,
        ticktext=tickvals_x.strftime('%b %y')
    ),
    yaxis=dict(
        title='Temps de sommeil',
        tickmode='array',
        tickvals=tickvals_y,
        ticktext=ticktext_y
    ),
    title="Sommeil mensuel"
)


fig_temps_sommeil_hist=px.histogram(data_frame=df_dodo,x='Temps sommeil théorique',color='Catégorie note lendemain',marginal="box",color_discrete_map=couleur)

fig_hist_reveil=px.histogram(data_frame=df_dodo,x='Minutes réveil',color="Catégorie note", 
                           marginal="box",
                            color_discrete_map=couleur)
y_min = df_dodo['Minutes réveil'].min()
y_max = df_dodo['Minutes réveil'].max()

tickvals_x = [y_min + i * (y_max - y_min) / 8 for i in range(9)]
ticktext_x=[minutes_to_time(val) for val in tickvals_x]
fig_hist_reveil.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_x,
        ticktext=ticktext_x,    
    ),
    title="Distribution des heures de réveil"
)

## Temps sommeil montre

df_sommeil_montre=dfs[dfs.index>='2024-06-22']
df_sommeil_montre['Total sommeil']=(df_sommeil_montre['Sommeil profond']+df_sommeil_montre['Sommeil léger']+df_sommeil_montre['Sommeil paradoxal'])/60
fig_hist_sommeil_montre=px.histogram(df_sommeil_montre,x='Total sommeil',color='Catégorie note lendemain',marginal='box',color_discrete_map=couleur)

## Histogramme dodo

fig_hist_dodo=px.histogram(data_frame=df_dodo,
                           x='Heure dodo minutes',
                           color="Catégorie note lendemain", 
                           marginal="box",
                            color_discrete_map=couleur)
fig_hist_dodo.add_shape(
    type="line",
    x0=0, x1=0,
    y0=0, y1=1,
    xref='x', yref='paper',
    line=dict(color="red", width=2)
)

y_min = df_dodo['Heure dodo minutes'].min()
y_max = df_dodo['Heure dodo minutes'].max()

tickvals_x = [y_min + i * (y_max - y_min) / 8 for i in range(9)]
ticktext_x=[minutes_to_time(val) for val in tickvals_x]
fig_hist_dodo.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=tickvals_x,
        ticktext=ticktext_x,    
    ),
    title="Distribution des heures de dodo"
)

## Lien entre durée de sommeil et forme

df_sommeil_montre['Sommeil profond veille']=df_sommeil_montre['Sommeil profond'].shift(1)
df_sommeil_montre['Sommeil léger veille']=df_sommeil_montre['Sommeil léger'].shift(1)
df_sommeil_montre['Sommeil paradoxal veille']=df_sommeil_montre['Sommeil paradoxal'].shift(1)
df_sommeil_montre['Total sommeil veille']=df_sommeil_montre['Total sommeil'].shift(1)
df_sommeil_montre['Score de sommeil veille']=df_sommeil_montre['Score de sommeil'].shift(1)
df_sommeil_montre['VFC veille']=df_sommeil_montre['VFC'].shift(1)

coef=df_sommeil_montre['Total sommeil veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_sommeil_montre_forme=px.scatter(df_sommeil_montre,x='Total sommeil veille',y='Forme',trendline="ols",title=f"Corrélation entre ma durée de sommeil et mon niveau de forme du lendemain de {coef}")
for trace in fig_scatter_sommeil_montre_forme.data:
    if "trendline" in trace.name:  # Sélectionner la droite de régression
        trace.line.color = "gray"

df_sommeil_montre['Ratio profond veille']=df_sommeil_montre['Sommeil profond veille']/(df_sommeil_montre['Sommeil profond veille']+df_sommeil_montre['Sommeil paradoxal veille']+df_sommeil_montre['Sommeil léger veille'])*100
df_sommeil_montre['Ratio paradoxal veille']=df_sommeil_montre['Sommeil paradoxal veille']/(df_sommeil_montre['Sommeil profond veille']+df_sommeil_montre['Sommeil paradoxal veille']+df_sommeil_montre['Sommeil léger veille'])*100
df_sommeil_montre['Ratio léger veille']=df_sommeil_montre['Sommeil léger veille']/(df_sommeil_montre['Sommeil profond veille']+df_sommeil_montre['Sommeil paradoxal veille']+df_sommeil_montre['Sommeil léger veille'])*100

coef=df_sommeil_montre['Sommeil profond veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_sommeil_profond_forme=px.scatter(df_sommeil_montre,x='Sommeil profond veille',y='Forme',trendline="ols",title=f"Durée Sommeil profond vs niveau de forme du lendemain : Corrélation de {coef}",
                                             labels={'Sommeil profond veille': 'Sommeil profond (minutes)'})

coef=df_sommeil_montre['Sommeil paradoxal veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_sommeil_paradoxal_forme=px.scatter(df_sommeil_montre,x='Sommeil paradoxal veille',y='Forme',trendline="ols",title=f"Durée Sommeil paradoxal vs Niveau de forme du lendemain : Corrélation de {coef}",
                                               labels={'Sommeil paradoxal veille': 'Sommeil paradoxal (minutes)'})

coef=df_sommeil_montre['Sommeil léger veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_sommeil_leger_forme=px.scatter(df_sommeil_montre,x='Sommeil léger veille',y='Forme',trendline="ols",title=f"Durée Sommeil léger vs Niveau de forme du lendemain : Corrélation de {coef}",
                                           labels={'Sommeil léger veille': 'Sommeil léger (minutes)'})

## Ratio
st.dataframe(df_sommeil_montre)
coef=df_sommeil_montre['Ratio profond veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_ratio_profond_forme=px.scatter(df_sommeil_montre,x='Ratio profond veille',y='Forme',trendline="ols",title=f"% Sommeil profond vs Niveau de forme du lendemain : Corrélation de {coef}",
                                           labels={'Ratio profond veille': 'Sommeil profond (en % sur la durée de la nuit)'})

coef=df_sommeil_montre['Ratio paradoxal veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_ratio_paradoxal_forme=px.scatter(df_sommeil_montre,x='Ratio paradoxal veille',y='Forme',trendline="ols",title=f"% Sommeil paradoxal vs Niveau de forme du lendemain : Corrélation de {coef}",
                                             labels={'Ratio paradoxal veille': 'Sommeil paradoxal (en % sur la durée de la nuit)'})

coef=df_sommeil_montre['Ratio léger veille'].corr(df_sommeil_montre['Forme']).round(2)
fig_scatter_ratio_leger_forme=px.scatter(df_sommeil_montre,x='Ratio léger veille',y='Forme',trendline="ols",title=f"% Sommeil léger vs Niveau de forme du lendemain : Corrélation de {coef}",
                                         labels={'Ratio léger veille': 'Sommeil léger (en % sur la durée de la nuit)'})

## Impact du sommeil sur le jour de la semaine
fig_box_sommeil_semaine=px.box(df_sommeil_montre,x='Jour semaine',y='Total sommeil veille',color="Catégorie note",category_orders={'Jour semaine':jours_semaine_ordre},color_discrete_map=couleur)

fig_box_sommeil_theorique_semaine=px.box(df_dodo,x='Jour semaine',y='Temps sommeil théorique',color="Catégorie note",category_orders={'Jour semaine':jours_semaine_ordre},color_discrete_map=couleur)

def heure_dodo_compartiments(x):
    if (x>=0) & (x<30):
        return '00h-00h29'
    elif (x>=30) & (x<60):
        return '00h30-00h59'
    elif (x>=60) & (x<120):
        return '1h-1h59'
    elif x>=120:
        return '>= 2h'
    elif (x>=-30) & (x<0):
        return '23h30-23h59'
    elif (x>=-60) & (x<-30):
        return '23h-23h29'
    elif x<-60:
        return '< 23h'
    

## Score de sommeil
coef=df_sommeil_montre['Score de sommeil veille'].corr(df_sommeil_montre['Forme'])
fig_scatter_score_sommeil_forme=px.scatter(df_sommeil_montre,x='Score de sommeil veille',y='Forme'
                                           ,trendline="ols",title=f"% Sommeil léger vs Niveau de forme du lendemain : Corrélation de {coef:.2f}",
                                         labels={'Ratio léger veille': 'Sommeil léger (en % sur la durée de la nuit)'})

## VFC
df_points_VFC=df_sommeil_montre.groupby(['VFC','Forme']).size().reset_index(name='count')
coef=df_sommeil_montre['VFC'].corr(df_sommeil_montre['Forme'])
fig_scatter_VFC_forme=px.scatter(df_points_VFC,x='VFC',y='Forme',size='count',height=500,
                                 title=f"VFC de la veille vs Niveau de forme - Corrélation : {coef:.2f}", trendline="ols")


a0,b0,c,d,e,f,g,h=st.columns(8)
with a0:
    st.metric("Heure réveil moyen",moyenne_heure_str)
with b0:
    st.metric("Heure lever moyen",moyenne_lever_str)
with c:
    st.metric("Heure dodo moyen",moyenne_heure_dodo_str)

sous_onglet = st.sidebar.radio(
    "Sous-onglets",
    options=["Sommeil","Réveil et dodo","Avant de dormir"],
    index=0,  # Sous-onglet par défaut
)

if sous_onglet=="Sommeil":
    y,z=st.columns(2)
    with y :
        st.plotly_chart(fig_line_sommeil_2_courbes)
        st.plotly_chart(fig_box_sommeil_semaine)
        st.plotly_chart(fig_scatter_ratio_profond_forme)
        st.plotly_chart(fig_scatter_ratio_leger_forme)
        st.plotly_chart(fig_scatter_ratio_paradoxal_forme)
        st.plotly_chart(fig_scatter_score_sommeil_forme)
        st.plotly_chart(fig_scatter_VFC_forme)
    with z:
        st.plotly_chart(fig_hist_sommeil_montre)
        st.plotly_chart(fig_scatter_sommeil_montre_forme)
        st.plotly_chart(fig_scatter_sommeil_profond_forme)
        st.plotly_chart(fig_scatter_sommeil_leger_forme)
        st.plotly_chart(fig_scatter_sommeil_paradoxal_forme)
    

elif sous_onglet=="Réveil et dodo":
    a,b=st.columns(2)
    with a:
        st.plotly_chart(fig_line_reveil)
        st.plotly_chart(fig_line_dodo_mensuel)
    with b:
        st.plotly_chart(fig_hist_reveil)
        st.plotly_chart(fig_hist_dodo)

elif sous_onglet=="Avant de dormir":
    sous_onglet2 = st.radio(
    "Sous-onglets",
    options=["Dodo sans tel","Dodo en lisant"],
    index=0) 

    if sous_onglet2=="Dodo sans tel":
        dft=dfs[~dfs['Dodo sans tel'].isna()]
        

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

        '''periode_lisant = st.sidebar.slider(
                    "Période:",
                    min_value=pd.to_datetime("2024-01-06").to_pydatetime(),
                    max_value=hier,
                    value=(pd.to_datetime("2024-01-06").to_pydatetime(), hier),
                    format="YYYY-MM-DD"  
            )
        dfs = dfl[(dfl.index >= periode_lisant[0]) & (dfl.index <= periode_lisant[1])]'''

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
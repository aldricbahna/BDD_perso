import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
import numpy as np

@st.cache_data
def load_data():
    data=pd.read_excel("BILAN_JOURNEE_mai25.xlsx", index_col='Jour', parse_dates=True)
    df=data.copy()
    df['Somme réseaux']=df['Snap']+df['Insta']+df['Twitter']+df['BeReal']
    ajd = datetime.today().date()
    hier=ajd-timedelta(days=1)


    #Lendemain
    df['Messe'].fillna(0,inplace=True)
    df['Jour semaine'] = df.index.strftime('%A')
    df['Numéro semaine']=df.index.isocalendar().week
    df['Numéro jour']=df.index.day
    df['Mois']=df.index.month
    df['Année']=df.index.year
    jours = {
    'Monday': 'lundi',
    'Tuesday': 'mardi',
    'Wednesday': 'mercredi',
    'Thursday': 'jeudi',
    'Friday': 'vendredi',
    'Saturday': 'samedi',
    'Sunday': 'dimanche'
    }

    df['Jour semaine'] = df['Jour semaine'].map(jours)
    jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

    df['Activité?']=df['Activité'].map(lambda x: 'oui' if pd.notna(x) and x != '' else 'non')
    df['Transport?']=df['Transport'].map(lambda x: 'oui' if pd.notna(x) and x != '' else 'non')
    df['Match de sport?']=df['Match de sport'].map(lambda x: 'non' if x==0 else 'oui')
    df['Footing?']=df['Footing'].map(lambda x: 'non' if x==0 else 'oui')

    cols_presque_binaires=['Activité?', 'Transport?', 'Match de sport?']

    cols_binaires=["Lever direct",	"Lecture au petit-déj",	"A l'heure", "Parents","Laëtitia","Famille","Eugé","Sport","Ciné","Film","Docu",	"Restau","Fast food","Café/bar solo","Lecture dehors","Café/bar avec copains","Café/bar Eugé",
    "Repas copains","Vois copains","Soirée chill","Soirée","Dodo avec Eugé","Dodo en lisant","Dodo sans tel","Messe","Réveil sans tel (30 mn)", "CB","CP","Temps calme"]

        
    for col in cols_binaires:
        df[f'{col}?'] = df[col].apply(lambda x: 'oui' if x == 1 else ('non' if x == 0 else np.nan))

    df['Dodo en lisant veille']=df['Dodo en lisant'].shift(1)
    df['Dodo en lisant veille?']=df['Dodo en lisant?'].shift(1)

    df['Dodo sans tel veille']=df['Dodo sans tel'].shift(1)
    df['Dodo sans tel veille?']=df['Dodo sans tel?'].shift(1)

    df['Heure lever'] = pd.to_datetime(df['Heure lever'], format='%H:%M:%S')
    df['Heure réveil'] = pd.to_datetime(df['Heure réveil'], format='%H:%M:%S')
    df['Heure dodo'] = pd.to_datetime(df['Heure dodo'], format='%H:%M:%S')
    df['Heure dodo détecté'] = pd.to_datetime(df['Heure dodo détecté'], format='%H:%M:%S')
    df['Début travail'] = pd.to_datetime(df['Début travail'], format='%H:%M:%S')
    df['Heure footing'] = pd.to_datetime(df['Heure footing'], format='%H:%M:%S')
    df['Temps lever']=(df['Heure lever'] - df['Heure réveil']).dt.total_seconds()/60

    df['Lieu principal']=df['Lieu'].str.split('/').str[0]
    order_box=['oui','non']
    #palette=sns.color_palette("Set2")

    def categorie_note(note):
        if note >= 7:
            return "Bien (7-10)"
        elif note >= 6:
            return "Correct (6-6,5)"
        elif note <= 5.5:
            return "Mauvais (0-5,5)"
        else:
            return np.nan

    df['Catégorie note'] = df['Note'].map(categorie_note)
    df['Catégorie note lendemain']=df['Catégorie note'].shift(-1)
    df['Note lendemain']=df['Note'].shift(-1)
    colors=['#66CDAA', '#FFD700', '#FF7F7F']
    color_mapping = {
    'Bien (7-10)': colors[0],  
    'Correct (6-6,5)': colors[1],  
    'Mauvais (0-5,5)': colors[2]  
    }

    colors2 = ["#66c2a5", "#fc8d62"]
    color_mapping2 = {
    'oui': colors2[0],  
    'non': colors2[1]}

    dict_fatigue={'Très en forme':10,
              'En forme':8.75,
              'Assez en forme':7.5,
              'Correct':6.25,
              'Moyen':5,
              'Un peu fatigué':4,
              'Assez fatigué':3.5,
              'Fatigué':2.5,
              'Très fatigué':1.25}
    
    df['Forme']=df['Fatigue'].map(dict_fatigue)
    df['Forme lendemain']=df['Forme'].shift(-1)
    df['Somme réseaux lendemain']=df['Somme réseaux'].shift(-1)


    dict_meteo={'Très beau temps':10,                       
        'Beau temps':8.5,                            
        'Moyen':5,                             
        'Correct':6,                             
        'Pas mal':7,                              
        'Mauvais temps':3,                        
        'Médiocre':4,                             
        'Mi beau temps mi mauvais':5.5,                      
        'Très mauvais temps':2, 
        'Mi mauvais temps, mi pas mal':5,            
        'Mi beau temps mi moyen':6.5,                      
        'Mi beau temps mi médiocre':6,
        'Mi beau temps mi très mauvais temps':5, 
        'Mi correct mi mauvais':4.5,
        'Mi correct mi très beau':8,                 
        'Mi mauvais, mi très beau temps':6.5,            
        'Mi beau temps mi correct':7,              
        'Mi beau, mi mauvais, mi moyen':5.5,            
        'Beau temps, un peu moche':7,
        'Très beau temps, un peu moche':7.5,            
        'Mi médiocre, mi très mauvais temps':3,
        'Mi médiocre, mi correct':5,     
        'Mi moyen mi très beau':7.5,                  
        'Mi médiocre, mi très beau temps':7,
        'Beau temps, un peu mauvais':7,
        'Très beau temps, un peu mauvais':8,
        'Mi médiocre, mi pas mal':5.5,
        'Exécrable':1,
        'Neige':4,
        }
    
    df['Météo num']=df['Météo'].map(dict_meteo)

    dict_alimentation={'Très saine':10,
                  'Saine':8.5,
                  'Assez saine':7,
                  'Correct':6,
                  'Moyenne':5,
                  'Médiocre':4,
                  'Très moyenne':3,
                  'Mauvaise':1}  
    df['Alimentation num']=df['Alimentation'].map(dict_alimentation)

    dict_sucre={'Très peu':10,
                  'Un peu':8.5,
                  'Assez peu':7,
                  'Correct':6,
                  'Moyen':5,
                  'Pas mal':4,
                  'Beaucoup':2.5,
                  'Enorme':1}
    df['Sucre num']=df['Sucre'].map(dict_sucre)

    return df,color_mapping,color_mapping2
    
import streamlit as st
import pandas as pd
from data import load_data


st.set_page_config(layout="wide")

from auth import check_password
check_password()

df,couleur,couleur_box=load_data()

st.header(f"Bienvenue dans mon dashboard personnel")

st.subheader(f"Cela fait {df.shape[0]} que je me suis lancé dans cette aventure !")

st.write("N'hésitez pas à naviguer à travers les différents onglets")
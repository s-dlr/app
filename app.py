import sys

import pandas as pd
import streamlit as st

from src.data.indicateurs import *
from src.data.objet import Objet
from src.variables import *
from src.sql_client import ClientSQL
from src.flow.navigation import *

st.set_page_config(
    page_title="Home", page_icon="🧊", layout="wide", initial_sidebar_state="collapsed"
)
st.set_option("client.showSidebarNavigation", False)

with st.sidebar:
    uploaded_arborescence = st.file_uploader(
        "Choisir une arborescence", key="arborescence_file"
    )
    uploaded_objets = st.file_uploader(
        "Choisir un fichier objet",
        key="objets_file"
    )

try:
    st.header(f'Bonjour {st.session_state.equipe} !')
    go_to_next_question()
except:
    st.header("Créer une équipe our cmmencer à jouer")
    st.switch_page("pages/login.py")

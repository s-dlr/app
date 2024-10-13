import sys

import pandas as pd
import streamlit as st

from src.data.indicateurs import *
from src.data.objet import Objet
from src.variables import *
from src.sql_client import ClientSQL
from streamlit_utils.navigation import *

st.set_page_config(
    page_title="Home", page_icon="🧊", layout="wide", initial_sidebar_state="collapsed"
)
st.set_option("client.showSidebarNavigation", False)

if "equipe" in st.session_state:
    st.header("Commencer le prochain programme")
    st.page_link(
        "pages/load_data.py", label="Commencer", icon=":material/settings:"
    )
else:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")

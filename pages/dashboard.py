from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

from src.variables import *

# Requêtes
QUERY_INDICATEURS = f'SELECT * FROM `Indicateurs`'
QUERY_ARMEES = f"SELECT * FROM `Armees`"

# Connexion
dashboard_connection = st.connection("astrolabedb", autocommit=True, ttl=1)

# Equipes disponibles
df_indicateurs = dashboard_connection.query(QUERY_INDICATEURS, ttl=5)
display_equipes = st.multiselect(
    'Equipes',
    df_indicateurs[EQUIPE].unique()
)

# Courbes indicateurs
col1, col2 = st.columns(2)
with col1:
    st.markdown(f":blue[Evolution des budgets]")
    st.line_chart(
        df_indicateurs[df_indicateurs[EQUIPE].isin(display_equipes)],
        x=ANNEE,
        y=BUDGET,
        color=EQUIPE,
    )

with col2:
    st.markdown(f":blue[Evolution des niveau technologiques]")
    st.line_chart(
        df_indicateurs[df_indicateurs[EQUIPE].isin(display_equipes)],
        x=ANNEE,
        y=NIVEAU_TECHNO,
        color=EQUIPE,
    )

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")

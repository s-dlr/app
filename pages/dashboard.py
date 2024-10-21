from src.variables import *

import streamlit as st

# Requêtes
QUERY_INDICATEURS = f'SELECT * FROM `Indicateurs`'

# Connexion
dashboard_connection = st.connection("astrolabedb", autocommit=True, ttl=1)

# Equipes disponibles
df_indicateurs = dashboard_connection.query(QUERY_INDICATEURS, ttl=5)
display_equipes = st.multiselect(
    'Equipes',
    df_indicateurs[EQUIPE].unique()
)

# Courbes budget
st.line_chart(df_indicateurs[df_indicateurs[EQUIPE] in display_equipes], x=ANNEE, y=BUDGET, color=EQUIPE)

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")

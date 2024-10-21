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
st.divider()

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
st.divider()

# Niveaux armées
df_armees = dashboard_connection.query(QUERY_ARMEES, ttl=5)
data_chart = df_armees.sort_values()
# st.bar_chart(df_armees.pi)
for equipe, col in zip(display_equipes, st.columns(display_equipes)):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=df_armees[df_armees[EQUIPE] == equipe]["terre"].iloc[0],
            title={"text": "Armée de terre"},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

from src.variables import *
from streamlit_utils.display_functions import *

st.set_page_config(
    page_title="Dashboard",
    page_icon=":information_source:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Requêtes
QUERY_INDICATEURS = f'SELECT * FROM `Indicateurs`'
QUERY_ARMEES = f"SELECT * FROM `Armee`"
QUERY_DEPENDANCE = """
    SELECT UNIQUE equipe, dependance_export FROM Objets
    WHERE Objets.nom IN (SELECT objet FROM Constructions)
    UNION
    SELECT UNIQUE equipe, dependance_export FROM Programmes
    WHERE Programmes.debut IS NOT NULL AND dependance_export!=0;
"""
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

if display_equipes is not None:
    # Niveaux armées
    df_armees = dashboard_connection.query(QUERY_ARMEES, ttl=5)

    # Dépendances
    df_dependances = dashboard_connection.query(QUERY_DEPENDANCE, ttl=5)
    df_dependances_chart = df_dependances.copy()
    df_dependances_chart[DEPENDANCE_EXPORT] = df_dependances_chart[DEPENDANCE_EXPORT].apply(lambda x: x.split(","))
    df_dependances_chart = df_dependances_chart.explode(DEPENDANCE_EXPORT)

    # Affichage
    for equipe, col in zip(display_equipes, st.columns(len(display_equipes))):
        with col.container(border=True):
            df_equipe = df_armees[df_armees[EQUIPE] == equipe]
            niveaux_armee = df_equipe.iloc[df_equipe[ANNEE].argmax()]
            col.markdown(f":blue[Armée de {equipe} en {df_equipe[ANNEE].max()}]")
            fig = display_gauges_armees(
                niveaux_armee[["terre", "air", "mer", "rens"]].to_dict()
            )
            col.plotly_chart(fig, use_container_width=True, key=f"gauge_terre_{equipe}")

            col.markdown(f":blue[Dépendances de {equipe} en {df_equipe[ANNEE].max()}]")
            pays_dependance_equipe = df_dependances_chart[df_dependances_chart[EQUIPE] == equipe][DEPENDANCE_EXPORT].values()
            line_pays = ''
            for pays in pays_dependance_equipe:
                line_pays += DRAPEAUX.get(pays.strip(), "")
            st.write(line_pays)

"""
# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ["Group 1", "Group 2", "Group 3"]

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

# Plot!
st.plotly_chart(fig, use_container_width=True)
"""

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")

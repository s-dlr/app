import streamlit as st

from src.flow.navigation import *

def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    st.session_state.sql_client.update_sql_objet(st.session_state.objet)
    # Aller à la prochaine arborescence
    go_to_next_question()

st.set_page_config(
    page_title="Achat de matériel",
    page_icon=":material/shopping_cart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "arborescence" in st.session_state and st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
    # Contexte et question
    st.title(st.session_state.arborescence.arborescence)
    st.write(st.session_state.arborescence.question.contexte_question)
    st.markdown(f"**Combien de {st.session_state.objet.nom} souhaitez vous acheter ?**")

    # TODO Afficher les caractéristiques de l'objet

    # Slider
    min_nb_unit = st.session_state.arborescence.question.min_nb_unit
    max_nb_unit = st.session_state.arborescence.question.max_nb_unit
    slider_unites = st.slider("Nombre d'unités", min_nb_unit, max_nb_unit, 1)

    # Bouton
    st.button(
        type="primary",
        label="VALIDER",
        use_container_width=True,
        on_click=buy_unit,
        disabled=False,
    )

elif (
    "arborescence" in st.session_state
    and st.session_state.arborescence.type_question == CHOIX_OPTION
):
    st.header("Commencer le prochain programme")
    st.page_link("pages/options.py", label="Commencer", icon=":material/settings:")

elif "arborescence" not in st.session_state:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")

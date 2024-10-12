import streamlit as st

from streamlit_utils.display_functions import *
from streamlit_utils.navigation import *


def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    st.session_state.sql_client.update_sql_objet(st.session_state.objet)
    # Aller à la prochaine question ou arborescence
    next_question = st.session_state.arborescence.get_next_question()
    st.session_state.objet.send_to_sql(st.session_state.sql_client)
    # TODO Lancer la construction
    if next_question != 0:
        st.session_state.arborescence.load_data(next_question)
    else:
        st.session_state.arborescence = False

st.set_page_config(
    page_title="Achat de matériel",
    page_icon=":material/shopping_cart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if st.session_state.arborescence:
    if st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:

        # Contexte et question
        st.title(st.session_state.arborescence.arborescence)
        st.write(st.session_state.arborescence.question.contexte_question)
        st.markdown(f"**Combien de {st.session_state.objet.nom} souhaitez vous acheter ?**")
        st.divider()

        # Caractéristiques de l'objet courant
        st.header(f"Caractéristiques de {st.session_state.objet.nom}")
        display_objet(st.session_state.objet.to_dict())
        st.divider()

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

    elif st.session_state.arborescence.type_question == CHOIX_OPTION:
        st.header("Commencer le prochain programme")
        st.page_link("pages/options.py", label="Commencer", icon=":material/settings:")


else:
    if "equipe" in st.session_state:
        st.header("Commencer le prochain programme")
        st.page_link("pages/load_data.py", label="Commencer", icon=":material/settings:")
    else:
        st.write("Aucune partie en cours. Connectez vous d'abord.")
        st.page_link("pages/login.py", label="Se connecter", icon="🏠")

import streamlit as st

from src.flow.navigation import *
from src.variables import *

EFFET_IMMEDIAT: str = "Effets immédiats sur vos compteurs"
LABELS: dict = {
    EUROPEANISATION: "Européanisation",
    NIVEAU_TECHNO: "Niveau technologique",
}

def display_metrics(effets_dict: dict, compteurs: dict):
    """
    Affiche des métriques
    """
    columns = st.columns(len(effets_dict))
    i = 0
    for compteur, effet in effets_dict.items():
        columns[i].metric(
            label=LABELS[compteur],
            value=compteurs.get(compteur, 0) + effet,
            delta=effet,
        )
        i += 1

def display_option_data(option):
    """
    Affiche toutes les informations correspondant
    """
    # TODO Récupérer les valeurs des compteurs
    compteurs = {EUROPEANISATION: 3, NIVEAU_TECHNO: 2}
    # Effet immédiat
    effets_immediat_dict = option.effet_immediat.to_dict()
    if len(effets_immediat_dict) > 0:
        st.markdown(f":blue[{EFFET_IMMEDIAT}]")
        display_metrics(effets_immediat_dict, compteurs)

def display_list_options() -> None:
    """
    Affiche la liste des options
    """
    list_options = st.session_state.arborescence.question.options
    # Radio button for options
    st.radio(
        label="Choix",
        options=[opt.texte_option for opt in list_options],
        index=None,
        label_visibility="collapsed",
        key="radio_options",
    )
    # Affichage des données correspondant à chaque option
    columns = st.columns(len(list_options))
    for option, col in zip(list_options, columns):
        if "radio_options" not in st.session_state:
            st.session_state["radio_options"] = False
        with col.container(
            border=(st.session_state.radio_options == option.texte_option)
        ):
            display_option_data(option)


st.set_page_config(
    page_title="Options",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.divider()

# Liste des options
display_list_options()

# Données correspondant aux options
display_option_data()

# Bouton
st.button(
    type="primary",
    label="VALIDER",
    use_container_width=True,
    on_click=go_to_next_question,
    disabled=st.session_state.radio_options,
)

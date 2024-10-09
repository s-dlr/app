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

def next_step():
    # Application des modifications à l'objet
    selected_option = st.session_state.arborescence.question.get_option_by_text(
        st.session_state.select_option
    )
    objet_option = st.session_state[selected_option.objet]
    objet_option.apply_modification(selected_option.modification_objet)
    # Application des modification au programme
    # TODO
    # Prochaine question
    next_question_type = st.session_state.arborescence.get_next_question_type(
        st.session_state.select_option
    )
    if next_question_type == CHOIX_OPTION:
        go_to_next_question()
    elif next_question_type == CHOIX_OPTION:
        st.switch_page("pages/buy.py")
        go_to_next_question()

st.set_page_config(
    page_title="Options",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "arborescence" in st.session_state and st.session_state.arborescence.type_question == CHOIX_OPTION:
    # Contexte et question
    st.title(st.session_state.arborescence.arborescence)
    st.write(st.session_state.arborescence.question.contexte_question)
    st.markdown(f"**{st.session_state.arborescence.question.texte_question}**")
    st.divider()

    # Liste des options
    list_options = st.session_state.arborescence.question.options

    # Radio button for options
    st.radio(
        label="Choix",
        options=[opt.texte_option for opt in list_options],
        index=None,
        label_visibility="collapsed",
        key="select_option",
    )

    # Affichage des données correspondant à chaque option
    columns = st.columns(len(list_options))
    for option, col in zip(list_options, columns):
        with col.container(
            border=(st.session_state.select_option == option.texte_option)
        ):
            display_option_data(option)

    # Bouton validation
    st.button(
        type="primary",
        label="VALIDER",
        use_container_width=True,
        on_click=next_step,
        disabled=(st.session_state.select_option == ""),
    )

else:
    st.write("Not available")

import streamlit as st

from src.flow.navigation import *

def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """

    objet_achete = st.session_state[st.session_state.arborescence.question.objet]
    st.session_state.sql_client.update_sql_objet(objet_achete)
    # Aller à la prochaine arborescence
    next_question_type = st.session_state.arborescence.get_next_question_type(
        st.session_state.select_option
    )
    if next_question_type == CHOIX_OPTION:
        go_to_next_question()
        st.switch_page("pages/options.py")
    else:
        go_to_next_question()

st.set_page_config(
    page_title="Achat",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "arborescence" in st.session_state and st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
    # Contexte et question
    st.title(st.session_state.arborescence.arborescence)
    st.write(st.session_state.arborescence.question.contexte_question)
    st.markdown(f"**{st.session_state.arborescence.question.texte_question}**")

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

else:
    st.write("Not available")
    st.write(st.session_state.arborescence.type_question)
    st.write(st.session_state.select_option)
    st.write(
        st.session_state.arborescence.get_next_question(st.session_state.select_option)
    )

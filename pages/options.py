import streamlit as st
import pandas as pd

from streamlit_utils.display_functions import *
from streamlit_utils.manage_state import *
from streamlit_utils.navigation import *
from src.variables import *

def next_step():
    """
    Passage à la prochaine étape du programme
    Seuls les effets immédiats ont un caractère définitif
    Les autres modifications ne sont pas envoyés à SQL
    """
    st.session_state["loading"] = True
    selected_option = st.session_state.arborescence.question.get_option_by_text(
        st.session_state.select_option
    )
    # Application des effets immédiats
    if st.session_state.indicateurs.apply_modification(selected_option.effet_immediat):
        st.success(selected_option.effet_immediat.to_dict())
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
    if st.session_state.armee.apply_modification(selected_option.effet_immediat):
        st.session_state.armee.send_to_sql(st.session_state.sql_client)
    # Application des modification au programme
    if selected_option.programme:
        programme_option = st.session_state["programme " + selected_option.programme]
        if programme_option.apply_modification(selected_option.modification_programme):
            programme_option.send_to_sql(st.session_state.sql_client)
        if "launch_programme" in selected_option.commandes:
            launch_programme(programme_option.nom)
    # Application des modifications à l'objet
    if selected_option.objet:
        # Save object
        objet_option = st.session_state[selected_option.objet]
        if objet_option.apply_modification(selected_option.modification_objet):
            objet_option.send_to_sql(st.session_state.sql_client)
    # Passage à la prochaine question
    if "select_option" not in st.session_state:
        st.session_state["select_option"] = None
    next_question = st.session_state.arborescence.get_next_question(
        st.session_state.select_option
    )
    question_pause_satellite = (
        st.session_state.arborescence.question.num_question == 6
        and st.session_state.arborescence.arborescence == "Satellites phase 1"
    )
    if next_question != 0 and not question_pause_satellite:
        st.session_state.arborescence.load_data(next_question)
        st.session_state.annee = st.session_state.arborescence.question.annee
        update_indicateurs()
        push_etat_to_sql(st.session_state.arborescence.arborescence, next_question)
    else:
        st.session_state.arborescence = False
        push_etat_to_sql(st.session_state.prochaine_arborescence, 1)
        if question_pause_satellite:
            push_etat_satellite_2(next_question)
    st.session_state["loading"] = False

st.set_page_config(
    page_title="Définition des besoins",
    page_icon=":material/settings:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def option_key(number):
    return f"{st.session_state.arborescence.arborescence}_{st.session_state.arborescence.question.num_question}_{number}"


# Timeline
if "annee" in st.session_state:
    display_annee()

if "arborescence" not in st.session_state:
    st.session_state["arborescence"] = False

if "equipe" not in st.session_state:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")

else:

    if st.session_state.arborescence:
        # Contexte et question
        st.title(st.session_state.arborescence.arborescence)
        if (
            st.session_state.arborescence.question.image != ""
            and st.session_state.arborescence.question.image is not None
        ):
            st.image(IMAGE_DIR + st.session_state.arborescence.question.image)
        st.write(st.session_state.arborescence.question.contexte_question)
        st.markdown(f"**{st.session_state.arborescence.question.texte_question}**")
        st.divider()

        # Liste des options
        list_options = st.session_state.arborescence.question.options

        # Radio button for options
        if "select_option" not in st.session_state:
            st.session_state["select_option"] = list_options[0].texte_option
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
                st.header(f"Option {option.numero_option}")
                # Effets immédiats indicateurs et atmées
                effets_immediat_dict = option.effet_immediat.to_dict()
                if len(effets_immediat_dict) > 0:
                    st.subheader(f":blue[{EFFET_IMMEDIAT_DESC}]")
                    display_metrics(
                        {
                            key: effets_immediat_dict.get(key, 0)
                            for key in [EUROPEANISATION, BUDGET, NIVEAU_TECHNO]
                        }
                    )
                    modification_dict = {
                        key: effets_immediat_dict.get(f"bonus_{key}", 0)
                        for key in [AIR, MER, TERRE, RENS]
                    }
                    if len(modification_dict) > 0:
                        fig = display_gauges_armees(
                            values=st.session_state.armee.to_dict(),
                            modifications=modification_dict,
                            grid=True,
                        )
                        fig.update_layout(
                            height=300,
                            showlegend=True,
                        )
                        st.plotly_chart(
                            fig, key=f"gauge_armee_{option_key(option.numero_option)}"
                        )
                # Objet
                if option.objet:
                    display_objet(
                        st.session_state[option.objet].to_dict(),
                        modification_objet=option.modification_objet.to_dict(),
                        key=f"objet_{option_key(option.numero_option)}",
                    )
                # Programme
                if option.programme:
                    display_programme(
                        st.session_state["programme " + option.programme].to_dict(),
                        modification_programme=option.modification_programme.to_dict(),
                        key=f"programme_{option_key(option.numero_option)}",
                    )

        # Bouton validation
        st.button(
            type="primary",
            label="VALIDER",
            use_container_width=True,
            on_click=next_step,
            disabled=(st.session_state.select_option is None),
        )

    else :
        if st.session_state.prochaine_arborescence:
            st.header("Fin du programme")
            def button_action():
                st.session_state["loading"] = True
                load_next_arborescence(st.session_state.prochaine_arborescence)
                st.session_state["loading"] = False
            st.button(
                label="Commencer un autre programme",
                icon=":material/settings:",
                type="secondary",
                on_click=button_action,
            )
        else:
            st.title("Fin du jeu")
            st.write("Vous pouvez encore acheter des unités si vous le souhaitez")

    st.page_link(
        "pages/store.py",
        label="Acheter des unités",
        icon=":material/shopping_cart:",
        disabled=st.session_state["loading"],
    )

st.page_link(
    "pages/dashboard.py",
    label="Dashboard",
    icon=":material/dataset:",
    disabled=st.session_state["loading"],
)

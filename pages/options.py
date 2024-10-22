import streamlit as st

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
    selected_option = st.session_state.arborescence.question.get_option_by_text(
        st.session_state.select_option
    )
    # Application des effets immédiats
    if st.session_state.indicateurs.apply_modification(selected_option.effet_immediat):
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
        # Objet courant utilsé pour le prochain achat
        st.session_state["objet"] = objet_option
    # Passage à la prochaine question
    if "select_option" not in st.session_state:
        st.session_state["select_option"] = None
    next_question = st.session_state.arborescence.get_next_question(
        st.session_state.select_option
    )
    if next_question != 0:
        st.session_state.arborescence.load_data(next_question)
        st.session_state.annee = st.session_state.arborescence.question.annee
        update_indicateurs()
        push_etat_to_sql(st.session_state.arborescence.arborescence, next_question)
    else:
        st.session_state.arborescence = False

st.set_page_config(
    page_title="Définition des besoins",
    page_icon=":material/settings:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Timeline
if "annee" in st.session_state:
    display_annee()

if "arborescence" not in st.session_state:
    st.session_state["arborescence"] = False


if st.session_state.arborescence:

    # Contexte et question
    st.title(st.session_state.arborescence.arborescence)
    if st.session_state.arborescence.question.image != "":
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
            # Effet immédiat
            effets_immediat_dict = option.effet_immediat.to_dict()
            if len(effets_immediat_dict) > 0:
                st.subheader(f":blue[{EFFET_IMMEDIAT_DESC}]")
                display_metrics(effets_immediat_dict)
            # Objet
            if option.objet:
                display_objet(
                    st.session_state[option.objet].to_dict(),
                    modification_objet=option.modification_objet.to_dict(),
                    key=f"objet_{st.session_state.arborescence.arborescence}_{st.session_state.arborescence.question.num_question}_{option.numero_option}",
                )
            # Programme
            if option.programme:
                display_programme(
                    st.session_state["programme " + option.programme].to_dict(),
                    modification_programme=option.modification_programme.to_dict(),
                    key=f"programme_{st.session_state.arborescence.arborescence}_{st.session_state.arborescence.question.num_question}_{option.numero_option}",
                )

    # Bouton validation
    st.button(
        type="primary",
        label="VALIDER",
        use_container_width=True,
        on_click=next_step,
        disabled=(st.session_state.select_option is None),
    )
    st.page_link(
        "pages/store.py",
        label="Acheter des unités",
        icon=":material/shopping_cart:",
    )

else:
    if "equipe" in st.session_state:
        st.header("Fin du programme")
        st.page_link(
            "pages/load_data.py",
            label="Commencer un autre programme",
            icon=":material/settings:",
        )
        st.page_link(
            "pages/store.py",
            label="Acheter des unités",
            icon=":material/shopping_cart:",
        )
    else:
        st.write("Aucune partie en cours. Connectez vous d'abord.")
        st.page_link("pages/login.py", label="Se connecter", icon="🏠")

st.page_link("pages/dashboard.py", label="Dashboard", icon=":material/dataset:")

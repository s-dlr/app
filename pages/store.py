import math
import streamlit as st

from src.data.objet import Construction
from streamlit_utils.display_functions import *
from streamlit_utils.navigation import *

def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    objet = st.session_state[st.session_state[st.session_state.selected_objet]]
    duree_construction = math.ceil(st.session_state.nb_unites / objet.unite_par_an)
    construction = Construction(
        objet=objet.nom,
        debut=st.session_state.annee,
        fin=st.session_state.annee + duree_construction - 1,
        nombre_unites=st.session_state.nb_unites,
    )
    construction.send_to_sql(st.session_state.sql_client)


st.set_page_config(
    page_title="Achat de matériel",
    page_icon=":material/shopping_cart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Timeline
if "annee" in st.session_state:
    display_annee()

if "arborescence" not in st.session_state:
    st.session_state["arborescence"] = False

if "equipe" in st.session_state:

    list_objets_disponibles = get_objets_disponibles()

    if len(list_objets_disponibles) > 0:

        # Contexte et question
        st.title("Achat d'unités")
        st.write("Vous pouvez choisir des unités à acheter")
        st.markdown(
            f"**Combien de {st.session_state.objet.nom} souhaitez vous acheter ?**"
        )
        if "selected_objet" not in st.session_state:
            st.session_state["selected_objet"] = None
        select_objets = st.selectbox(
            "Quel objet souhaitez vous acheter ?",
            options=list_objets_disponibles,
            key="selected_objet",
            index=None,
            placeholder="Choisissez un objet à acheter"
        )
        st.divider()

        # TODO afficher les objets déjà en construction et leur terme

        if st.session_state.selected_objet:
            # Caractéristiques de l'objet courant
            st.header(f"Caractéristiques de {st.session_state.selected_objet}")
            display_objet(st.session_state[st.session_state.selected_objet].to_dict())
            st.divider()

            # Slider
            min_nb_unit = 0
            max_nb_unit = st.session_state[st.session_state.selected_objet].max_nb_utile
            slider_unites = st.slider("Nombre d'unités", min_nb_unit, max_nb_unit, 1, key="nb_unites")

            # TODO gain en fonction du nombre d'unités

            # Bouton
            if st.button(
                type="primary",
                label="ACHETER",
                use_container_width=True,
                on_click=buy_unit,
                disabled=False,
            ):
                st.success(
                    f"Vous avez commandé {st.session_state.nb_unites} {st.session_state.selected_objet}s"
                )

    else:
        st.header("Vous n'avez aucun objet disponible à l'achat")

    if st.session_state.arborescence:
        st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")
    else:
        st.page_link(
            "pages/load_data.py",
            label="Commencer le prochain programme",
            icon=":material/settings:",
        )

else:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")

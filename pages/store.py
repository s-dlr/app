import math
import streamlit as st

from src.data.objet import Construction
from streamlit_utils.display_functions import *
from streamlit_utils.navigation import *


def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    objet = st.session_state[st.session_state.selected_objet]
    # Vérification si une construction est déjà lancées
    query = f"""
    SELECT * FROM `Constructions`
    WHERE `equipe` = '{st.session_state.equipe}' AND `objet` = '{objet.nom}' AND `fin` < {st.session_state.annee};"""
    df_constructions = st.session_state.sql_client.get_custom_query(query)
    if df_constructions.shape[0] > 0:
        construction_en_cours = df_constructions.iloc[0].to_dict()
    else:
        # Application du cout fixe
        cout_fixe = Modification(cout_fixe=objet.cout_fixe)
        st.session_state.indicateurs.apply_modification(cout_fixe)
        construction_en_cours = {DEBUT: st.session_state.annee, NOMBRE_UNITE: 0}
    # Concaténer les constructions
    total_nb_constructions = (
        construction_en_cours.get(NOMBRE_UNITE) + st.session_state.nb_unites
    )
    duree_construction = math.ceil(total_nb_constructions / objet.unite_par_an)
    construction = Construction(
        objet=objet.nom,
        debut=construction_en_cours.get(DEBUT),
        fin=construction_en_cours.get(DEBUT) + duree_construction - 1,
        nombre_unites=total_nb_constructions,
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
        def button_action():
            load_next_arborescence(st.session_state.prochaine_arborescence)
        st.button(
            label="Commencer un autre programme",
            icon=":material/settings:",
            type="secondary",
            on_click=button_action,
        )

else:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")

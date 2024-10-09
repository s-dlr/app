import typing as T

import pandas as pd
import streamlit as st

from src.flow.views.abstract_view import AbstractView
from src.flow.arborescence.question import *
from src.flow.arborescence.option import Option
from src.data.modification import Modification
from src.variables import *


class OptionsView(AbstractView):

    EFFET_IMMEDIAT: str = "Effets immédiats sur vos compteurs"
    LABELS: dict = {
        EUROPEANISATION: "Européanisation",
        NIVEAU_TECHNO: "Niveau technologique",
    }

    def display_metrics(self, effets_dict: dict, compteurs: dict):
        """
        Display effets with metrics components
        """
        columns = st.columns(len(effets_dict))
        i = 0
        for compteur, effet in effets_dict.items():
            columns[i].metric(
                label=OptionsView.LABELS[compteur],
                value=compteurs.get(compteur, 0) + effet,
                delta=effet,
            )
            i += 1

    def display_option_data(self, option: Option):
        """
        Affiche toutes les informations correspondant
        """
        # TODO Récupérer les valeurs des compteurs
        compteurs = {EUROPEANISATION: 3, NIVEAU_TECHNO: 2}
        # Effet immédiat
        effets_immediat_dict = option.effet_immediat.to_dict()
        if len(effets_immediat_dict) > 0:
            st.markdown(f":blue[{OptionsView.EFFET_IMMEDIAT}]")
            self.display_metrics(effets_immediat_dict, compteurs)

    def display_list_options(self) -> None:
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
            key="radio_options"
        )
        # Affichage des données correspondant à chaque option
        columns = st.columns(len(list_options))
        for option, col in zip(list_options, columns):
            if "radio_options" not in st.session_state:
                st.session_state["radio_options"] = False
            with col.container(
                border=True #(st.session_state.radio_options == option.texte_option)
            ):
                self.display_option_data(option)

    def show(self) -> None:
        """
        Affichage de la page option
        """
        super().show()
        st.divider()
        self.display_list_options()

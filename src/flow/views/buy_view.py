import typing as T

import streamlit as st

from src.flow.views.abstract_view import AbstractView
from src.flow.arborescence.question import Question
from src.flow.arborescence.option import Option


class BuyView(AbstractView):

    def show(self) -> None:
        """
        Affichage de la page option
        """
        super().show()
        st.divider()
        min_nb_unit = st.session_state.arborescence.question.nb_units.min_nb_unit
        max_nb_unit = st.session_state.arborescence.question.nb_units.max_nb_unit
        self.slider_unites = st.slider("Nombre d'unités", min_nb_unit, max_nb_unit, 1)
        # TODO afficher cooût par an, cout total, et bonus
import streamlit as st

from src.flow.arborescence.question import Question

from src.variables import *


class AbstractView:

    def __init__(self) -> None:
        pass

    def display_question(self) -> None:
        st.write(st.session_state.arborescence.question.contexte_question)
        st.markdown(f"**{st.session_state.arborescence.question.texte_question}**")

    def display_button(self, on_click, disabled=False) -> None:
        st.button(
            type="primary",
            label="VALIDER",
            use_container_width=True,
            on_click=on_click,
            disabled=disabled,
        )

    def show(self) -> None:
        st.title(st.session_state.arborescence.arborescence)
        self.display_question()

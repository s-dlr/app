from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src.flow.arborescence.option import Option
from src.flow.arborescence.number_units import NumberUnits
from src.variables import *


@dataclass
class Question:
    contexte_question: str
    num_question: str
    texte_question: str

    def create_options(self, options_df: pd.DataFrame):
        self.options = []
        for _, option_data in options_df.iterrows():
            if option_data[NUMERO_OPTION] == NOMBRE_UNITE:
                self.nb_units = NumberUnits(
                    objet=option_data[OBJET],
                    min_nb_unit=int(option_data[TEXTE_OPTION].split("a")[0]),
                    max_nb_unit=int(option_data[TEXTE_OPTION].split("a")[1]),
                    prochaine_question=int(option_data[PROCHAINE_QUESTION]),
                )
                self.type = CHOIX_NOMBRE_UNITE
                break
            else:
                option = Option(**option_data.to_dict())
                if option.check_prerequis():
                    # TODO récupérer les seuils via l'API
                    self.options.append(option)
                self.type = CHOIX_OPTION

    def get_next_question(self, texte_option: str) -> Option:
        for opt in self.options:
            if opt.texte_option == texte_option:
                return opt.prochaine_question

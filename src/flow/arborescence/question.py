from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.option import Option
from src.variables import *

@dataclass
class QuestionOptions:
    contexte_question: str
    num_question: int
    texte_question: str
    annee: int
    image: str = ""

    def create_options(self, options_df: pd.DataFrame):
        self.options = []
        for _, option_data in options_df.iterrows():
            option = Option(**option_data.to_dict())
            if option.check_prerequis():
                # TODO récupérer les seuils via l'API
                self.options.append(option)

    def get_option_by_text(self, texte_option: str) -> Option:
        for opt in self.options:
            if opt.texte_option == texte_option:
                return opt

    def get_next_question(self, texte_option: str) -> Option:
        return self.get_option_by_text(texte_option).prochaine_question

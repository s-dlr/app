from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.question import *
from src.variables import *

@dataclass
class Arborescence:
    arborescence: str = "test"

    def __post_init__(self) -> None:
        # TODO remove programme test
        # self.df_arborescence = pd.read_csv(ARBORESCENCES[self.arborescence], sep=";")
        self.df_arborescence = pd.read_csv(self.arborescence, sep=";", dtype=str)
        self.arborescence = "Programme test"
        self.df_arborescence.fillna("", inplace=True)
        self.df_arborescence[NUM_QUESTION] = self.df_arborescence[NUM_QUESTION].astype(
            int
        )
        self.df_arborescence[PROCHAINE_QUESTION] = self.df_arborescence[
            PROCHAINE_QUESTION
        ].astype(int)
        self.load_data(num_question=1)

    def load_data(self, num_question: int = 1) -> None:
        """
        Instantie l'étape de l'arboarescence correpondant à la question
        """
        data = self.df_arborescence[self.df_arborescence[NUM_QUESTION] == num_question]
        question_data = data.iloc[0][[NUM_QUESTION, CONTEXTE_QUESTION, TEXTE_QUESTION, ANNEE, IMAGE]]
        option_data = data[
            [
                NUMERO_OPTION,
                TEXTE_OPTION,
                PROCHAINE_QUESTION,
                PREREQUIS,
                EFFET_IMMEDIAT,
                MODIFICATION_OBJET,
                MODIFICATION_PROGRAMME,
                OBJET,
                PROGRAMME,
                COMMANDES,
            ]
        ].fillna("")
        self.question = QuestionOptions(**question_data.to_dict())
        self.question.create_options(option_data)

    def get_next_question(self, select_option: str) -> str:
        return self.question.get_next_question(select_option)

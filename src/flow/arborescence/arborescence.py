from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.question import *
from src.variables import *

@dataclass
class Arborescence:
    arborescence: str

    def __post_init__(self) -> None:
        self.df_arborescence = pd.read_csv(ARBORESCENCES[self.arborescence], sep=";")
        self.load_data(num_question=1)

    def load_data(self, num_question: int = 1) -> None:
        """
        Instantie l'étape de l'arboarescence correpondant à la question
        """
        data = self.df_arborescence[self.df_arborescence[NUM_QUESTION] == num_question]
        question_data = data.iloc[0][[NUM_QUESTION, CONTEXTE_QUESTION, TEXTE_QUESTION]]
        if data[NUMERO_OPTION].iloc[0] == NOMBRE_UNITE:
            option_data = data.iloc[0]
            self.question = QuestionAchat(
                objet=option_data[OBJET],
                contexte_question=question_data[CONTEXTE_QUESTION],
                num_question=question_data[NUM_QUESTION],
                texte_question=question_data[TEXTE_QUESTION],
                min_nb_unit=int(option_data[TEXTE_OPTION].split("a")[0]),
                max_nb_unit=int(option_data[TEXTE_OPTION].split("a")[1]),
                prochaine_qestion=0,
            )
            self.question.create_options(option_data)
            self.type_question = CHOIX_NOMBRE_UNITE
        else:
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
                ]
            ].fillna("")
            self.question = QuestionOptions(**question_data.to_dict())
            self.question.create_options(option_data)
            self.type_question = CHOIX_OPTION

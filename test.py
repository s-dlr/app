from src.flow.arborescence.arborescence import Arborescence
from src.data.indicateurs import *

arborescence = Arborescence(arborescence="Programme exemple")
print(arborescence.question.get_option_by_text("Sur étagère").prochaine_question)
# indicateurs = Indicateurs()
# print(indicateurs.to_dict())

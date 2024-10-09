from src.flow.arborescence.arborescence import Arborescence
from src.data.indicateurs import *
from src.data.objet import Objet
from src.data.modification import Modification

# arborescence = Arborescence(arborescence="Programme exemple")
# print(arborescence.question.get_option_by_text("Sur étagère").prochaine_question)
# indicateurs = Indicateurs()
# print(indicateurs.to_dict())

modif = Modification("cout:+1\nniveau_techno:+1")
objet = Objet()
objet.apply_modification(modif)
print(objet.cout_unitaire)

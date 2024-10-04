from src.flow.arborescence.arborescence import Arborescence
from src.variables import *

arb = Arborescence("Programme exemple")

print(arb.question.options[0].prerequis.europeanisation <= 0.)
print(arb.question.options[0].prerequis.niveau_techno)
print(arb.question.options[0].prerequis.niveau_techno <= 0.)

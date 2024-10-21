DATA_DIR = "src/flow/files"

EQUIPE = "equipe"

# Etat de l'équipe
ETAT = "Etat"
ARBORESCENCE = "arborescence"
QUESTION = "question"

# Colonnes arborescence
NUM_QUESTION = "num_question"
ANNEE = "annee" 
CONTEXTE_QUESTION = "contexte_question"
TEXTE_QUESTION = "texte_question"
NUMERO_OPTION = "numero_option"
TEXTE_OPTION = "texte_option"
PROCHAINE_QUESTION = "prochaine_question"
PREREQUIS = "prerequis"
EFFET_IMMEDIAT = "effet_immediat"
MODIFICATION_OBJET = "modification_objet"
MODIFICATION_PROGRAMME = "modification_programme"
OBJET = "objet"  # objet concerné par l'option. Un des objet de l'arbrescence
PROGRAMME = "programme" # programme concerné par l'option
COMMANDES = "commandes" # "launch_programme" ou "send_to_store"
IMAGE = "image"

# Attributs objets
NOM = "nom"
COUT_UNITAIRE = "cout_unitaire"
STD_COUT = "std_cout"
COUT_FIXE = "cout_fixe"
BONUS_TERRE = "bonus_terre"
BONUS_MER = "bonus_mer"
BONUS_AIR = "bonus_air"
BONUS_RENS = "bonus_rens"
MAX_NB_UTILE = "max_nb_utile"
UNITE_PAR_AN = "unite_par_an"
DEPENDANCE_EXPORT = "dependance_export"
MIN_NB_UTILE = "min_nb_utile"

# Attributs programmes
COUT = "cout"
DEBUT = "debut"
FIN = "fin"
DUREE = "duree"
# Compteurs
EUROPEANISATION = "europeanisation"
BUDGET = "budget"
NIVEAU_TECHNO = "niveau_techno"

# Variable
NOMBRE_UNITE = "nombre_unites"

# Fichiers
PROCHAINES_ARBORESCENCE = {
    "Drone d'attaque et de surveillance": "Fusil individuel",
    "Fusil individuel": None,
}
ARBORESCENCES = {
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/arborescences/arborescence_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/arborescences/arborescence_FIA.csv",
}
FICHIERS_OBJETS = {
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/objets/objets_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/objets/objets_FIA.csv",
}
FICHIERS_PROGRAMMES = {
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/programmes/programmes_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/programmes/programmes_FIA.csv",
}
IMAGE_DIR = f"{DATA_DIR}/images/"

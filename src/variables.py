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

# Armées
TERRE = "terre"
AIR = "air"
MER = "mer"
RENS = "rens"

# Variable
NOMBRE_UNITE = "nombre_unites"

# Fichiers
PROCHAINES_ARBORESCENCE = {
    "Frégate de lutte anti-sous-marine": "Satellites phase 1",
    "Satellites phase 1": "Drone d'attaque et de surveillance",
    "Drone d'attaque et de surveillance": "Fusil individuel",
    "Fusil individuel": "Satellites phase 2",
    "Satellites phase 2": "Dissuasion nucléaire",
    "Dissuasion nucléaire": "Radar aérien",
    "Radar aérien": None,
}
ARBORESCENCES = {
    "Frégate de lutte anti-sous-marine": f"{DATA_DIR}/arborescences/arborescence_FREMM.csv",
    "Satellites phase 1": f"{DATA_DIR}/arborescences/arborescence_satellite.csv",
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/arborescences/arborescence_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/arborescences/arborescence_FIA.csv",
    "Dissuasion nucléaire": f"{DATA_DIR}/arborescences/arborescence_DIS.csv",
    "Satellites phase 2": f"{DATA_DIR}/arborescences/arborescence_satellite.csv",
    "Radar aérien": f"{DATA_DIR}/arborescences/arborescence_RADAR.csv",
}
FICHIERS_OBJETS = {
    "Frégate de lutte anti-sous-marine": f"{DATA_DIR}/objets/objets_FREMM.csv",
    "Satellites phase 1": f"{DATA_DIR}/objets/objets_satellite.csv",
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/objets/objets_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/objets/objets_FIA.csv",
    "Dissuasion nucléaire": f"{DATA_DIR}/objets/objets_DIS.csv",
    "Satellites phase 2": f"{DATA_DIR}/objets/objets_satellite.csv",
    "Radar aérien": f"{DATA_DIR}/objets/objets_RADAR.csv",
}
FICHIERS_PROGRAMMES = {
    "Frégate de lutte anti-sous-marine": f"{DATA_DIR}/programmes/programmes_FREMM.csv",
    "Satellites phase 1": f"{DATA_DIR}/programmes/programmes_satellite.csv",
    "Drone d'attaque et de surveillance": f"{DATA_DIR}/programmes/programmes_MALE.csv",
    "Fusil individuel": f"{DATA_DIR}/programmes/programmes_FIA.csv",
    "Dissuasion nucléaire": f"{DATA_DIR}/programmes/programmes_DIS.csv",
    "Satellites phase 2": f"{DATA_DIR}/programmes/programmes_satellite.csv",
    "Radar aérien": f"{DATA_DIR}/programmes/programmes_RADAR.csv",
}
IMAGE_DIR = f"{DATA_DIR}/images/"

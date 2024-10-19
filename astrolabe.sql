-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : ven. 18 oct. 2024 à 18:45
-- Version du serveur : 10.11.9-MariaDB-ubu2204
-- Version de PHP : 8.2.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `astrolabe`
--

-- --------------------------------------------------------

--
-- Structure de la table `Armee`
--

CREATE TABLE `Armee` (
  `equipe` varchar(20) NOT NULL,
  `terre` int(11) NOT NULL,
  `air` int(11) NOT NULL,
  `mer` int(11) NOT NULL,
  `rens` int(11) NOT NULL,
  `annee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Constructions`
--

CREATE TABLE `Constructions` (
  `equipe` varchar(50) NOT NULL,
  `objet` varchar(50) NOT NULL,
  `debut` int(11) NOT NULL COMMENT 'année de début de construction (année de l''achat)',
  `fin` int(11) NOT NULL COMMENT 'Année de fin de la construction (dépend de l''année de début et du nombre d''objets)',
  `nombre_unites` int(11) NOT NULL COMMENT 'Nombre d''objets à construire'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Indicateurs`
--

CREATE TABLE `Indicateurs` (
  `equipe` varchar(20) NOT NULL,
  `europeanisation` int(11) NOT NULL,
  `niveau_techno` int(11) NOT NULL,
  `budget` int(11) NOT NULL,
  `annee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Structure de la table `Objets`
--

CREATE TABLE `Objets` (
  `equipe` varchar(50) NOT NULL,
  `nom` varchar(20) NOT NULL,
  `cout_unitaire` float DEFAULT NULL COMMENT 'Coût TOTAL d''un objet',
  `std_cout` float DEFAULT NULL COMMENT 'Appliqué au cout par unité',
  `cout_fixe` float DEFAULT NULL COMMENT 'Cout fixe par an tant que la production est en cours',
  `bonus_terre` int(11) DEFAULT NULL COMMENT 'Bonus par unité',
  `bonus_mer` int(11) DEFAULT NULL,
  `bonus_air` int(11) DEFAULT NULL,
  `bonus_rens` int(11) DEFAULT NULL,
  `max_nb_utile` int(11) DEFAULT NULL COMMENT 'Les bonus ne s''appliquent pas au delà de ce seuil',
  `unite_par_an` float DEFAULT NULL COMMENT 'Nombre d''unités qui peuvent être produites par an (pas forcément entier)',
  `budget` float DEFAULT NULL COMMENT 'Impact dur le budget par unité',
  `dependance_export` text DEFAULT NULL,
  `niveau_techno` float DEFAULT NULL,
  `annee` int(11) NOT NULL COMMENT 'Année à partir de laquelle il est possible d''acheter l''objet',
  `demande_armee` int(11) NOT NULL COMMENT 'Nombre d''unités demandées par l''armée'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Programmes`
--

CREATE TABLE `Programmes` (
  `equipe` varchar(50) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `cout` float DEFAULT NULL COMMENT 'Coût du programme par an',
  `std_cout` float DEFAULT NULL,
  `bonus_terre` int(11) DEFAULT NULL COMMENT 'Bonus rapporté par le programme par an',
  `bonus_mer` int(11) DEFAULT NULL,
  `bonus_air` int(11) DEFAULT NULL,
  `bonus_rens` int(11) DEFAULT NULL,
  `budget` float DEFAULT NULL COMMENT 'Apport du programme sur le budget par an (positif ou négatif)',
  `dependance_export` text DEFAULT NULL COMMENT 'Dépendances créées par le programme',
  `niveau_techno` float DEFAULT NULL COMMENT 'Impact du programme sur le niveau technologique (par an)',
  `duree` int(11) NOT NULL COMMENT 'Durée du programme (en années)',
  `debut` int(11) NOT NULL COMMENT 'Année de lancement du programme (attribut créé automatiquement par la webapp) NON MODIFIABLE',
  `fin` int(11) NOT NULL COMMENT 'Année de fin du programme (attribut créé automatiquement par la webapp lors du lancement du programme) NON MODIFIABLE'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Armee`
--
ALTER TABLE `Armee`
  ADD PRIMARY KEY (`equipe`,`annee`);

--
-- Index pour la table `Indicateurs`
--
ALTER TABLE `Indicateurs`
  ADD PRIMARY KEY (`equipe`,`annee`);

--
-- Index pour la table `Objets`
--
ALTER TABLE `Objets`
  ADD PRIMARY KEY (`equipe`,`nom`);

--
-- Index pour la table `Programmes`
--
ALTER TABLE `Programmes`
  ADD PRIMARY KEY (`equipe`,`nom`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

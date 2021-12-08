CREATE DATABASE IF NOT EXISTS trombinoscope;

USE trombinoscope;

CREATE TABLE IF NOT EXISTS genre (
    id_genre INT(11) NOT NULL AUTO_INCREMENT,
    genre VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(id_genre)
) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS statut (
    id_statut INT(11) NOT NULL AUTO_INCREMENT,
    qualification VARCHAR(256) NOT NULL UNIQUE,
    PRIMARY KEY(id_statut)
) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS personnes (
    id_personne INT(11) NOT NULL AUTO_INCREMENT,
    nom VARCHAR(256) NOT NULL,
    prenom VARCHAR(256) NOT NULL,
    photo VARCHAR(512),
    id_genre INT(11) NOT NULL,
    id_statut INT(11) NOT NULL,
    PRIMARY KEY(id_personne),
    UNIQUE(nom, prenom, id_genre),
    CONSTRAINT `personne_id_genre` FOREIGN KEY (`id_genre`) REFERENCES `genre`(`id_genre`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `personne_id_statut` FOREIGN KEY (`id_statut`) REFERENCES `statut`(`id_statut`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

INSERT INTO genre(genre)
    VALUES
    ('M.'),
    ('Mme.'),
    ('Mlle.');

INSERT INTO statut(qualification)
    VALUES
    ('Promo 1'),
    ('Promo 2'),
    ('Formateur'),
    ('Chargé de projet');

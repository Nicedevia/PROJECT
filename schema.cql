-- Active: 1714136785342@@127.0.0.1@3306
-- Création du Keyspace
CREATE KEYSPACE IF NOT EXISTS vitesse_data 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Sélection du Keyspace
USE vitesse_data;

-- Création de la table vitesse
CREATE TABLE IF NOT EXISTS vitesse (
    sensor_id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    speed FLOAT
);

-- Création de la table jour_ferie
CREATE TABLE IF NOT EXISTS jour_ferie (
    region TEXT,
    date DATE,
    holiday_name TEXT,
    PRIMARY KEY (region, date)
);

-- Création de la table limitation
CREATE TABLE IF NOT EXISTS limitation (
    sensor_id UUID PRIMARY KEY,
    speed_limit FLOAT
);

-- Création de la table meteo
CREATE TABLE IF NOT EXISTS meteo (
    sensor_id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT
);

# Analyse des Types de Paiement dans les Taxis de NYC

## Introduction
Ce projet vise à analyser les différents types de paiement utilisés dans les taxis de New York City. L'objectif est de fournir des insights utiles pour les chauffeurs et les gestionnaires de flottes afin d'optimiser leurs opérations et d'améliorer l'expérience client.

## Outils Utilisés
- **DBT Cloud** : Pour la transformation des données.
- **BigQuery** : Pour le stockage et l'interrogation des données.

## Objectifs
1. Vue globale des types de paiements:
    * Quels types sont les plus utilisés ?
    *  Lesquels génèrent le plus d’argent ?
2. L’évolution du type de paiement dans le temps: 
    * Evolution du type de paiement ?
    * Existence de Pattern de paiement dans l’année ?
3. Impact des zones sur le type de paiement :
    * Carte des zones/quartiers avec leur type de paiement
    * Aéroport + zone touristique 
4. Aller plus loin:
    * ML pour prédiction si trajet en cash ou carte
    * Voir outlier pour trajet de carte en cash
    * Covid ?


## Description des Données
Datas dans bigquery.
Les données utilisées pour cette analyse proviennent de la table `yellow_trip_data_2019_01`. Le projet comporte les tables semblables pour tout les mois de 2019 et les 6 premiers mois de 2020.
 Voici une description des colonnes principales de cette table :

- **VendorID** : Un code indiquant le fournisseur TPEP qui a fourni l'enregistrement. 1 = Creative Mobile Technologies, LLC; 2 = VeriFone Inc.
- **tpep_pickup_datetime** : La date et l'heure à laquelle le compteur a été engagé.
- **tpep_dropoff_datetime** : La date et l'heure à laquelle le compteur a été désengagé.
- **passenger_count** : Le nombre de passagers dans le véhicule. Il s'agit d'une valeur saisie par le conducteur.
- **trip_distance** : La distance du trajet en miles rapportée par le taximètre.
- **RatecodeID** : Le code tarifaire final en vigueur à la fin du trajet. 1 = Tarif standard, 2 = JFK, 3 = Newark, 4 = Nassau ou Westchester, 5 = Tarif négocié, 6 = Trajet de groupe.
- **store_and_fwd_flag** : Ce drapeau indique si l'enregistrement du trajet a été conservé en mémoire dans le véhicule avant d'être envoyé au fournisseur, c'est-à-dire "store and forward", car le véhicule n'avait pas de connexion au serveur. Y = trajet stocké et transmis, N = trajet non stocké et transmis.
- **PULocationID** : Zone de taxi TLC dans laquelle le taximètre a été engagé.
- **DOLocationID** : Zone de taxi TLC dans laquelle le taximètre a été désengagé.
- **payment_type** : Un code numérique indiquant comment le passager a payé le trajet. 1 = Carte de crédit, 2 = Espèces, 3 = Pas de frais, 4 = Litige, 5 = Inconnu, 6 = Trajet annulé.
- **fare_amount** : Le tarif calculé par le compteur en fonction du temps et de la distance.
- **extra** : Suppléments divers et surtaxes. Actuellement, cela inclut uniquement les frais de 0,50 $ et 1 $ pour les heures de pointe et les charges de nuit.
- **mta_tax** : Taxe MTA de 0,50 $ qui est automatiquement déclenchée en fonction du tarif au compteur en vigueur.
- **tip_amount** : Montant du pourboire – Ce champ est automatiquement rempli pour les pourboires par carte de crédit. Les pourboires en espèces ne sont pas inclus.
- **tolls_amount** : Montant total de tous les péages payés pendant le trajet.
- **improvement_surcharge** : Surtaxe d'amélioration de 0,30 $ appliquée aux trajets au moment du déclenchement du compteur. La surtaxe d'amélioration a commencé à être perçue en 2015.
- **total_amount** : Le montant total facturé aux passagers. N'inclut pas les pourboires en espèces.
- **congestion_surchage** : Le montant ajouté au prix pour congestion de traffic

Il existe également une table `taxi_zone_lookup`
avec comme colonnes:
- **LocationID** : Identifiant unique de la zone de taxi.
- **Borough** : Arrondissement de NYC où se trouve la zone de taxi.
- **Zone** : Nom de la zone de taxi.
- **service_zone** : Zone de service spécifique (ex. : aéroport, zone touristique).


## Étapes du Projet
### Partie 1 : Etude globale: 

1. **Extraction des Données** : Importer les données de BigQuery dans DBT Cloud.
2. **Transformation des Données** :
    - **Bronze Layer** : Importer les données brutes de chaque mois.
    - **Silver Layer** : Nettoyer et enrichir les données, ajouter une colonne `trip_id` unique et non nulle.
    - **Gold Layer** : Agréger les données par type de paiement et calculer les métriques.
3. **Analyse des Données** :
    - **gold_payment_summary** : Résumé des types de paiements, incluant le nombre de trajets et le montant total par type de paiement.
    - **gold_payment_trends** : Tendances des types de paiements au fil du temps.
4. **Visualisation des Résultats** : Créer des visualisations pour présenter les résultats de l'analyse.
5. **Recommandations** : Fournir des recommandations basées sur les insights obtenus.

## Conclusion
Cette analyse fournira des insights précieux pour les chauffeurs et les gestionnaires de flottes de taxis à NYC, leur permettant d'optimiser les types de paiement acceptés et d'améliorer l'expérience client.

## Auteurs
- Pierre Gosson


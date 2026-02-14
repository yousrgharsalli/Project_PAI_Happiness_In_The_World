# 🌍 Happiness Index Analyzer

**Happiness Index Analyzer** est une application de bureau interactive développée en Python.  
Elle permet d’explorer, de filtrer, de comparer et de visualiser les données du **World Happiness Report** à travers plusieurs années et indicateurs socio-économiques.

L’application repose sur :
- **Pandas** pour le traitement et le filtrage des données,
- **PyQt6** pour l’interface graphique,
- **Matplotlib** pour les graphiques classiques,
- **Plotly** pour la visualisation cartographique interactive.

---

##  Fonctionnalités principales

L’application est organisée en **trois onglets complémentaires**, chacun répondant à un objectif d’analyse spécifique.

### 1. Onglet *Vue d’ensemble* (Exploration par pays)
Cet onglet est dédié à l’analyse descriptive et au filtrage détaillé des données.

- **Filtres avancés** :
  - Année, Région, Pays
  - Bornes min/max sur tous les indicateurs (Score de bonheur, PIB, Famille, Espérance de vie, Liberté, Confiance, Générosité)
- **Tableau interactif** affichant les données filtrées
- **Graphiques dynamiques** :
  - Répartition régionale
  - Distribution des scores de bonheur
- Mise à jour automatique des visualisations en fonction des filtres sélectionnés

---

### 2. Onglet *Comparaison*
Cet onglet permet de comparer plusieurs pays afin d’identifier des tendances et des corrélations.

- **Nuage de points (Scatter plot)** pour analyser la relation entre deux indicateurs
- **Courbes temporelles (Line chart)** pour suivre l’évolution d’un indicateur au fil des années
- **Sélection multiple de pays** pour une comparaison simultanée

---

### 3. Onglet *Carte interactive*
Cet onglet propose une **visualisation géographique interactive** des données à l’échelle mondiale.

- Carte du monde interactive (zoom, déplacement, info-bulles)
- **Highlight automatique des pays** correspondant aux filtres sélectionnés
- Coloration des pays selon un indicateur (ex : Score de bonheur)
- Infobulles affichant les principales données du pays sélectionné
- Basé sur **Plotly** et intégré dans l’interface PyQt via un composant web

---

## Technologies utilisées

- **Python 3**
- **PyQt6** : interface graphique (fenêtres, onglets, widgets)
- **Pandas** : chargement, nettoyage et filtrage du fichier CSV
- **Matplotlib** : graphiques statistiques intégrés
- **Plotly** : visualisation cartographique interactive
- **PyQt6-WebEngine** : intégration de contenu web interactif
- **GitHub Actions** : vérification automatique de l’installation et des imports

---

## 📂 Structure du Projet

Voici une brève description des fichiers source :

* `main.py` : Point d'entrée de l'application. Initialise la fenêtre principale et charge les onglets.
* `data_manager.py` : Gère le chargement du fichier CSV, le nettoyage des colonnes et la logique de filtrage des données.
* `happiness.csv` : Le jeu de données source (délimiteur `;`).
* **Interface (UI)**
    * `tab_country.py` : Logique et mise en page de l'onglet "Exploration".
    * `tab_comparison.py` : Logique et mise en page de l'onglet "Comparaison".
    * `tab_map_interactive.py`: Logique et mise en page de l'onglet "Carte".
* **Graphiques**
    * `graph_base.py` : Classe mère configurant le canevas Matplotlib pour PyQt.
    * `graph_country.py` : Gère les graphiques de l'onglet Exploration (Pie, Hist).
    * `graph_compare.py` : Gère les graphiques de l'onglet Comparaison (Scatter, Line).

## ⚙️ Installation et Lancement
###  Prérequis
- Python 3.10 ou supérieur
- Environnement virtuel recommandé


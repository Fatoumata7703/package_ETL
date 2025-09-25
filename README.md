# ETL Cacao - Pipeline Data Engineering

**Projet par Fatoumata Siby**

Un projet complet de Data Engineering avec un **notebook Jupyter** pour le pipeline ETL et un **site web Flask moderne** pour visualiser les résultats.

## Vue d'ensemble

Ce projet analyse les données de **1,795 barres de chocolat** extraites depuis le site Codecademy. Il combine :
1. **`my_pipe.ipynb`** : Pipeline ETL complet et modulaire
2. **Site Flask** : Dashboard web moderne avec thème bleu/blanc

## Pipeline ETL

### Source des données
- **Site** : [Codecademy Cacao Ratings](https://content.codecademy.com/courses/beautifulsoup/cacao/index.html)
- **Données** : 1,795 barres de chocolat avec évaluations de 1 à 5
- **Colonnes** : Company, Specific Bean Origin, REF, Review Date, Cocoa Percent, Company Location, Rating, Bean Type, Broad Bean Origin

### 5 Grandes étapes de transformation

1. **Extraction** : Web scraping avec BeautifulSoup
2. **Nettoyage** : Suppression des caractères spéciaux et normalisation
3. **Conversion Types** : Transformation des pourcentages et dates
4. **Uniformisation** : Standardisation des chaînes de caractères
5. **Contrôle Qualité** : Imputation des valeurs manquantes et validation

### Structure des datasets
- **`data/raw/cacao_raw.csv`** : Données brutes extraites (avec caractères spéciaux)
- **`data/interim/cacao_interim.csv`** : Données après nettoyage (valeurs manquantes)
- **`data/processed/cacao_clean.csv`** : Dataset final prêt pour l'analyse

## Site Web Dashboard

### Design moderne
- **Thème** : Bleu et blanc avec dégradés élégants
- **Style** : Dashboard futuriste avec animations fluides
- **Responsive** : Adaptatif pour tous les écrans

### Fonctionnalités
- **Dashboard principal** : Vue d'ensemble du projet ETL
- **Page Datasets** : Aperçu et téléchargement des 3 datasets
- **Page Transformations** : Visualisation détaillée du pipeline ETL
- **Modales interactives** : Aperçu des données avec tables
- **Animations** : Effets visuels et particules flottantes

## Installation et utilisation

### 1. Installation
```bash
git clone https://github.com/fatoumatasiby/etl-cacao
cd etl-cacao
pip install -r requirements.txt
```

### 2. Exécution du pipeline ETL
```bash
jupyter notebook my_pipe.ipynb
# Exécuter toutes les cellules dans l'ordre
```

### 3. Lancement du site web
```bash
python app.py
# Ouvrir http://localhost:5000
```

## Structure du projet

```
etl-cacao/
├── my_pipe.ipynb              # Pipeline ETL principal
├── app.py                     # Application Flask
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation
│
├── templates/                 # Templates HTML
│   ├── index.html            # Dashboard principal
│   ├── datasets.html         # Page des datasets
│   └── transformations.html  # Page des transformations
│
├── static/                    # Fichiers statiques
│   └── css/
│       └── dashboard.css     # Style bleu/blanc moderne
│
├── data/                      # Datasets (générés par le notebook)
│   ├── raw/                  # Données brutes
│   ├── interim/              # Données nettoyées
│   └── processed/            # Données finales
│
└── modules/                   # Modules ETL (utilisés par le notebook)
    ├── extraction/           # Web scraping
    ├── transformation/       # Nettoyage et conversion
    ├── imputation/          # Gestion des valeurs manquantes
    └── package_exploration_data/  # Analyse des données
```

## Technologies utilisées

### Backend
- **Python 3.9+** : Langage principal
- **Pandas** : Manipulation des données
- **BeautifulSoup4** : Web scraping
- **Flask** : Framework web

### Frontend
- **HTML5/CSS3** : Structure et style
- **JavaScript ES6+** : Interactions
- **Font Awesome** : Icônes
- **Google Fonts** : Typographie (Inter, JetBrains Mono)

### Data Engineering
- **Jupyter Notebook** : Développement ETL
- **NumPy** : Calculs numériques


## Workflow complet

```
Web Scraping → Nettoyage → Conversion → Uniformisation → Contrôle Qualité
     ↓              ↓           ↓            ↓              ↓
  data/raw/    data/interim/  data/processed/  →  Site Web Flask
```

## Fonctionnalités du site

### Dashboard principal
- Présentation du projet ETL Cacao
- Pipeline visuel avec 5 étapes
- Statistiques des datasets
- Navigation vers les pages détaillées

### Page Datasets
- Aperçu des 3 datasets (brut, nettoyé, final)
- Modales interactives avec tables de données
- Boutons de téléchargement
- Statistiques détaillées

### Page Transformations
- Visualisation des 5 grandes étapes
- Détails des sous-étapes
- Exemples de transformations
- Pipeline visuel complet

## Déploiement

### Local
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Projet Data Engineering Complet** - Pipeline ETL + Dashboard Web Moderne

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/fatoumatasiby/etl-cacao)
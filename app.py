#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL CACAO - LE PLUS BEAU SITE DU MONDE
Pipeline Data Engineering pour l'analyse des données de cacao
"""

from flask import Flask, render_template, send_file, jsonify, request
import os
import pandas as pd
import json
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'etl_cacao_secret_key_2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Chemins des datasets
DATASETS_PATH = {
    'raw': 'data/raw/cacao_raw.csv',
    'interim': 'data/interim/cacao_interim.csv',
    'clean': 'data/processed/cacao_clean.csv'
}

# ===========================================
# ROUTES PRINCIPALES
# ===========================================

@app.route('/')
def index():
    """Page d'accueil - Dashboard futuriste ETL Cacao"""
    logger.info(" Accès au dashboard principal")
    return render_template('index.html')

@app.route('/datasets')
def datasets():
    """Page des datasets - Dashboard futuriste"""
    logger.info(" Accès à la page des datasets")
    return render_template('datasets.html')

@app.route('/transformations')
def transformations():
    """Page des transformations - Dashboard futuriste"""
    logger.info(" Accès à la page des transformations")
    return render_template('transformations.html')


@app.route('/api/datasets')
def get_datasets():
    """API pour récupérer les informations des datasets"""
    try:
        datasets_info = {}
        
        for dataset_type, file_path in DATASETS_PATH.items():
            if os.path.exists(file_path):
                # Lire le fichier CSV
                df = pd.read_csv(file_path)
                
                # Calculer la taille du fichier
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                
                datasets_info[dataset_type] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'size': f"{size_mb:.1f} MB",
                    'columns_list': df.columns.tolist(),
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                    'dtypes': df.dtypes.astype(str).to_dict()
                }
            else:
                datasets_info[dataset_type] = {
                    'error': f"Fichier {file_path} non trouvé",
                    'rows': 0,
                    'columns': 0,
                    'size': '0 MB'
                }
        
        return jsonify({
            'success': True,
            'datasets': datasets_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f" Erreur lors de la récupération des datasets: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset/<dataset_type>')
def get_dataset_preview(dataset_type):
    """API pour récupérer un aperçu d'un dataset"""
    try:
        if dataset_type not in DATASETS_PATH:
            return jsonify({'error': 'Type de dataset invalide'}), 400
        
        file_path = DATASETS_PATH[dataset_type]
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Fichier non trouvé'}), 404
        
        # Lire le dataset
        df = pd.read_csv(file_path)
        
        # Récupérer les 10 premières lignes
        preview_data = df.head(10).to_dict('records')
        
        return jsonify({
            'success': True,
            'dataset_type': dataset_type,
            'filename': os.path.basename(file_path),
            'rows': len(df),
            'columns': len(df.columns),
            'columns_list': df.columns.tolist(),
            'preview_data': preview_data,
            'dtypes': df.dtypes.astype(str).to_dict()
        })
        
    except Exception as e:
        logger.error(f" Erreur lors de la récupération du dataset {dataset_type}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<dataset_type>')
def download_dataset(dataset_type):
    """Téléchargement d'un dataset"""
    try:
        if dataset_type not in DATASETS_PATH:
            return jsonify({'error': 'Type de dataset invalide'}), 400
        
        file_path = DATASETS_PATH[dataset_type]
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Fichier non trouvé'}), 404
        
        logger.info(f" Téléchargement du dataset {dataset_type}")
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"cacao_{dataset_type}.csv",
            mimetype='text/csv'
        )
        
    except Exception as e:
        logger.error(f" Erreur lors du téléchargement du dataset {dataset_type}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/pipeline/status')
def get_pipeline_status():
    """API pour récupérer le statut du pipeline ETL"""
    try:
        pipeline_status = {
            'extract': {
                'status': 'completed',
                'description': 'Web scraping terminé',
                'records': 1795,
                'timestamp': '2024-01-15T10:30:00Z'
            },
            'transform': {
                'status': 'completed',
                'description': 'Transformation des données terminée',
                'steps': [
                    'Nettoyage des caractères',
                    'Conversion des types',
                    'Uniformisation des pays',
                    'Imputation des valeurs manquantes'
                ],
                'timestamp': '2024-01-15T10:45:00Z'
            },
            'load': {
                'status': 'completed',
                'description': 'Chargement final terminé',
                'final_records': 1795,
                'duplicates_removed': 0,
                'timestamp': '2024-01-15T11:00:00Z'
            }
        }
        
        return jsonify({
            'success': True,
            'pipeline': pipeline_status,
            'overall_status': 'completed',
            'last_run': '2024-01-15T11:00:00Z'
        })
        
    except Exception as e:
        logger.error(f" Erreur lors de la récupération du statut du pipeline: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/transformations')
def get_transformations():
    """API pour récupérer les détails des transformations"""
    try:
        transformations = {
            'character_cleaning': {
                'name': 'Nettoyage des Caractères',
                'description': 'Suppression des caractères de contrôle, spéciaux et correction des problèmes d\'encodage',
                'steps': [
                    'Détection des caractères de contrôle',
                    'Suppression des caractères spéciaux (*, +)',
                    'Correction des problèmes d\'encodage (Nave → Naive)',
                    'Uniformisation des chaînes de caractères'
                ],
                'files_affected': ['Company', 'Origine spécifique du harirot', 'Type de fève'],
                'records_modified': 6
            },
            'type_conversion': {
                'name': 'Conversion des Types',
                'description': 'Transformation des types de données pour optimiser l\'analyse',
                'steps': [
                    'Suppression du symbole % et conversion en float',
                    'Conversion des dates et REF en int',
                    'Uniformisation des noms de pays',
                    'Validation des types de données'
                ],
                'files_affected': ['Pourcentage de cacao', 'Date de la revue', 'REF', 'Broad Bean Origin'],
                'records_modified': 1795
            },
            'missing_values': {
                'name': 'Imputation des Valeurs Manquantes',
                'description': 'Gestion intelligente des valeurs manquantes selon leur proportion',
                'steps': [
                    'Analyse des valeurs manquantes par colonne',
                    'Type de fève: 888 valeurs (49.5%) → "Unknown"',
                    'Broad Bean Origin: 74 valeurs (4.1%) → Mode "Venezuela"',
                    'Validation de la distribution finale'
                ],
                'files_affected': ['Type de fève', 'Broad Bean Origin'],
                'records_modified': 962
            },
            'quality_check': {
                'name': 'Contrôle Qualité Final',
                'description': 'Validation finale de la qualité des données',
                'steps': [
                    'Vérification des doublons (0 trouvé)',
                    'Contrôle de la cohérence des données',
                    'Validation des types de données',
                    'Génération du dataset final'
                ],
                'files_affected': 'Toutes les colonnes',
                'records_modified': 1795
            }
        }
        
        return jsonify({
            'success': True,
            'transformations': transformations,
            'total_steps': len(transformations),
            'pipeline_duration': '30 minutes'
        })
        
    except Exception as e:
        logger.error(f" Erreur lors de la récupération des transformations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# ROUTES D'ERREUR
# ===========================================

@app.errorhandler(404)
def not_found(error):
    """Page 404 personnalisée"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Page 500 personnalisée"""
    logger.error(f" Erreur interne: {error}")
    return jsonify({
        'success': False,
        'error': 'Erreur interne du serveur'
    }), 500

# ===========================================
# FONCTIONS UTILITAIRES
# ===========================================

def check_datasets_exist():
    """Vérifier que tous les datasets existent"""
    missing_files = []
    
    for dataset_type, file_path in DATASETS_PATH.items():
        if not os.path.exists(file_path):
            missing_files.append(f"{dataset_type}: {file_path}")
    
    if missing_files:
        logger.warning(f" Fichiers manquants: {missing_files}")
        return False
    
    logger.info(" Tous les datasets sont présents")
    return True

def get_dataset_stats(file_path):
    """Récupérer les statistiques d'un dataset"""
    try:
        if not os.path.exists(file_path):
            return None
        
        df = pd.read_csv(file_path)
        file_size = os.path.getsize(file_path)
        
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'size_bytes': file_size,
            'size_mb': file_size / (1024 * 1024),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'null_counts': df.isnull().sum().to_dict()
        }
    except Exception as e:
        logger.error(f" Erreur lors de l'analyse du dataset {file_path}: {e}")
        return None

# ===========================================
# INITIALISATION
# ===========================================

def initialize_app():
    """Initialisation de l'application"""
    logger.info(" Initialisation de ETL Cacao...")
    
    # Vérifier les datasets
    if not check_datasets_exist():
        logger.warning(" Certains datasets sont manquants")
    
    # Créer les dossiers nécessaires
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/interim', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    logger.info(" ETL Cacao initialisé avec succès!")

# Initialiser l'application au démarrage
initialize_app()

# ===========================================
# LANCEMENT DE L'APPLICATION
# ===========================================

if __name__ == '__main__':
    print("""
     ETL CACAO - LE PLUS BEAU SITE DU MONDE
    ==========================================
    
     Démarrage du serveur Flask...
     Pipeline Data Engineering pour le cacao
     Site: http://localhost:5000
    
    """)
    
    # Vérifier les datasets au démarrage
    check_datasets_exist()
    
    # Lancer l'application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

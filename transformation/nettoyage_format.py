import pandas as pd
import numpy as np
import re
from datetime import datetime

class NettoyeurFormat:
    """
    Cette classe permet de nettoyer et uniformiser les formats de données
    - Suppression des % et conversion en float
    - Formatage des dates
    - Uniformisation des chaînes (capitalisation)
    """
    
    @staticmethod
    def nettoyer_pourcentages(df, colonne='Cocoa Percent'):
        """
        Supprime le symbole % et convertit en float
        
        Args:
            df (DataFrame): DataFrame à nettoyer
            colonne (str): Nom de la colonne contenant les pourcentages
            
        Returns:
            DataFrame: DataFrame avec la colonne transformée
        """
        df_clean = df.copy()
        
        if colonne in df_clean.columns:
            print(f"🔄 Nettoyage des pourcentages dans '{colonne}'...")
            
            # Compter les valeurs avant transformation
            valeurs_avant = df_clean[colonne].value_counts().head(5)
            
            # Supprimer le symbole % et convertir en float
            df_clean[colonne] = df_clean[colonne].astype(str).str.replace('%', '').astype(float)
            
            print(f"✅ Pourcentages nettoyés - Exemples: {valeurs_avant.head(3).to_dict()}")
            
        return df_clean
    
    @staticmethod
    def nettoyer_dates(df, colonne='Review Date'):
        """
        Uniformise le format des dates
        
        Args:
            df (DataFrame): DataFrame à nettoyer
            colonne (str): Nom de la colonne contenant les dates
            
        Returns:
            DataFrame: DataFrame avec les dates formatées
        """
        df_clean = df.copy()
        
        if colonne in df_clean.columns:
            print(f"🔄 Nettoyage des dates dans '{colonne}'...")
            
            # Compter les valeurs avant transformation
            valeurs_avant = df_clean[colonne].value_counts().head(5)
            
            # Convertir en datetime si ce n'est pas déjà fait
            df_clean[colonne] = pd.to_datetime(df_clean[colonne], errors='coerce')
            
            # Formater en YYYY-MM-DD
            df_clean[colonne] = df_clean[colonne].dt.strftime('%Y-%m-%d')
            
            print(f"✅ Dates nettoyées - Exemples: {valeurs_avant.head(3).to_dict()}")
            
        return df_clean
    
    @staticmethod
    def uniformiser_chaines(df, colonnes_texte=None):
        """
        Uniformise la capitalisation des chaînes de caractères
        
        Args:
            df (DataFrame): DataFrame à nettoyer
            colonnes_texte (list): Liste des colonnes à uniformiser
            
        Returns:
            DataFrame: DataFrame avec les chaînes uniformisées
        """
        df_clean = df.copy()
        
        if colonnes_texte is None:
            # Colonnes texte par défaut
            colonnes_texte = ['Company', 'Company Location', 'Bean Type', 'Broad Bean Origin', 'Specific Bean Origin or Bar Name']
        
        print("🔄 Uniformisation des chaînes de caractères...")
        
        for colonne in colonnes_texte:
            if colonne in df_clean.columns:
                # Compter les valeurs avant transformation
                valeurs_avant = df_clean[colonne].value_counts().head(3)
                
                # Uniformiser la capitalisation (première lettre majuscule)
                df_clean[colonne] = df_clean[colonne].astype(str).str.title()
                
                print(f"   ✅ {colonne}: {valeurs_avant.head(2).to_dict()}")
        
        return df_clean
    
    @staticmethod
    def nettoyer_format_complet(df):
        """
        Effectue un nettoyage complet du format
        
        Args:
            df (DataFrame): DataFrame à nettoyer
            
        Returns:
            DataFrame: DataFrame complètement nettoyé
        """
        print("🚀 DÉMARRAGE DU NETTOYAGE DE FORMAT COMPLET")
        print("=" * 50)
        
        df_clean = df.copy()
        
        # 1. Nettoyer les pourcentages
        df_clean = NettoyeurFormat.nettoyer_pourcentages(df_clean)
        
        # 2. Nettoyer les dates
        df_clean = NettoyeurFormat.nettoyer_dates(df_clean)
        
        # 3. Uniformiser les chaînes
        df_clean = NettoyeurFormat.uniformiser_chaines(df_clean)
        
        print("=" * 50)
        print("✅ NETTOYAGE DE FORMAT TERMINÉ")
        print(f"📊 DataFrame final: {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes")
        
        return df_clean

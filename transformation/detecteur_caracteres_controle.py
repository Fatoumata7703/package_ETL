"""
Module de détection des caractères de contrôle
Classe pour détecter les caractères de contrôle
"""

import pandas as pd
import unicodedata

class DetecteurCaracteresControle:
    """
    Cette classe permet de détecter les caractères de contrôle dans un DataFrame
    """
    
    @staticmethod
    def detecter_caracteres_controle(df):
        """
        Cette fonction détecte les caractères de contrôle et les supprime
        
        Arguments
        ---------------
            df: pd.DataFrame, la base de données à analyser
        
        Return
        ----------------
            df_clean : pd.DataFrame, le DataFrame nettoyé
        """
        
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame")
        
        if df.empty:
            return df
        
        # Copier le DataFrame pour ne pas modifier l'original
        df_clean = df.copy()
        colonnes_problematiques = []
        
        # Analyser chaque colonne
        for col in df_clean.columns:
            colonne = df_clean[col]
            caracteres_controle_trouves = False
            
            # Analyser chaque valeur non vide
            for idx, valeur in colonne.items():
                if pd.notna(valeur) and str(valeur).strip() != '':
                    text = str(valeur)
                    
                    # Détecter et supprimer les caractères de contrôle
                    text_clean = ""
                    for char in text:
                        category = unicodedata.category(char)
                        if category[0] == 'C' and char not in '\n\r\t':
                            caracteres_controle_trouves = True
                        else:
                            text_clean += char
                    
                    # Mettre à jour la valeur si des caractères ont été supprimés
                    if caracteres_controle_trouves:
                        df_clean.at[idx, col] = text_clean
            
            # Enregistrer les colonnes problématiques
            if caracteres_controle_trouves:
                colonnes_problematiques.append(col)
        
        # Afficher le résumé
        if colonnes_problematiques:
            print(f"Caractères de contrôle détectés et supprimés dans les colonnes: {', '.join(colonnes_problematiques)}")
        else:
            print("Aucun caractère de contrôle détecté - DataFrame propre")
        
        return df_clean
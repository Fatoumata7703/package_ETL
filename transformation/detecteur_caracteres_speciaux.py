"""
Module de détection des caractères spéciaux
Classe pour détecter et supprimer les caractères spéciaux
"""

import pandas as pd
import re

class DetecteurCaracteresSpeciaux:
    """
    Cette classe permet de détecter et supprimer les caractères spéciaux dans un DataFrame
    """
    
    @staticmethod
    def detecter_caracteres_speciaux(df, caracteres_cibles=None):
        """
        Cette fonction détecte et supprime les caractères spéciaux au début et à la fin des chaînes
        
        Arguments
        ---------------
            df: pd.DataFrame, la base de données à analyser
            caracteres_cibles: list, liste des caractères spéciaux à supprimer (ex: ['#', '@', '$', '%'])
        
        Return
        ----------------
            df_clean : pd.DataFrame, le DataFrame nettoyé
        """
        
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame")
        
        if df.empty:
            return df
        
        # Caractères spéciaux par défaut si non spécifiés
        if caracteres_cibles is None:
            caracteres_cibles = ['#', '@', '$', '&', '*', '+', '=', '|', '\\', '/', '?', '!', '~', '`', '^', '°']
        
        # Copier le DataFrame pour ne pas modifier l'original
        df_clean = df.copy()
        colonnes_problematiques = []
        
        # Analyser chaque colonne
        for col in df_clean.columns:
            colonne = df_clean[col]
            caracteres_speciaux_trouves = False
            details_suppression = []
            
            # Analyser chaque valeur non vide
            for idx, valeur in colonne.items():
                if pd.notna(valeur) and str(valeur).strip() != '':
                    text = str(valeur).strip()
                    text_original = text
                    caracteres_debut = []
                    caracteres_fin = []
                    
                    # Supprimer les caractères spéciaux au début
                    while text and text[0] in caracteres_cibles:
                        caracteres_debut.append(text[0])
                        text = text[1:]
                        caracteres_speciaux_trouves = True
                    
                    # Supprimer les caractères spéciaux à la fin
                    while text and text[-1] in caracteres_cibles:
                        caracteres_fin.append(text[-1])
                        text = text[:-1]
                        caracteres_speciaux_trouves = True
                    
                    # Enregistrer les détails de suppression
                    if caracteres_debut or caracteres_fin:
                        detail = f"Ligne {idx}: '{text_original}'"
                        if caracteres_debut:
                            detail += f" (début: {''.join(caracteres_debut)})"
                        if caracteres_fin:
                            detail += f" (fin: {''.join(caracteres_fin)})"
                        details_suppression.append(detail)
                    
                    # Mettre à jour la valeur si des caractères ont été supprimés
                    if text != text_original:
                        df_clean.at[idx, col] = text
            
            # Enregistrer les colonnes problématiques avec détails
            if caracteres_speciaux_trouves:
                colonnes_problematiques.append({
                    'colonne': col,
                    'details': details_suppression[:3]  # Limiter à 3 exemples
                })
        
        # Afficher le résumé détaillé
        if colonnes_problematiques:
            print("Caractères spéciaux détectés et supprimés:")
            for col_info in colonnes_problematiques:
                print(f"  Colonne '{col_info['colonne']}':")
                for detail in col_info['details']:
                    print(f"    - {detail}")
                if len(col_info['details']) == 3:
                    print(f"    - ... et autres")
        else:
            print("Aucun caractère spécial détecté - DataFrame propre")
        
        return df_clean
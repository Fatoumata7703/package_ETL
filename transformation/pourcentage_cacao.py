"""
Module de transformation du pourcentage de cacao
Classe pour nettoyer la colonne 'Pourcentage de cacao'
"""

import pandas as pd

class TransformateurPourcentageCacao:
    """
    Cette classe permet de transformer la colonne 'Pourcentage de cacao'
    en supprimant le caractère '%' et en convertissant en float
    """
    
    @staticmethod
    def transformer_pourcentage(df, colonne="Pourcentage de cacao"):
        """
        Supprime le symbole '%' et convertit la colonne en float
        
        Arguments
        ---------------
            df: pd.DataFrame, la base de données à transformer
            colonne: str, nom de la colonne contenant les pourcentages
        
        Return
        ----------------
            df_clean : pd.DataFrame, le DataFrame avec la colonne transformée
        """
        
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame")
        
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' n'existe pas dans le DataFrame")
        
        # Copier le DataFrame
        df_clean = df.copy()
        
        # Supprimer le % et convertir en float
        df_clean[colonne] = (
            df_clean[colonne]
            .astype(str)       # conversion en string pour manipuler
            .str.replace("%", "", regex=False)  # enlever le %
            .str.strip()       # enlever espaces éventuels
        )
        
        # Conversion en float (gestion des erreurs)
        df_clean[colonne] = pd.to_numeric(df_clean[colonne], errors="coerce")
        
        print(f"Colonne '{colonne}' transformée : % supprimé et valeurs converties en float.")
        
        return df_clean

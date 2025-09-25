# transformation/imputation_autre.py

import pandas as pd

class ImputationAutre:
    """
    Classe pour imputer les valeurs manquantes d'une colonne
    catégorielle par la modalité 'Autre'.
    """

    @staticmethod
    def imputer_colonne(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
        """
        Impute les valeurs manquantes d'une seule colonne par 'Autre'.

        Arguments
        ---------------
        df : pd.DataFrame
        colonne : str, nom de la colonne à imputer

        Return
        ---------------
        df_clean : pd.DataFrame avec la colonne imputée
        """
        if colonne not in df.columns:
            raise ValueError(f"Colonne '{colonne}' introuvable dans le DataFrame")

        df_clean = df.copy()
        df_clean[colonne] = df_clean[colonne].fillna("Autre")  # remplace NaN par "Autre"

        return df_clean

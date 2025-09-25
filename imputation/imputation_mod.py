# transformation/imputation_mode.py

import pandas as pd

class ImputationMode:
    """
    Classe pour imputer les valeurs manquantes d'une colonne
    catégorielle par la valeur la plus fréquente (mode).
    """

    @staticmethod
    def imputer_colonne(df: pd.DataFrame, colonne: str):
        """
        Impute les valeurs manquantes d'une seule colonne par le mode.

        Arguments
        ---------------
        df : pd.DataFrame
            Le DataFrame à traiter.
        colonne : str
            Nom de la colonne à imputer.

        Return
        ---------------
        df_clean : pd.DataFrame
            DataFrame avec la colonne imputée
        """
        if colonne not in df.columns:
            raise ValueError(f"Colonne '{colonne}' introuvable dans le DataFrame")

        df_clean = df.copy()
        mode_val = df_clean[colonne].mode()[0]  # valeur la plus fréquente
        df_clean[colonne] = df_clean[colonne].fillna(mode_val)

        return df_clean

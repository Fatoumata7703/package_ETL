import pandas as pd


class Normalise:
    """
    Cette classe permet de calculer le nombre de valeurs manquantes
    """

    @staticmethod
    def min_max_normalize(df, col):
        """
            Normalise les valeurs d'une colonne d'un DataFrame en utilisant la normalisation min-max.

            Formule utilisée :
                x_norm = (x - x_min) / (x_max - x_min)

            Arguments
            ---------------
            df : pd.DataFrame
                Le DataFrame contenant la colonne à normaliser.
            col : str
                Le nom de la colonne à normaliser.

            Return
            ----------------
            df : pd.DataFrame
                Le DataFrame avec la colonne normalisée (valeurs entre 0 et 1).
        """

        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

        return df
    

    




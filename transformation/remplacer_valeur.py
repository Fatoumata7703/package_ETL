import pandas as pd
import numpy as np

class Nettoyeur:
    """
    Cette classe permet de nettoyer un DataFrame en remplaçant
    les cellules vides ou remplies uniquement d'espaces par NaN.
    """

    @staticmethod
    def clean_empty_cells(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remplace toutes les chaînes vides, espaces, ou valeurs uniquement
        composées de blancs par NaN dans un DataFrame.

        Arguments
        ---------------
            df : pd.DataFrame
                Le DataFrame à nettoyer.

        Return
        ---------------
            df : pd.DataFrame
                Le DataFrame nettoyé avec les cellules vides remplacées par NaN.
        """
        return df.replace(r'^\s*$', np.nan, regex=True)

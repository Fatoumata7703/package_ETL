import pandas as pd

class TypeColonne:
    """
    Cette classe permet de convertir une ou plusieurs colonnes d'un DataFrame
    vers un type donné.
    """

    @staticmethod
    def convertir_colonnes(df: pd.DataFrame, colonnes, dtype) -> pd.DataFrame:
        """
        Convertit une ou plusieurs colonnes du DataFrame vers le type spécifié.

        Arguments
        ---------------
        df : pd.DataFrame
            Le DataFrame à traiter.
        colonnes : str ou list
            Le nom de la colonne ou la liste de colonnes à convertir.
        dtype : type
            Le type vers lequel convertir les colonnes (ex: int, float, 'category').

        Return
        ----------------
        df : pd.DataFrame
            Le DataFrame avec les colonnes converties.
        """
        if isinstance(colonnes, str):
            colonnes = [colonnes]

        for col in colonnes:
            if col not in df.columns:
                raise ValueError(f"La colonne '{col}' n'existe pas dans le DataFrame.")
            df[col] = df[col].astype(dtype)

        return df

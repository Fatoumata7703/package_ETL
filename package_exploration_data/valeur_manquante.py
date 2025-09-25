import pandas as pd


class ValeurManquante:
    """
    Cette classe permet de calculer le nombre de valeurs manquantes
    """

    @staticmethod
    def calcul_valeur_manquante(df: pd.DataFrame):
        """
        Cette fonction calcule les valeurs manquantes

        Arguments
        ---------------
            df: pd.DataFrame , la base de données de l'étude

        Return
        ----------------
          res : (int) , le nombre total de valeurs manquantes.
        """

        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame")
        
        if df.empty:  
            return pd.DataFrame()
        
        res = df.isnull().sum()

        return res 

    
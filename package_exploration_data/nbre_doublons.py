import pandas as pd


class NbreDoublons:
    """
    Cette classe permet de calculer le nombre de valeurs manquantes
    """

    @staticmethod
    def calcul_nbre_doublons(df: pd.DataFrame):
        """
        Cette fonction calcule les doublons

        Arguments
        ---------------
            df: pd.DataFrame , la base de données de l'étude

        Return
        ----------------
          res : (int) , le nombre total de  doublons.
        """

        doublon= df.duplicated().sum()
        

        return doublon


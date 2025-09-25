# transformation/uniformiser_pays.py

import pandas as pd

class UniformiserPays:
    """
    Classe pour uniformiser l'écriture des pays :
    - Exceptions en majuscules (ex: 'U.S.A.', 'UK')
    - Chaque mot d'un pays composé avec majuscule (ex: 'New Zealand')
    - Un mot seul : première lettre majuscule
    """

    @staticmethod
    def uniformiser(df, colonnes, exceptions=None):
        """
        Uniformise les colonnes contenant des pays.

        Arguments
        ---------------
            df : pd.DataFrame
            colonnes : list, liste des colonnes à traiter
            exceptions : list, valeurs à garder en majuscules (ex: ['U.S.A.', 'UK'])

        Return
        ---------------
            df_clean : pd.DataFrame
        """

        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame")

        df_clean = df.copy()

        # Exceptions par défaut
        if exceptions is None:
            exceptions = ["U.S.A.", "USA", "U.K.", "UK", "UAE", "U.A.E."]

        def nettoyer_pays(val):
            if pd.isna(val) or str(val).strip() == "":
                return val

            val = str(val).strip()

            # Cas exceptionnels → retour direct
            if val in exceptions:
                return val

            # Découper par espace et mettre en majuscule chaque mot
            mots = val.split()
            mots_nettoyes = [mot.capitalize() for mot in mots]

            return " ".join(mots_nettoyes)

        # Appliquer à chaque colonne
        for col in colonnes:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(nettoyer_pays)
            else:
                print(f"Colonne '{col}' introuvable dans le DataFrame")

        return df_clean

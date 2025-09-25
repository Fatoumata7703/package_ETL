# etl/save_interim_data.py

import os
import pandas as pd

class SaveInterimData:
    """
    Classe pour sauvegarder un DataFrame intermédiaire de cacao
    dans data/interim/cacao_interim.csv
    """

    @staticmethod
    def save(df: pd.DataFrame, filename="cacao_interim.csv"):
        """
        Sauvegarde le DataFrame dans le dossier data/interim.

        Arguments
        ---------------
        df : pd.DataFrame
            Le DataFrame à sauvegarder.
        filename : str
            Nom du fichier CSV à créer.
        """
        if df is None or df.empty:
            print("Erreur : DataFrame vide ou None")
            return

        # Création du dossier interim si n'existe pas
        interim_dir = "data/interim"
        os.makedirs(interim_dir, exist_ok=True)

        # Chemin du fichier CSV
        interim_file = os.path.join(interim_dir, filename)

        # Sauvegarde du DataFrame
        df.to_csv(interim_file, index=False)
        print(f"Dataset intermédiaire sauvegardé dans : {interim_file}")

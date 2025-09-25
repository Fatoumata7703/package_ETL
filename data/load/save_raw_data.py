# etl/save_raw_data.py

import os
import pandas as pd

class SaveRawData:
    """
    Classe pour sauvegarder un DataFrame brut de cacao dans data/raw/cacao_raw.csv
    """

    @staticmethod
    def save(df: pd.DataFrame, filename="cacao_raw.csv"):
        """
        Sauvegarde le DataFrame dans le dossier data/raw.

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

        # Création du dossier raw si n'existe pas
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)

        # Chemin du fichier CSV
        raw_file = os.path.join(raw_dir, filename)

        # Sauvegarde du DataFrame
        df.to_csv(raw_file, index=False)
        print(f"Dataset brut sauvegardé dans : {raw_file}")




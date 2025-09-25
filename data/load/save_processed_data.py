# etl/save_processed_data.py

import os
import pandas as pd

class SaveProcessedData:
    """
    Classe pour sauvegarder un DataFrame final de cacao
    dans data/processed/cacao_clean.csv
    """

    @staticmethod
    def save(df: pd.DataFrame, filename="cacao_clean.csv"):
        """
        Sauvegarde le DataFrame dans le dossier data/processed.

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

        # Création du dossier processed si n'existe pas
        processed_dir = "data/processed"
        os.makedirs(processed_dir, exist_ok=True)

        # Chemin du fichier CSV
        processed_file = os.path.join(processed_dir, filename)

        # Sauvegarde du DataFrame
        df.to_csv(processed_file, index=False)
        print(f"Dataset intermédiaire sauvegardé dans : {processed_file}")

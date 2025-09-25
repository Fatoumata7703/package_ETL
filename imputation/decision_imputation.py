# transformation/decision_imputation.py

import pandas as pd

class DecisionImputation:
    """
    Classe pour analyser plusieurs colonnes catégorielles et proposer une stratégie d'imputation,
    avec un affichage clair et structuré.
    """

    @staticmethod
    def analyser_et_afficher(df: pd.DataFrame, colonnes=None, seuil_mode=0.1, seuil_max=0.5):
        """
        Analyse une ou plusieurs colonnes catégorielles et affiche un rapport lisible.

        Arguments
        ---------------
        df : pd.DataFrame
        colonnes : list, colonnes à analyser (par défaut toutes les catégorielles)
        seuil_mode : float, proportion max de missing pour utiliser le mode
        seuil_max : float, proportion au-dessus de laquelle on choisit 'Unknown'
        """

        if colonnes is None:
            colonnes = df.select_dtypes(include=["object", "category"]).columns.tolist()

        print("\n===== Rapport d'Analyse d'Imputation =====")

        for col in colonnes:
            if col not in df.columns:
                print(f"\nColonne '{col}' introuvable, ignorée.")
                continue

            total = len(df)
            nb_missing = df[col].isna().sum()
            prop_missing = nb_missing / total if total > 0 else 0
            nb_categories = df[col].nunique(dropna=True)
            mode_val = df[col].mode()[0] if nb_missing < total and not df[col].mode().empty else None

            # Décision + justification courte
            if prop_missing > seuil_max:
                strategie = "Unknown"
                justification = [
                    f"Taux de valeurs manquantes élevé : {prop_missing*100:.1f}% (> {seuil_max*100:.0f}%).",
                    "Imputer par le mode introduirait un biais majeur.",
                    "Solution retenue : remplacer par 'Unknown'."
                ]
            elif prop_missing <= seuil_mode:
                strategie = "mode"
                justification = [
                    f"Taux de valeurs manquantes faible : {prop_missing*100:.1f}% (≤ {seuil_mode*100:.0f}%).",
                    f"Imputation par la valeur la plus fréquente est fiable ('{mode_val}').",
                    "Solution retenue : utiliser le mode."
                ]
            else:
                strategie = "Unknown"
                justification = [
                    f"Taux intermédiaire de valeurs manquantes : {prop_missing*100:.1f}%.",
                    f"Nombre élevé de catégories uniques : {nb_categories}.",
                    "Imputation par le mode risquerait de déséquilibrer la distribution.",
                    "Solution retenue : remplacer par 'Unknown'."
                ]

            # Affichage détaillé et structuré
            print(f"\nColonne : {col}")
            print(f"   - Proportion de valeurs manquantes : {prop_missing*100:.1f}% ({nb_missing}/{total})")
            print(f"   - Nombre de catégories uniques : {nb_categories}")
            print(f"   - Valeur la plus fréquente (mode) : {mode_val}")
            print(f"   - Stratégie suggérée : {strategie}")
            print("   - Justification :")
            for ligne in justification:
                print(f"       * {ligne}")

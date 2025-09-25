"""
Module de détection des problèmes d'encodage
Classe pour détecter les parties mal encodées
"""

import pandas as pd
import re
import unicodedata

class DetecteurProblemesEncodage:
    """
    Classe pour détecter les problèmes d'encodage dans un DataFrame
    """
    
    @staticmethod
    def detecter_problemes_encodage(df):
        """
        MÉTHODE STATIQUE QUI DÉTECTE LES PARTIES MAL ENCODÉES
        - Caractères de remplacement
        - Séquences d'encodage bizarres
        - Problèmes d'encodage spécifiques (Nave → Naive, etc.)
        """
        print("🔍 Problèmes d'encodage (résumé)")
        print("=" * 50)
        print(f"DataFrame: {df.shape[0]} lignes, {df.shape[1]} colonnes\n")
        
        resultats = {}
        replacement_char = '\uFFFD'  # Unicode Replacement Character (�)
        df_clean = df.copy()
        
        colonnes_avec_problemes = []
        for col in df.columns:
            colonne = df[col]
            total_lignes = len(colonne)
            lignes_non_vides = colonne.notna().sum()
            
            # Compter les problèmes d'encodage
            encodage_count = 0
            lignes_problematiques = []
            
            # Analyser chaque valeur non vide
            for idx, valeur in colonne.items():
                if pd.notna(valeur) and str(valeur).strip() != '':
                    text = str(valeur)
                    problemes_trouves = []
                    
                    # 1. Détecter le caractère de remplacement Unicode (U+FFFD)
                    if replacement_char in text:
                        problemes_trouves.append({
                            'type': 'Caractère de remplacement',
                            'caractere': replacement_char,
                            'description': 'Caractère de remplacement Unicode (U+FFFD)'
                        })
                    
                    # 2. Détecter les séquences d'encodage bizarres
                    if '\\x' in text or '\\u' in text:
                        problemes_trouves.append({
                            'type': 'Séquence d\'encodage',
                            'caractere': '\\x ou \\u',
                            'description': 'Séquences d\'échappement d\'encodage'
                        })
                    
                    # 3. Détecter les problèmes d'encodage spécifiques
                    problemes_encodage_communs = {
                        'Nave': 'Naive',
                        'Nve': 'Naive',
                        'Ã©': 'é',
                        'Ã ': 'à',
                        'Ã¨': 'è',
                        'Ã§': 'ç',
                        'Ã´': 'ô',
                        'Ã®': 'î',
                        'Ã¯': 'ï'
                    }
                    
                    for wrong, correct in problemes_encodage_communs.items():
                        if wrong in text:
                            problemes_trouves.append({
                                'type': 'Problème d\'encodage spécifique',
                                'caractere': wrong,
                                'correction': correct,
                                'description': f'Caractère mal encodé: {wrong} → {correct}'
                            })
                    
                    # Construire une suggestion de correction (sans modifier le DataFrame)
                    suggestion = text
                    if replacement_char in suggestion:
                        suggestion = suggestion.replace(replacement_char, '')
                    for wrong, correct in problemes_encodage_communs.items():
                        if wrong in suggestion:
                            suggestion = suggestion.replace(wrong, correct)

                    if problemes_trouves:
                        encodage_count += 1
                        lignes_problematiques.append({
                            'ligne': idx,
                            'valeur': text,
                            'problemes': problemes_trouves,
                            'suggestion': suggestion if suggestion != text else None
                        })
            
            if encodage_count > 0:
                colonnes_avec_problemes.append({
                    'colonne': col,
                    'encodage_count': encodage_count,
                    'exemples': lignes_problematiques[:3]
                })
                # Appliquer la correction
                for prob in lignes_problematiques:
                    suggestion = prob.get('suggestion')
                    if suggestion is not None:
                        df_clean.at[prob['ligne'], col] = suggestion
            
            # Stocker les résultats
            resultats[col] = {
                'total_lignes': total_lignes,
                'lignes_non_vides': lignes_non_vides,
                'encodage_count': encodage_count,
                'lignes_problematiques': lignes_problematiques
            }
        
        # Affichage final concis et joli
        if not colonnes_avec_problemes:
            print("✅ Aucun problème d'encodage détecté")
        else:
            for info in colonnes_avec_problemes:
                print(f"• Colonne: {info['colonne']}  (\u26A0\uFE0F {info['encodage_count']} valeur(s))")
                for ex in info['exemples']:
                    before = ex['valeur']
                    before_prev = before[:60] + ('...' if len(before) > 60 else '')
                    after = ex.get('suggestion') or before
                    after_prev = after[:60] + ('...' if len(after) > 60 else '')
                    print(f"   - Ligne {ex['ligne']}: '{before_prev}' → '{after_prev}'")
                if info['encodage_count'] > len(info['exemples']):
                    print(f"   - ... et {info['encodage_count'] - len(info['exemples'])} autre(s)")

        return df_clean

import pandas as pd
import numpy as np

class SafeConverter:
    """
    Classe pour les conversions sécurisées de types de données
    """
    
    @staticmethod
    def safe_float(text):
        """Convertit en float de manière sécurisée"""
        if not text or text in ["", "&nbsp;", " "]:
            return np.nan
        try:
            return float(text)
        except ValueError:
            return np.nan
    
   
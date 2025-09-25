"""
Module d'extraction des données de cacao
Web scraping depuis le site Codecademy
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformation.safe_conversion import SafeConverter

class ScraperCacao:
    """
    Cette classe permet d'extraire les données de cacao depuis le web
    """
    
    @staticmethod
    def extract_data():
        """
        Cette fonction extrait toutes les données et renvoie le DataFrame
        
        Arguments
        ---------------
            Aucun
        
        Return
        ----------------
            df : pd.DataFrame, les données extraites du web
        """
        
        try:
            # Récupération de la page web
            webpage = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")
            soup = BeautifulSoup(webpage.content, "html.parser")
            
            # Récupération de toutes les colonnes disponibles
            rating_column = soup.find_all(attrs={"class": "Rating"})
            cocoa_percent_tags = soup.find_all(attrs={"class": "CocoaPercent"})
            company_column = soup.find_all(attrs={"class": "Company"})
            origin_column = soup.find_all(attrs={"class": "Origin"})  # Specific Bean Origin
            broad_bean_origin_column = soup.find_all(attrs={"class": "BroadBeanOrigin"})  # Broad Bean Origin
            ref_column = soup.find_all(attrs={"class": "REF"})
            review_date_column = soup.find_all(attrs={"class": "ReviewDate"})
            bean_type_column = soup.find_all(attrs={"class": "BeanType"})
            company_location_column = soup.find_all(attrs={"class": "CompanyLocation"})
            
            # Création des listes vides pour stocker les données
            ratings = []
            cocoa_percents = []
            companies = []
            specific_origins = []  # Specific Bean Origin
            broad_origins = []     # Broad Bean Origin
            refs = []
            review_dates = []
            bean_types = []
            company_locations = []
            
            # Extraction des données (en sautant l'en-tête avec [1:])
            for x in rating_column[1:]:
                ratings.append(SafeConverter.safe_float(x.get_text().replace("\n", "").strip()))
            
            for cm in company_column[1:]:
                companies.append(cm.get_text().replace("\n", "").strip())
            
            for org in origin_column[1:]:
                specific_origins.append(org.get_text().replace("\n", "").strip())
            
            for broad_org in broad_bean_origin_column[1:]:
                broad_origins.append(broad_org.get_text().replace("\n", "").strip())
            
            for cacao in cocoa_percent_tags[1:]:
                cocoa_percents.append(cacao.get_text().replace("\n", "").strip())
            
            for ref in ref_column[1:]:
                refs.append(ref.get_text().replace("\n", "").strip())
            
            for date in review_date_column[1:]:
                review_dates.append(date.get_text().replace("\n", "").strip())
            
            for bean in bean_type_column[1:]:
                bean_types.append(bean.get_text().replace("\n", "").strip())
            
            for location in company_location_column[1:]:
                company_locations.append(location.get_text().replace("\n", "").strip())
            
            # Création du DataFrame avec toutes les colonnes
            data = {
                "Company": companies,
                "Origine spécifique du harirot": specific_origins,
                "REF": refs,
                "Date de la revue": review_dates,
                "Pourcentage de cacao": cocoa_percents,
                "Localisation de l'entreprise": company_locations,
                "Note": ratings,
                "Type de fève": bean_types,
                "Broad Bean Origin": broad_origins 
            }
            
            # Créer le DataFrame
            df = pd.DataFrame.from_dict(data)
            
            return df
            
        except Exception as e:
            print(f"Erreur lors de l'extraction: {e}")
            return None

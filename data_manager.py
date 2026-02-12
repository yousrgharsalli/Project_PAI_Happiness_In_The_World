import pandas as pd  # Importation de la bibliothèque Pandas pour la manipulation de données
import os  # Importation du module OS pour gérer les chemins de fichiers sur le système d'exploitation

class DataManager:
    def __init__(self, filename="happiness_fixed.csv"):
        # --- GESTION DU CHEMIN DU FICHIER ---
        # Récupèration du dossier où se trouve le script actuel 
        current_folder = os.path.dirname(os.path.abspath(__file__))
        # Construction du chemin complet 
        file_path = os.path.join(current_folder, filename)
        
        # Initialisation d'un DataFrame 
        self.df = pd.DataFrame()

        # Vérification de l'existence du fichier 
        if not os.path.exists(file_path):
            print(f"ERREUR : Le fichier est introuvable ici : {file_path}")
            return

        try:
            # --- CHARGEMENT DU FICHIER ---
            self.df = pd.read_csv(file_path, sep=';', decimal='.')
            
            # Nettoyage des noms de colonnes :
            self.df.columns = self.df.columns.str.strip().str.replace('\ufeff', '')

            # Conversion de la colonne année en texte 
            self.df['Year'] = self.df['Year'].astype(str)

        except Exception as e:
            print(f"ERREUR : {e}")

    def get_all_years(self):
        '''
        Renvoie la liste des années uniques, triées par ordre croissant et renvoie une liste vide si la colonne n'a pas été chargée.
        
        '''
        if self.df.empty: return []
       
        return sorted(self.df['Year'].unique())

    def get_all_regions(self):
        '''
        Renvoie les valeurs unique des régions et enlève la valeurs NaN et renvoie une liste vide si la colonne n'a pas été chargée.
        
        '''
        if self.df.empty or 'Region' not in self.df.columns: return []
        
        return sorted(self.df['Region'].dropna().unique())

    def get_all_countries(self):
        '''
        Renvoie les valeurs unique des pays et enlève la valeurs NaN et renvoie une liste vide si la colonne n'a pas été chargée.
        
        '''

        if self.df.empty: return []
        return sorted(self.df['Country'].unique())
    
    # --- NOUVELLE FONCTION DE FILTRAGE AVANCÉ ---
    def filter_data_advanced(self, year, region, country, 
                             happ_min, happ_max,
                             gdp_min, gdp_max,
                             fam_min, fam_max,
                             health_min, health_max,
                             free_min, free_max,
                             trust_min, trust_max,
                             gen_min, gen_max):
        '''
    Applique un filtrage avancé sur les données en combinant des filtres textuels (année, région, pays) et des filtres
    numériques (bornes minimales et maximales sur plusieurs indicateurs).

    :param year: Année sélectionnée pour le filtrage 
    :param region: Région sélectionnée ou "Toutes"
    :param country: Pays sélectionné ou "Toutes"

    :param happ_min: Valeur minimale du score de bonheur
    :param happ_max: Valeur maximale du score de bonheur

    :param gdp_min: Valeur minimale du PIB par habitant
    :param gdp_max: Valeur maximale du PIB par habitant

    :param fam_min: Valeur minimale de l'indicateur Family
    :param fam_max: Valeur maximale de l'indicateur Family

    :param health_min: Valeur minimale de l'espérance de vie 
    :param health_max: Valeur maximale de l'espérance de vie 
 
    :param free_min: Valeur minimale de l'indicateur Freedom
    :param free_max: Valeur maximale de l'indicateur Freedom

    :param trust_min: Valeur minimale de l'indicateur Trust 
    :param trust_max: Valeur maximale de l'indicateur Trust 

    :param gen_min: Valeur minimale de l'indicateur Generosity
    :param gen_max: Valeur maximale de l'indicateur Generosity
        '''
        
        if self.df.empty: return pd.DataFrame()
        
        # Création d'une cope du DataFrame original.
        df = self.df.copy()

        # 1. Filtres Textuels (Listes déroulantes)
        if year != "Toutes":
            df = df[df['Year'] == year]
        if region != "Toutes":
            df = df[df['Region'] == region]
        if country != "Toutes":
            df = df[df['Country'] == country]

        # 2. Filtres Numériques (Bornes Min et Max)
        try:
            df = df[
                (df['Happiness Score'] >= happ_min) & (df['Happiness Score'] <= happ_max) &
                (df['Economy (GDP per Capita)'] >= gdp_min) & (df['Economy (GDP per Capita)'] <= gdp_max) &
                (df['Family'] >= fam_min) & (df['Family'] <= fam_max) &
                (df['Health (Life Expectancy)'] >= health_min) & (df['Health (Life Expectancy)'] <= health_max) &
                (df['Freedom'] >= free_min) & (df['Freedom'] <= free_max) &
                (df['Trust (Government Corruption)'] >= trust_min) & (df['Trust (Government Corruption)'] <= trust_max) &
                (df['Generosity'] >= gen_min) & (df['Generosity'] <= gen_max)
            ]
        except KeyError as e:
            print(f"Erreur de colonne manquante lors du filtrage : {e}")
        
        return df
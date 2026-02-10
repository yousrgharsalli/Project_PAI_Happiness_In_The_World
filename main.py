import sys  # Module système nécessaire pour gérer les arguments de lancement et la fermeture propre du script
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from data_manager import DataManager

# --- IMPORT DES ONGLETS PERSONNALISÉS ---
# On importe les classes (écrans) définies dans les autres fichiers .py.
# Cela permet de découper le code et de garder ce fichier principal propre et court.
from tab_country import CountryTab
from tab_comparison import ComparisonTab
from tab_map_interactive import MapTabInteractive

class MainWindow(QMainWindow):
    """
    Fenêtre Principale de l'application (Le cadre global).
    Elle hérite de QMainWindow, ce qui lui donne accès aux fonctionnalités de base 
    d'une fenêtre (titre, redimensionnement, barre de statut, etc.).
    """
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURATION DE LA FENÊTRE ---
        self.setWindowTitle("Happiness Index Analyzer - Projet Supop")  # Titre affiché dans la barre supérieure
        self.resize(1400, 900)  # Taille initiale de la fenêtre (Largeur, Hauteur) en pixels

        # 1. Chargement des données (CENTRALISÉ)
        # On instancie DataManager une seule fois ici au démarrage.
        # C'est la "Source de Vérité" unique pour toute l'application.
        self.data_manager = DataManager()
        
        # Sécurité critique : Vérifier si le chargement a réussi
        if self.data_manager.df.empty:
            # Affiche une boîte de dialogue "Pop-up" critique si le CSV est introuvable ou vide
            QMessageBox.critical(self, "Erreur", "Impossible de charger les données happiness.csv")

        # 2. Création du conteneur d'onglets
        # QTabWidget est le composant qui gère la barre de navigation et l'affichage des pages
        self.tabs = QTabWidget()
        
        # setCentralWidget indique à la fenêtre principale que les onglets doivent occuper tout l'espace disponible
        self.setCentralWidget(self.tabs)
        
        # 3. Instanciation des onglets (Injection de dépendance)
        # IMPORTANT : On passe 'self.data_manager' entre parenthèses.
        # Cela permet d'envoyer les données déjà chargées aux onglets.
        # Ainsi, les onglets n'ont pas besoin de recharger le CSV eux-mêmes (gain de mémoire et de temps).
        self.tab_country = CountryTab(self.data_manager)
        self.tab_comparison = ComparisonTab(self.data_manager)
        self.tab_map = MapTabInteractive(self.data_manager)
        # 4. Ajout visuel des onglets dans la fenêtre
        # Le premier argument est le widget (l'écran), le second est le titre écrit sur l'onglet
        self.tabs.addTab(self.tab_country, "Vue d'ensemble")
        self.tabs.addTab(self.tab_comparison, "Comparaison")
        self.tabs.addTab(self.tab_map, "Carte")
# --- POINT D'ENTRÉE DU PROGRAMME ---
# Ce bloc vérifie si ce fichier est le script principal exécuté par l'utilisateur.
if __name__ == "__main__":
    # 1. Création de l'application PyQt
    # C'est l'objet qui gère toute la logique de fond (clics souris, clavier, rafraîchissement écran).
    # sys.argv transmet les commandes du terminal (nécessaire par convention).
    app = QApplication(sys.argv)
    
    # 2. Création de l'objet fenêtre (mais elle est encore cachée en mémoire)
    window = MainWindow()
    
    # 3. Rendre la fenêtre visible à l'écran
    window.show()
    
    # 4. Lancement de la "Boucle d'événements" (Event Loop)
    # app.exec() lance une boucle infinie qui attend les actions de l'utilisateur.
    # Le script reste bloqué sur cette ligne tant qu'on ne ferme pas la fenêtre.
    # sys.exit() assure que le script Python s'arrête proprement quand la fenêtre est fermée.
    sys.exit(app.exec())
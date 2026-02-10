from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox, QDoubleSpinBox
from PyQt6.QtCore import QUrl
import plotly.express as px
import pycountry
from PyQt6.QtWebEngineWidgets import QWebEngineView
NAME_FIX = {
    "United States": "United States",
    "Russia": "Russian Federation",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Iran": "Iran, Islamic Republic of",
    "Vietnam": "Viet Nam",
}

def to_iso3(country_name: str):
    name = NAME_FIX.get(country_name, country_name)
    c = pycountry.countries.get(name=name)
    if c:
        return c.alpha_3
    # tentative fuzzy (plus permissive)
    try:
        matches = pycountry.countries.search_fuzzy(name)
        return matches[0].alpha_3
    except Exception:
        return None

class MapTabInteractive(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        
        self.data_manager = data_manager

        main = QHBoxLayout(self)

        # --- Filtres (comme ton Option A) ---
        filters_box = QGroupBox("Filtres")
        left = QVBoxLayout(filters_box)

        left.addWidget(QLabel("Année :"))
        self.combo_year = QComboBox()
        self.combo_year.addItems(["Toutes"] + self.data_manager.get_all_years())
        left.addWidget(self.combo_year)

        left.addWidget(QLabel("Pays :"))
        self.combo_country = QComboBox()
        self.combo_country.addItems(["Toutes"] + self.data_manager.get_all_countries())
        left.addWidget(self.combo_country)

        left.addWidget(QLabel("Région :"))
        self.combo_region = QComboBox()
        self.combo_region.addItems(["Toutes"] + self.data_manager.get_all_regions())
        left.addWidget(self.combo_region)

        self.happ_min, self.happ_max = self._add_minmax(left, "Happiness", 0.0, 10.0, 0.0, 10.0)
        self.gdp_min, self.gdp_max = self._add_minmax(left, "Economy", 0.0, 2.0, 0.0, 2.0)
        self.fam_min, self.fam_max = self._add_minmax(left, "Family", 0.0, 2.0, 0.0, 2.0)
        self.health_min, self.health_max = self._add_minmax(left, "Health", 0.0, 1.0, 0.0, 1.0)
        self.free_min, self.free_max = self._add_minmax(left, "Freedom", 0.0, 1.0, 0.0, 1.0)
        self.trust_min, self.trust_max = self._add_minmax(left, "Trust", 0.0, 1.0, 0.0, 1.0)
        self.gen_min, self.gen_max = self._add_minmax(left, "Generosity", 0.0, 1.0, 0.0, 1.0)

        left.addStretch(1)

        # --- Carte interactive (web) ---

        
        self.web = QWebEngineView()

        main.addWidget(filters_box, 1)
        main.addWidget(self.web, 3)

        # Signals
        for w in [self.combo_year, self.combo_country, self.combo_region]:
            w.currentTextChanged.connect(self.refresh)
        for w in [self.happ_min, self.happ_max, self.gdp_min, self.gdp_max, self.fam_min, self.fam_max,
                  self.health_min, self.health_max, self.free_min, self.free_max, self.trust_min, self.trust_max,
                  self.gen_min, self.gen_max]:
            w.valueChanged.connect(self.refresh)

        self.refresh()

    def _add_minmax(self, layout, label, min_val, max_val, default_min, default_max):
        layout.addWidget(QLabel(f"{label} Min :"))
        sp_min = QDoubleSpinBox(); sp_min.setRange(min_val, max_val); sp_min.setDecimals(2); sp_min.setValue(default_min)
        layout.addWidget(sp_min)
        layout.addWidget(QLabel(f"{label} Max :"))
        sp_max = QDoubleSpinBox(); sp_max.setRange(min_val, max_val); sp_max.setDecimals(2); sp_max.setValue(default_max)
        layout.addWidget(sp_max)
        return sp_min, sp_max

    def refresh(self):
        if self.data_manager.df.empty:
            self.web.setHtml("<h3>Pas de données</h3>")
            return

        year = self.combo_year.currentText()
        region = self.combo_region.currentText()
        country = self.combo_country.currentText()

        df = self.data_manager.filter_data_advanced(
            year, region, country,
            self.happ_min.value(), self.happ_max.value(),
            self.gdp_min.value(), self.gdp_max.value(),
            self.fam_min.value(), self.fam_max.value(),
            self.health_min.value(), self.health_max.value(),
            self.free_min.value(), self.free_max.value(),
            self.trust_min.value(), self.trust_max.value(),
            self.gen_min.value(), self.gen_max.value()
        ).copy()

        # Convertir les pays en ISO3
        df["iso3"] = df["Country"].apply(to_iso3)
        df = df.dropna(subset=["iso3"])

        # Choisis ce que tu veux colorer : ici Happiness Score
        fig = px.choropleth(
            df,
            locations="iso3",
            color="Happiness Score",
            hover_name="Country",
            hover_data=["Year", "Region", "Economy (GDP per Capita)", "Health (Life Expectancy)", "Freedom"],
            projection="natural earth",
            title=f"Carte interactive — pays filtrés: {df['Country'].nunique()}"
        )
        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

        # Afficher dans PyQt (HTML)
        self.web.setHtml(fig.to_html(include_plotlyjs="cdn"))

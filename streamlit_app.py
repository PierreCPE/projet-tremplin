import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import matplotlib.colors as mcolors
import folium
from streamlit_folium import folium_static
from google.oauth2 import service_account
from pandas_gbq import read_gbq
import json


st.set_page_config(
    page_title="Étude des paiements Taxi NYC",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Activer le thème sombre pour Altair
alt.themes.enable("dark")

# CSS pour personnalisation
st.markdown("""
    <style>
    /* Fond noir général */
    .stApp {
        background-color: #121212;
        color: white;
    }
    
    /* Titres et textes */
    h1, h2, h3, h4, h5, h6 {
        color: #BB86FC;
    }

    /* Labels des widgets */
    label {
        color: white !important;
        font-weight: bold;
    }

    /* Barre latérale */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
    }

    /* Bouton de collapse de la barre latérale */
    [data-testid="stSidebarCollapseButton"] {
        color: white !important;
    }

    /* KPI en boîte compacte */
    .kpi-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }

    .kpi-box {
        background-color: black;
        padding: 24px;
        border-radius: 10px;
        text-align: center;
        width: 360px;
        margin: auto;
    }

    .kpi-value {
        color: white;
        font-size: 54px;
        font-weight: bold;
    }

    .kpi-label {
        color: #BB86FC;
        font-size: 36px;
    }

    /* Fond noir pour le tableau */
    .dataframe {
        background-color: #1E1E1E;
        color: white;
    }

    /* Ajuster les graphiques */
    .stPlotlyChart, .stPyplot {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Fonction pour formatage des grands nombres
def format_large_number(value):
    return f"{value/1_000_000:.1f}M" if value >= 1_000_000 else f"{value:,}"

# Données
data = {
    "payment_type": ["Carte", "Espèces", "Autre", "Crédit", "Inconnu"],
    "total_trips": [23246764, 8289088, 39662, 13377, 3],
    "total_revenue": [437129175.84, 126905655.80, 637824.18, 240425.69, 102.02]
}

df = pd.DataFrame(data)

# Barre latérale
with st.sidebar:
    st.title('🚕 Dashboard Paiements Taxi NYC')
    
    analysis_point = ("Étude globale", "Étude temporelle", "Étude géographique")
    selected_analysis = st.selectbox('📊 Sélectionner un type d\'analyse', analysis_point)

    st.write(f"🔍 **Vue sélectionnée :** {selected_analysis}")

# Affichage en fonction de l'analyse sélectionnée:

if selected_analysis == "Étude globale":
    
    # Disposition des KPI en ligne
    st.header("🚀 Indicateurs Clés de Performance (KPI)")
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-label">🛺 Trajets</div>
                <div class="kpi-value">{format_large_number(df["total_trips"].sum())}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">💵 Revenu</div>
                <div class="kpi-value">${format_large_number(df["total_revenue"].sum())}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">💲 Tarif Moyen</div>
                <div class="kpi-value">${df['total_revenue'].sum() / df['total_trips'].sum():.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Titre principal
    st.title("📊 Tableau de Bord des Paiements Taxi NYC")

    # Graphiques à barres (couleurs classiques)
    st.subheader("📊 Nombre de trajets et Revenu par mode de paiement")

    col1, col2, col3 = st.columns([1, 2, 1])  # Pour centrer les graphes

    with col2:
        st.write("**Nombre de trajets par mode de paiement**")  
        st.bar_chart(df.set_index("payment_type")[["total_trips"]], use_container_width=True)
        st.write("**Revenu par mode de paiement**")
        st.bar_chart(df.set_index("payment_type")[["total_revenue"]], use_container_width=True)

    # Graphiques en secteurs plus petits et centrés avec légende
    st.subheader("📌 Répartition des Paiements")
    col1, col2, col3 = st.columns([1, 2, 1])

    colors = plt.cm.Paired.colors

    with col1:
        st.write("")  # Pour centrer

    with col2:
        col_a, col_b = st.columns(2)

        with col_a:
            st.write("**🧾 Répartition des Trajets**")
            fig, ax = plt.subplots(figsize=(3, 3), facecolor='#121212')  
            wedges, texts, autotexts = ax.pie(
                df["total_trips"], 
                autopct=lambda p: f'{p:.0f}%' if p > 5 else '', 
                colors=colors,
                labels=None
            )
            ax.set_facecolor('#121212')
            for text in texts + autotexts:
                text.set_color("white")
            st.pyplot(fig)

        with col_b:
            st.write("**💰 Répartition des Revenus**")
            fig, ax = plt.subplots(figsize=(3, 3), facecolor='#121212')  
            wedges, texts, autotexts = ax.pie(
                df["total_revenue"], 
                autopct=lambda p: f'{p:.0f}%' if p > 5 else '', 
                colors=colors,
                labels=None
            )
            ax.set_facecolor('#121212')
            for text in texts + autotexts:
                text.set_color("white")
            st.pyplot(fig)

    # Ajout de la légende pour les camemberts
    st.write("📍 **Légende des modes de paiement**")
    legend_colors = [f'<span style="color: {mcolors.to_hex(colors[i])}; font-size: 14px;">⬤ {df["payment_type"][i]}</span>' for i in range(len(df))]
    st.markdown(" &nbsp; &nbsp; ".join(legend_colors), unsafe_allow_html=True)

    with col3:
        st.write("")  # Pour centrer

    # Tableau de données avec fond noir
    st.header("📄 Tableau Détailé")
    st.dataframe(df.style.set_properties(**{"background-color": "#1E1E1E", "color": "white"}))

    
elif selected_analysis == "Étude temporelle":
    st.write("🔍 **Étude temporelle en cours de développement...**")


elif selected_analysis == "Étude géographique":
    st.write("🔍 **Étude géographique**")

    # Authentification avec BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    # Requête pour récupérer les données de BigQuery
    query = """
    SELECT State, County, City, Name, RegionID, Coordinates
    FROM `projet-tremplin-451615.dbt_pgosson.NY_ZillowNeighborhoods_CSV_Table`
    WHERE City = 'New York'
    """
    df_geo = read_gbq(query, project_id="projet-tremplin-451615", credentials=credentials)

    # Créer une carte Folium
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    # Ajouter les polygones des quartiers à la carte
    for _, row in df_geo.iterrows():
        coordinates = json.loads(row['Coordinates'])
        if coordinates:  # Vérifier si les coordonnées sont présentes
            folium.GeoJson(coordinates).add_to(m)

    # Afficher la carte dans Streamlit
    folium_static(m)


# Informations
with st.expander('ℹ️ À propos', expanded=True):
    st.write('''
    - **Données :** [Kaggle NYC taxi Dataset](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019)
    - **Objectif :** Analyse des types de paiement utilisés par les passagers des taxis de New York.
    ''')
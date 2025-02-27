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
import geopandas as gpd
from google.cloud import bigquery
import pydeck as pdk
import random
import plotly.express as px
import plotly.graph_objects as go

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


# Barre latérale
with st.sidebar:
    st.title('🚕 Dashboard Paiements Taxi NYC')
    
    analysis_point = ("Étude globale", "Étude temporelle", "Étude géographique")
    selected_analysis = st.selectbox('📊 Sélectionner un type d\'analyse', analysis_point)

    st.write(f"🔍 **Vue sélectionnée :** {selected_analysis}")

# Affichage en fonction de l'analyse sélectionnée:

if selected_analysis == "Étude globale":


    # Authentification BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(credentials=credentials)

    # Données
    data = {
        "payment_type": ["Carte", "Espèces", "Autre", "Crédit", "Inconnu"],
        "total_trips": [23246764, 8289088, 39662, 13377, 3],
        "total_revenue": [437129175.84, 126905655.80, 637824.18, 240425.69, 102.02]
    }

    df = pd.DataFrame(data)
    
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

    # Authentification BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(credentials=credentials)

    @st.cache_data
    def load_shapefile():
        shapefile_path = "../data_geo/ZillowNeighborhoods-NY.shp"
        return gpd.read_file(shapefile_path)

    gdf = load_shapefile()

    # Filtrer uniquement les zones de la ville de New York
    gdf = gdf[gdf["City"] == "New York"]
    
    @st.cache_data
    def fetch_taxi_data():
        query = """
        SELECT 
            l1.Zone AS pickup_zone, 
            l2.Zone AS dropoff_zone, 
            f.payment_type,
            COUNT(*) AS trip_count,
            ROUND(AVG(f.total_amount), 2) AS avg_fare,
            ROUND(AVG(f.tip_amount), 2) AS avg_tip
        FROM `projet-tremplin-451615.dbt_pgosson.fct_yellow_taxi_payment_location` f
        JOIN `projet-tremplin-451615.dbt_pgosson.dim_yellow_taxi_location` l1 ON f.PULocationID = l1.LocationID
        JOIN `projet-tremplin-451615.dbt_pgosson.dim_yellow_taxi_location` l2 ON f.DOLocationID = l2.LocationID
        GROUP BY 1, 2, 3
        ORDER BY trip_count DESC
        
        """
        return client.query(query).to_dataframe()

    df_taxi = fetch_taxi_data()

    # Fonction pour générer des couleurs aléatoires
    def random_color():
        return [random.randint(0, 255) for _ in range(3)] + [100]  # Couleur RGB avec transparence

    st.title("Analyse des flux de paiements 💳💵")

    # Appliquer des couleurs aléatoires aux zones
    gdf["color"] = gdf.apply(lambda x: random_color(), axis=1)

    # Affichage de la carte
    layer = pdk.Layer(
        "GeoJsonLayer",
        data=gdf,
        get_fill_color="color",  # Utiliser la colonne des couleurs générées
        get_line_color=[204, 204, 0],  # Jaune plus sombre
        pickable=True,
    )

    view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=10, pitch=40)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    # Sélection des zones
    pickup_zone = st.selectbox("Sélectionnez la zone de départ", df_taxi["pickup_zone"].unique())
    dropoff_zone = st.selectbox("Sélectionnez la zone d'arrivée", df_taxi["dropoff_zone"].unique())

    # Filtrer les flux de paiement pour les zones sélectionnées
    filtered_df = df_taxi[
        (df_taxi["pickup_zone"] == pickup_zone) & (df_taxi["dropoff_zone"] == dropoff_zone)
    ]

    # Fusion des données de géométrie
    gdf = gdf.merge(df_taxi.groupby("pickup_zone")["trip_count"].sum().reset_index(), 
                    left_on="Name", right_on="pickup_zone", how="left")



    # 📊 Diagramme des flux de paiement
    if not filtered_df.empty:

        # Mapping des types de paiement
        payment_type_mapping = {
            1: 'Credit card',
            2: 'Cash',
            3: 'No charge',
            4: 'Dispute',
            5: 'Unknown'
        }

        # Appliquer le mapping aux types de paiement
        filtered_df['payment_type_name'] = filtered_df['payment_type'].map(payment_type_mapping)


      # Ajouter du padding entre la carte et le graphique circulaire
        st.write("")
        st.write("")

        cols = st.columns([1, 1])

    with cols[0]:
        payment_type = df_taxi["payment_type"].unique()
        
        fig = px.pie(filtered_df, values='trip_count', names='payment_type_name',
                     title=f'Répartition des paiements entre {pickup_zone} et {dropoff_zone}',
                     height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with cols[1]:
        st.write("📍 **Légende des types de paiement**")
        colors = px.colors.qualitative.Plotly
        legend_html = "<ul>"
        for i, (payment_type, name) in enumerate(payment_type_mapping.items()):
            legend_html += f"<li style='color:{colors[i]};'>{name}</li>"
        legend_html += f"<li style='color:{colors[len(payment_type_mapping)]};'>Other</li></ul>"
        st.markdown(legend_html, unsafe_allow_html=True)

    st.write("💰 Moyenne des paiements par type :")
    st.dataframe(filtered_df[["payment_type_name", "avg_fare", "avg_tip"]])

    # Graphique pour les zones de service "Airports" et "EWR"
    st.write("✈️ **Comparaison des paiements : Aéroports vs Autres zones**")



    # Nouvelle requête pour récupérer les données avec distinction des aéroports
    @st.cache_data
    def fetch_payment_comparison():
        query = """
        SELECT 
            CASE 
                WHEN l1.service_zone IN ('Airports', 'EWR') OR l2.service_zone IN ('Airports', 'EWR') 
                THEN 'Aéroports' ELSE 'Autres zones' 
            END AS zone_category,
            f.payment_type,
            COUNT(*) AS trip_count,
            SUM(f.total_amount) AS total_fare,
            ROUND(AVG(f.total_amount), 2) AS avg_fare
        FROM `projet-tremplin-451615.dbt_pgosson.fct_yellow_taxi_payment_location` f
        JOIN `projet-tremplin-451615.dbt_pgosson.dim_yellow_taxi_location` l1 ON f.PULocationID = l1.LocationID
        JOIN `projet-tremplin-451615.dbt_pgosson.dim_yellow_taxi_location` l2 ON f.DOLocationID = l2.LocationID
        GROUP BY 1, 2
        """
        return client.query(query).to_dataframe()

    df_comparison = fetch_payment_comparison()

    df_comparison["payment_type_name"] = df_comparison["payment_type"].map(payment_type_mapping)

    # Séparer les données en deux groupes
    df_airport = df_comparison[df_comparison["zone_category"] == "Aéroports"]
    df_other = df_comparison[df_comparison["zone_category"] == "Autres zones"]

    # 📊 Graphiques circulaires pour la répartition des paiements
    cols = st.columns(2)

    with cols[0]:
        st.write("💳 **Répartition des paiements - Aéroports**")
        if not df_airport.empty:
            fig_airport_pie = px.pie(
                df_airport, values="trip_count", names="payment_type_name",
                title="Aéroports : Nombre de trajets par mode de paiement"
            )
            st.plotly_chart(fig_airport_pie, use_container_width=True)

    with cols[1]:
        st.write("🏙️ **Répartition des paiements - Autres zones**")
        if not df_other.empty:
            fig_other_pie = px.pie(
                df_other, values="trip_count", names="payment_type_name",
                title="Autres zones : Nombre de trajets par mode de paiement"
            )
            st.plotly_chart(fig_other_pie, use_container_width=True)

    # 📊 Comparaison des sommes et moyennes des paiements
    st.write("💰 **Comparaison des paiements entre aéroports et autres zones**")
    st.dataframe(df_comparison.pivot_table(
        index="zone_category", columns="payment_type_name",
        values=["total_fare", "avg_fare"], aggfunc="sum"
    ).round(2))


# Informations
with st.expander('ℹ️ À propos', expanded=True):
    st.write('''
    - **Données :** [Kaggle NYC taxi Dataset](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019)
    - **Objectif :** Analyse des types de paiement utilisés par les passagers des taxis de New York.
    ''')
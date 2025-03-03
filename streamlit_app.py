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
from shapely.geometry import shape
from streamlit_folium import st_folium


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
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


# Barre latérale
with st.sidebar:
    st.title('🚕 Dashboard Paiements Taxi NYC')
    
    analysis_point = ("Étude globale", "Étude temporelle", "Étude géographique")
    selected_analysis = st.selectbox('📊 Sélectionner un type d\'analyse', analysis_point)

    st.write(f"🔍 **Vue sélectionnée :** {selected_analysis}")

    st.markdown(f"""
    <div class="kpi-container" style="flex-direction: column; align-items: center;">
        <div class="kpi-box" style="background-color: #28C6FF; width: 100%; margin-bottom: 10px;">
            <div class="kpi-label" style="color: white; font-size: 24px;">💳 CARD</div>
        </div>
        <div class="kpi-box" style="background-color: #FF9810; width: 100%;">
            <div class="kpi-label" style="color: white; font-size: 24px;">💵 CASH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Affichage en fonction de l'analyse sélectionnée:

if selected_analysis == "Étude globale":


    # Authentification BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(credentials=credentials)

    # Données summary : 

    @st.cache_data
    def fetch_taxi_summary_data():
        query = """
        SELECT 
            payment_type, 
            payment_type_name,
            total_trips,
            total_revenue_with_tips AS total_revenue,
            avg_fare_with_tips AS avg_fare
        FROM `projet-tremplin-451615.dbt_pgosson.fct_yellow_taxi_payment_summary`
       
        """
        return client.query(query).to_dataframe()
    
    df = fetch_taxi_summary_data()

    # Disposition des KPI en ligne
    st.header("🚀 Indicateurs Clés de Performance (KPI)")
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-label" style="color: white;">🛺 Trajets</div>
                <div class="kpi-value">{format_large_number(df["total_trips"].sum())}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label" style="color: white;">💵 Revenu</div>
                <div class="kpi-value">${format_large_number(df["total_revenue"].sum())}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label" style="color: white;">💲 Tarif Moyen</div>
                <div class="kpi-value">${df['total_revenue'].sum() / df['total_trips'].sum():.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Titre principal
    st.title("📊 Tableau de Bord des Paiements Taxi NYC")

    # Graphiques à barres (couleurs classiques)
    st.subheader("📊 Nombre de trajets et Revenu par mode de paiement")

    col1, col2, col3 = st.columns([33, 66, 33])  # Pour centrer les graphes

    color_mapping = {
        "Cash": "#FF9810",
        "Credit card": "#28C6FF",
        "No charge": "#FFD700",
        "Dispute": "#FF4500",
        "Unknown": "#808080"
    }


    with col2:
        st.write("🧾 **Nombre de trajets par mode de paiement**")
        df["formatted_trips"] = df["total_trips"].apply(format_large_number)
        
        fig_trips = px.bar(df, x="total_trips", y="payment_type_name", 
                        orientation="h", text="formatted_trips",
                        title="Nombre de trajets par mode de paiement",
                        color="payment_type_name", color_discrete_map=color_mapping)
        fig_trips.update_traces(textposition="inside")
        fig_trips.update_xaxes(title_text="Nombre de trajets", tickformat=",")
        st.plotly_chart(fig_trips, use_container_width=True)

        # 🔄 **Graphique du revenu**
        st.write("💰 **Revenu par mode de paiement**")
        df["formatted_revenue"] = df["total_revenue"].apply(format_large_number)
        
        fig_revenue = px.bar(df, x="total_revenue", y="payment_type_name", 
                            orientation="h", text="formatted_revenue",
                            title="Revenu par mode de paiement",
                            color="payment_type_name", color_discrete_map=color_mapping)
        fig_revenue.update_traces(textposition="inside")
        fig_revenue.update_xaxes(title_text="Revenu ($)", tickformat=",")
        st.plotly_chart(fig_revenue, use_container_width=True)

    # Graphiques en secteurs plus petits et centrés avec légende
    st.subheader("📌 Répartition des Paiements")
    col1, col2 = st.columns([1, 1])

    # Couleurs pour les graphiques en secteurs

    color_sequence = ["#28C6FF", "#FF9810", "#FFD700", "#FF4500", "#808080"]
    # 🔄 **Graphique des trajets**
    with col1:
        st.write("🧾 **Répartition des trajets**")
        fig_trips = px.pie(df, values="total_trips", names="payment_type_name",
                        title="Répartition des trajets par mode de paiement",
                        hole=0.4, color_discrete_sequence=color_sequence)
        st.plotly_chart(fig_trips, use_container_width=True)

    # 💰 **Graphique des revenus**
    with col2:
        st.write("💰 **Répartition des revenus**")
        fig_revenue = px.pie(df, values="total_revenue", names="payment_type_name",
                            title="Répartition des revenus par mode de paiement",
                            hole=0.4, color_discrete_sequence=color_sequence)
        st.plotly_chart(fig_revenue, use_container_width=True)

    # 📋 **Comparaison des paiements**
    st.write("📊 **Statistiques moyennes par mode de paiement**")
    st.dataframe(df[["payment_type_name", "total_trips", "total_revenue", "avg_fare"]])

    # Tableau de données avec fond noir
    st.header("📄 Tableau Détailé")
    st.dataframe(df.style.set_properties(**{"background-color": "#1E1E1E", "color": "white"}))

    
elif selected_analysis == "Étude temporelle":


    
    # Authentification BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    # Chargement de la data avec la requête optimisée
    @st.cache_data
    def fetch_payment_trends():
        query = """
            WITH time_agg AS (
                SELECT DISTINCT 
                    date,
                    MAX(is_holiday) AS is_holiday,  
                    MAX(is_weekend) AS is_weekend
                FROM `projet-tremplin-451615.dbt_pgosson.dim_yellow_taxi_time`
                GROUP BY date
            ),

            agg_fct AS (
                SELECT 
                    DATE(tpep_pickup_datetime) AS date,
                    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour_of_day,
                    COUNT(*) AS total_trips,
                    100 * SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) / COUNT(*) AS cash_percentage,
                    100 * SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) / COUNT(*) AS card_percentage,
                    COALESCE(time_agg.is_holiday, FALSE) AS is_holiday 
                FROM `projet-tremplin-451615.dbt_pgosson.fct_yellow_taxi_payment_location` fct
                LEFT JOIN time_agg
                    ON DATE(fct.tpep_pickup_datetime) = time_agg.date  
                
                GROUP BY date, hour_of_day, is_holiday
            )

            SELECT * FROM agg_fct
            ORDER BY date, hour_of_day;

        """

        df = client.query(query).to_dataframe()
        return df

    df = fetch_payment_trends()

    # KPI pour les paiements en cash et par carte
    st.header("🚀 Indicateurs Clés de Performance (KPI)")

    cash_percentage = df["cash_percentage"].mean()
    card_percentage = df["card_percentage"].mean()
    # Conversion de ma colonne date en datetime
    df["date"] = pd.to_datetime(df["date"])

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-box" style="background-color: #FF9810;">
                <div class="kpi-label" style="color: white;">💵 CASH</div>
                <div class="kpi-value">{cash_percentage:.2f}%</div>
                <div class="kpi-description">Proportion des paiements en cash par rapport au nombre total de trajets</div>
            </div>
            <div class="kpi-box" style="background-color: #28C6FF;">
                <div class="kpi-label" style="color: white;">💳 CARD</div>
                <div class="kpi-value">{card_percentage:.2f}%</div>
                <div class="kpi-description">Proportion des paiements par carte par rapport au nombre total de trajets</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage des graphiques dans Streamlit
    st.write("📊 **Analyse temporelle approfondie des paiements**")

    # Évolution globale des paiements
    st.subheader("📈 Évolution globale des paiements")
    df_trends = df.groupby("date")[["cash_percentage", "card_percentage"]].mean().reset_index()
    df_trends["cash_ma"] = df_trends["cash_percentage"].rolling(window=12).mean()
    df_trends["card_ma"] = df_trends["card_percentage"].rolling(window=12).mean()

    fig_trends = px.line(df_trends, x="date", y=["cash_ma", "card_ma"],
                        labels={"value": "Pourcentage", "date": "Date"},
                        title="Moyenne mobile des paiements en cash et carte",
                        color_discrete_map={"cash_ma": "#FF9810", "card_ma": "#28C6FF"})
    st.plotly_chart(fig_trends, use_container_width=True)

    # Comparaison avant/après COVID
    df["pre_covid"] = df["date"] < pd.to_datetime("2020-03-01")
    df_covid_trend = df.groupby(["pre_covid"])[["cash_percentage", "card_percentage"]].mean().reset_index()
    fig_covid = px.bar(df_covid_trend, x="pre_covid", y=["cash_percentage", "card_percentage"],
                    labels={"pre_covid": "Période", "value": "Pourcentage"},
                    title="Comparaison avant/après COVID",
                    barmode="group", color_discrete_map={"cash_percentage": "#FF9810", "card_percentage": "#28C6FF"})
    st.plotly_chart(fig_covid, use_container_width=True)

    # Répartition des paiements par heure
    st.subheader("⏰ Répartition des paiements selon l'heure de la journée")
    df_hourly = df.groupby("hour_of_day")[["cash_percentage", "card_percentage"]].mean().reset_index()
    fig_hourly = px.line(df_hourly, x="hour_of_day", y=["cash_percentage", "card_percentage"],
                        labels={"hour_of_day": "Heure", "value": "Pourcentage"},
                        title="Répartition des paiements en cash et carte par heure",
                        markers=True, color_discrete_map={"cash_percentage": "#FF9810", "card_percentage": "#28C6FF"})
    st.plotly_chart(fig_hourly, use_container_width=True)

    # Comparaison des paiements par période de la journée
    df["time_period"] = pd.cut(df["hour_of_day"], bins=[0, 6, 10, 18, 23],
                            labels=["Nuit", "Matin", "Journée", "Soirée"])
    df_period = df.groupby("time_period")[["cash_percentage", "card_percentage"]].mean().reset_index()
    fig_period = px.bar(df_period, x="time_period", y=["cash_percentage", "card_percentage"],
                        labels={"time_period": "Période", "value": "Pourcentage"},
                        title="Comparaison des paiements selon la période de la journée",
                        barmode="group", color_discrete_map={"cash_percentage": "#FF9810", "card_percentage": "#28C6FF"})
    st.plotly_chart(fig_period, use_container_width=True)

    # Impact des événements (jours fériés)
    st.subheader("🎊 Impact des événements et saisonnalité")
    df_event = df[df["is_holiday"] == True].groupby("date")[["cash_percentage", "card_percentage"]].mean().reset_index()

    # Créer le graphique
    fig_event = px.line(df_event, x="date", y=["cash_percentage", "card_percentage"],
                        labels={"date": "Date", "value": "Pourcentage"},
                        title="Évolution des paiements pendant les jours fériés",
                        color_discrete_map={"cash_percentage": "#FF9810", "card_percentage": "#28C6FF"})

    # Ajouter des lignes verticales pour chaque jour férié
    for holiday_date in df_event["date"]:
        fig_event.add_shape(
            type="line",
            x0=holiday_date, y0=0, x1=holiday_date, y1=1,
            xref="x", yref="paper",
            line=dict(color="#003189", width=2, dash="dash")
        )

    st.plotly_chart(fig_event, use_container_width=True)

    # Heatmap jours/heures
    df["weekday_name"] = df["date"].dt.strftime("%A")

    # Définir l'ordre des jours de la semaine
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convertir la colonne weekday_name en type catégoriel avec l'ordre défini
    df["weekday_name"] = pd.Categorical(df["weekday_name"], categories=weekday_order, ordered=True)

    df_heatmap = df.groupby(["weekday_name", "hour_of_day"])["cash_percentage"].mean().reset_index()

    # Inverser l'ordre des jours de la semaine pour la heatmap
    df_heatmap["weekday_name"] = pd.Categorical(df_heatmap["weekday_name"], categories=weekday_order[::-1], ordered=True)

    # Définir une échelle de couleurs personnalisée allant du plus clair au plus foncé en utilisant la couleur de base #FF9810
    colorscale = [
        [0, "rgba(255, 152, 16, 0.1)"],  # Plus clair
        [1, "rgba(255, 152, 16, 1)"]     # Plus foncé
    ]

    fig_heatmap = px.density_heatmap(df_heatmap, x="hour_of_day", y="weekday_name", z="cash_percentage",
                                    title="Heatmap des paiements en cash par jour et heure",
                                    labels={"hour_of_day": "Heure", "weekday_name": "Jour"},
                                    color_continuous_scale=colorscale)
    st.plotly_chart(fig_heatmap, use_container_width=True)



elif selected_analysis == "Étude géographique":

    st.write("🔍 **Étude géographique**")

    # Authentification BigQuery
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(credentials=credentials)

    # @st.cache_data
    # def load_shapefile():
    #     shapefile_path = "../data_geo/ZillowNeighborhoods-NY.shp"
    #     return gpd.read_file(shapefile_path)

    # gdf = load_shapefile()

    # # Filtrer uniquement les zones de la ville de New York
    # gdf = gdf[gdf["City"] == "New York"]

    if "event_data" not in st.session_state:
        st.session_state.event_data = None

    # Requête BigQuery pour récupérer les données de geographie de zones de paiement



    @st.cache_data
    def fetch_zones_data():
        query = """
        SELECT 
            OBJECTID, 
            Shape_Leng, 
            Shape_Area, 
            zone, 
            LocationID, 
            borough, 
            ST_AsGeoJSON(st_geogfromtext(the_geom)) as geometry
        FROM `projet-tremplin-451615.dbt_pgosson.taxi_zone_geo_csv`
        """
        return client.query(query).to_dataframe()

    gdf = fetch_zones_data()

    # Convertir la colonne geometry en GeoDataFrame
    gdf['geometry'] = gdf['geometry'].apply(lambda x: shape(json.loads(x)))
    gdf = gpd.GeoDataFrame(gdf, geometry='geometry')

    # Définir le CRS sur le GeoDataFrame
    gdf.set_crs(epsg=4326, inplace=True)


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

    st.title("Analyse des flux de paiements 💳💵")


    # Initialisation de session_state
    if "selected_pickup" not in st.session_state:
        st.session_state.selected_pickup = None
    if "selected_dropoff" not in st.session_state:
        st.session_state.selected_dropoff = None

    # Sélection via dropdown
    pickup_zone = st.selectbox(
        "Sélectionnez la zone de départ",
        gdf["zone"].unique(),
        index=list(gdf["zone"].unique()).index(st.session_state.selected_pickup) if st.session_state.selected_pickup in gdf["zone"].unique() else 0,
        key="last_selected_pickup",
    )

    dropoff_zone = st.selectbox(
        "Sélectionnez la zone d'arrivée",
        gdf["zone"].unique(),
        index=list(gdf["zone"].unique()).index(st.session_state.selected_dropoff) if st.session_state.selected_dropoff in gdf["zone"].unique() else 0,
        key="last_selected_dropoff",
    )

    # Mettre à jour les sélections dans session_state
    st.session_state.selected_pickup = pickup_zone
    st.session_state.selected_dropoff = dropoff_zone

    # Création de la carte Folium
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10, control_scale=True)

    for _, row in gdf.iterrows():
        folium.GeoJson(
            row['geometry'],
            name=row['zone'],
            tooltip=row['zone'],
            style_function=lambda x, row=row: {
                'fillColor': 'green' if row['zone'] == st.session_state.selected_pickup else 'red' if row['zone'] == st.session_state.selected_dropoff else 'blue',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5
            },
            highlight_function=lambda x: {'weight': 3, 'color': 'yellow'},
            popup=row['zone'],
            control=False,
        ).add_to(m)

    folium_static(m, width=1400, height=600)

    st.write(f"**Pickup sélectionné** : {st.session_state.selected_pickup}")
    st.write(f"**Dropoff sélectionné** : {st.session_state.selected_dropoff}")

    # Filtrer les flux de paiement pour les zones sélectionnées
    filtered_df = df_taxi[
        (df_taxi["pickup_zone"] == pickup_zone) & (df_taxi["dropoff_zone"] == dropoff_zone)
    ]

    # # Fusion des données de géométrie
    # gdf = gdf.merge(df_taxi.groupby("pickup_zone")["trip_count"].sum().reset_index(), 
    #                 left_on="Name", right_on="pickup_zone", how="left")



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

    color_sequence = ["#28C6FF", "#FF9810", "#FFD700", "#FF4500", "#808080"]


    with cols[0]:
        payment_type = df_taxi["payment_type"].unique()
        
        fig = px.pie(filtered_df, values='trip_count', names='payment_type_name',
                     title=f'Répartition des paiements entre {pickup_zone} et {dropoff_zone}',
                     height=300, width=200, color_discrete_sequence=color_sequence)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with cols[1]:
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
                title="Aéroports : Nombre de trajets par mode de paiement",
                color_discrete_sequence=color_sequence
            )
            st.plotly_chart(fig_airport_pie, use_container_width=True)

    with cols[1]:
        st.write("🏙️ **Répartition des paiements - Autres zones**")
        if not df_other.empty:
            fig_other_pie = px.pie(
                df_other, values="trip_count", names="payment_type_name",
                title="Autres zones : Nombre de trajets par mode de paiement",
                color_discrete_sequence=color_sequence
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
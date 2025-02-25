import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

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
    
    /* Modifier les titres */
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

    /* KPI en blanc */
    div[data-testid="metric-container"] > label {
        color: white !important;
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
    "payment_type": [1, 2, 3, 4, 5],
    "total_trips": [23246764, 8289088, 39662, 13377, 3],
    "total_revenue": [437129175.84, 126905655.80, 637824.18, 240425.69, 102.02],
    "avg_fare": [18.80, 15.30, 16.08, 17.97, 34.00]
}

df = pd.DataFrame(data)

# Barre latérale
with st.sidebar:
    st.title('🚕 Dashboard Paiements Taxi NYC')
    
    analysis_point = ("Étude globale", "Étude temporelle", "Étude géographique")
    selected_analysis = st.selectbox('📊 Sélectionner un type d\'analyse', analysis_point)

    st.write(f"🔍 **Vue sélectionnée :** {selected_analysis}")

# Disposition des KPI en haut à droite
col1, col2 = st.columns([2, 1])

with col2:
    st.header("🚀 Indicateurs Clés de Performance (KPI)")
    st.metric(label="🛺 Nombre Total de Trajets", value=format_large_number(df["total_trips"].sum()))
    st.metric(label="💵 Revenu Total", value=f"${format_large_number(df['total_revenue'].sum())}")
    st.metric(label="💲 Tarif Moyen", value=f"${df['total_revenue'].sum() / df['total_trips'].sum():.2f}")

# Titre principal
with col1:
    st.title("📊 Tableau de Bord des Paiements Taxi NYC")

# Résumé général
st.header("📌 Résumé")
st.write(f"**🧾 Total des Trajets :** {format_large_number(df['total_trips'].sum())}")
st.write(f"**💰 Revenu Total :** ${format_large_number(df['total_revenue'].sum())}")
st.write(f"**💳 Tarif Moyen Global :** ${df['total_revenue'].sum() / df['total_trips'].sum():.2f}")

# Graphiques en colonnes
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Graphiques à Barres")
    st.bar_chart(df.set_index("payment_type")["total_trips"], use_container_width=True)
    st.bar_chart(df.set_index("payment_type")["total_revenue"], use_container_width=True)

# Graphiques en secteurs en dessous et côte à côte
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Répartition des Trajets par Type de Paiement")
    fig, ax = plt.subplots(facecolor='#121212')  # Fond noir
    df.set_index("payment_type")["total_trips"].plot.pie(autopct='%1.1f%%', figsize=(5, 5), ax=ax, colors=plt.cm.Paired.colors)
    ax.set_facecolor('#121212')  # Fond noir
    ax.set_ylabel("")  # Enlever le label automatique
    st.pyplot(fig)

with col2:
    st.subheader("🎯 Répartition des Revenus par Type de Paiement")
    fig, ax = plt.subplots(facecolor='#121212')  # Fond noir
    df.set_index("payment_type")["total_revenue"].plot.pie(autopct='%1.1f%%', figsize=(5, 5), ax=ax, colors=plt.cm.Paired.colors)
    ax.set_facecolor('#121212')  # Fond noir
    ax.set_ylabel("")  # Enlever le label automatique
    st.pyplot(fig)

# Tableau de données avec fond noir
st.header("📄 Tableau Détailé")
st.dataframe(df.style.set_properties(**{"background-color": "#1E1E1E", "color": "white"}))

# Informations
with st.expander('ℹ️ À propos', expanded=True):
    st.write('''
    - **Données :** [Kaggle NYC taxi Dataset](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019)
    - **Objectif :** Analyse des types de paiement utilisés par les passagers des taxis de New York.
    ''')

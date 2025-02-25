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

# Injecter du CSS personnalisé pour le mode sombre
st.markdown("""
    <style>
    /* Changer le fond principal */
    .stApp {
        background-color: #121212;
        color: white;
    }
    
    /* Modifier les titres et textes */
    h1, h2, h3, h4, h5, h6 {
        color: #BB86FC;
    }
    
    /* Modifier les composants interactifs */
    .stTextInput, .stSelectbox, .stMetric {
        background-color: #1E1E1E !important;
        color: white !important;
    }

    /* Modifier les barres latérales */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
    }

    /* Modifier les widgets de texte */
    .stMarkdown {
        color: white;
    }

    /* Boutons et autres éléments */
    .stButton>button {
        background-color: #BB86FC;
        color: white;
        border-radius: 5px;
    }
    
    /* Ajuster les graphiques Matplotlib */
    .stPlotlyChart, .stPyplot {
        background-color: transparent !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

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
    selected_analysis = st.selectbox('Sélectionner un type d\'analyse', analysis_point)
    
    st.write(f"🔍 **Vue sélectionnée :** {selected_analysis}")

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('🎨 Thème des couleurs', color_theme_list)

# Titre principal
st.title("📊 Tableau de Bord des Paiements Taxi NYC")

# Résumé général
st.header("📌 Résumé")
st.write(f"**🧾 Total des Trajets :** {df['total_trips'].sum():,}")
st.write(f"**💰 Revenu Total :** ${df['total_revenue'].sum():,.2f}")
st.write(f"**💳 Tarif Moyen Global :** ${df['total_revenue'].sum() / df['total_trips'].sum():.2f}")

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Graphiques à Barres")
    st.bar_chart(df.set_index("payment_type")["total_trips"], use_container_width=True)
    st.bar_chart(df.set_index("payment_type")["total_revenue"], use_container_width=True)

with col2:
    st.subheader("📈 Graphiques en Secteurs")
    fig, ax = plt.subplots()
    df.set_index("payment_type")["total_trips"].plot.pie(autopct='%1.1f%%', figsize=(5, 5), ax=ax)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    df.set_index("payment_type")["total_revenue"].plot.pie(autopct='%1.1f%%', figsize=(5, 5), ax=ax)
    st.pyplot(fig)

# Tableau de données
st.header("📄 Tableau Détailé")
st.dataframe(df.style.set_properties(**{"background-color": "#1E1E1E", "color": "white"}))

# KPI
st.header("🚀 Indicateurs Clés de Performance (KPI)")
st.metric(label="🛺 Nombre Total de Trajets", value=df["total_trips"].sum())
st.metric(label="💵 Revenu Total", value=f"${df['total_revenue'].sum():,.2f}")
st.metric(label="💲 Tarif Moyen", value=f"${df['total_revenue'].sum() / df['total_trips'].sum():.2f}")

# Informations
with st.expander('ℹ️ À propos', expanded=True):
    st.write('''
    - **Données :** [Kaggle NYC taxi Dataset](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019)
    - **Objectif :** Analyse des types de paiement utilisés par les passagers des taxis de New York.
    ''')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import matplotlib.colors as mcolors

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

    /* KPI en boîte compacte */
    .kpi-box {
        background-color: black;
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        width: 120px;
        margin: auto;
    }

    .kpi-value {
        color: white;
        font-size: 18px;
        font-weight: bold;
    }

    .kpi-label {
        color: #BB86FC;
        font-size: 12px;
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

# Disposition des KPI en haut à droite
col1, col2 = st.columns([2, 1])

with col2:
    st.header("🚀 Indicateurs Clés de Performance (KPI)")
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">🛺 Trajets</div>
        <div class="kpi-value">{format_large_number(df["total_trips"].sum())}</div>
    </div><br>
    <div class="kpi-box">
        <div class="kpi-label">💵 Revenu</div>
        <div class="kpi-value">${format_large_number(df["total_revenue"].sum())}</div>
    </div><br>
    <div class="kpi-box">
        <div class="kpi-label">💲 Tarif Moyen</div>
        <div class="kpi-value">${df['total_revenue'].sum() / df['total_trips'].sum():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Titre principal
with col1:
    st.title("📊 Tableau de Bord des Paiements Taxi NYC")

# Graphiques à barres (couleurs classiques)
st.subheader("📊 Nombre de trajets et Revenu par mode de paiement")

col1, col2, col3 = st.columns([1, 2, 1])  # Pour centrer les graphes

with col2:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(df["payment_type"], df["total_trips"], color='royalblue')
    ax.set_xlabel("Type de Paiement")
    ax.set_ylabel("Nombre de Trajets")
    ax.set_title("Nombre de trajets par type de paiement")
    for i, v in enumerate(df["total_trips"]):
        ax.text(i, v, format_large_number(v), ha='center', va='bottom', fontsize=10)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(df["payment_type"], df["total_revenue"], color='orange')
    ax.set_xlabel("Type de Paiement")
    ax.set_ylabel("Revenu Total ($)")
    ax.set_title("Revenu total par type de paiement")
    for i, v in enumerate(df["total_revenue"]):
        ax.text(i, v, format_large_number(v), ha='center', va='bottom', fontsize=10)
    st.pyplot(fig)

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

# Informations
with st.expander('ℹ️ À propos', expanded=True):
    st.write('''
    - **Données :** [Kaggle NYC taxi Dataset](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019)
    - **Objectif :** Analyse des types de paiement utilisés par les passagers des taxis de New York.
    ''')
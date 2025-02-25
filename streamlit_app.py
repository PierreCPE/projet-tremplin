import streamlit as st
import pandas as pd

# Créer les données
data = {
    "payment_type": [1, 2, 3, 4, 5],
    "total_trips": [23246764, 8289088, 39662, 13377, 3],
    "total_revenue": [437129175.849967, 126905655.80001087, 637824.17999999877, 240425.69000000015, 102.02],
    "avg_fare": [18.803872050750805, 15.309966042102586, 16.081493116837269, 17.973064962248664, 34.006666666666668]
}

df = pd.DataFrame(data)

# Titre du tableau de bord
st.title("Tableau de Bord des Trajets de Taxi")

# Carte de Résumé
st.header("Résumé")
st.write("**Total des Trajets :**", df["total_trips"].sum())
st.write("**Revenu Total :**", df["total_revenue"].sum())
st.write("**Tarif Moyen Global :**", df["total_revenue"].sum() / df["total_trips"].sum())

# Graphiques à Barres
st.header("Graphiques à Barres")
st.bar_chart(df.set_index("payment_type")["total_trips"], use_container_width=True)
st.bar_chart(df.set_index("payment_type")["total_revenue"], use_container_width=True)

# Graphiques en Secteurs
st.header("Graphiques en Secteurs")
st.write("**Pourcentage des Trajets par Type de Paiement**")
st.pyplot(df.set_index("payment_type")["total_trips"].plot.pie(autopct='%1.1f%%', figsize=(5, 5)).figure)

st.write("**Pourcentage des Revenus par Type de Paiement**")
st.pyplot(df.set_index("payment_type")["total_revenue"].plot.pie(autopct='%1.1f%%', figsize=(5, 5)).figure)

# Tableau Détailé
st.header("Tableau Détailé")
st.write(df)

# Visualisation des Tarifs Moyens
st.header("Tarifs Moyens par Type de Paiement")
st.bar_chart(df.set_index("payment_type")["avg_fare"], use_container_width=True)

# Indicateurs Clés de Performance (KPI)
st.header("Indicateurs Clés de Performance (KPI)")
st.metric(label="Nombre Total de Trajets", value=df["total_trips"].sum())
st.metric(label="Revenu Total", value=df["total_revenue"].sum())
st.metric(label="Tarif Moyen Global", value=round(df["total_revenue"].sum() / df["total_trips"].sum(), 2))

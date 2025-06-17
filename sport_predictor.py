import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# 🚀 Configurer la page Streamlit
st.set_page_config(page_title="Prédiction de Score Sportif", layout="centered")

# 🎯 Titre de l'application
st.title("⚽ Prédiction de Score Sportif par la Loi Normale")
st.markdown("""
Bienvenue ! Cette application estime le score futur d'une équipe  
en utilisant la loi normale, basée sur ses scores passés.
""")
st.divider()

# ℹ️ Explication dans la barre latérale
st.sidebar.title("ℹ️ À propos")
st.sidebar.write("""
La loi normale (ou loi de Gauss) modélise les scores fréquents autour de la moyenne.  
Plus la courbe est étroite, plus l'équipe est régulière.
""")

# 📝 Entrée utilisateur : scores passés sous forme de liste
st.subheader("📊 Entrez les scores passés")
st.write("Saisissez les scores (exemple : 1,2,2,3,3,2,1,4,2,3)")
scores_str = st.text_input("Scores séparés par des virgules", "1,2,2,3,3,2,1,4,2,3")

try:
    # 🔢 Transformer la chaîne en liste de nombres
    scores = [float(s) for s in scores_str.split(",")]

    # 📊 Calcul de la moyenne (mu) et écart-type (sigma)
    mu = np.mean(scores)
    sigma = np.std(scores, ddof=0)

    st.success("✅ Données traitées avec succès !")

    # 📌 Afficher les statistiques de base
    st.subheader("📌 Statistiques")
    st.write(f"- Moyenne (μ) = {mu:.2f}  👉 Score moyen")
    st.write(f"- Écart-type (σ) = {sigma:.2f}  👉 Variabilité des scores")

    # 🎲 Simuler 1000 scores selon la loi normale
    st.subheader("🎲 Simulation des scores futurs")
    simulated = np.random.normal(mu, sigma, 1000)

    # 📈 Afficher un histogramme simple
    fig, ax = plt.subplots()
    ax.hist(simulated, bins=10, color='lightblue', edgecolor='black')
    ax.set_xlabel("Score simulé")
    ax.set_ylabel("Fréquence")
    ax.set_title("Histogramme des scores simulés")
    st.pyplot(fig)

    # 🎯 Probabilité pour un score précis
    st.subheader("🎯 Probabilité pour un score donné")
    # Définir la limite max du slider selon les données + marge
    max_score = max(max(scores), max(simulated))
    max_limit = max(5, int(max_score) + 2)
    x = st.slider("Choisissez un score", 0.0, float(max_limit), float(mu))

    # Calculer la densité de probabilité (pdf)
    prob_density = norm.pdf(x, mu, sigma)
    st.write(f"📍 Densité de probabilité pour le score {x:.2f} : {prob_density:.4f}")

    # 📦 Probabilité que le score soit dans un intervalle
    st.subheader("📦 Probabilité dans un intervalle")
    a, b = st.slider(
        "Sélectionnez un intervalle",
        0.0, float(max_limit),
        (float(max(0, mu - sigma)), float(mu + sigma)),
        step=0.5
    )

    # Calculer la probabilité cumulée entre a et b
    prob_interval = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
    st.write(f"📦 Probabilité que le score soit entre {a:.1f} et {b:.1f} : **{prob_interval:.2%}**")


except Exception as e:
    st.error("⚠️ Erreur : " + str(e))

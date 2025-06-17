import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# Configuration de la page
st.set_page_config(page_title="Prédiction de Score Sportif", layout="centered")

# Titre principal
st.title("⚽ Prédiction de Score Sportif par la Loi Normale")
st.markdown("""
Bienvenue ! Cette application vous aide à **estimer le score futur d'une équipe** à partir de ses performances passées, en utilisant une méthode mathématique appelée **loi normale**.
""")
st.divider()

# -- Sidebar explicative --
st.sidebar.title("ℹ️ À propos")
st.sidebar.markdown("""
Ce projet utilise la **loi normale** (ou loi de Gauss), une courbe en cloche qui modélise les scores les plus fréquents autour d'une moyenne.

Plus la courbe est centrée, plus les scores sont prévisibles.
""")

# -- Entrée utilisateur --
st.subheader("📊 Entrez les scores passés")
st.markdown("Saisissez les scores récents d'une équipe. Un score = nombre de buts dans un match.")
default = "1,2,2,3,3,2,1,4,2,3"
scores_str = st.text_input("Exemple : " + default, value=default)

# -- Traitement --
try:
    scores = list(map(float, scores_str.split(",")))
    mu = np.mean(scores)
    sigma = np.std(scores, ddof=0)

    st.success("✅ Données traitées avec succès !")

    # Affichage des stats
    st.subheader("📌 Statistiques de base")
    st.markdown(f"""
    - **Moyenne (μ)** = {mu:.2f}  
      👉 Le score typique de l'équipe.
    - **Écart-type (σ)** = {sigma:.2f}  
      👉 Plus σ est petit, plus les scores sont réguliers.
    """)

    # Simulation des scores
    st.subheader("📊 Simulation des scores futurs")
    st.markdown("""
    Voici 1000 scores simulés selon la loi normale.  
    Plus une barre est haute, plus ce score est **probable**.
    """)
    simulated = np.random.normal(mu, sigma, 1000)
    fig, ax = plt.subplots()
    ax.hist(simulated, bins=10, color='lightgreen', edgecolor='black')
    ax.set_xlabel("Score simulé")
    ax.set_ylabel("Fréquence")
    ax.set_title("Histogramme des scores simulés")
    st.pyplot(fig)

    # Estimation d'un score précis
    st.subheader("🎯 Probabilité pour un score donné")
    st.markdown("""
    Choisissez un score. Nous calculons sa **densité de probabilité**, c’est-à-dire à quel point ce score est probable (plus c’est élevé, mieux c’est).
    """)
    x = st.slider("Choisissez un score", 0.0, 5.0, 2.5)
    densite = norm.pdf(x, mu, sigma)
    st.write(f"📍 Densité pour le score **{x}** : **{densite:.4f}**")

    # Intervalle de score
    st.subheader("📦 Probabilité d’un intervalle de scores")
    st.markdown("""
    Sélectionnez un intervalle. L'application vous donne la **probabilité réelle** que le score soit compris dans cet intervalle.
    """)
    a, b = st.slider("Intervalle probable", 0, 5, (1, 3))
    p_intervalle = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
    st.write(f"📦 Proba que le score soit entre {a} et {b} : **{p_intervalle:.2%}**")

except Exception as e:
    st.error("⚠️ Une erreur est survenue : " + str(e))

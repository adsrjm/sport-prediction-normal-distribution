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
st.write("Saisissez les scores (exemple : 1,2,2,3,3)")
scores_str = st.text_input("Scores séparés par des virgules", "1,2,2,3,3")

try:
    # 🔢 Transformer la chaîne en liste de nombres
    scores = [float(s) for s in scores_str.split(",")]
    scores = [s for s in scores if s >= 0]  # Exclure les scores négatifs

    # 📊 Calcul de la moyenne (mu) et écart-type (sigma)
    mu = np.mean(scores)
    sigma = np.std(scores, ddof=0)

    st.success("✅ Données traitées avec succès !")

    # 📌 Afficher les statistiques de base
    st.subheader("📌 Statistiques")
    st.write(f"- Moyenne (μ) = {mu:.2f}  👉 Score moyen")
    st.write(f"- Écart-type (σ) = {sigma:.2f}  👉 Variabilité des scores")

    # 🎲 Simuler 1000 scores selon la loi normale, arrondis à des entiers ≥ 0
    st.subheader("🎲 Simulation des scores futurs")
    simulated = np.random.normal(mu, sigma, 1000)
    simulated = np.round(simulated).astype(int)
    simulated = simulated[simulated >= 0]

    # 📈 Afficher un histogramme discret + la courbe de Gauss
    fig, ax = plt.subplots()

    # Histogramme des scores simulés
    bins = np.arange(min(simulated), max(simulated) + 2) - 0.5
    counts, _, _ = ax.hist(simulated, bins=bins, color='lightgreen', edgecolor='black', density=True, label="Scores simulés")
    ax.set_xticks(np.arange(min(simulated), max(simulated)+1))

    # Courbe de la loi normale de Gauss (continue)
    x_vals = np.linspace(min(simulated) - 1, max(simulated) + 1, 300)
    pdf_vals = norm.pdf(x_vals, mu, sigma)
    ax.plot(x_vals, pdf_vals, color='orange', lw=2, label="Loi normale de Gauss")

    ax.set_xlabel("Score")
    ax.set_ylabel("Densité")
    ax.set_title("Distribution des scores vs loi normale")
    ax.legend()
    st.pyplot(fig)

    # 🎯 Probabilité pour un score entier donné
    st.subheader("🎯 Probabilité pour un score donné")
    
    max_score = max(max(scores), max(simulated))
    max_limit = int(np.ceil(max_score + 3))  # Pour slider

    # Initialiser score sélectionné
    if 'selected_score' not in st.session_state:
        st.session_state.selected_score = int(round(mu))

    x = st.slider(
        "Choisissez un score entier",
        min_value=0,
        max_value=int(max_limit),
        value=st.session_state.selected_score,
        step=1,
        key='score_slider'
    )
    st.session_state.selected_score = x

    # 🔍 Probabilité discrète via la loi normale : P(x-0.5 < X < x+0.5)
    prob_discrete = norm.cdf(x + 0.5, mu, sigma) - norm.cdf(x - 0.5, mu, sigma)
    st.write(f"📍 Probabilité que le score soit **exactement {x}** : **{prob_discrete:.2%}**")

    # 📦 Probabilité que le score soit dans un intervalle [a, b]
    st.subheader("📦 Probabilité dans un intervalle")

    default_low = int(np.floor(mu - sigma))
    default_high = int(np.ceil(mu + sigma))
    default_low = max(0, default_low)

    if 'interval_values' not in st.session_state:
        st.session_state.interval_values = (default_low, default_high)

    a, b = st.slider(
        "Sélectionnez un intervalle entier",
        min_value=0,
        max_value=int(max_limit),
        value=st.session_state.interval_values,
        step=1,
        key='interval_slider'
    )
    st.session_state.interval_values = (a, b)

    if a > b:
        a, b = b, a

    # Calcul de la somme des probabilités discrètes entre a et b
    scores_range = np.arange(a, b + 1)
    probs = [norm.cdf(k + 0.5, mu, sigma) - norm.cdf(k - 0.5, mu, sigma) for k in scores_range]
    st.write(f"📦 Probabilité que le score soit entre {a} et {b} : **{sum(probs):.2%}**")

except Exception as e:
    st.error("⚠️ Erreur : " + str(e))

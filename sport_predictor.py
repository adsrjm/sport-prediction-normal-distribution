import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# 🚀 Page Streamlit
st.set_page_config(page_title="Prédiction de Score Sportif", layout="centered")
st.title("⚽ Prédiction de Score Sportif par la Loi Normale")
st.markdown("Entrez les scores passés pour estimer un futur score par la loi normale de Gauss.")
st.divider()

# 📊 Entrée utilisateur
scores_str = st.text_input("📥 Scores (ex: 1,2,2,3)", "1,2,2,3")
try:
    scores = [float(s) for s in scores_str.split(",") if float(s) >= 0]
    mu, sigma = np.mean(scores), np.std(scores)
    st.write(f"📌 Moyenne μ = {mu:.2f}, Écart-type σ = {sigma:.2f}")

    # 🎲 Simulation arrondie à des entiers ≥ 0
    sim = np.round(np.random.normal(mu, sigma, 1000)).astype(int)
    sim = sim[sim >= 0]

    # 📈 Histogramme + courbe de Gauss
    fig, ax = plt.subplots()
    bins = np.arange(min(sim), max(sim) + 2) - 0.5
    ax.hist(sim, bins=bins, density=True, alpha=0.6, label="Scores simulés", color="lightgreen", edgecolor="black")
    x_vals = np.linspace(min(sim)-1, max(sim)+1, 300)
    ax.plot(x_vals, norm.pdf(x_vals, mu, sigma), 'orange', lw=2, label="Loi normale de Gauss")
    ax.set_xticks(np.arange(min(sim), max(sim)+1))
    ax.set_xlabel("Score"); ax.set_ylabel("Densité"); ax.legend()
    st.pyplot(fig)

    # 🎯 Probabilité d’un score précis
    x = st.slider("🎯 Score à estimer", 0, int(max(sim)+3), int(round(mu)))
    p_x = norm.cdf(x+0.5, mu, sigma) - norm.cdf(x-0.5, mu, sigma)
    st.write(f"📍 P(score = {x}) ≈ **{p_x:.2%}**")

    # 📦 Probabilité dans un intervalle entier
    a, b = st.slider("📦 Intervalle [a, b]", 0, int(max(sim)+3), (max(0, x-1), x+1))
    if a > b: a, b = b, a
    proba = sum(norm.cdf(k+0.5, mu, sigma) - norm.cdf(k-0.5, mu, sigma) for k in range(a, b+1))
    st.write(f"📦 P({a} ≤ score ≤ {b}) ≈ **{proba:.2%}**")

except Exception as e:
    st.error("⚠️ Erreur : " + str(e))
git 
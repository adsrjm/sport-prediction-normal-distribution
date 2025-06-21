import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# 🚀 Configuration de la page
st.set_page_config(page_title="Prédiction de Score Sportif", layout="centered")
st.title("⚽ Prédiction de Score Sportif par la Loi Normale")
st.markdown("Entrez les scores passés pour estimer un futur score par la loi normale de Gauss.")
st.markdown("(Séparés par des virgules et validez avec Entrée.)")
st.divider()

# 📊 Entrée utilisateur
st.markdown("### 📥 Scores (ex: 1,2,2,3)")
scores_str = st.text_input("", "1,2,2,3")

try:
    scores = [float(s) for s in scores_str.split(",") if float(s) >= 0]
    mu, sigma = np.mean(scores), np.std(scores)

    st.markdown(f"### 📌 Moyenne μ = {mu:.2f}")
    st.markdown(f"### 📌 Écart-type σ = {sigma:.2f}")

    # 🎲 Simulation arrondie à des entiers ≥ 0
    sim = np.round(np.random.normal(mu, sigma, 1000)).astype(int)
    sim = sim[sim >= 0]

    # 📈 Histogramme + courbe normale
    fig, ax = plt.subplots()
    bins = np.arange(min(sim), max(sim) + 2) - 0.5
    ax.hist(sim, bins=bins, density=True, alpha=0.6, color="lightgreen", edgecolor="black", label="Scores simulés")
    x_vals = np.linspace(min(sim)-1, max(sim)+1, 300)
    ax.plot(x_vals, norm.pdf(x_vals, mu, sigma), 'orange', lw=2, label="Loi normale de Gauss")
    ax.set_xticks(np.arange(min(sim), max(sim)+1))
    ax.set_xlabel("Score")
    ax.set_ylabel("Densité")
    ax.legend()
    st.pyplot(fig)

    # 🎯 Score à estimer
    st.markdown("### 🎯 Score à estimer")
    score_input = st.slider(" ", 0, int(max(sim) + 3), int(round(mu)))

    p_x = norm.cdf(score_input + 0.5, mu, sigma) - norm.cdf(score_input - 0.5, mu, sigma)
    st.markdown(f"""
        <div style="padding: 1rem; background-color: #e6f7ff; border-left: 6px solid #1890ff;">
            <h3 style="margin: 0; font-size: 1.5rem;">📍 P(score = {score_input}) ≈ <strong>{p_x:.2%}</strong></h3>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Erreur : " + str(e))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

st.set_page_config(page_title="Sport Score Predictor", layout="centered")
st.title("⚽ Prédiction de Score Sportif")
st.write("Modélisation des scores à l'aide de la loi normale")

scores_str = st.text_input(
    "Entrez les scores (séparés par des virgules)",
    value="1,2,2,3,3,2,1,4,2,3"
)

try:
    scores = list(map(float, scores_str.split(",")))
    mu = np.mean(scores)
    sigma = np.std(scores, ddof=0)

    st.write(f"**Moyenne (μ)** = {mu:.2f}")
    st.write(f"**Écart‑type (σ)** = {sigma:.2f}")

    sim = np.random.normal(mu, sigma, 1000)
    fig, ax = plt.subplots()
    ax.hist(sim, bins=10, color='skyblue', edgecolor='black')
    ax.set_title("Histogramme des scores simulés")
    st.pyplot(fig)

    x = st.slider("Score à estimer", 0.0, 5.0, 2.5)
    prob = norm.pdf(x, mu, sigma)
    st.write(f"Proba densité en {x} ≈ **{prob:.4f}**")

    a, b = st.slider("Intervalle de score", 0, 5, (1, 3))
    interval_prob = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
    st.write(f"Proba score ∈ [{a}, {b}] ≈ **{interval_prob:.2%}**")

except Exception as e:
    st.error("Erreur dans l'entrée : " + str(e))

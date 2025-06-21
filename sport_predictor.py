import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

st.set_page_config(page_title="Prédiction de Score Sportif", layout="centered")
st.title("⚽ Prédiction de Score Sportif par la Loi Normale")
st.markdown("Entrez les scores passés (séparés par des virgules) et validez avec Entrée.")
st.divider()

st.markdown("### 📥 Scores (ex: 1,2,2,3)")
scores_str = st.text_input("", "1,2,2,3")

try:
    scores = [float(s) for s in scores_str.split(",") if float(s) >= 0]
    mu, sigma = np.mean(scores), np.std(scores)

    st.markdown(f"### 📌 Moyenne μ = {mu:.2f}")
    st.markdown(f"### 📌 Écart-type σ = {sigma:.2f}")

    sim = np.round(np.random.normal(mu, sigma, 1000)).astype(int)
    sim = sim[sim >= 0]

    fig, ax = plt.subplots()
    bins = np.arange(min(sim), max(sim) + 2) - 0.5
    ax.hist(sim, bins=bins, density=True, alpha=0.6, color="lightgreen", edgecolor="black", label="Scores simulés")
    x_vals = np.linspace(min(sim) - 1, max(sim) + 1, 300)
    ax.plot(x_vals, norm.pdf(x_vals, mu, sigma), 'orange', lw=2, label="Loi normale de Gauss")
    ax.set_xticks(np.arange(min(sim), max(sim) + 1))
    ax.set_xlabel("Score")
    ax.set_ylabel("Densité")
    ax.legend()
    st.pyplot(fig)

    max_score = int(np.max(scores))

    if 'score_input' not in st.session_state or st.session_state.get('last_scores_str') != scores_str:
        st.session_state.score_input = int(round(mu))
        st.session_state.last_scores_str = scores_str

    st.markdown("### 🎯 Score à estimer")
    score_input = st.slider(
        " ",
        min_value=0,
        max_value=max_score,
        value=st.session_state.score_input,
        key='score_slider'
    )
    st.session_state.score_input = score_input

    p_x = norm.cdf(score_input + 0.5, mu, sigma) - norm.cdf(score_input - 0.5, mu, sigma)
    st.markdown(f"""
        <div style="padding: 1rem; background-color: #e6f7ff; border-left: 6px solid #1890ff;">
            <h3 style="margin: 0; font-size: 1.5rem;">📍 P(score = {score_input}) ≈ <strong>{p_x:.2%}</strong></h3>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Erreur : " + str(e))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# 🚀 Page Streamlit
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

    # 📈 Histogramme + courbe de Gauss
    fig, ax = plt.subplots()
    bins = np.arange(min(sim), max(sim) + 2) - 0.5
    ax.hist(sim, bins=bins, density=True, alpha=0.6, label="Scores simulés", color="lightgreen", edgecolor="black")
    x_vals = np.linspace(min(sim)-1, max(sim)+1, 300)
    ax.plot(x_vals, norm.pdf(x_vals, mu, sigma), 'orange', lw=2, label="Loi normale de Gauss")
    ax.set_xticks(np.arange(min(sim), max(sim)+1))
    ax.set_xlabel("Score"); ax.set_ylabel("Densité"); ax.legend()
    st.pyplot(fig)

    # 🧠 Initialisation indépendante via session_state
    if 'score_input' not in st.session_state:
        st.session_state.score_input = int(round(mu))
    if 'interval_ab' not in st.session_state:
        st.session_state.interval_ab = (max(0, int(round(mu) - 1)), int(round(mu) + 1))

    # 🎯 Score à estimer
    st.markdown("### 🎯 Score à estimer")
    score_input = st.slider(
        " ", 
        min_value=0, 
        max_value=int(max(sim)+3), 
        value=st.session_state.score_input, 
        key="score_slider"
    )
    st.session_state.score_input = score_input

    p_x = norm.cdf(score_input + 0.5, mu, sigma) - norm.cdf(score_input - 0.5, mu, sigma)
    st.markdown(f"### 📍 P(score = {score_input}) ≈ **{p_x:.2%}**")

    # 📦 Intervalle [a, b]
    st.markdown("### 📦 Intervalle [a, b]")
    a, b = st.slider(
        " ", 
        min_value=0, 
        max_value=int(max(sim)+3), 
        value=st.session_state.interval_ab, 
        key="interval_slider"
    )
    if a > b:
        a, b = b, a
    st.session_state.interval_ab = (a, b)

    proba = sum(norm.cdf(k+0.5, mu, sigma) - norm.cdf(k-0.5, mu, sigma) for k in range(a, b+1))

    # ✅ Résultat mis en évidence
    st.markdown(f"""
        <div style="padding: 1rem; background-color: #e6f7ff; border-left: 6px solid #1890ff;">
            <h3 style="margin: 0; font-size: 1.5rem;">📦 P({a} ≤ score ≤ {b}) ≈ <strong>{proba:.2%}</strong></h3>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Erreur : " + str(e))

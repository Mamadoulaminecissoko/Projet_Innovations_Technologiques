import streamlit as st
import json
import os

st.set_page_config(page_title="3. Nutrition OMS - MamaCare", page_icon="🥣", layout="wide")

st.title("🥣 Module 3 : Conseiller Nutritionnel OMS (0 à 5 ans)")
st.caption("Module géré par : **Adja Fatou Binetou SARR**")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nutrition_oms.json")

data = {}
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

tranches = data.get("tranches_age", [])

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Âge de l'enfant (en mois) :", min_value=0, max_value=60, value=6)
with col2:
    poids = st.number_input("Poids actuel de l'enfant (en kg) :", min_value=1.5, max_value=30.0, value=7.5, step=0.1)

# Évaluation indicative poids/âge simplifiée OMS
poids_theorique_moyen = 3.3 + (0.5 * age)
seuil_alerte = poids_theorique_moyen * 0.70

if poids < seuil_alerte and age > 0:
    st.error(f"⚠️ **Attention au poids :** Le poids ({poids} kg) est nettement inférieur à la moyenne indicative ({poids_theorique_moyen:.1f} kg). Veuillez consulter le poste de santé pour un suivi nutritionnel.")
else:
    st.success(f"✅ **Poids en bonne progression :** Poids ({poids} kg) dans la courbe normale pour {age} mois.")

st.markdown("---")
st.markdown("### 🥗 Recommandations alimentaires officielles selon l'âge :")

for t in tranches:
    # Trouver la tranche correspondante
    est_concerne = False
    if "0 à 6" in t["tranche"] and age <= 6:
        est_concerne = True
    elif "6 à 8" in t["tranche"] and 6 < age <= 8:
        est_concerne = True
    elif "9 à 11" in t["tranche"] and 8 < age <= 11:
        est_concerne = True
    elif "12 à 24" in t["tranche"] and age > 11:
        est_concerne = True

    if est_concerne:
        st.subheader(f"📌 {t['titre']} ({t['tranche']})")
        st.info(f"**Recommandation OMS :** {t['recommandation_fr']}")
        st.write(f"🗣️ **En Wolof :** *{t.get('recommandation_wo', '')}*")
        st.write(f"⏰ **Fréquence :** {t['frequence']}")
        if "aliments_conseilles" in t:
            st.markdown("**Aliments locaux recommandés au Sénégal :**")
            for alim in t["aliments_conseilles"]:
                st.markdown(f"- 🍲 {alim}")

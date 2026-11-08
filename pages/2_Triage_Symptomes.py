import streamlit as st
import json
import os

st.set_page_config(page_title="2. Triage Symptômes - MamaCare", page_icon="🩺", layout="wide")

st.title("🩺 Module 2 : Triage des Symptômes (Protocole PCIME OMS)")
st.caption("Module géré par : **Mamadou Lamine CISSOKO**")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "symptomes_pcime.json")

data = {}
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

danger_signs = data.get("signes_generaux_danger_oms", [])
courants = data.get("symptomes_courants", [])
centres = data.get("centres_sante_ziguinchor", [])

col_age, col_duree = st.columns(2)
with col_age:
    age_mois = st.number_input("Âge de l'enfant (en mois) :", min_value=0, max_value=60, value=6)
with col_duree:
    duree_jours = st.number_input("Depuis combien de jours l'enfant est-il malade ?", min_value=0, max_value=30, value=1)

st.markdown("### ⚠️ Cochez si l'enfant présente l'un de ces signes :")
dangers_coches = []
for s in danger_signs:
    if st.checkbox(f"{s['label_fr']} ({s['label_wo']})", key=s["code"]):
        dangers_coches.append(s)

st.markdown("### 🔍 Autres symptômes courants observés :")
courants_coches = []
for c in courants:
    if st.checkbox(c["label_fr"], key=c["code"]):
        courants_coches.append(c)

if st.button("Évaluer l'état de l'enfant"):
    st.markdown("---")
    # Algorithme PCIME OMS
    if len(dangers_coches) > 0 or (age_mois < 2 and any(c["code"] == "fievre_simple" for c in courants_coches)):
        st.error("## 🔴 ALERTE ROUGE : SIGNE GÉNÉRAL DE DANGER — URGENCE MÉDICALE")
        st.write("**L'enfant doit être conduit IMMÉDIATEMENT au centre de santé ou aux urgences pédiatriques.** Ne lui donnez aucun comprimé sans avis médical.")
        st.markdown("### 🏥 Centres de santé et urgences recommandés à Ziguinchor :")
        for centre in centres:
            st.markdown(f"- **{centre['nom']}** ({centre['type']}) — *{centre['quartier']}*")
    elif any(c["gravite"] == "JAUNE" for c in courants_coches) or duree_jours >= 2:
        st.warning("## 🟡 ALERTE JAUNE : SURVEILLANCE & CONSULTATION SOUS 24H")
        for c in courants_coches:
            st.write(f"- **{c['label_fr']}** : {c['conseil_fr']}")
        st.info("💡 En Casamance, faites réaliser systématiquement un **Test de Diagnostic Rapide (TDR) du Paludisme** au poste de santé.")
    else:
        st.success("## 🟢 ZONE VERTE : SITUATION BÉNIGNE — SOINS À DOMICILE")
        st.write("Aucun signe de gravité immédiat détecté. Continuez l'allaitement maternel régulier, nettoyez le nez et surveillez attentivement l'évolution.")

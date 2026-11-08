import streamlit as st
import json
import os
from datetime import date, timedelta

st.set_page_config(page_title="4. Calendrier Vaccinal - MamaCare", page_icon="💉", layout="wide")

st.title("💉 Module 4 : Carnet & Rappels Vaccinaux (PEV Sénégal)")
st.caption("Module géré par : **Colle SYLL**")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vaccins_pev_senegal.json")

data = {}
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

calendrier = data.get("calendrier", [])

col_nom, col_date = st.columns(2)
with col_nom:
    prenom_enfant = st.text_input("Prénom de l'enfant :", value="Moussa")
with col_date:
    date_naissance = st.date_input("Date de naissance de l'enfant :", value=date.today() - timedelta(days=60))

age_jours = (date.today() - date_naissance).days
age_mois = age_jours // 30

st.info(f"👶 **{prenom_enfant}** est âgé(e) d'environ **{age_mois} mois** ({age_jours} jours).")

st.markdown("### 📅 Calendrier Officiel du Programme Élargi de Vaccination (PEV) :")

prochain_vaccin = None

for step in calendrier:
    date_theorique = date_naissance + timedelta(days=step["age_cible_jours"])
    est_passe = date.today() >= date_theorique
    
    if not est_passe and prochain_vaccin is None:
        prochain_vaccin = (step, date_theorique)

    statut_icone = "✅ Passé / Dû" if est_passe else "⏳ À venir"
    
    with st.expander(f"{statut_icone} — {step['etape']} (Date prévue : {date_theorique.strftime('%d/%m/%Y')})"):
        st.write(f"**Vaccins administrés :**")
        for v in step["vaccins"]:
            st.markdown(f"- 💉 **{v['nom']}** : protège contre *{v['protection']}*")

if prochain_vaccin:
    step_p, date_p = prochain_vaccin
    st.markdown("---")
    st.warning(f"🔔 **PROCHAIN RENDEZ-VOUS : {step_p['etape']}** (Date cible : {date_p.strftime('%d/%m/%Y')})")
    
    if st.button("📲 Simuler l'envoi d'un Rappel SMS / Vocal à la mère"):
        st.success(f"SMS simulé envoyé : 'Bonjour Mme, rappel pour {prenom_enfant} : rendez-vous pour sa vaccination ({step_p['etape']}) au poste de santé le plus proche. La vaccination est gratuite !'")

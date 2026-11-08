import streamlit as st

st.set_page_config(
    page_title="MamaCare IA - Santé Maternelle & Pédiatrie",
    page_icon="🤱",
    layout="wide"
)

st.title("🤱 MamaCare IA — Assistante Santé Maternelle & Pédiatrie")
st.caption("Université Assane Seck de Ziguinchor (UASZ) — L3 Ingénierie Informatique — Cours : Innovation Technologique (Groupe 10)")

st.markdown("""
Bienvenue sur **MamaCare IA**, la plateforme intelligente d'appui à la santé de la mère et du jeune enfant (0 à 5 ans) en Casamance et au Sénégal.
Cette solution est conçue pour briser la barrière linguistique et rendre les recommandations de l'OMS et du Ministère de la Santé accessibles à toutes les mères.

---
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 💬 1. Chatbot IA Médical\n**Responsable : Mamadou SENE**\n\nPosez vos questions à une IA entraînée sur les directives de l'OMS et du Ministère de la Santé du Sénégal, avec un cadre éthique strict.")

with col2:
    st.warning("### 🩺 2. Triage des Symptômes\n**Responsable : Mamadou Lamine CISSOKO**\n\nTriage selon le protocole OMS/PCIME (Vert, Jaune, Rouge). Détection rapide des signes de danger vital et orientation vers les centres de santé de Ziguinchor.")

with col3:
    st.success("### 🥣 3. Nutrition Infantile OMS\n**Responsable : Adja Fatou Binetou SARR**\n\nGuide de nutrition de 0 à 5 ans avec des aliments locaux (rouye enrichi, bouye, niébé, moringa) et calculateur de croissance Poids/Âge.")

col4, col5 = st.columns(2)

with col4:
    st.info("### 💉 4. Calendrier Vaccinal PEV\n**Responsable : Colle SYLL**\n\nCalculateur automatique des échéances du Programme Élargi de Vaccination (PEV) du Sénégal et simulation de rappels.")

with col5:
    st.success("### 🔊 5. Langues Locales & Audio\n**Responsable : Mame Diarra NDIAYE**\n\nConseils audios et écrits disponibles en Wolof, Pulaar, Diola et Français pour les mères non francophones.")

st.markdown("---")
st.markdown("👉 **Utilisez le menu à gauche pour naviguer entre les différents modules développés par le groupe.**")

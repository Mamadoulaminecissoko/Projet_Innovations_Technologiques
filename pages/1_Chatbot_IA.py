import streamlit as st
import json
import os

st.set_page_config(page_title="1. Chatbot IA - MamaCare", page_icon="💬", layout="wide")

st.title("💬 Module 1 : Chatbot IA & Garde-Fou Éthique")
st.caption("Module géré par : **Mamadou SENE**")

st.markdown("""
> ⚠️ **Cadre Éthique Strict de l'OMS :** Cette IA informe et oriente. Elle **ne pose aucun diagnostic médical** et ne **prescrit aucun médicament**.
""")

# Chargement de la base locale (Fonctionne même sans connexion internet !)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "base_connaissances_ia.json")

faq_data = []
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f).get("faq_medicale_validee", [])

langue = st.selectbox("🌐 Langue de réponse souhaitée :", ["Français", "Wolof", "Pulaar", "Diola"])
lang_key = "fr" if langue == "Français" else ("wo" if langue == "Wolof" else ("pu" if langue == "Pulaar" else "dio"))

question_rapide = st.selectbox(
    "💡 Ou choisissez une question médicale fréquente :",
    ["-- Écrire ma propre question ci-dessous --"] + [item["question_fr"] for item in faq_data]
)

user_prompt = st.text_input("Posez votre question sur la santé de votre enfant :", 
                            value="" if question_rapide.startswith("--") else question_rapide)

if st.button("Obtenir une réponse sécurisée"):
    if not user_prompt.strip():
        st.warning("Veuillez poser une question.")
    else:
        # Recherche dans la base validée OMS
        reponse_trouvee = None
        prompt_lower = user_prompt.lower()
        for item in faq_data:
            if any(mot in prompt_lower for mot in item["mots_cles"]) or item["question_fr"].lower() in prompt_lower:
                reponse_trouvee = item.get(f"reponse_{lang_key}", item["reponse_fr"])
                break
        
        st.markdown("### 📋 Réponse de l'Assistante :")
        if reponse_trouvee:
            st.success(reponse_trouvee)
        else:
            st.info("Pour toute question spécifique sur des symptômes non répertoriés, veuillez consulter le poste de santé le plus proche avec le carnet de santé de l'enfant.")

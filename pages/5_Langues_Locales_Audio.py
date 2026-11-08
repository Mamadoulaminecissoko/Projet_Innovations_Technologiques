import streamlit as st
import json
import os

st.set_page_config(page_title="5. Langues Locales & Audio - MamaCare", page_icon="🔊", layout="wide")

st.title("🔊 Module 5 : Assistance Vocale & Langues Nationales")
st.caption("Module géré par : **Mame Diarra NDIAYE**")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "langues_locales.json")

data = {}
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

messages = data.get("messages_cles", [])

st.markdown("""
Ce module assure l'accessibilité aux mères de famille non alphabétisées en français, en fournissant les conseils clés en **Wolof**, **Pulaar**, **Diola** et **Français**.
""")

langue_choisie = st.radio(
    "🗣️ Choisissez votre langue d'écoute :",
    ["Wolof (Oualof)", "Pulaar (Peul)", "Diola (Jola)", "Français"],
    horizontal=True
)

code_lang = "wo" if "Wolof" in langue_choisie else ("pu" if "Pulaar" in langue_choisie else ("dio" if "Diola" in langue_choisie else "fr"))

st.markdown("---")
st.markdown(f"### 📢 Conseils de santé essentiels en **{langue_choisie}** :")

for msg in messages:
    with st.container():
        st.subheader(f"📌 {msg['titre']}")
        texte = msg.get(code_lang, msg.get("fr"))
        st.info(texte)
        
        # Bouton d'écoute / simulation audio
        if st.button(f"🔊 Écouter l'enregistrement audio ({msg['id']})", key=msg["id"]):
            st.success(f"Lecture audio en cours en {langue_choisie}...")
            # Si un fichier audio réel existe dans assets/audio, st.audio le lit
            audio_path = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", f"{msg['id']}_{code_lang}.mp3")
            if os.path.exists(audio_path):
                st.audio(audio_path)
            else:
                st.caption(f"*(Fichier audio de démonstration `{msg['id']}_{code_lang}.mp3` à placer dans assets/audio/)*")

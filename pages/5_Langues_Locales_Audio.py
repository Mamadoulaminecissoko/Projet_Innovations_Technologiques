import json
from io import BytesIO
from pathlib import Path

import streamlit as st
from gtts import gTTS
from gtts.lang import tts_langs
from gtts.tts import gTTSError


st.set_page_config(
    page_title="5. Langues locales & audio - MamaCare",
    page_icon="🔊",
    layout="wide",
)

st.title("🔊 Module 5 : Langues locales & audio")
st.caption("Module géré par : **Mame Diarra NDIAYE**")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "langues_locales.json"
AUDIO_DIRECTORY = PROJECT_ROOT / "assets" / "audio"


@st.cache_data(show_spinner=False)
def generate_speech(text: str, language_code: str) -> bytes:
    audio = BytesIO()
    gTTS(text=text, lang=language_code).write_to_fp(audio)
    return audio.getvalue()


try:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    st.error(f"Fichier de données introuvable : {DATA_PATH}")
    st.stop()
except json.JSONDecodeError as error:
    st.error(f"Le fichier de données contient du JSON invalide : {error}")
    st.stop()

languages = data.get("langues_supportees", [])
messages = data.get("messages_cles", [])
if not languages or not messages:
    st.error("Le fichier de données doit contenir des langues et des messages.")
    st.stop()

st.markdown(
    "Consultez les conseils écrits en français, wolof, pulaar ou diola. "
    "La lecture audio utilise un enregistrement ajouté au projet ou, si la "
    "langue est prise en charge, une synthèse vocale en ligne."
)
if data.get("avertissement_medical"):
    st.warning(data["avertissement_medical"])

language_names = [language["nom"] for language in languages]
selected_language_name = st.radio(
    "🗣️ Choisissez votre langue :",
    language_names,
    horizontal=True,
)
selected_language = next(
    language for language in languages
    if language["nom"] == selected_language_name
)
language_code = selected_language["code"]

categories = ["Tous les conseils"] + sorted(
    {message.get("categorie", "Autres") for message in messages}
)
selected_category = st.selectbox("Filtrer par thème", categories)
visible_messages = [
    message for message in messages
    if selected_category == "Tous les conseils"
    or message.get("categorie", "Autres") == selected_category
]

st.markdown("---")
st.subheader(f"📢 Conseils en {selected_language_name}")

supported_tts_languages = tts_langs()
for message in visible_messages:
    message_id = message["id"]
    text = message.get(language_code) or message.get("fr")

    with st.container(border=True):
        category = message.get("categorie", "Conseil")
        st.caption(category)
        st.subheader(message["titre"])
        st.info(text)

        recording_path = AUDIO_DIRECTORY / f"{message_id}_{language_code}.mp3"
        if recording_path.is_file():
            st.audio(str(recording_path), format="audio/mpeg")
        elif language_code in supported_tts_languages:
            if st.button(
                f"🔊 Écouter en {selected_language_name}",
                key=f"audio_{message_id}_{language_code}",
            ):
                try:
                    audio_bytes = generate_speech(text, language_code)
                except gTTSError as error:
                    st.error(
                        "La synthèse vocale n’a pas pu être générée. "
                        f"Vérifiez votre connexion Internet et réessayez. Détail : {error}"
                    )
                else:
                    st.audio(audio_bytes, format="audio/mpeg")
        else:
            st.caption(
                "Aucun enregistrement disponible pour cette phrase. "
                f"Pour ajouter une voix locale, placez "
                f"`{message_id}_{language_code}.mp3` dans `assets/audio/`."
            )

st.caption(
    "La synthèse vocale nécessite une connexion Internet. "
    "Les langues sans voix compatible nécessitent un enregistrement audio local."
)

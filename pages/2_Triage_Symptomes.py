
import streamlit as st
import json
import os

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Triage pédiatrique | MamaCare IA",
    page_icon="🩺",
    layout="wide"
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "symptomes_pcime.json"
)

st.markdown("""
<style>
    .main-title {
        color: #176B87;
        font-size: 32px;
        font-weight: 800;
    }
    .subtitle {
        color: #64748b;
        font-size: 15px;
    }
    .section-title {
        color: #176B87;
        font-size: 21px;
        font-weight: 700;
    }
    div.stButton > button {
        background-color: #176B87;
        color: white;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #12536a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CHARGEMENT DES DONNEES
# --------------------------------------------------

@st.cache_data
def charger_donnees():
    with open(DATA_PATH, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


try:
    data = charger_donnees()
except (FileNotFoundError, json.JSONDecodeError):
    st.error("Impossible de charger les données du module.")
    st.stop()


danger_signs = data.get("signes_generaux_danger_oms", [])
symptomes = data.get("symptomes_courants", [])
centres = data.get("centres_sante_ziguinchor", [])


# --------------------------------------------------
# EN-TETE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🩺 MamaCare IA</div>',
    unsafe_allow_html=True
)

st.subheader("Module 2 : Triage des symptômes")

st.markdown(
    '<div class="subtitle">'
    'Assistant pédagogique d’orientation sanitaire '
    'pour les enfants de 0 à 5 ans.'
    '</div>',
    unsafe_allow_html=True
)

st.caption("Responsable du module : Mamadou Lamine CISSOKO")

st.divider()

st.info(
    "Ce module aide à reconnaître certains signes nécessitant "
    "une consultation. Il ne réalise aucun diagnostic médical "
    "et ne remplace pas un professionnel de santé."
)


# --------------------------------------------------
# FORMULAIRE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">👶 1. Informations sur l’enfant</div>',
    unsafe_allow_html=True
)

with st.form("formulaire_triage"):

    col1, col2 = st.columns(2)

    with col1:
        age_mois = st.number_input(
            "Âge de l'enfant (en mois)",
            min_value=0,
            max_value=60,
            value=6,
            step=1
        )

    with col2:
        duree_jours = st.number_input(
            "Durée de la maladie (en jours)",
            min_value=0,
            max_value=30,
            value=1,
            step=1
        )

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🚨 2. Signes de danger'
        '</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "Cochez tous les signes observés. "
        "Si un signe de danger est présent, n'attendez pas "
        "le résultat du formulaire pour rechercher une aide médicale."
    )

    dangers_coches = []

    for signe in danger_signs:
        if st.checkbox(
            signe["label_fr"] + " (" + signe.get("label_wo", "") + ")",
            key="danger_" + signe["code"]
        ):
            dangers_coches.append(signe)

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🔍 3. Autres symptômes observés'
        '</div>',
        unsafe_allow_html=True
    )

    symptomes_coches = []

    for symptome in symptomes:
        if st.checkbox(
            symptome["label_fr"],
            key="symptome_" + symptome["code"]
        ):
            symptomes_coches.append(symptome)

    st.divider()

    evaluation = st.form_submit_button(
        "🔎 ÉVALUER LES SYMPTÔMES"
    )



# --------------------------------------------------
# ANALYSE ET ORIENTATION
# --------------------------------------------------

if evaluation:

    st.divider()

    # Les quatre signes généraux de danger classiques
    codes_danger_general = {
        "incapable_boire_teter",
        "vomit_tout",
        "convulsions",
        "lethargique_inconscient"
    }

    # Récupération des codes sélectionnés
    codes_dangers = {
        signe["code"] for signe in dangers_coches
    }

    codes_symptomes = {
        symptome["code"] for symptome in symptomes_coches
    }

    # Identification des catégories de danger
    signes_generaux = [
        signe for signe in dangers_coches
        if signe["code"] in codes_danger_general
    ]

    autres_signes_urgents = [
        signe for signe in dangers_coches
        if signe["code"] not in codes_danger_general
    ]

    # --------------------------------------------------
    # CAS 1 : AUCUN SYMPTÔME SÉLECTIONNÉ
    # --------------------------------------------------

    if not dangers_coches and not symptomes_coches:

        st.info(
            "Aucun symptôme n'a été sélectionné. "
            "L'application ne peut pas établir une orientation. "
            "Cela ne signifie pas que l'enfant est en bonne santé."
        )

    # --------------------------------------------------
    # CAS 2 : FIÈVRE CHEZ UN NOURRISSON DE MOINS DE 2 MOIS
    # --------------------------------------------------

    elif age_mois < 2 and "fievre_simple" in codes_symptomes:

        st.error(
            "🔴 ALERTE ROUGE — ÉVALUATION MÉDICALE URGENTE"
        )

        st.write(
            "Une fièvre chez un nourrisson de moins de deux mois "
            "nécessite une évaluation médicale immédiate."
        )

    # --------------------------------------------------
    # CAS 3 : PRÉSENCE D'UN SIGNE GÉNÉRAL DE DANGER
    # --------------------------------------------------

    elif signes_generaux:

        st.error(
            "🔴 ALERTE ROUGE — SIGNE GÉNÉRAL DE DANGER"
        )

        st.write(
            "Au moins un signe général de danger a été signalé. "
            "Une évaluation médicale urgente est nécessaire."
        )

        st.markdown("### Signes généraux sélectionnés")

        for signe in signes_generaux:
            st.write("- " + signe["label_fr"])

        if autres_signes_urgents:

            st.markdown("### Autres signes urgents sélectionnés")

            for signe in autres_signes_urgents:
                st.write("- " + signe["label_fr"])

        st.markdown("### 🏥 Structures sanitaires référencées")

        st.warning(
            "Recherchez une structure capable de prendre en charge "
            "une urgence pédiatrique. Ne retardez pas la recherche "
            "d'une aide médicale pour remplir ce formulaire."
        )

        for centre in centres:

            with st.container(border=True):
                st.markdown("**🏥 " + centre["nom"] + "**")
                st.write("Type : " + centre["type"])
                st.write("Localisation : " + centre["quartier"])

    # --------------------------------------------------
    # CAS 4 : AUTRES SIGNES URGENTS
    # --------------------------------------------------

    elif autres_signes_urgents:

        st.error(
            "🔴 ALERTE ROUGE — AUTRE SIGNE NÉCESSITANT "
            "UNE ÉVALUATION URGENTE"
        )

        st.write(
            "Un signe nécessitant une évaluation urgente "
            "a été sélectionné. Recherchez une aide médicale "
            "sans attendre."
        )

        st.markdown("### Signes sélectionnés")

        for signe in autres_signes_urgents:
            st.write("- " + signe["label_fr"])

        st.markdown("### 🏥 Structures sanitaires référencées")

        for centre in centres:

            with st.container(border=True):
                st.markdown("**🏥 " + centre["nom"] + "**")
                st.write("Type : " + centre["type"])
                st.write("Localisation : " + centre["quartier"])

    # --------------------------------------------------
    # CAS 5 : SYMPTÔMES NÉCESSITANT UNE CONSULTATION
    # --------------------------------------------------

    elif any(
        symptome.get("gravite") == "JAUNE"
        for symptome in symptomes_coches
    ):

        st.warning(
            "🟡 ALERTE JAUNE — AVIS MÉDICAL RECOMMANDÉ"
        )

        st.write(
            "Les symptômes sélectionnés nécessitent une "
            "évaluation adaptée par un professionnel de santé."
        )

        for symptome in symptomes_coches:

            st.markdown("#### " + symptome["label_fr"])

            st.write(symptome.get("conseil_fr", ""))

    # --------------------------------------------------
    # CAS 6 : SYMPTÔMES CLASSÉS COMME LÉGERS
    # --------------------------------------------------

    elif symptomes_coches:

        st.success(
            "🟢 ZONE VERTE — AUCUN SIGNE URGENT "
            "IDENTIFIÉ PAR LES ÉLÉMENTS SÉLECTIONNÉS"
        )

        st.write(
            "Les symptômes sélectionnés sont classés comme légers "
            "dans cette démonstration. Surveillez l'évolution "
            "de l'enfant et demandez un avis médical si nécessaire."
        )

        for symptome in symptomes_coches:
            st.write("- " + symptome["label_fr"])
            st.write(symptome.get("conseil_fr", ""))

    # --------------------------------------------------
    # RÉSUMÉ DE L'ÉVALUATION
    # --------------------------------------------------

    st.divider()

    st.markdown("### 📋 Résumé de l'évaluation")

    col_age, col_duree = st.columns(2)

    with col_age:
        st.metric("Âge de l'enfant", str(age_mois) + " mois")

    with col_duree:
        st.metric("Durée de la maladie", str(duree_jours) + " jour(s)")

    st.caption(
        "Résultat fourni à titre pédagogique. "
        "Cette démonstration ne remplace pas une évaluation "
        "médicale. Une absence de signe sélectionné ne garantit "
        "pas l'absence de maladie."
    )

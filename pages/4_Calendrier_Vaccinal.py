import streamlit as st
import json
import os
from datetime import date, timedelta

st.set_page_config(
    page_title="4. Carnet & Calendrier Vaccinal - MamaCare IA",
    page_icon="💉",
    layout="wide"
)

# -------------------------------------------------------------
# TITRE ET EN-TÊTE DU MODULE
# -------------------------------------------------------------
st.title("💉 Module 4 : Carnet de Santé & Rappels Vaccinaux")
st.caption("Programme Élargi de Vaccination (PEV) — Ministère de la Santé du Sénégal | Responsable : **Colle SYLL**")

st.markdown("""
Ce module permet aux mères et aux sages-femmes de suivre précisément les vaccins obligatoires et gratuits de l'enfant 
selon le calendrier officiel du Sénégal, de simuler des rappels SMS/WhatsApp et de calculer le taux de couverture vaccinale.
""")

# -------------------------------------------------------------
# CHARGEMENT DES DONNÉES DU SÉNÉGAL
# -------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vaccins_pev_senegal.json")

calendrier = []
recommandation_cle = "La vaccination protège votre enfant. Elle est 100% gratuite dans tous les postes de santé du Sénégal."

if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        calendrier = data.get("calendrier", [])
        recommandation_cle = data.get("recommandation_cle", recommandation_cle)

# -------------------------------------------------------------
# INITIALISATION DE L'ÉTAT DE SESSION (Suivi des vaccins cochés)
# -------------------------------------------------------------
if "vaccins_faits" not in st.session_state:
    st.session_state["vaccins_faits"] = set()

# -------------------------------------------------------------
# FORMULAIRE DE L'ENFANT
# -------------------------------------------------------------
st.markdown("### 👶 Profil de l'enfant")
with st.container():
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        prenom_enfant = st.text_input("Prénom du bébé :", value="Moussa")
    with col2:
        sexe_enfant = st.selectbox("Sexe :", ["Garçon", "Fille"])
    with col3:
        # Valeur par défaut : bébé né il y a 75 jours (environ 2 mois et demi)
        date_naissance = st.date_input("Date de naissance :", value=date.today() - timedelta(days=75))

# Calcul de l'âge
aujourdhui = date.today()
age_jours = (aujourdhui - date_naissance).days

if age_jours < 0:
    st.error("⚠️ La date de naissance ne peut pas être dans le futur !")
    st.stop()

age_semaines = age_jours // 7
age_mois = age_jours // 30

st.info(f"📌 **{prenom_enfant}** est âgé(e) de : **{age_jours} jours** (soit environ **{age_semaines} semaines** / **{age_mois} mois**).")

# -------------------------------------------------------------
# STATISTIQUES & COUVERTURE VACCINALE
# -------------------------------------------------------------
total_vaccins = sum(len(step["vaccins"]) for step in calendrier)
nb_faits = len(st.session_state["vaccins_faits"])
pourcentage = int((nb_faits / total_vaccins) * 100) if total_vaccins > 0 else 0

st.markdown("### 📊 Couverture vaccinale actuelle")
st.progress(pourcentage / 100)
st.caption(f"**{nb_faits} / {total_vaccins} doses administrées ({pourcentage}%)**")

st.markdown("---")

# -------------------------------------------------------------
# CALENDRIER PEV DÉTAILLÉ
# -------------------------------------------------------------
st.markdown("### 📅 Calendrier Vaccinal Officiel (PEV Sénégal)")
st.caption("Cochez les vaccins déjà reçus dans le carnet de santé de l'enfant :")

prochain_rendez_vous = None
vaccins_en_retard = []

for idx, step in enumerate(calendrier):
    date_prevue = date_naissance + timedelta(days=step["age_cible_jours"])
    est_date_passee = aujourdhui >= date_prevue
    
    # Vérifier si tous les vaccins de cette étape sont cochés
    tous_coches = all(f"{step['etape']}_{v['nom']}" in st.session_state["vaccins_faits"] for v in step["vaccins"])
    
    # Détecter le prochain rendez-vous
    if not tous_coches and prochain_rendez_vous is None:
        prochain_rendez_vous = (step, date_prevue)
    
    # Détecter le retard (date passée mais vaccins non faits)
    if est_date_passee and not tous_coches:
        vaccins_en_retard.append((step, date_prevue))

    # Titre de la boîte
    if tous_coches:
        badge = "🟢 VALIDÉ"
    elif est_date_passee:
        badge = "🔴 EN RETARD / DÛ MAINTENANT"
    else:
        badge = "⏳ PROGRAMMÉ"

    with st.expander(f"{badge} — {step['etape']} (Prévu le : {date_prevue.strftime('%d/%m/%Y')})", expanded=(not tous_coches and est_date_passee)):
        st.write(f"**Âge recommandé :** {step['age_cible_label']}")
        st.write("**Vaccins de cette étape :**")
        
        for v in step["vaccins"]:
            cle_vaccin = f"{step['etape']}_{v['nom']}"
            est_fait = cle_vaccin in st.session_state["vaccins_faits"]
            
            check = st.checkbox(
                f"**{v['nom']}** — Protège contre : *{v['protection']}*",
                value=est_fait,
                key=cle_vaccin
            )
            
            if check:
                st.session_state["vaccins_faits"].add(cle_vaccin)
            else:
                st.session_state["vaccins_faits"].discard(cle_vaccin)

# -------------------------------------------------------------
# ALERTES & SIMULATEUR DE RAPPEL SMS / WHATSAPP
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🔔 Alertes et Rappels Automatiques")

if vaccins_en_retard:
    st.error(f"⚠️ **ATTENTION :** {len(vaccins_en_retard)} rendez-vous vaccinal(aux) accuse(nt) un retard. Rendez-vous au poste de santé le plus proche avec le carnet de santé.")
elif prochain_rendez_vous:
    step_p, date_p = prochain_rendez_vous
    jours_restants = (date_p - aujourdhui).days
    st.success(f"✅ Prochaine séance : **{step_p['etape']}** prévue le **{date_p.strftime('%d/%m/%Y')}** (dans {jours_restants} jours).")

# Générateur de notification pour la mère
st.markdown("#### 📲 Simuler un Rappel pour la maman")
col_lang, col_canal = st.columns(2)
with col_lang:
    langue_sms = st.selectbox("Langue du rappel :", ["Français", "Wolof"])
with col_canal:
    canal = st.selectbox("Canal d'envoi :", ["SMS Classique", "Message WhatsApp", "Message Vocal"])

cible_etape = prochain_rendez_vous[0]['etape'] if prochain_rendez_vous else "Vaccination à jour"
cible_date = prochain_rendez_vous[1].strftime('%d/%m/%Y') if prochain_rendez_vous else "N/A"

if langue_sms == "Français":
    message_texte = (
        f"Salam Mme ! Rappel de santé pour {prenom_enfant} : "
        f"son prochain vaccin ({cible_etape}) est prévu pour le {cible_date}. "
        f"La vaccination protège contre les maladies graves et est ENTIÈREMENT GRATUITE au poste de santé. "
        f"N'oubliez pas d'apporter son carnet de santé."
    )
else:
    message_texte = (
        f"Nanga def Yaay ! Rappel wér-gi-yaram ngir {prenom_enfant} : "
        f"ñaqam bi war ({cible_etape}) mi ngi war a am ci bésu {cible_date}. "
        f"Ñaq yi amul benn fey ci poste de santé bi, te dafay aar sa doom ci feebar yu tar. "
        f"Bul fatte yóbbaale carnet de santé bi."
    )

st.text_area("Aperçu du message généré automatiquement :", value=message_texte, height=110)

if st.button("🚀 Déclencher la simulation d'envoi"):
    st.success(f"Notification ({canal}) transmise avec succès au numéro de la mère !")
    st.balloons()

# -------------------------------------------------------------
# FOIRE AUX QUESTIONS & CENTRES DE SANTÉ LOCAUX (ZIGUINCHOR)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🏥 Bon à savoir pour les mamans")

with st.expander("❓ Mon enfant a un peu de fièvre après le vaccin, que faire ?"):
    st.write("""
    Une légère fièvre ou une petite douleur à l'endroit de la piqûre est une réaction normale qui prouve que le corps fabrique ses défenses.
    - Déshabillez un peu le bébé.
    - Donnez-lui le sein souvent.
    - Si la fièvre dépasse 38,5°C ou dure plus de 48h, demandez conseil à la sage-femme du poste de santé.
    """)

with st.expander("❓ Où faire vacciner mon enfant à Ziguinchor ?"):
    st.write("""
    La vaccination est disponible **gratuitement** dans tous les centres publics :
    - **Centre de Santé de Silence** (Ziguinchor Ville)
    - **Poste de santé de Néma**
    - **Poste de santé de Lyndiane**
    - **Poste de santé de Kandé**
    - **Hôpital de la Paix de Ziguinchor** (Service de Pédiatrie)
    """)

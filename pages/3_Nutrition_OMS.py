import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="3. Nutrition OMS - MamaCare IA",
    page_icon="🥣",
    layout="wide"
)

# -------------------------------------------------------------
# TITRE & EN-TÊTE DU MODULE
# -------------------------------------------------------------
st.title("🥣 Module 3 : Conseiller Nutritionnel & Croissance OMS (0 à 5 ans)")
st.caption("Normes OMS & Valorisation des Produits Locaux du Sénégal | Responsable : **Adja Fatou Binetou SARR**")

st.markdown("""
Ce module permet aux mères et agents de santé d'évaluer la croissance pondérale de l'enfant selon les **courbes officielles de l'OMS (Z-scores Poids/Âge)**, 
d'identifier précocement la malnutrition (MAM / MAS) et de guider la diversification alimentaire grâce aux **ressources agricoles locales de la Casamance et du Sénégal** (Mil, Niébé, Pâte d'arachide, Moringa, Bouye).
""")

# -------------------------------------------------------------
# CHARGEMENT DES DONNÉES NUTRITIONNELLES
# -------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nutrition_oms.json")

data = {}
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

normes_oms = data.get("normes_croissance_poids_age", {})
tranches_age = data.get("tranches_age", [])
recettes = data.get("recettes_locales_enrichies", [])
bareme_zones = data.get("bareme_classification_oms", {}).get("zones", [])
regles_hygiene = data.get("regles_hygiene_sevrage", [])

# -------------------------------------------------------------
# FONCTIONS UTILITAIRES : CALCUL ET INTERPOLATION OMS
# -------------------------------------------------------------
def get_seuils_oms(age_mois, sexe_key):
    """Calcule par interpolation linéaire les seuils OMS (-3SD, -2SD, Médiane, +2SD) pour un âge donné."""
    ages = np.array(normes_oms.get("ages_mois", []))
    sexe_data = normes_oms.get("garcons" if sexe_key == "garcon" else "filles", {})
    
    sd3neg_arr = np.array(sexe_data.get("sd3neg", []))
    sd2neg_arr = np.array(sexe_data.get("sd2neg", []))
    med_arr = np.array(sexe_data.get("mediane", []))
    sd2pos_arr = np.array(sexe_data.get("sd2pos", []))
    
    sd3neg_val = float(np.interp(age_mois, ages, sd3neg_arr))
    sd2neg_val = float(np.interp(age_mois, ages, sd2neg_arr))
    med_val = float(np.interp(age_mois, ages, med_arr))
    sd2pos_val = float(np.interp(age_mois, ages, sd2pos_arr))
    
    return {
        "sd3neg": sd3neg_val,
        "sd2neg": sd2neg_val,
        "mediane": med_val,
        "sd2pos": sd2pos_val,
        "ages_courbe": ages,
        "sd3neg_courbe": sd3neg_arr,
        "sd2neg_courbe": sd2neg_arr,
        "mediane_courbe": med_arr,
        "sd2pos_courbe": sd2pos_arr
    }

def evaluer_statut(poids, seuils):
    """Évalue le statut nutritionnel d'après les seuils OMS."""
    if poids < seuils["sd3neg"]:
        return {
            "code": "ROUGE",
            "statut": "Insuffisance Pondérale Sévère (Alerte Rouge - MAS)",
            "couleur": "error",
            "symbole": "🔴",
            "message": "Poids sous le seuil critique OMS (-3 Écart-Type). Risque élevé de Malnutrition Aiguë Sévère.",
            "action": "🚨 CONSULTATION D'URGENCE : Conduire immédiatement l'enfant au poste de santé ou au Centre de Récupération Nutritionnelle (CREN)."
        }
    elif poids < seuils["sd2neg"]:
        return {
            "code": "JAUNE",
            "statut": "Insuffisance Pondérale Modérée (Alerte Jaune - MAM)",
            "couleur": "warning",
            "symbole": "🟡",
            "message": "Poids inférieur à la normale OMS (entre -2 et -3 Écart-Type). Risque de Malnutrition Aiguë Modérée.",
            "action": "⚠️ VIGILANCE NUTRITIONNELLE : Enrichir systématiquement les bouillies (pâte d'arachide, moringa, farine de niébé) et consulter sous 7 jours."
        }
    elif poids <= seuils["sd2pos"]:
        return {
            "code": "VERT",
            "statut": "Poids Normal (Zone Verte - Croissance Harmonieuse)",
            "couleur": "success",
            "symbole": "🟢",
            "message": "Poids conforme aux standards de développement de l'OMS (entre -2 et +2 Écart-Type).",
            "action": "✅ EXCELLENTE ÉVOLUTION : Continuer l'alimentation diversifiée et le suivi mensuel en consultation post-natale."
        }
    else:
        return {
            "code": "ORANGE",
            "statut": "Poids Supérieur à la Moyenne (> +2SD)",
            "couleur": "info",
            "symbole": "🔵",
            "message": "Poids supérieur à la courbe normale OMS (+2 Écart-Type).",
            "action": "ℹ️ CONSEIL : Éviter les bouillies trop sucrées et les biscuits industriels. Privilégier les légumes et l'activité ludique."
        }

# -------------------------------------------------------------
# INTERFACE PRINCIPALE PAR ONGLETS
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Évaluation & Courbe OMS",
    "🥗 Guide Alimentaire selon l'Âge",
    "🍲 Recettes Locales Fortifiées",
    "🛡️ Hygiène & Prévention",
    "📄 Fiche Bilan Téléchargeable"
])

# =============================================================
# ONGLET 1 : CALCULATEUR ET COURBE OFFICIELLE OMS
# =============================================================
with tab1:
    st.subheader("📈 Diagnostic de la Croissance Pondérale (Z-Scores OMS)")
    st.write("Saisissez les informations de l'enfant pour visualiser sa position exacte sur la courbe du carnet de santé.")
    
    col_form1, col_form2, col_form3, col_form4 = st.columns([2, 2, 2, 2])
    with col_form1:
        nom_enfant = st.text_input("Prénom de l'enfant :", value="Awa", key="nutri_nom")
    with col_form2:
        sexe_label = st.selectbox("Sexe de l'enfant :", ["Fille 👧", "Garçon 👦"], key="nutri_sexe")
        sexe_key = "garcon" if "Garçon" in sexe_label else "fille"
    with col_form3:
        age_mois = st.slider("Âge (en mois) :", min_value=0, max_value=60, value=9, step=1, key="nutri_age")
    with col_form4:
        poids_actuel = st.number_input("Poids actuel (kg) :", min_value=1.5, max_value=35.0, value=8.2, step=0.1, key="nutri_poids")
    
    # Calculs des repères OMS
    seuils = get_seuils_oms(age_mois, sexe_key)
    statut = evaluer_statut(poids_actuel, seuils)
    ecart_kg = poids_actuel - seuils["mediane"]
    
    st.markdown("---")
    
    # Affichage des métriques clés
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Poids actuel de l'enfant", f"{poids_actuel:.1f} kg")
    with m2:
        st.metric("Poids Médian OMS (Idéal)", f"{seuils['mediane']:.1f} kg")
    with m3:
        signe = "+" if ecart_kg >= 0 else ""
        st.metric("Écart / Médiane", f"{signe}{ecart_kg:.1f} kg", delta=f"{signe}{ecart_kg:.1f} kg")
    with m4:
        st.metric("Seuil Alerte Dénutrition (-2SD)", f"{seuils['sd2neg']:.1f} kg")
    
    # Message de diagnostic
    if statut["couleur"] == "error":
        st.error(f"### {statut['symbole']} {statut['statut']}\n**{statut['message']}**\n\n{statut['action']}")
    elif statut["couleur"] == "warning":
        st.warning(f"### {statut['symbole']} {statut['statut']}\n**{statut['message']}**\n\n{statut['action']}")
    elif statut["couleur"] == "success":
        st.success(f"### {statut['symbole']} {statut['statut']}\n**{statut['message']}**\n\n{statut['action']}")
    else:
        st.info(f"### {statut['symbole']} {statut['statut']}\n**{statut['message']}**\n\n{statut['action']}")
    
    # Graphique Courbe de Croissance OMS
    st.markdown("#### 📉 Courbe de Croissance Poids / Âge OMS (0 à 60 mois)")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ages = seuils["ages_courbe"]
    sd3neg = seuils["sd3neg_courbe"]
    sd2neg = seuils["sd2neg_courbe"]
    med = seuils["mediane_courbe"]
    sd2pos = seuils["sd2pos_courbe"]
    
    # Zones de couleur OMS
    ax.fill_between(ages, sd2neg, sd2pos, color="#c8e6c9", alpha=0.6, label="Zone Verte : Poids Normal (-2SD à +2SD)")
    ax.fill_between(ages, sd3neg, sd2neg, color="#fff9c4", alpha=0.8, label="Zone Jaune : Insuffisance modérée MAM (-3SD à -2SD)")
    ax.fill_between(ages, 0, sd3neg, color="#ffcdd2", alpha=0.6, label="Zone Rouge : Danger MAS (<-3SD)")
    
    # Lignes des seuils
    ax.plot(ages, med, color="#2e7d32", linewidth=2.2, linestyle="-", label="Médiane OMS (Moyenne idéale)")
    ax.plot(ages, sd2neg, color="#fbc02d", linewidth=1.5, linestyle="--", label="Seuil -2 Écart-Type (MAM)")
    ax.plot(ages, sd3neg, color="#d32f2f", linewidth=1.5, linestyle="--", label="Seuil -3 Écart-Type (MAS)")
    
    # Point de l'enfant
    point_color = "#d32f2f" if statut["code"] == "ROUGE" else ("#f57f17" if statut["code"] == "JAUNE" else ("#2e7d32" if statut["code"] == "VERT" else "#1976d2"))
    ax.scatter([age_mois], [poids_actuel], color=point_color, s=160, zorder=5, edgecolor="black", linewidth=1.8, label=f"Position de {nom_enfant} ({poids_actuel} kg)")
    
    ax.annotate(
        f"{nom_enfant}\n({poids_actuel} kg à {age_mois} mois)",
        xy=(age_mois, poids_actuel),
        xytext=(age_mois + 1.5, poids_actuel + 0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=point_color, lw=1.5),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", color=point_color, lw=1.5),
        fontweight="bold"
    )
    
    ax.set_title(f"Courbe de Suivi de Croissance OMS — {sexe_label} (0 à 5 ans)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Âge de l'enfant (en mois)", fontsize=10, fontweight="bold")
    ax.set_ylabel("Poids (en kilogrammes)", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, max(26, float(poids_actuel + 3)))
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.95)
    
    st.pyplot(fig)
    plt.close(fig)

# =============================================================
# ONGLET 2 : GUIDE ALIMENTAIRE OFFICIEL SELON L'ÂGE
# =============================================================
with tab2:
    st.subheader("🥗 Recommandations Nutritionnelles OMS & Ministère de la Santé")
    
    # Sélection de la tranche d'âge
    options_tranches = [f"{t['tranche']} — {t['titre']}" for t in tranches_age]
    
    # Index par défaut basé sur l'âge sélectionné dans l'onglet 1
    idx_default = 0
    if age_mois <= 6:
        idx_default = 0
    elif age_mois <= 8:
        idx_default = 1
    elif age_mois <= 11:
        idx_default = 2
    elif age_mois <= 23:
        idx_default = 3
    else:
        idx_default = 4
    
    tranche_choisie = st.selectbox("Sélectionnez la tranche d'âge à consulter :", options_tranches, index=idx_default)
    item_tranche = tranches_age[options_tranches.index(tranche_choisie)]
    
    st.markdown(f"### 📌 {item_tranche['titre']} (`{item_tranche['tranche']}`)")
    st.caption(f"Badge officiel : **{item_tranche.get('badge', '')}**")
    
    col_guide_fr, col_guide_wo = st.columns(2)
    with col_guide_fr:
        st.info(f"**🇫🇷 Recommandation Officielle (Français) :**\n\n{item_tranche['recommandation_fr']}")
    with col_guide_wo:
        st.success(f"**🇸🇳 Recommandation ci Wolof :**\n\n*{item_tranche['recommandation_wo']}*")
    
    c_freq, c_consist, c_quant = st.columns(3)
    with c_freq:
        st.write(f"⏰ **Fréquence :** {item_tranche.get('frequence', 'Non spécifié')}")
    with c_consist:
        st.write(f"🥣 **Consistance :** {item_tranche.get('consistance', 'Non spécifié')}")
    with c_quant:
        if "quantite" in item_tranche:
            st.write(f"🥄 **Quantité par repas :** {item_tranche['quantite']}")
        elif "colostrum" in item_tranche:
            st.write(f"💧 **Colostrum :** {item_tranche['colostrum']}")
            
    st.markdown("---")
    col_conseils, col_interdits = st.columns(2)
    
    with col_conseils:
        st.markdown("#### ✅ Aliments locaux hautement recommandés :")
        if "aliments_conseilles" in item_tranche:
            for alim in item_tranche["aliments_conseilles"]:
                st.markdown(f"- 🍲 **{alim}**")
        else:
            st.markdown("- 🤱 **Lait maternel exclusif à 100% (Aucun autre aliment)**")
            
    with col_interdits:
        st.markdown("#### 🚫 Pratiques et aliments formellement déconseillés :")
        for interdit in item_tranche.get("aliments_interdits", []):
            st.markdown(f"- ❌ *{interdit}*")

# =============================================================
# ONGLET 3 : RECETTES LOCALES ENRICHIES DU SÉNÉGAL
# =============================================================
with tab3:
    st.subheader("🍲 Guide des Recettes Fortifiées Locales (Casamance & Sénégal)")
    st.write("Recettes pédiatriques équilibrées à base d'ingrédients locaux sains, peu coûteux et très riches en micronutriments.")
    
    recette_noms = [r["nom"] for r in recettes]
    recette_selection = st.selectbox("Choisissez une recette pédiatrique à préparer :", recette_noms)
    r = next(item for item in recettes if item["nom"] == recette_selection)
    
    st.markdown(f"### {r['nom']}")
    
    r_c1, r_c2, r_c3 = st.columns(3)
    with r_c1:
        st.info(f"👶 **Âge d'introduction :** {r['age_cible']}")
    with r_c2:
        st.warning(f"⏱️ **Temps de cuisson :** {r['temps_preparation']}")
    with r_c3:
        st.success(f"💰 **Coût :** {r['cout']}")
        
    st.markdown(f"**🌟 Valeur Nutritionnelle OMS :** {r['valeur_nutritionnelle']}")
    
    col_rec_ing, col_rec_prep = st.columns([1, 2])
    with col_rec_ing:
        st.markdown("#### 🛒 Ingrédients locaux :")
        for ing in r["ingredients"]:
            st.markdown(f"- {ing}")
            
    with col_rec_prep:
        st.markdown("#### 👩‍🍳 Préparation étape par étape :")
        for etape in r["etapes"]:
            st.write(etape)
            
    st.markdown(f"> 💡 **Conseil d'expert OMS :** {r['astuce_oms']}")

# =============================================================
# ONGLET 4 : HYGIÈNE & PRÉVENTION DE LA MALNUTRITION
# =============================================================
with tab4:
    st.subheader("🛡️ Hygiène du Sevrage & Dépistage Précoce")
    
    st.markdown("#### 💧 Les 4 Règles d'Or de l'Hygiène pour éviter les diarrhées mortelles")
    st.caption("Au Sénégal, la diarrhée du nourrisson lors de la diversification est souvent causée par le manque d'eau propre ou l'usage de biberons.")
    
    for rh in regles_hygiene:
        with st.expander(f"📌 {rh['regle']}", expanded=True):
            st.write(rh["detail"])
            
    st.markdown("---")
    st.markdown("#### 🔍 Signes d'alerte clinique de la malnutrition à surveiller chez l'enfant :")
    
    c_alerte1, c_alerte2 = st.columns(2)
    with c_alerte1:
        st.error("""
        **1. Le Kwashiorkor (Malnutrition par carence en protéines) :**
        - Enflure / œdème qui commence par le dos des deux pieds et des jambes (fait le test du godet : presser avec le pouce 3 secondes, l'empreinte reste marquée).
        - Visage boursouflé (« visage lunaire »).
        - Cheveux cassants, décolorés (roux ou grisâtres).
        - Tristesse, apathie et perte totale d'appétit.
        """)
    with c_alerte2:
        st.error("""
        **2. Le Marasme (Malnutrition par fonte énergétique totale) :**
        - Émaciation extrême : la peau sur les os, fonte visible des muscles des fesses (« culotte flottante »).
        - Côtes et os saillants bien visibles.
        - Visage de vieillard ridé.
        - Enfant anxieux et affamé au début, puis léthargique.
        """)

# =============================================================
# ONGLET 5 : FICHE BILAN NUTRITIONNEL TÉLÉCHARGEABLE
# =============================================================
with tab5:
    st.subheader("📄 Fiche Bilan Nutritionnelle Personnalisée")
    st.write("Générez et téléchargez le compte-rendu pour le carnet de santé de l'enfant ou pour l'équipe du poste de santé.")
    
    fiche_texte = f"""======================================================================
               FICHE DE SUIVI NUTRITIONNEL PÉDIATRIQUE (OMS)
                          PLATEFORME MAMACARE IA
             Université Assane Seck de Ziguinchor (UASZ) - Groupe 10
             Module géré par : ADJA FATOU BINETOU SARR
======================================================================

1. IDENTITÉ DE L'ENFANT
----------------------------------------------------------------------
Prénom de l'enfant : {nom_enfant}
Sexe               : {sexe_label}
Âge actuel         : {age_mois} mois
Poids mesuré       : {poids_actuel} kg

2. ANALYSE STATISTIQUE SELON LES STANDARDS DE L'OMS
----------------------------------------------------------------------
Poids Médian de référence (Idéal) : {seuils['mediane']:.1f} kg
Seuil Insuffisance Modérée (-2SD) : {seuils['sd2neg']:.1f} kg
Seuil Malnutrition Sévère (-3SD)  : {seuils['sd3neg']:.1f} kg
Écart par rapport à la médiane    : {ecart_kg:+.1f} kg

3. DIAGNOSTIC ET CLASSIFICATION
----------------------------------------------------------------------
Statut : {statut['statut']}
Évaluation clinique : {statut['message']}
Conduite à tenir recommandée :
{statut['action']}

4. CONSEILS ALIMENTAIRES POUR CET ÂGE ({item_tranche['tranche']})
----------------------------------------------------------------------
Titre : {item_tranche['titre']}
Recommandation officielle :
{item_tranche['recommandation_fr']}

Recommandation en Wolof :
{item_tranche['recommandation_wo']}

Fréquence recommandée : {item_tranche.get('frequence', 'Selon besoin')}
Consistance adaptée   : {item_tranche.get('consistance', 'Aliments sains')}

5. RECETTE LOCALE CASAMANÇAISE CONSEILLÉE
----------------------------------------------------------------------
Nom de la recette : {r['nom']}
Ingrédients :
{chr(10).join(['- ' + ing for ing in r['ingredients']])}

Préparation :
{chr(10).join([etape for etape in r['etapes']])}

Rappel d'hygiène : Toujours laver les mains au savon et à l'eau propre.
======================================================================
Fiche générée automatiquement par MamaCare IA — Santé Maternelle & Pédiatrie
"""
    
    st.text_area("Aperçu de la fiche récapitulative :", value=fiche_texte, height=320)
    
    st.download_button(
        label=f"📥 Télécharger la Fiche Nutrition de {nom_enfant} (.txt)",
        data=fiche_texte,
        file_name=f"Fiche_Nutrition_MamaCare_{nom_enfant}_{age_mois}mois.txt",
        mime="text/plain"
    )

st.markdown("---")
st.caption("MamaCare IA — Module 3 Nutrition Pédiatrique OMS — UASZ L3 Ingénierie Informatique — Adja Fatou Binetou SARR")

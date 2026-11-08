# 🤱 MamaCare IA — Santé Maternelle & Pédiatrie
**Université Assane Seck de Ziguinchor (UASZ)** — Département d'Informatique — L3 Ingénierie Informatique  
**Projet d'Innovation Technologique — Groupe N° 10**

---

## 👥 Membres du Groupe & Branches Git dédiées

| Membre | Module assigné | Fichier Page | Fichier Données | Nom de la branche Git |
| :--- | :--- | :--- | :--- | :--- |
| **Mamadou SENE** | Module 1 : Chatbot IA & Garde-Fou | `pages/1_Chatbot_IA.py` | `data/base_connaissances_ia.json` | `feature/chatbot-sene` |
| **Mamadou Lamine CISSOKO** | Module 2 : Triage Symptômes PCIME | `pages/2_Triage_Symptomes.py` | `data/symptomes_pcime.json` | `feature/triage-cissoko` |
| **Adja Fatou Binetou SARR** | Module 3 : Nutrition OMS (0-5 ans) | `pages/3_Nutrition_OMS.py` | `data/nutrition_oms.json` | `feature/nutrition-sarr` |
| **Colle SYLL** | Module 4 : Calendrier Vaccinal PEV | `pages/4_Calendrier_Vaccinal.py` | `data/vaccins_pev_senegal.json` | `feature/vaccins-syll` |
| **Mame Diarra NDIAYE** | Module 5 : Langues Locales & Audio | `pages/5_Langues_Locales_Audio.py` | `data/langues_locales.json` | `feature/audio-ndiaye` |

---

## 🚀 Installation & Démarrage Rapide

1. Cloner le projet :
```bash
git clone <URL_DU_DEPOT_GITHUB>
cd MamaCare_IA
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l'application :
```bash
streamlit run app.py
```

---

## 🌿 Comment travailler sur sa propre branche Git (Zéro Conflit)

Chaque membre crée et utilise **uniquement** sa propre branche :

### 1. Créer et aller sur sa branche :
```bash
# Exemple pour Mamadou Sene :
git checkout -b feature/chatbot-sene

# Exemple pour Colle Syll :
git checkout -b feature/vaccins-syll
```

### 2. Travailler sur ses fichiers :
Chacun ne modifie **que ses 2 fichiers** attitrés (`pages/...` et `data/...`).

### 3. Sauvegarder et envoyer sur GitHub :
```bash
git add pages/ data/
git commit -m "Mise a jour de mon module"
git push -u origin feature/nom-de-ma-branche
```

### 4. Fusionner sur `main` :
Sur GitHub, créer une **Pull Request** pour fusionner votre branche sur `main` proprement !

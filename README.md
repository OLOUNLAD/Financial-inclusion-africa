# 🌍 Financial Inclusion in Africa — Projet Intégrateur Data Science

> **Projet Intégrateur : De la donnée brute au déploiement d'une application fonctionnelle avec réentraînement automatique.**  
> Données réelles issues de la plateforme **Zindi Africa** (*Financial Inclusion in Africa Challenge*).  
> Algorithme retenu : **XGBoost** avec optimisation du seuil de décision (**ROC-AUC : 0.8767**).

---

## 📌 1. Contexte Métier & Objectif

L'inclusion financière reste un levier majeur de développement économique en Afrique subsaharienne. L'accès à un compte bancaire formel facilite l'épargne sécurisée, l'obtention de crédits et la résilience économique des ménages.

* **Problème Data Science :** Classification binaire supervisée (`bank_account` = `Yes` ou `No`).
* **Périmètre géographique :** Kenya, Rwanda, Tanzanie, Ouganda (~23 524 individus analysés).
* **Enjeux :** Identifier les facteurs socio-démographiques favorisant l'exclusion bancaire pour orienter les offres de micro-finance et de Mobile Money.

---

## 🐙 2. Guide d'Initialisation et Publication sur GitHub

Si vous venez de recevoir ce dossier (ou pour le chef de groupe qui crée le dépôt distant) :

### Étape 1 : Créer le dépôt sur GitHub
1. Connectez-vous sur [GitHub](https://github.com) et cliquez sur **« New repository »**.
2. Nommez le dépôt (ex: `financial-inclusion-africa`).
3. Choisissez **Public** *(exigé par le barème)*.
4. Ne cochez **PAS** « Add README » ou « Add .gitignore » (ils existent déjà dans ce dossier).
5. Cliquez sur **« Create repository »**.

### Étape 2 : Relier ce dossier local au dépôt GitHub
Dans le terminal, à la racine du dossier `Data_science` :

```bash
# 1. Vérifier la branche par défaut (main)
git branch -M main

# 2. Lier votre dépôt distant (remplacez avec votre URL GitHub)
git remote add origin https://github.com/<votre-utilisateur-github>/financial-inclusion-africa.git

# 3. Envoyer tout le projet sur GitHub
git push -u origin main
```

### Étape 3 : Pour les collègues qui récupèrent le projet
Une fois en ligne, les autres membres du groupe peuvent simplement cloner le dépôt :
```bash
git clone https://github.com/<votre-utilisateur-github>/financial-inclusion-africa.git
cd financial-inclusion-africa
```

---

## 🚀 3. Déploiement et Lancement de l'Application

Le modèle entraîné est déjà présent dans `models/best_model.joblib`. **L'application est immédiatement fonctionnelle sans réentraînement.**

### Option A : Déploiement Docker (Recommandé - 1 commande)
La solution la plus rapide et portable (aucune installation de dépendances requise, Docker s'occupe de tout) :

```bash
docker-compose up --build
```
👉 Ouvrez votre navigateur sur : **`http://localhost:8000`**

---

### Option B : Lancement Local (Python + FastAPI)
Si vous préférez exécuter l'application directement dans votre environnement Python :

```bash
# 1. Activer votre environnement Conda ou créer un venv
conda activate data
# ou: python -m venv venv && source venv/bin/activate

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Compiler le frontend React (si ce n'est pas déjà fait)
cd frontend && npm install && npm run build && cd ..

# 4. Lancer le serveur API FastAPI (qui sert aussi l'interface web)
uvicorn api:app --port 8000
```
👉 Ouvrez votre navigateur sur : **`http://localhost:8000`**

---

### Option C : Mode Développement Frontend (Rechargement à chaud)
Si vous souhaitez apporter des modifications en direct au code React :
```bash
# Terminal 1 : API FastAPI
uvicorn api:app --port 8000

# Terminal 2 : Serveur Vite React avec hot-reload
cd frontend && npm run dev
```
👉 Interface de dev sur : **`http://localhost:5173`** (avec proxy automatique vers l'API 8000).

---

### Option D : Déploiement Cloud Public Gratuit (Bonus pour la soutenance)
Pour donner un lien public en ligne accessible par le jury (sans machine locale) :
1. Créez un compte gratuit sur [Render.com](https://render.com).
2. Cliquez sur **New +** $\rightarrow$ **Web Service**.
3. Connectez votre dépôt GitHub `financial-inclusion-africa`.
4. Sélectionnez l'environnement **Docker** (Render détecte automatiquement le `Dockerfile`).
5. Cliquez sur **Deploy** : en 3 minutes, vous obtenez une URL publique HTTPS du type `https://finclusion-africa.onrender.com`.

---

## 🔁 4. Automatisation et Réentraînement (MLOps)

Conformément à la section 2.4 du sujet, le pipeline de réentraînement automatique gère l'arrivée de nouvelles données, valide la qualité du modèle avant mise en production, et met à jour l'application en continu.

### A. Déclenchement Manuel
```bash
# Avec les données actuelles
python src/retrain.py

# Avec un nouveau fichier de données
python src/retrain.py --data-path data/NouvellesDonnees.csv --min-roc-auc 0.75
```
* Le script compare 4 algorithmes, calcule le seuil de décision optimal et contrôle que le ROC-AUC est $\ge 0.75$.
* L'historique complet des exécutions est consigné dans **`retraining.log`**.
* L'API FastAPI recharge le modèle dynamiquement : le nouveau modèle est **actif immédiatement sans redémarrer le serveur**.

### B. Pipeline Planifié par Cron (Automatique)
Un script et un fichier de configuration prêts à l'emploi sont fournis :
* Script exécutable : [`scripts/retrain_cron.sh`](scripts/retrain_cron.sh)
* Planification exemple : [`cron/crontab.txt`](cron/crontab.txt)

```bash
# Pour programmer un réentraînement automatique chaque dimanche à 02h00 :
crontab -e
# Ajouter la ligne :
0 2 * * 0 /chemin/vers/Data_science/scripts/retrain_cron.sh >> /chemin/vers/Data_science/retraining.log 2>&1
```

### C. Déclenchement Distant via API REST (Webhook / Airflow)
Vous pouvez déclencher le réentraînement à distance en un appel HTTP :
```bash
curl -X POST http://localhost:8000/api/retrain
```

---

## 📂 5. Architecture du Projet

```text
├── api.py                         # Serveur API REST FastAPI & hébergement du frontend
├── frontend/                      # Application Web React moderne (Vite, Tailwind, Recharts)
│   ├── src/
│   │   ├── App.tsx                # Composants interactifs & jauge de prédiction
│   │   └── index.css              # Thème Emerald Slate (21st.dev tokens)
│   └── package.json
├── data/
│   ├── Train.csv                  # Données d'entraînement Zindi (~23 524 lignes)
│   ├── Test.csv                   # Données de test
│   └── VariableDefinitions.csv    # Dictionnaire des variables FinScope
├── models/
│   ├── best_model.joblib          # Pipeline sérialisé complet (prétraitement + XGBoost)
│   └── metrics.json               # Scores et métriques comparatives
├── src/
│   ├── EDA_financial_inclusion.py # Script complet d'analyse exploratoire (EDA)
│   ├── preprocessing.py           # Nettoyage, encodage OneHot et Standardisation
│   ├── train.py                   # Entraînement et benchmark des modèles
│   └── retrain.py                 # Pipeline de réentraînement avec garde-fous
├── scripts/
│   └── retrain_cron.sh            # Script shell d'exécution pour tâche cron
├── cron/
│   └── crontab.txt                # Exemple de configuration crontab
├── Dockerfile                     # Image multi-étape (Node build + Python runtime)
├── docker-compose.yml             # Orchestration Docker Compose
├── requirements.txt               # Dépendances Python
├── retraining.log                 # Journal de bord des réentraînements
└── README.md                      # Documentation du projet
```

---

## 📊 6. Résultats et Comparatif des Modèles

Évaluation rigoureuse sur un échantillon de test de **20 % (stratifié)**. En raison du fort déséquilibre de la cible (~14 % de bancarisés), les modèles sont évalués sur le **ROC-AUC** et le **F1-Score**, avec un **seuil de décision optimisé par validation croisée**.

| Modèle | Accuracy | Précision | Rappel (Recall) | F1-Score | ROC-AUC | Seuil optimal |
|---|---|---|---|---|---|---|
| **Régression Logistique** | 85.70 % | 49.35 % | 62.69 % | 0.5522 | 0.8646 | 0.65 |
| **Random Forest** | 85.55 % | 48.95 % | 63.60 % | 0.5532 | 0.8702 | 0.62 |
| **LightGBM** | 87.08 % | 53.71 % | 59.06 % | 0.5626 | 0.8766 | 0.69 |
| **XGBoost (Modèle Retenu)** | **86.93 %** | **53.14 %** | **60.12 %** | **0.5641** | **0.8767** | **0.68** |

### Enseignements clés de modélisation :
1. **Facteurs dominants :** Le niveau d'instruction (`Tertiary education`) et le type d'emploi (`Formally employed`) sont les prédicteurs les plus puissants de l'inclusion financière.
2. **Gestion du déséquilibre :** L'ajustement du poids des classes (`scale_pos_weight`) et l'optimisation du seuil de décision à **0.68** permettent de maximiser le F1-Score tout en maintenant un excellent Rappel sur la classe minoritaire.
3. **Sélection :** **XGBoost** surpasse les autres algorithmes avec un score ROC-AUC de **0.8767**.

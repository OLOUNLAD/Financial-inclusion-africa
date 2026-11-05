# Finclusion Africa

Application d'intelligence artificielle permettant de prédire la probabilité qu'un individu dispose d'un compte bancaire formel en Afrique de l'Est (Kenya, Rwanda, Tanzanie, Ouganda) à partir de son profil socio-démographique.

🔗 **Démo en ligne :** [https://financial-inclusion-africa-4duh.onrender.com](https://financial-inclusion-africa-4duh.onrender.com/)

* **Données :** Enquêtes FinScope issues du challenge Zindi Africa.
* **Modèle en production :** XGBoost.

---

## Installation et Lancement

### Avec Docker (Recommandé)
Une seule commande pour construire et lancer l'application :
```bash
docker-compose up --build
```
L'interface est accessible sur **http://localhost:8000**.

### Sans Docker (Python local)
Prérequis : Python 3.10+ et Node.js 20+

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Compiler l'interface web (React)
cd frontend && npm install && npm run build && cd ..

# 3. Lancer l'application
uvicorn api:app --port 8000
```
L'interface est accessible sur **http://localhost:8000**.

---

## 🔁 Réentraînement du modèle

Le modèle pré-entraîné est déjà inclus dans `models/best_model.joblib`.

Pour réentraîner le modèle sur de nouvelles données ou planifier une mise à jour :
```bash
python src/retrain.py                          # Données par défaut
python src/retrain.py --data-path nouveau.csv  # Nouvelles données
```

---

## 📂 Structure du projet

```text
├── api.py                         # API FastAPI et serveur web
├── frontend/                      # Interface utilisateur React
├── data/                          # Données d'entraînement et dictionnaires
├── models/                        # Modèle sérialisé (XGBoost) et métriques
├── src/
│   ├── EDA_financial_inclusion.py # Analyse exploratoire des données
│   ├── preprocessing.py           # Pipeline de transformation des features
│   ├── train.py                   # Entraînement et benchmark
│   └── retrain.py                 # Script de réentraînement automatique
├── scripts/
│   └── retrain_cron.sh            # Script pour automatisation (cron)
├── Dockerfile / docker-compose.yml # Fichiers de conteneurisation
└── requirements.txt               # Dépendances Python
```

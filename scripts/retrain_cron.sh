#!/usr/bin/env bash
# ==============================================================================
# Script de réentraînement automatique planifié (exécuté par cron ou orchestrateur)
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "------------------------------------------------------------------"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Démarrage du réentraînement automatique..."

# Détection de l'exécutable Python (Conda ou système)
if [ -f "/home/stj/.conda/envs/data/bin/python" ]; then
    PYTHON_BIN="/home/stj/.conda/envs/data/bin/python"
elif [ -f "$PROJECT_DIR/venv/bin/python" ]; then
    PYTHON_BIN="$PROJECT_DIR/venv/bin/python"
else
    PYTHON_BIN="python3"
fi

# Exécution du réentraînement
$PYTHON_BIN src/retrain.py --data-path data/Train.csv --min-roc-auc 0.75

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fin du pipeline de réentraînement."
echo "------------------------------------------------------------------"


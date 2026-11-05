import os
import sys

# Assurer l'accès aux modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import logging
from datetime import datetime
import json
import joblib

from src.train import train_and_select_best_model

LOG_FILE = "retraining.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run_retraining(data_path: str = "data/Train.csv", min_roc_auc: float = 0.75):
    """Exécute le réentraînement automatique et valide le nouveau modèle avant mise en production."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Démarrage du pipeline de réentraînement...")
    logging.info(f"Démarrage du réentraînement avec le fichier : {data_path}")
    
    try:
        pipeline, metrics = train_and_select_best_model(data_path=data_path)
        new_roc_auc = metrics["roc_auc"]
        
        # Critère d'acceptation du nouveau modèle
        if new_roc_auc >= min_roc_auc:
            msg = (f"Réentraînement réussi avec succès. Modèle : {metrics['model']} | "
                   f"ROC-AUC: {new_roc_auc:.4f} >= Seuil ({min_roc_auc:.4f}). "
                   f"Nouveau modèle déployé en production.")
            print(f"✅ {msg}")
            logging.info(msg)
            return True
        else:
            msg = (f"Alerte : Le modèle réentraîné ({metrics['model']}) a un ROC-AUC de {new_roc_auc:.4f}, "
                   f"inférieur au seuil exigé de {min_roc_auc:.4f}. Le modèle n'est pas déployé.")
            print(f"⚠️ {msg}")
            logging.warning(msg)
            return False
            
    except Exception as e:
        err_msg = f"Erreur critique lors du réentraînement : {str(e)}"
        print(f"❌ {err_msg}")
        logging.error(err_msg, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de réentraînement automatique du modèle Data Science.")
    parser.add_argument("--data-path", type=str, default="data/Train.csv", help="Chemin vers les nouvelles données.")
    parser.add_argument("--min-roc-auc", type=float, default=0.75, help="Seuil minimal de ROC-AUC pour valider le modèle.")
    args = parser.parse_args()
    
    run_retraining(data_path=args.data_path, min_roc_auc=args.min_roc_auc)

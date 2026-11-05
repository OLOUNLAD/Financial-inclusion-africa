import os
import sys

# Assurer l'accès aux modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    precision_recall_curve,
    classification_report
)
import lightgbm as lgb
from xgboost import XGBClassifier

from src.preprocessing import (
    load_raw_data,
    split_features_target,
    get_feature_preprocessor
)


def find_best_threshold(pipeline, X_train, y_train) -> float:
    """Trouve le seuil de décision qui maximise le F1-score.

    Les probabilités sont obtenues par validation croisée sur le jeu d'entraînement
    uniquement (le jeu de test n'est jamais utilisé pour choisir le seuil).
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    proba = cross_val_predict(pipeline, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_train, proba)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    return float(thresholds[f1[:-1].argmax()])


def evaluate_model(pipeline, X_test, y_test, model_name: str, threshold: float = 0.5) -> dict:
    """Évalue un modèle (au seuil donné) et retourne un dictionnaire de métriques."""
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)
    
    metrics = {
        "model": model_name,
        "threshold": float(threshold),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba))
    }
    return metrics


def train_and_select_best_model(data_path: str = "data/Train.csv", model_dir: str = "models"):
    """Entraîne et compare plusieurs modèles, puis sauvegarde le meilleur."""
    os.makedirs(model_dir, exist_ok=True)
    
    print("🔹 Chargement des données...")
    df = load_raw_data(data_path)
    X, y = split_features_target(df)
    
    print(f" Dataset: {X.shape[0]} lignes, {X.shape[1]} variables.")
    print(f"   Distribution de la cible: {dict(y.value_counts(normalize=True).round(3))}")
    
    # Division train / test stratifiée
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    preprocessor = get_feature_preprocessor()
    
    # Poids de la classe minoritaire (≈ 5,9) pour XGBoost
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    # Hyperparamètres des modèles à base d'arbres choisis plus "réguliers" (testés en validation croisée)
    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Random_Forest": RandomForestClassifier(n_estimators=150, max_depth=10, class_weight="balanced", random_state=42, n_jobs=-1),
        "LightGBM": lgb.LGBMClassifier(
            n_estimators=300, max_depth=4, num_leaves=15, learning_rate=0.03, min_child_samples=30,
            subsample=0.8, subsample_freq=1, colsample_bytree=0.7, reg_lambda=5,
            class_weight="balanced", random_state=42, verbose=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300, max_depth=4, learning_rate=0.03, min_child_weight=3,
            subsample=0.8, colsample_bytree=0.7, reg_lambda=5,
            scale_pos_weight=scale_pos_weight, eval_metric="logloss", random_state=42
        )
    }
    
    results = []
    trained_pipelines = {}
    
    print("\n🚀 Entraînement et comparaison des modèles :")
    for name, clf in models.items():
        print(f"   - Entraînement de {name}...")
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        pipeline.fit(X_train, y_train)
        
        # Seuil de décision optimisé pour le F1 (calculé sur le train uniquement)
        threshold = find_best_threshold(pipeline, X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test, name, threshold)
        results.append(metrics)
        trained_pipelines[name] = pipeline
        print(f"     -> F1-Score: {metrics['f1_score']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f} | Seuil: {threshold:.2f}")
    
    # Sélection du meilleur modèle basé sur le ROC-AUC / F1-Score
    best_result = max(results, key=lambda m: m["roc_auc"])
    best_name = best_result["model"]
    best_pipeline = trained_pipelines[best_name]
    
    print(f"\n🏆 Meilleur modèle retenu : {best_name} (ROC-AUC = {best_result['roc_auc']:.4f})")
    
    # Sauvegarde
    model_path = os.path.join(model_dir, "best_model.joblib")
    metrics_path = os.path.join(model_dir, "metrics.json")
    
    joblib.dump(best_pipeline, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({"all_models": results, "best_model": best_result}, f, indent=4)
        
    print(f" Modèle sauvegardé dans : {model_path}")
    print(f" Métriques sauvegardées dans : {metrics_path}")
    return best_pipeline, best_result


if __name__ == "__main__":
    train_and_select_best_model()

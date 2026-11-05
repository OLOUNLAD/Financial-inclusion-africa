"""API FastAPI : expose le modèle entraîné, les métriques et des statistiques du dataset au frontend React."""
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from src.retrain import run_retraining

MODEL_PATH = "models/best_model.joblib"
METRICS_PATH = "models/metrics.json"
DATA_PATH = "data/Train.csv"
FRONTEND_DIST = "frontend/dist"

app = FastAPI(title="Financial Inclusion in Africa API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_model():
    return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None


def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


class Profile(BaseModel):
    country: str
    year: int
    location_type: str
    cellphone_access: str
    household_size: int = Field(ge=1, le=30)
    age_of_respondent: int = Field(ge=16, le=100)
    gender_of_respondent: str
    relationship_with_head: str
    marital_status: str
    education_level: str
    job_type: str


@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": os.path.exists(MODEL_PATH)}


@app.post("/api/predict")
def predict(profile: Profile):
    model = load_model()
    if model is None:
        raise HTTPException(503, "Aucun modèle trouvé. Lancez `python src/train.py`.")
    metrics = load_metrics()
    threshold = metrics["best_model"].get("threshold", 0.5) if metrics else 0.5
    proba = float(model.predict_proba(pd.DataFrame([profile.model_dump()]))[0][1])
    return {"probability": proba, "threshold": threshold, "banked": proba >= threshold}


@app.post("/api/retrain")
def trigger_retraining(data_path: str = "data/Train.csv", min_roc_auc: float = 0.75):
    """Déclenche le réentraînement du modèle (appelable par cron, webhook ou orchestrateur type Airflow)."""
    success = run_retraining(data_path=data_path, min_roc_auc=min_roc_auc)
    if not success:
        raise HTTPException(status_code=400, detail="Le modèle réentraîné n'a pas atteint le seuil de performance.")
    return {"status": "success", "message": "Modèle réentraîné et déployé en production", "metrics": load_metrics()}


@app.get("/api/metrics")
def metrics():
    data = load_metrics()
    if data is None:
        raise HTTPException(404, "metrics.json introuvable. Lancez `python src/train.py`.")
    return data


@app.get("/api/stats")
def stats():
    """Taux de bancarisation par variable, calculés sur Train.csv."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(404, "data/Train.csv introuvable.")
    df = pd.read_csv(DATA_PATH)
    df["y"] = (df["bank_account"] == "Yes").astype(int)

    def rate(col):
        g = df.groupby(col)["y"].agg(["mean", "count"]).reset_index()
        return [{"label": str(r[col]), "rate": round(float(r["mean"]) * 100, 2), "count": int(r["count"])}
                for _, r in g.sort_values("mean", ascending=False).iterrows()]

    return {
        "total": int(len(df)),
        "banked_rate": round(float(df["y"].mean()) * 100, 2),
        "by_country": rate("country"),
        "by_education": rate("education_level"),
        "by_job": rate("job_type"),
        "by_location": rate("location_type"),
        "by_gender": rate("gender_of_respondent"),
    }


# En production (Docker), l'API sert aussi le frontend compilé.
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")


import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Finclusion Africa | AI Banking Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS moderne (Design System FinTech & Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Gradient & Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 40%, #047857 100%);
        border-radius: 16px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #a7f3d0;
        font-weight: 500;
        max-width: 850px;
        line-height: 1.5;
    }
    .badge-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #ecfdf5;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Cartes Modernes */
    .glass-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .dark-mode .glass-card {
        background: #1e293b;
        border-color: #334155;
    }
    
    .card-header-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Résultat & KPI */
    .kpi-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #059669;
        margin-bottom: 0.8rem;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    /* Style des boutons Streamlit */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.4);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Chemins des fichiers
MODEL_PATH = "models/best_model.joblib"
METRICS_PATH = "models/metrics.json"
DATA_PATH = "data/Train.csv"


@st.cache_resource
def load_trained_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


@st.cache_data
def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


@st.cache_data
def load_dataset_sample():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None


# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="badge-tag">⚡ Machine Learning en Production • Zindi Africa Challenge</div>
    <div class="hero-title">🌍 Finclusion Africa — Plateforme d'Inclusion Bancaire</div>
    <div class="hero-subtitle">
        Modèle d'intelligence artificielle de pointe permettant de prédire l'accès aux services bancaires formels 
        en Afrique de l'Est (Kenya, Rwanda, Tanzanie, Ouganda) pour orienter les politiques d'inclusion financière et de micro-finance.
    </div>
</div>
""", unsafe_allow_html=True)

# Chargement du modèle et métriques
model = load_trained_model()
metrics_data = load_metrics()
df_data = load_dataset_sample()

# Navigation principale avec onglets stylisés
tab_sim, tab_data, tab_models = st.tabs([
    "🎯 Simulateur de Prédiction",
    "📊 Analyse des Données (EDA)",
    "⚙️ Modèles & Performances"
])

# ==============================================================================
# ONGLET 1 : SIMULATEUR DE PRÉDICTION
# ==============================================================================
with tab_sim:
    if model is None:
        st.error("⚠️ Aucun modèle trouvé dans `models/best_model.joblib`. Veuillez exécuter `python src/train.py`.")
    else:
        st.markdown("### 📋 Saisie du profil de l'individu")
        st.caption("Remplissez les informations socio-démographiques pour évaluer instantanément la probabilité de bancarisation.")

        # Formulaire structuré en 3 blocs visuels
        col_geo, col_demo, col_eco = st.columns(3)

        with col_geo:
            st.markdown("##### 📍 1. Localisation & Connectivité")
            country = st.selectbox("Pays", ["Kenya", "Rwanda", "Tanzania", "Uganda"], index=0)
            location_type = st.radio("Milieu de résidence", ["Urban", "Rural"], horizontal=True)
            cellphone_access = st.radio("Possède un téléphone portable", ["Yes", "No"], horizontal=True)
            year = st.selectbox("Année de référence", [2018, 2017, 2016], index=0)

        with col_demo:
            st.markdown("##### 👤 2. Démographie & Foyer")
            gender_of_respondent = st.radio("Genre", ["Female", "Male"], horizontal=True)
            age_of_respondent = st.slider("Âge (années)", min_value=16, max_value=100, value=32)
            household_size = st.slider("Taille du ménage", min_value=1, max_value=20, value=4)
            relationship_with_head = st.selectbox(
                "Lien avec le chef de famille",
                ["Head of Household", "Spouse", "Child", "Parent", "Other relative", "Other non-relatives", "Dont know"]
            )

        with col_eco:
            st.markdown("##### 💼 3. Éducation & Activité")
            education_level = st.selectbox(
                "Niveau d'éducation",
                [
                    "Tertiary education",
                    "Vocational/Specialised training",
                    "Secondary education",
                    "Primary education",
                    "No formal education",
                    "Other/Dont know/RTA"
                ],
                index=2
            )
            job_type = st.selectbox(
                "Type d'emploi / Revenu",
                [
                    "Formally employed Private",
                    "Formally employed Government",
                    "Self employed",
                    "Informally employed",
                    "Farming and Fishing",
                    "Remittance Dependent",
                    "Government Dependent",
                    "Other Income",
                    "No Income"
                ],
                index=2
            )
            marital_status = st.selectbox(
                "Statut matrimonial",
                ["Married/Living together", "Single/Never Married", "Widowed", "Divorced/Seperated", "Don’t know"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🚀 Calculer la Prédiction IA", use_container_width=True)

        if predict_btn:
            input_df = pd.DataFrame([{
                "country": country,
                "year": year,
                "location_type": location_type,
                "cellphone_access": cellphone_access,
                "household_size": household_size,
                "age_of_respondent": age_of_respondent,
                "gender_of_respondent": gender_of_respondent,
                "relationship_with_head": relationship_with_head,
                "marital_status": marital_status,
                "education_level": education_level,
                "job_type": job_type
            }])

            # Calcul de la probabilité
            proba = model.predict_proba(input_df)[0][1]
            threshold = metrics_data["best_model"].get("threshold", 0.68) if metrics_data else 0.68
            is_banked = int(proba >= threshold)

            st.markdown("---")
            st.markdown("### 📊 Résultat de l'Évaluation")

            res_col1, res_col2 = st.columns([1.1, 1.4])

            with res_col1:
                # Graphique Jauge Interactif Plotly
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=proba * 100,
                    number={'suffix': "%", 'font': {'size': 38, 'weight': 'bold', 'color': '#0f172a'}},
                    title={'text': "<b>Probabilité de Bancarisation</b><br><span style='font-size:0.85em;color:#64748b'>Score calculé par XGBoost</span>", 'font': {'size': 16}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                        'bar': {'color': "#10b981" if is_banked else "#f59e0b", 'thickness': 0.3},
                        'bgcolor': "white",
                        'borderwidth': 1,
                        'bordercolor': "#cbd5e1",
                        'steps': [
                            {'range': [0, 40], 'color': '#fee2e2'},
                            {'range': [40, threshold * 100], 'color': '#fef3c7'},
                            {'range': [threshold * 100, 100], 'color': '#d1fae5'}
                        ],
                        'threshold': {
                            'line': {'color': "#dc2626", 'width': 3},
                            'thickness': 0.8,
                            'value': threshold * 100
                        }
                    }
                ))
                fig_gauge.update_layout(
                    height=280,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Plus Jakarta Sans'}
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

            with res_col2:
                if is_banked:
                    st.success(f"### ✅ Profil : BANCARISÉ (Score: {proba*100:.1f} %)")
                    st.markdown(f"""
                    - **Statut :** La probabilité dépasse le seuil optimal d'inclusion (**{threshold*100:.1f} %**).
                    - **Facteurs déterminants :** Niveau d'instruction élevé, emploi formel ou présence en zone urbaine avec connectivité mobile.
                    - **Recommandation commerciale :** Candidat idéal pour des services bancaires classiques, des produits d'épargne rémunérée ou des lignes de crédit formelles.
                    """)
                else:
                    st.warning(f"### ⚠️ Profil : NON BANCARISÉ (Score: {proba*100:.1f} %)")
                    st.markdown(f"""
                    - **Statut :** La probabilité est sous le seuil d'inclusion financière (**{threshold*100:.1f} %**).
                    - **Facteurs de vulnérabilité :** Activité informelle/agricole, milieu rural ou absence d'instruction supérieure.
                    - **Recommandation stratégique :** Profil cible pour les programmes d'inclusion financière, le **Mobile Money (ex: M-Pesa)**, ou la micro-finance sans conditions de revenus fixes.
                    """)

# ==============================================================================
# ONGLET 2 : ANALYSE DES DONNÉES (EDA)
# ==============================================================================
with tab_data:
    st.markdown("### 🔍 Analyse Exploratoire des Données (FinScope)")
    st.caption("Aperçu interactif des déterminants majeurs issus du travail d'EDA.")

    if df_data is not None:
        # Métriques clés du dataset
        m1, m2, m3, m4 = st.columns(4)
        total_records = len(df_data)
        bank_rate = (df_data["bank_account"] == "Yes").mean() * 100
        m1.metric("Individus Enquêtés", f"{total_records:,}")
        m2.metric("Taux Moyen d'Inclusion", f"{bank_rate:.1f} %", delta="Cible déséquilibrée", delta_color="inverse")
        m3.metric("Pays Couverts", "4 (KE, RW, TZ, UG)")
        m4.metric("Données Manquantes", "0 (Dataset Propre)")

        st.markdown("---")

        # Visualisations interactives Plotly
        c_chart1, c_chart2 = st.columns(2)

        with c_chart1:
            # Taux par pays
            rate_country = df_data.groupby("country")["bank_account"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
            fig_country = px.bar(
                rate_country,
                x="country",
                y="bank_account",
                title="<b>Taux d'Inclusion Financière par Pays (%)</b>",
                color="country",
                text=rate_country["bank_account"].apply(lambda x: f"{x:.1f}%"),
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_country.update_layout(showlegend=False, yaxis_title="% avec compte bancaire", xaxis_title="")
            st.plotly_chart(fig_country, use_container_width=True)

        with c_chart2:
            # Taux par niveau d'éducation
            rate_edu = df_data.groupby("education_level")["bank_account"].apply(lambda s: (s == "Yes").mean() * 100).reset_index().sort_values("bank_account", ascending=True)
            fig_edu = px.bar(
                rate_edu,
                y="education_level",
                x="bank_account",
                orientation="h",
                title="<b>Impact de l'Éducation sur la Bancarisation (%)</b>",
                color="bank_account",
                color_continuous_scale="Viridis",
                text=rate_edu["bank_account"].apply(lambda x: f"{x:.1f}%")
            )
            fig_edu.update_layout(yaxis_title="", xaxis_title="% avec compte bancaire", coloraxis_showscale=False)
            st.plotly_chart(fig_edu, use_container_width=True)

        st.markdown("##### 📄 Échantillon des Données Brutes")
        st.dataframe(df_data.head(8), use_container_width=True)

# ==============================================================================
# ONGLET 3 : MODÈLES ET PERFORMANCES
# ==============================================================================
with tab_models:
    st.markdown("### 🏆 Comparatif et Performances des Algorithmes ML")
    st.caption("Évaluation rigoureuse sur le jeu de test (20% stratifié) avec seuil optimisé pour classes déséquilibrées.")

    if metrics_data:
        best = metrics_data["best_model"]
        
        # Cartes KPI du meilleur modèle
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Modèle Vainqueur", best["model"])
        k2.metric("ROC-AUC Score", f"{best['roc_auc']:.4f}", delta="Excellente discrimination")
        k3.metric("F1-Score Optimisé", f"{best['f1_score']:.4f}", delta=f"Seuil: {best.get('threshold', 0.5):.2f}")
        k4.metric("Précision Globale", f"{best['accuracy']*100:.1f} %")

        st.markdown("---")

        # Tableau comparatif complet
        st.markdown("##### 📊 Comparaison de tous les modèles testés")
        df_models = pd.DataFrame(metrics_data["all_models"])
        
        # Formater les colonnes
        format_df = df_models.copy()
        format_df["accuracy"] = (format_df["accuracy"] * 100).round(2).astype(str) + " %"
        format_df["precision"] = (format_df["precision"] * 100).round(2).astype(str) + " %"
        format_df["recall"] = (format_df["recall"] * 100).round(2).astype(str) + " %"
        format_df["f1_score"] = format_df["f1_score"].round(4)
        format_df["roc_auc"] = format_df["roc_auc"].round(4)
        
        st.dataframe(format_df.set_index("model"), use_container_width=True)

        # Graphique comparatif ROC-AUC vs F1
        fig_comp = px.bar(
            df_models,
            x="model",
            y=["roc_auc", "f1_score"],
            barmode="group",
            title="<b>Comparaison ROC-AUC vs F1-Score par Algorithme</b>",
            color_discrete_sequence=["#059669", "#0284c7"]
        )
        fig_comp.update_layout(yaxis_title="Score", xaxis_title="")
        st.plotly_chart(fig_comp, use_container_width=True)

    else:
        st.info("Aucune métrique disponible. Veuillez exécuter `python src/train.py`.")

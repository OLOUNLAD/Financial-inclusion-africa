"""Script de génération de la présentation PowerPoint officielle.

Style : sobre, académique et professionnel (sans emoji, sans thèmes criards).
Format : 16:9 panoramique standard.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 1. Initialisation de la présentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Palette sobre et professionnelle
COLOR_PRIMARY = RGBColor(15, 23, 42)      # Ardoise foncée #0f172a
COLOR_TEXT = RGBColor(30, 41, 59)          # Gris très foncé #1e293b
COLOR_MUTED = RGBColor(100, 116, 139)     # Gris neutre #64748b
COLOR_BORDER = RGBColor(203, 213, 225)    # Gris clair #cbd5e1
COLOR_BG_CARD = RGBColor(248, 250, 252)   # Fond gris très clair #f8fafc
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_FAMILY = "Arial"


def add_header(slide, title_text, category_text="PROJET INTÉGRATEUR – SCIENCE DES DONNÉES"):
    """Ajoute l'en-tête standardisé de chaque slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Catégorie / Fil d'Ariane
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_FAMILY
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_MUTED
    p_cat.space_after = Pt(4)
    
    # Titre de la slide
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY


def add_bullet_points(slide, points, left=Inches(0.8), top=Inches(1.8), width=Inches(11.7), height=Inches(5.0)):
    """Ajoute une zone de texte avec des puces formelles."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    for i, pt_text in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = pt_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(15)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(14)
        p.level = 0


# ==============================================================================
# SLIDE 1 : PAGE DE GARDE
# ==============================================================================
blank_layout = prs.slide_layouts[6]
s1 = prs.slides.add_slide(blank_layout)

title_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(4.5))
tf1 = title_box.text_frame
tf1.word_wrap = True

p_inst = tf1.paragraphs[0]
p_inst.text = "CERTIFICATION EN SCIENCE DES DONNÉES • TRAVAUX PRATIQUES"
p_inst.font.name = FONT_FAMILY
p_inst.font.size = Pt(12)
p_inst.font.bold = True
p_inst.font.color.rgb = COLOR_MUTED
p_inst.space_after = Pt(14)

p_t1 = tf1.add_paragraph()
p_t1.text = "De la Donnée Brute au Déploiement"
p_t1.font.name = FONT_FAMILY
p_t1.font.size = Pt(32)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_PRIMARY
p_t1.space_after = Pt(8)

p_sub = tf1.add_paragraph()
p_sub.text = "Modélisation et Déploiement de l'Inclusion Financière en Afrique de l'Est"
p_sub.font.name = FONT_FAMILY
p_sub.font.size = Pt(18)
p_sub.font.color.rgb = COLOR_TEXT
p_sub.space_after = Pt(36)

p_meta = tf1.add_paragraph()
p_meta.text = (
    "Enseignant : Msc. Osias Noël TOSSOU\n"
    "Dépôt GitHub : https://github.com/OLOUNLAD/Financial-inclusion-africa\n"
    "Application en production : https://financial-inclusion-africa-4duh.onrender.com\n"
    "Date : Novembre 2026"
)
p_meta.font.name = FONT_FAMILY
p_meta.font.size = Pt(13)
p_meta.font.color.rgb = COLOR_MUTED

# ==============================================================================
# SLIDE 2 : SOMMAIRE
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Plan de la Présentation", "STRUCTURE DU PROJET")
add_bullet_points(s2, [
    "1. Contexte & Problématique Métier : Enjeux économiques en Afrique de l'Est",
    "2. Analyse Exploratoire des Données (EDA) : Audit statistique et facteurs déterminants",
    "3. Prétraitement & Feature Engineering : Stratification et gestion du déséquilibre",
    "4. Modélisation & Comparatif : Évaluation des 4 algorithmes et sélection de XGBoost",
    "5. Architecture de Déploiement : Service REST FastAPI, interface React et Docker",
    "6. Pipeline d'Automatisation (MLOps) : Réentraînement automatique et tâche planifiée",
    "7. Démonstration de l'Application en Ligne & Perspectives d'Évolution"
])

# ==============================================================================
# SLIDE 3 : CONTEXTE ET ENJEUX MÉTIER
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Contexte et Enjeux de l'Inclusion Financière", "1. PROBLÉMATIQUE MÉTIER")
add_bullet_points(s3, [
    "Rôle clé de l'inclusion financière : levier central de réduction de la pauvreté, d'épargne sécurisée et d'accès au crédit pour les populations vulnérables.",
    "Contexte en Afrique subsaharienne : essor massif du Mobile Money, mais une part importante de la population adulte demeure exclue du système bancaire formel.",
    "Périmètre de l'étude : quatre économies d'Afrique de l'Est aux dynamiques variées (Kenya, Rwanda, Tanzanie, Ouganda).",
    "Enjeu opérationnel : identifier les freins socio-démographiques à la bancarisation pour concevoir des offres de micro-finance et d'épargne ciblées."
])

# ==============================================================================
# SLIDE 4 : CADRAGE DU PROBLÈME DATA SCIENCE
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Cadrage Data Science et Acteurs Concernés", "1. PROBLÉMATIQUE MÉTIER")
add_bullet_points(s4, [
    "Formulation du problème : classification binaire supervisée.",
    "Variable cible (Y) : détention d'un compte bancaire commercial (bank_account = Yes ou No).",
    "Variables explicatives (X) : caractéristiques socio-démographiques, économiques et d'équipement de l'individu.",
    "Bénéficiaires directs :",
    "  • Banques et institutions de micro-finance : scoring d'éligibilité et acquisition client.",
    "  • Régulateurs et banques centrales : mesure et suivi des politiques d'inclusion.",
    "  • Organisations de développement et ONG : ciblage des populations marginalisées."
])

# ==============================================================================
# SLIDE 5 : DESCRIPTION DU JEU DE DONNÉES
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Description du Jeu de Données FinScope", "2. ANALYSE EXPLORATOIRE (EDA)")
add_bullet_points(s5, [
    "Source des données : enquêtes nationales FinScope, hébergées sur la plateforme Zindi Africa.",
    "Volumétrie : 23 524 observations consolidées sur 4 pays et 13 variables.",
    "Variables numériques : âge de l'enquêté (16 à 100 ans) et taille du ménage (1 à 21 membres).",
    "Variables catégorielles : pays, milieu de résidence (Rural / Urban), possession d'un téléphone portable (Yes / No), genre, statut matrimonial, niveau d'éducation, profession.",
    "Période de collecte : années 2016 à 2018."
])

# ==============================================================================
# SLIDE 6 : QUALITÉ DES DONNÉES
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Audit de la Qualité des Données", "2. ANALYSE EXPLORATOIRE (EDA)")
add_bullet_points(s6, [
    "Valeurs manquantes : aucune donnée manquante (dataset complet à 100 %).",
    "Spécificité de l'identifiant (uniqueid) : la variable n'est pas unique globalement ; l'individu est identifié par le couple (country, uniqueid). Colonne exclue de la modélisation.",
    "Préservation des profils identiques : 4 429 individus partagent un profil socio-démographique identique tout en ayant des identifiants distincts. Ces observations ont été intégralement conservées afin de respecter la distribution réelle de la population.",
    "Cohérence globale : aucune anomalie critique sur les âges et les variables qualitatives."
])

# ==============================================================================
# SLIDE 7 : DÉSÉQUILIBRE DE CLASSES
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Distribution de la Cible et Enjeux de Modélisation", "2. ANALYSE EXPLORATOIRE (EDA)")
add_bullet_points(s7, [
    "Distribution de la variable cible :",
    "  • Non bancarisés (No) : 20 212 individus, soit 85,92 % de l'échantillon.",
    "  • Bancarisés (Yes) : 3 312 individus, soit 14,08 % de l'échantillon.",
    "Ratio de déséquilibre : environ 6 individus non bancarisés pour 1 bancarisé.",
    "Conséquence méthodologique majeure :",
    "  • L'Accuracy brute est un indicateur inadapté (un prédicteur constant atteindrait 86 % de succès sans rien prédire).",
    "  • Nécessité impérative d'adopter des métriques adaptées : ROC-AUC et F1-Score sur la classe minoritaire."
])

# ==============================================================================
# SLIDE 8 : FACTEURS DISCRIMINANTS
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Principaux Enseignements Statistiques", "2. ANALYSE EXPLORATOIRE (EDA)")
add_bullet_points(s8, [
    "Niveau d'éducation (V de Cramér = 0,392) : déterminant n°1 de l'accès bancaire. Le taux passe de 4 % chez les personnes sans instruction à plus de 57 % au niveau supérieur.",
    "Type d'emploi (V de Cramér = 0,361) : 77 % de bancarisation chez les fonctionnaires et 54 % dans le privé formel, contre moins de 8 % dans le secteur informel ou agricole.",
    "Équipement en téléphonie mobile (V = 0,208) : pré-requis technique (18 % avec téléphone vs 2 % sans).",
    "Disparités territoriales : le Kenya présente le taux le plus élevé (25 %), suivi du Rwanda (11 %), de la Tanzanie (9 %) et de l'Ouganda (9 %).",
    "Dynamique d'âge : relation non linéaire en cloche, avec un pic d'accès entre 35 et 44 ans (18,2 %)."
])

# ==============================================================================
# SLIDE 9 : PRÉTRAITEMENT ET FEATURE ENGINEERING
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Pipeline de Prétraitement des Données", "3. MODÉLISATION")
add_bullet_points(s9, [
    "Encapsulation stricte scikit-learn (ColumnTransformer) pour éliminer tout risque de fuite d'information (data leakage).",
    "Traitement des variables numériques : centrage et réduction via StandardScaler (âge, taille du ménage, année).",
    "Traitement des variables catégorielles : encodage disjonctif complet via OneHotEncoder(handle_unknown='ignore').",
    "Stratégie de découpage : séparation train / test stratifiée à 80 % / 20 % préservant rigoureusement le ratio de 14,08 % de bancarisés dans les deux partitions."
])

# ==============================================================================
# SLIDE 10 : STRATÉGIE DE MODÉLISATION
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Choix des Algorithmes et Justification", "3. MODÉLISATION")
add_bullet_points(s10, [
    "1. Régression Logistique : modèle linéaire de référence (Baseline), rapide et explicable directement via les coefficients.",
    "2. Forêt Aléatoire (Random Forest) : méthode d'ensemble par ensachage (Bagging), robuste au surapprentissage et capturant les interactions complexes.",
    "3. LightGBM : gradient boosting sur arbres décisionnels, hautement optimisé en vitesse et en gestion de la mémoire.",
    "4. XGBoost : implémentation de pointe avec régularisation L2 et gestion intégrée de la pondération des classes via scale_pos_weight."
])

# ==============================================================================
# SLIDE 11 : TABLEAU COMPARATIF DES PERFORMANCES
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Benchmark Comparatif des Modèles", "3. MODÉLISATION")

# Création du tableau de comparaison
rows, cols = 5, 7
left, top, width, height = Inches(0.8), Inches(2.0), Inches(11.7), Inches(2.6)
table_shape = s11.shapes.add_table(rows, cols, left, top, width, height)
tbl = table_shape.table

headers = ["Modèle", "Accuracy", "Précision", "Rappel", "F1-Score", "ROC-AUC", "Seuil"]
tbl_data = [
    ["Régression Logistique", "85,70 %", "49,35 %", "62,69 %", "0,5522", "0,8646", "0,65"],
    ["Random Forest", "85,55 %", "48,95 %", "63,60 %", "0,5532", "0,8702", "0,62"],
    ["LightGBM", "87,08 %", "53,71 %", "59,06 %", "0,5626", "0,8766", "0,69"],
    ["XGBoost (Retenu)", "86,93 %", "53,14 %", "60,12 %", "0,5641", "0,8767", "0,68"]
]

for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_PRIMARY
    cell.text = h
    for p in cell.text_frame.paragraphs:
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

for row_idx, row in enumerate(tbl_data):
    for col_idx, val in enumerate(row):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BG_CARD if row_idx % 2 == 0 else COLOR_WHITE
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_FAMILY
            p.font.size = Pt(13)
            p.font.bold = (row_idx == 3)  # XGBoost en gras
            p.font.color.rgb = COLOR_TEXT
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

sub_box = s11.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8))
tf_sub = sub_box.text_frame
tf_sub.word_wrap = True
p_comm = tf_sub.paragraphs[0]
p_comm.text = (
    "Synthèse de l'évaluation sur l'échantillon de test indépendant (4 705 individus) :\n"
    "• Le seuil de décision optimal (0,68) est calculé par validation croisée à 5 plis sur l'entraînement pour maximiser le F1.\n"
    "• XGBoost surpasse l'ensemble des compétiteurs sur le ROC-AUC (0,8767) et le F1-Score (0,5641)."
)
p_comm.font.name = FONT_FAMILY
p_comm.font.size = Pt(14)
p_comm.font.color.rgb = COLOR_TEXT

# ==============================================================================
# SLIDE 12 : SÉLECTION DU MODÈLE FINAL
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Sélection Finale du Modèle XGBoost", "3. MODÉLISATION")
add_bullet_points(s12, [
    "Modèle retenu : XGBoost Classifier avec hyperparamètres régularisés.",
    "Raison du choix :",
    "  • Pouvoir de discrimination maximal (ROC-AUC = 0,8767), garantissant un classement fiable des probabilités.",
    "  • Excellent compromis entre détection des personnes bancarisées (Rappel = 60,12 %) et limitation des faux positifs (Précision = 53,14 %).",
    "  • Robustesse face au bruit statistique grâce aux pénalités de régularisation L2.",
    "Exportation pour la production : pipeline sérialisé sous models/best_model.joblib."
])

# ==============================================================================
# SLIDE 13 : ARCHITECTURE DE DÉPLOIEMENT
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Architecture Technique de Déploiement", "4. DÉPLOIEMENT & MLOPS")
add_bullet_points(s13, [
    "Séparation stricte des responsabilités (découpage frontend / backend) :",
    "  • Moteur d'inférence (FastAPI) : service web REST ultra-rapide (< 15 ms par requête) validant les données d'entrée via Pydantic.",
    "  • Interface utilisateur (React + Vite + Tailwind CSS) : interface web monopage interactive avec jauge de score SVG animée et tableaux de bord analytiques.",
    "Conteneurisation Docker multi-étape :",
    "  • Étape 1 : compilation TypeScript / Vite sous Node.js 22.",
    "  • Étape 2 : image de production légère Python 3.12-slim intégrant libgomp1 et Uvicorn.",
    "Orchestration standardisée : lancement en une seule commande via docker-compose up."
])

# ==============================================================================
# SLIDE 14 : AUTOMATISATION ET RÉENTRAÎNEMENT
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Pipeline de Réentraînement Automatique (Retraining)", "4. DÉPLOIEMENT & MLOPS")
add_bullet_points(s14, [
    "Objectif : prévenir la dérive des données (Data Drift) et la dérive de concept (Concept Drift) au fil du temps.",
    "Script dédié (src/retrain.py) :",
    "  • Réentraîne les modèles à l'arrivée de nouvelles données d'enquêtes.",
    "  • Contrôle de qualité automatisé : déploiement en production uniquement si ROC-AUC >= 0,75.",
    "  • Journalisation continue dans retraining.log avec horodatage et métriques.",
    "Modes d'exécution :",
    "  • Planifié : tâche Cron hebdomadaire (scripts/retrain_cron.sh).",
    "  • Distant : déclenchement par requête HTTP (POST /api/retrain) pour intégration avec Airflow ou webhooks."
])

# ==============================================================================
# SLIDE 15 : DÉMONSTRATION EN PRODUCTION
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "Démonstration de l'Application en Production", "5. DÉMONSTRATION")
add_bullet_points(s15, [
    "Application déployée publiquement et opérationnelle sur Render :",
    "  URL d'accès direct : https://financial-inclusion-africa-4duh.onrender.com",
    "Fonctionnalités disponibles en ligne :",
    "  • Simulateur de prédiction : saisie interactive des profils individuels et restitution du verdict par jauge dynamique.",
    "  • Visualisation de l'exploration : graphiques interactifs des taux d'inclusion par pays, niveau d'étude et activité.",
    "  • Monitoring des modèles : consultation en direct des métriques de validation et du seuil optimal retenu.",
    "Zéro interruption de service : rechargement dynamique du modèle à chaud après réentraînement."
])

# ==============================================================================
# SLIDE 16 : LIMITES, PERSPECTIVES ET CONCLUSION
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "Limites, Perspectives et Conclusion", "6. CONCLUSION")
add_bullet_points(s16, [
    "Limites identifiées :",
    "  • Corrélation temporelle et géographique (années de collecte spécifiques à chaque pays).",
    "  • Caractère purement qualitatif de la variable de revenu.",
    "Perspectives d'évolution :",
    "  • Intégration des volumes transactionnels de Mobile Money (M-Pesa, MTN).",
    "  • Implémentation de l'explicabilité locale (valeurs SHAP) pour justifier les scores individuels.",
    "Bilan : réalisation complète du cycle de vie de la Science des Données, de l'exploration rigoureuse au déploiement conteneurisé en production."
])

# Sauvegarde
output_path = "Presentation_Soutenance.pptx"
prs.save(output_path)
print(f"Présentation générée avec succès : {output_path} ({len(prs.slides)} slides)")

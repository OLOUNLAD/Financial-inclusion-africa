"""Générateur de présentation de soutenance haut de gamme, sobre et élégante.

Style : Design exécutif / académique institutionnel (style McKinsey / Stanford).
- Palette sobre et raffinée (Ardoise profonde, Bleu saphir sobre, cartes grises douces).
- Structure en cartes et blocs KPI pour aérer le contenu et éliminer les listes à puces monotones.
- Typographie soignée, hiérarchie visuelle stricte, zéro emoji, zéro artifice criard.
- Format : 16:9 panoramique standard (13.333" x 7.5").
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 1. Palette de couleurs raffinée et sobre
COLOR_BG_DARK = RGBColor(15, 23, 42)        # Midnight Slate #0f172a (Page de garde)
COLOR_NAVY = RGBColor(15, 23, 42)           # Titres principaux
COLOR_BLUE_ACCENT = RGBColor(30, 58, 138)   # Bleu institutionnel #1e3a8a
COLOR_BLUE_LINE = RGBColor(37, 99, 235)     # Ligne d'accent #2563eb
COLOR_BLUE_SOFT = RGBColor(239, 246, 255)   # Fond surligné #eff6ff
COLOR_BLUE_BORDER = RGBColor(191, 219, 254) # Bordure surlignée #bfdbfe

COLOR_TEXT_PRIMARY = RGBColor(30, 41, 59)   # Texte foncé #1e293b
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # Texte secondaire #64748b
COLOR_TEXT_LIGHT = RGBColor(226, 232, 240)  # Texte blanc cassé #e2e8f0

COLOR_CARD_BG = RGBColor(248, 250, 252)     # Fond carte #f8fafc
COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Bordure carte #e2e8f0
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Arial"
FONT_BODY = "Arial"


def init_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_slide_header(slide, title_text, category_text, slide_num):
    """Ajoute l'en-tête de slide moderne avec fil d'Ariane et séparateur élégant."""
    # En-tête textuel
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_HEADING
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE_ACCENT
    p_cat.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    # Ligne d'accent subtile sous le titre
    line_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.7), Inches(0.015))
    line_bg.fill.solid()
    line_bg.fill.fore_color.rgb = COLOR_CARD_BORDER
    line_bg.line.fill.background()

    line_accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(1.2), Inches(0.02))
    line_accent.fill.solid()
    line_accent.fill.fore_color.rgb = COLOR_BLUE_LINE
    line_accent.line.fill.background()

    # Footer institutionnel
    foot_tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
    ftf = foot_tb.text_frame
    ftf.word_wrap = True
    ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
    
    p_foot = ftf.paragraphs[0]
    p_foot.text = "Certification en Science des Données • Travaux Pratiques — Msc. Osias Noël TOSSOU"
    p_foot.font.name = FONT_BODY
    p_foot.font.size = Pt(9)
    p_foot.font.color.rgb = COLOR_TEXT_MUTED

    # Numéro de slide
    num_tb = slide.shapes.add_textbox(Inches(11.0), Inches(7.05), Inches(1.5), Inches(0.35))
    ntf = num_tb.text_frame
    ntf.word_wrap = True
    ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
    p_num = ntf.paragraphs[0]
    p_num.text = f"{slide_num:02d} / 16"
    p_num.font.name = FONT_BODY
    p_num.font.size = Pt(9)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_TEXT_MUTED
    p_num.alignment = PP_ALIGN.RIGHT


def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Crée une carte rectangulaire propre avec bordure douce."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card


def add_kpi_card(slide, left, top, width, height, value, label, subtext=None, val_color=COLOR_BLUE_ACCENT, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Crée une carte KPI moderne avec grande métrique chiffrée."""
    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.text = value
    p_val.font.name = FONT_HEADING
    p_val.font.size = Pt(28)
    p_val.font.bold = True
    p_val.font.color.rgb = val_color
    p_val.space_after = Pt(2)

    p_lbl = tf.add_paragraph()
    p_lbl.text = label
    p_lbl.font.name = FONT_HEADING
    p_lbl.font.size = Pt(11)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_NAVY
    
    if subtext:
        p_lbl.space_after = Pt(2)
        p_sub = tf.add_paragraph()
        p_sub.text = subtext
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED


def add_content_card(slide, left, top, width, height, title, items, tag=None, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, highlight=False):
    """Crée une carte de contenu structuré avec titre et puces formulées."""
    if highlight:
        bg_color = COLOR_BLUE_SOFT
        border_color = COLOR_BLUE_BORDER

    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.28), top + Inches(0.25), width - Inches(0.56), height - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Tag éventuel
    if tag:
        p_tag = tf.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_BLUE_ACCENT
        p_tag.space_after = Pt(2)
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(13.5)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY
    p_title.space_after = Pt(10)

    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(7)
        if isinstance(item, tuple):
            prefix, text = item
            run_pref = p.add_run()
            run_pref.text = prefix + " "
            run_pref.font.name = FONT_BODY
            run_pref.font.size = Pt(11)
            run_pref.font.bold = True
            run_pref.font.color.rgb = COLOR_NAVY

            run_txt = p.add_run()
            run_txt.text = text
            run_txt.font.name = FONT_BODY
            run_txt.font.size = Pt(11)
            run_txt.font.color.rgb = COLOR_TEXT_PRIMARY
        else:
            p.text = "• " + item
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_PRIMARY


# ==============================================================================
# CONSTRUCTION DES SLIDES
# ==============================================================================
prs = init_presentation()
blank_layout = prs.slide_layouts[6]

# ------------------------------------------------------------------------------
# SLIDE 1 : PAGE DE GARDE (Élégance institutionnelle sombre)
# ------------------------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)

# Fond sombre complet
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = COLOR_BG_DARK
bg1.line.fill.background()

# Ligne d'accent supérieure
top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = COLOR_BLUE_LINE
top_bar.line.fill.background()

# Bloc central
tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(10.9), Inches(3.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_badge = tf1.paragraphs[0]
p_badge.text = "CERTIFICATION EN SCIENCE DES DONNÉES • TRAVAUX PRATIQUES"
p_badge.font.name = FONT_HEADING
p_badge.font.size = Pt(11)
p_badge.font.bold = True
p_badge.font.color.rgb = RGBColor(148, 163, 184)
p_badge.space_after = Pt(14)

p_t1 = tf1.add_paragraph()
p_t1.text = "De la Donnée Brute au Déploiement"
p_t1.font.name = FONT_HEADING
p_t1.font.size = Pt(34)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_WHITE
p_t1.space_after = Pt(8)

p_sub = tf1.add_paragraph()
p_sub.text = "Modélisation et Déploiement de l'Inclusion Financière en Afrique de l'Est"
p_sub.font.name = FONT_HEADING
p_sub.font.size = Pt(18)
p_sub.font.color.rgb = RGBColor(191, 219, 254)

# 3 Cartes d'information au bas de la couverture
cover_cards = [
    ("Encadrement Académique", "Msc. Osias Noël TOSSOU", "Évaluation des travaux pratiques"),
    ("Dépôt GitHub", "OLOUNLAD/Financial-inclusion-africa", "Code source, pipeline et tests"),
    ("Déploiement Cloud", "financial-inclusion-africa-4duh.onrender.com", "Application web opérationnelle")
]

for i, (title, val, desc) in enumerate(cover_cards):
    cx = Inches(1.2 + i * 3.75)
    cy = Inches(4.8)
    cw = Inches(3.45)
    ch = Inches(1.6)

    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card.line.color.rgb = RGBColor(51, 65, 85)
    card.line.width = Pt(1)

    ctb = s1.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), cw - Inches(0.4), ch - Inches(0.4))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0

    p1 = ctf.paragraphs[0]
    p1.text = title.upper()
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(148, 163, 184)
    p1.space_after = Pt(4)

    p2 = ctf.add_paragraph()
    p2.text = val
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(2)

    p3 = ctf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9)
    p3.font.color.rgb = RGBColor(148, 163, 184)

# ------------------------------------------------------------------------------
# SLIDE 2 : SOMMAIRE (Structure en 6 cartes numérotées)
# ------------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_slide_header(s2, "Plan Structuré de la Soutenance", "STRUCTURE DU PROJET", 2)

agenda_items = [
    ("01", "Contexte & Problématique Métier", [
        ("Enjeu :", "Inclusion financière en Afrique de l'Est"),
        ("Cadrage :", "Classification binaire et parties prenantes")
    ]),
    ("02", "Analyse Exploratoire des Données (EDA)", [
        ("Audit :", "23 524 observations, intégrité et doublons"),
        ("Constats :", "Déséquilibre de classe et facteurs clés")
    ]),
    ("03", "Prétraitement & Feature Engineering", [
        ("Pipeline :", "ColumnTransformer scikit-learn rigoureux"),
        ("Découpage :", "Stratification 80/20 sans data leakage")
    ]),
    ("04", "Modélisation & Benchmark Comparatif", [
        ("Algorithmes :", "Régression Logistique, RF, LightGBM, XGBoost"),
        ("Sélection :", "XGBoost retenu (ROC-AUC 0,8767, seuil 0,68)")
    ]),
    ("05", "Architecture & Déploiement Full-Stack", [
        ("Backend / Frontend :", "FastAPI haute performance & React Vite"),
        ("Conteneurisation :", "Multi-stage Docker sur Render Cloud")
    ]),
    ("06", "MLOps, Démonstration & Bilan", [
        ("Automatisation :", "Quality gate ROC-AUC >= 0,75 & Cron"),
        ("Synthèse :", "Démonstration active, limites et perspectives")
    ]),
]

for idx, (num, title, bullets) in enumerate(agenda_items):
    row = idx // 3
    col = idx % 3
    bx = Inches(0.8 + col * 3.95)
    by = Inches(1.75 + row * 2.5)
    bw = Inches(3.75)
    bh = Inches(2.3)

    add_card(s2, bx, by, bw, bh)

    tb = s2.shapes.add_textbox(bx + Inches(0.25), by + Inches(0.2), bw - Inches(0.5), bh - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_num = tf.paragraphs[0]
    p_num.text = num
    p_num.font.name = FONT_HEADING
    p_num.font.size = Pt(18)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_BLUE_ACCENT
    p_num.space_after = Pt(2)

    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(12.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY
    p_t.space_after = Pt(8)

    for pref, desc in bullets:
        p_b = tf.add_paragraph()
        p_b.space_after = Pt(4)
        r_p = p_b.add_run()
        r_p.text = "• " + pref + " "
        r_p.font.name = FONT_BODY
        r_p.font.size = Pt(10)
        r_p.font.bold = True
        r_p.font.color.rgb = COLOR_NAVY

        r_d = p_b.add_run()
        r_d.text = desc
        r_d.font.name = FONT_BODY
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = COLOR_TEXT_PRIMARY

# ------------------------------------------------------------------------------
# SLIDE 3 : CONTEXTE ET ENJEUX MÉTIER (3 Cartes verticales)
# ------------------------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_slide_header(s3, "Contexte et Enjeux de l'Inclusion Financière", "1. PROBLÉMATIQUE MÉTIER", 3)

s3_cards = [
    ("Levier de Développement", [
        ("Rôle central :", "Vecteur essentiel de réduction de la pauvreté et de résilience face aux chocs économiques."),
        ("Bénéfices directs :", "Permet l'accès à l'épargne sécurisée, au micro-crédit d'investissement et à l'assurance."),
        ("Enjeu macro :", "Intégration formelle de populations historiquement marginalisées dans l'économie structurée.")
    ], "FONDATION"),
    ("Contexte Régional Est-Africain", [
        ("Périmètre géographique :", "Étude concentrée sur 4 nations clés : Kenya, Rwanda, Tanzanie et Ouganda."),
        ("Boom technologique :", "Pénétration fulgurante du Mobile Money (ex. M-Pesa au Kenya)."),
        ("Paradoxe persistant :", "Malgré les portefeuilles mobiles, une très large majorité n'a toujours aucun compte bancaire formel.")
    ], "GÉOGRAPHIE"),
    ("Finalité Opérationnelle", [
        ("Détection prédictive :", "Identifier avec précision les profils individuels susceptibles d'adopter des services bancaires."),
        ("Orientation des offres :", "Aider les banques et institutions de microfinance à concevoir des produits adaptés."),
        ("Politiques publiques :", "Guider les régulateurs pour maximiser l'impact des campagnes nationales d'inclusion.")
    ], "OBJECTIF")
]

for i, (title, items, tag) in enumerate(s3_cards):
    add_content_card(s3, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(5.0), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 4 : CADRAGE DU PROBLÈME DATA SCIENCE (2 Grandes cartes)
# ------------------------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_slide_header(s4, "Cadrage Data Science et Parties Prenantes", "1. PROBLÉMATIQUE MÉTIER", 4)

s4_left = [
    ("Type de problème :", "Classification binaire supervisée."),
    ("Variable cible (Y) :", "bank_account (1 = Yes, 0 = No)."),
    ("Variables d'entrée (X) :", "13 attributs socio-démographiques, économiques et d'équipement technologique."),
    ("Nature des données :", "Données tabulaires d'enquêtes individuelles (FinScope)."),
    ("Critère d'évaluation :", "Optimisation du ROC-AUC et du F1-Score sur la classe minoritaire pour contrer le déséquilibre."),
    ("Contrainte de production :", "Temps de latence d'inférence < 50 ms pour le déploiement API.")
]
add_content_card(s4, Inches(0.8), Inches(1.75), Inches(5.7), Inches(5.0), "Formulation Mathématique & Technique", s4_left, tag="CADRAGE ALGORITHMIQUE")

s4_right = [
    ("Banques Commerciales :", "Scoring prédictif des prospects, optimisation des coûts d'acquisition et ciblage des campagnes."),
    ("Institutions de Microfinance :", "Attribution sécurisée de micro-crédits et ouverture de comptes d'épargne ruraux."),
    ("Régulateurs & Banques Centrales :", "Suivi précis des indicateurs nationaux d'inclusion et pilotage des réglementations."),
    ("Bailleurs & ONG de Développement :", "Évaluation de l'efficacité des programmes d'aide et autonomisation financière des femmes.")
]
add_content_card(s4, Inches(6.8), Inches(1.75), Inches(5.7), Inches(5.0), "Acteurs Concernés & Cas d'Usage Métier", s4_right, tag="ÉCOSYSTÈME & VALEUR")

# ------------------------------------------------------------------------------
# SLIDE 5 : DESCRIPTION DU JEU DE DONNÉES (4 KPI en haut + 2 cartes en bas)
# ------------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_slide_header(s5, "Description du Jeu de Données FinScope", "2. ANALYSE EXPLORATOIRE (EDA)", 5)

kpis_s5 = [
    ("23 524", "Observations", "Échantillon consolidé"),
    ("4 Pays", "Afrique de l'Est", "Kenya, Rwanda, TZ, UG"),
    ("13", "Variables", "2 numériques, 7 qualitatives"),
    ("2016-2018", "Période d'Enquête", "Données Zindi Africa")
]

for i, (v, lbl, sub) in enumerate(kpis_s5):
    add_kpi_card(s5, Inches(0.8 + i * 2.95), Inches(1.75), Inches(2.85), Inches(1.5), v, lbl, sub)

s5_num = [
    ("Âge de l'individu :", "Variable continue s'étendant de 16 à 100 ans (médiane : 35 ans)."),
    ("Taille du ménage :", "Nombre de personnes résidant sous le même toit : 1 à 21 (médiane : 3 personnes)."),
    ("Année d'enquête :", "Année de réalisation de l'enquête FinScope (2016, 2017 ou 2018 selon le pays).")
]
add_content_card(s5, Inches(0.8), Inches(3.45), Inches(5.7), Inches(3.3), "Variables Numériques & Temporelles", s5_num, tag="DISTRIBUTIONS QUANTITATIVES")

s5_cat = [
    ("Socio-démographie :", "Genre, statut matrimonial, relation au chef de ménage."),
    ("Capital humain & Emploi :", "Niveau d'instruction (6 catégories), secteur d'activité / profession."),
    ("Environnement & Équipement :", "Milieu de résidence (Rural / Urban) et possession d'un téléphone mobile personnel.")
]
add_content_card(s5, Inches(6.8), Inches(3.45), Inches(5.7), Inches(3.3), "Variables Catégorielles Déterminantes", s5_cat, tag="PROFILS SOCIO-ÉCONOMIQUES")

# ------------------------------------------------------------------------------
# SLIDE 6 : AUDIT DE QUALITÉ DES DONNÉES (2 Cartes)
# ------------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_slide_header(s6, "Audit de la Qualité et Intégrité des Données", "2. ANALYSE EXPLORATOIRE (EDA)", 6)

s6_left = [
    ("Exhaustivité parfaite :", "Zéro valeur manquante sur l'ensemble des 23 524 lignes et 13 colonnes (100 % de complétude)."),
    ("Cohérence des types :", "Aucune incohérence de format détectée ; les valeurs numériques et catégorielles sont rigoureusement valides."),
    ("Rôle de l'identifiant (uniqueid) :", "L'identifiant n'est pas unique à l'échelle globale, mais uniquement par pays."),
    ("Traitement d'ingénierie :", "La colonne uniqueid a été retirée du pipeline d'apprentissage pour éliminer tout risque d'apprentissage par cœur arbitraire.")
]
add_content_card(s6, Inches(0.8), Inches(1.75), Inches(5.7), Inches(5.0), "Complétude & Cohérence Globale", s6_left, tag="AUDIT D'INTÉGRITÉ")

s6_right = [
    ("Constat initial :", "4 429 lignes partagent des combinaisons de variables socio-démographiques exactement identiques."),
    ("Vérification approfondie :", "Le croisement avec uniqueid prouve qu'il s'agit d'individus différents partageant des caractéristiques similaires (ex. 2 agriculteurs ruraux de 40 ans sans instruction)."),
    ("Décision méthodologique :", "Conservation intégrale des 4 429 observations."),
    ("Justification :", "Supprimer ces lignes aurait faussé la distribution réelle de la population en sous-représentant les profils démographiques les plus fréquents.")
]
add_content_card(s6, Inches(6.8), Inches(1.75), Inches(5.7), Inches(5.0), "Traitement des Profils Identiques", s6_right, tag="DÉCISION MÉTHODOLOGIQUE CLÉ")

# ------------------------------------------------------------------------------
# SLIDE 7 : DÉSÉQUILIBRE DE CLASSES (3 KPI en haut + 1 Grande carte en bas)
# ------------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_slide_header(s7, "Distribution de la Cible et Déséquilibre de Classes", "2. ANALYSE EXPLORATOIRE (EDA)", 7)

kpis_s7 = [
    ("85,92 %", "Non Bancarisés (No)", "20 212 répondants dans l'échantillon"),
    ("14,08 %", "Bancarisés (Yes)", "3 312 répondants dans l'échantillon"),
    ("6,1 : 1", "Ratio de Déséquilibre", "6 non bancarisés pour 1 bancarisé")
]

for i, (v, lbl, sub) in enumerate(kpis_s7):
    add_kpi_card(s7, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(1.6), v, lbl, sub,
                 val_color=COLOR_NAVY if i == 0 else (COLOR_BLUE_LINE if i == 1 else COLOR_BLUE_ACCENT))

s7_bottom = [
    ("Piège de l'Accuracy brute :", "Un prédicteur constant qui répondrait systématiquement 'No' obtiendrait une exactitude artificielle de 85,92 % tout en étant parfaitement inutile sur le plan métier."),
    ("Sélection de métriques robustes :", "Priorité stricte accordée au ROC-AUC (mesure du pouvoir séparateur global des probabilités) et au F1-Score sur la classe minoritaire 'Yes'."),
    ("Stratégie algorithmique :", "Introduction de pénalités de déséquilibre (scale_pos_weight = 6.1) pour forcer les modèles à accorder une importance équivalente aux profils bancarisés."),
    ("Calibration du seuil :", "Optimisation du seuil de décision au-delà de 0,50 pour équilibrer précisément précision et rappel.")
]
add_content_card(s7, Inches(0.8), Inches(3.55), Inches(11.7), Inches(3.2), "Implications Méthodologiques Majeures", s7_bottom, tag="STRATÉGIE DE MODÉLISATION")

# ------------------------------------------------------------------------------
# SLIDE 8 : FACTEURS DISCRIMINANTS (Grille 2x2)
# ------------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_slide_header(s8, "Principaux Enseignements Statistiques", "2. ANALYSE EXPLORATOIRE (EDA)", 8)

s8_items = [
    ("Niveau d'Instruction", [
        ("Cramér's V = 0,392 :", "Déterminant statistique numéro 1 de l'inclusion financière."),
        ("Gradient spectaculaire :", "Le taux de bancarisation passe de 4 % chez les personnes sans éducation formelle à plus de 57 % au niveau universitaire.")
    ], "DÉTERMINANT #1"),
    ("Type d'Activité & Emploi", [
        ("Cramér's V = 0,361 :", "Déterminant majeur lié à la régularité des flux de revenus."),
        ("Contraste formel / informel :", "77 % de bancarisation chez les fonctionnaires et 54 % dans le privé formel, contre < 8 % dans l'agriculture vivrière.")
    ], "DÉTERMINANT #2"),
    ("Téléphone Mobile", [
        ("Cramér's V = 0,208 :", "Condition sine qua non d'accès aux services financiers modernes."),
        ("Écart marqué :", "18 % de bancarisation chez les détenteurs de téléphone contre à peine 2 % chez ceux qui n'en possèdent pas.")
    ], "INFRASTRUCTURE"),
    ("Âge & Territoire", [
        ("Dynamique d'âge :", "Relation non linéaire en cloche : l'accès bancaire culmine sur la tranche 35-44 ans (18,2 %) avant de redescendre."),
        ("Disparités géographiques :", "Le Kenya domine largement (25 % de bancarisation), suivi du Rwanda (11 %), de la Tanzanie (9 %) et de l'Ouganda (9 %).")
    ], "DÉMOGRAPHIE")
]

for idx, (title, bullets, tag) in enumerate(s8_items):
    r = idx // 2
    c = idx % 2
    add_content_card(s8, Inches(0.8 + c * 5.95), Inches(1.75 + r * 2.5), Inches(5.75), Inches(2.3), title, bullets, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 9 : PRÉTRAITEMENT ET FEATURE ENGINEERING (3 Blocs séquentiels)
# ------------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
add_slide_header(s9, "Pipeline de Prétraitement et Feature Engineering", "3. MODÉLISATION", 9)

s9_steps = [
    ("1. Nettoyage & Filtrage", [
        ("Exclusion uniqueid :", "Élimination des identifiants non généralisables."),
        ("Encodage de la cible :", "Transformation binaire propre de bank_account ('Yes' -> 1, 'No' -> 0)."),
        ("Validation des formats :", "Contrôle des types stricts sous Pandas pour éviter toute incohérence.")
    ], "ÉTAPE 1"),
    ("2. ColumnTransformer Scikit-Learn", [
        ("StandardScaler :", "Centrage et réduction des variables numériques (âge, taille du ménage, année)."),
        ("OneHotEncoder :", "Encodage disjonctif complet des variables qualitatives avec handle_unknown='ignore'."),
        ("Sécurité leakage :", "Ajustement exclusif sur les données d'entraînement (fit sur train uniquement).")
    ], "ÉTAPE 2"),
    ("3. Partitionnement Stratifié", [
        ("Répartition 80 / 20 :", "18 819 individus pour l'entraînement, 4 705 pour le test indépendant."),
        ("Stratification stricte :", "Préservation exacte du ratio de 14,08 % de bancarisés dans les deux partitions."),
        ("Validation croisée :", "5-Fold Stratified K-Fold pour la sélection et le réglage des seuils.")
    ], "ÉTAPE 3")
]

for i, (title, items, tag) in enumerate(s9_steps):
    add_content_card(s9, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(5.0), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 10 : STRATÉGIE DE MODÉLISATION (4 Cartes 2x2)
# ------------------------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
add_slide_header(s10, "Stratégie de Modélisation et Algorithmes Évalués", "3. MODÉLISATION", 10)

s10_algos = [
    ("Régression Logistique", [
        ("Famille :", "Modèle linéaire probabiliste."),
        ("Rôle :", "Sert de référence de base (Baseline)."),
        ("Points forts :", "Calcul instantané, interprétabilité directe des coefficients en odds-ratios."),
        ("Limites :", "Incapacité à capturer nativement les interactions non linéaires complexes.")
    ], "BASELINE"),
    ("Forêt Aléatoire (Random Forest)", [
        ("Famille :", "Ensemble par ensachage d'arbres (Bagging)."),
        ("Rôle :", "Capture des relations non linéaires et réduction de variance."),
        ("Points forts :", "Robustesse face au bruit statistique, absence d'hypothèse de linéarité."),
        ("Limites :", "Taille mémoire importante et temps d'inférence modéré.")
    ], "BAGGING"),
    ("LightGBM", [
        ("Famille :", "Gradient Boosting leaf-wise sur histogrammes."),
        ("Rôle :", "Compétiteur moderne haute performance."),
        ("Points forts :", "Vitesse d'entraînement remarquable, faible empreinte mémoire."),
        ("Limites :", "Sensibilité au surapprentissage sur les petits sous-échantillons.")
    ], "BOOSTING RAPIDE"),
    ("XGBoost", [
        ("Famille :", "Gradient Boosting avec régularisation L1 et L2."),
        ("Rôle :", "Algorithme de pointe pour données tabulaires."),
        ("Points forts :", "Excellente gestion du déséquilibre (scale_pos_weight) et généralisation optimale."),
        ("Limites :", "Réglage fin des hyperparamètres nécessaire.")
    ], "BOOSTING RÉGULARISÉ")
]

for idx, (title, items, tag) in enumerate(s10_algos):
    r = idx // 2
    c = idx % 2
    add_content_card(s10, Inches(0.8 + c * 5.95), Inches(1.75 + r * 2.5), Inches(5.75), Inches(2.3), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 11 : BENCHMARK COMPARATIF (Tableau élégant + 3 KPI de synthèse)
# ------------------------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
add_slide_header(s11, "Benchmark Comparatif des Performances (Test Set)", "3. MODÉLISATION", 11)

# Tableau moderne
rows, cols = 5, 7
left, top, width, height = Inches(0.8), Inches(1.75), Inches(11.7), Inches(2.7)
table_shape = s11.shapes.add_table(rows, cols, left, top, width, height)
tbl = table_shape.table

headers = ["Algorithme", "Accuracy", "Précision", "Rappel", "F1-Score", "ROC-AUC", "Seuil Optimal"]
tbl_data = [
    ["Régression Logistique", "85,70 %", "49,35 %", "62,69 %", "0,5522", "0,8646", "0,65"],
    ["Random Forest", "85,55 %", "48,95 %", "63,60 %", "0,5532", "0,8702", "0,62"],
    ["LightGBM", "87,08 %", "53,71 %", "59,06 %", "0,5626", "0,8766", "0,69"],
    ["XGBoost (Modèle Retenu)", "86,93 %", "53,14 %", "60,12 %", "0,5641", "0,8767", "0,68"]
]

for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_NAVY
    cell.text = h
    for p in cell.text_frame.paragraphs:
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

for row_idx, row in enumerate(tbl_data):
    is_winner = (row_idx == 3)
    for col_idx, val in enumerate(row):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BLUE_SOFT if is_winner else (COLOR_CARD_BG if row_idx % 2 == 0 else COLOR_WHITE)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            p.font.bold = is_winner
            p.font.color.rgb = COLOR_BLUE_ACCENT if is_winner else COLOR_TEXT_PRIMARY
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

# 3 Cartes de synthèse sous le tableau
kpi_b11 = [
    ("0,8767", "Meilleur ROC-AUC", "XGBoost domine le pouvoir discriminant global"),
    ("0,5641", "Meilleur F1-Score", "Équilibre maximal entre précision et rappel"),
    ("0,68", "Seuil Optimal", "Optimisé par cross-validation à 5 plis sur train")
]

for i, (v, lbl, sub) in enumerate(kpi_b11):
    add_kpi_card(s11, Inches(0.8 + i * 3.95), Inches(4.75), Inches(3.75), Inches(1.9), v, lbl, sub,
                 val_color=COLOR_BLUE_LINE if i == 0 else COLOR_BLUE_ACCENT)

# ------------------------------------------------------------------------------
# SLIDE 12 : SÉLECTION DU MODÈLE FINAL (Colonne gauche KPI + Colonne droite)
# ------------------------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
add_slide_header(s12, "Sélection Finale du Modèle XGBoost", "3. MODÉLISATION", 12)

# Colonne gauche : 3 métriques clés
add_kpi_card(s12, Inches(0.8), Inches(1.75), Inches(4.0), Inches(1.55), "0,8767", "Score ROC-AUC", "Séparation probabiliste optimale")
add_kpi_card(s12, Inches(0.8), Inches(3.45), Inches(4.0), Inches(1.55), "0,5641", "Score F1 Minoritaire", "Seuil de décision calibré à 0,68")
add_kpi_card(s12, Inches(0.8), Inches(5.15), Inches(4.0), Inches(1.55), "60,12 %", "Taux de Rappel", "Détection de 6 bancarisés réels sur 10")

s12_right = [
    ("Excellence du compromis métrique :", "XGBoost délivre le meilleur score F1 (0,5641) tout en conservant une précision de 53,14 % et un rappel de 60,12 % sur l'échantillon test indépendant."),
    ("Robustesse prouvée par régularisation :", "L'application des pénalités L2 et le sous-échantillonnage préviennent tout surapprentissage sur les profils d'enquêtes marginaux."),
    ("Rôle clé du seuil optimisé (0,68) :", "Le seuil standard à 0,50 générait un excès de faux positifs. Le seuil à 0,68 calibré par validation croisée garantit que seules les opportunités qualifiées sont ciblées."),
    ("Sérialisation pour la production :", "Pipeline complet sérialisé dans models/best_model.joblib et métriques archivées dans models/metrics.json.")
]
add_content_card(s12, Inches(5.1), Inches(1.75), Inches(7.4), Inches(4.95), "Justification Décisionnelle & Exportation", s12_right, tag="CHOIX FINAL & ARTEFACTS")

# ------------------------------------------------------------------------------
# SLIDE 13 : ARCHITECTURE DE DÉPLOIEMENT (3 Blocs techniques verticaux)
# ------------------------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
add_slide_header(s13, "Architecture Technique de Déploiement Full-Stack", "4. DÉPLOIEMENT & MLOPS", 13)

s13_cards = [
    ("Moteur REST FastAPI", [
        ("Framework moderne :", "API Python asynchrone haute performance."),
        ("Validation Pydantic :", "Typage strict et contrôle d'intégrité des entrées."),
        ("Rapidité d'inférence :", "Temps de réponse moyen < 15 ms par requête."),
        ("Points de terminaison :", "/api/predict, /api/metrics, /api/stats, /api/retrain.")
    ], "BACKEND INFERENCE"),
    ("Interface Web React + Vite", [
        ("Technologies :", "React 18, Vite, TypeScript et Tailwind CSS."),
        ("Jauge dynamique SVG :", "Animation semi-circulaire intuitive du score de bancarisation."),
        ("Dashboards analytiques :", "Graphiques interactifs Recharts reproduisant l'EDA."),
        ("Expérience fluide :", "Simulation instantanée et responsive multi-écrans.")
    ], "FRONTEND INTERACTIF"),
    ("Conteneurisation Cloud", [
        ("Multi-Stage Docker :", "Étape 1 : compilation TypeScript (Node 22) -> Étape 2 : image de production Python 3.12-slim."),
        ("Optimisation image :", "Empreinte minimale intégrant Uvicorn et libgomp1."),
        ("Orchestration locale :", "docker-compose up pour exécution reproductible."),
        ("Hébergement Render :", "Déploiement cloud avec HTTPS actif et redémarrage automatique.")
    ], "DEVOPS & CLOUD")
]

for i, (title, items, tag) in enumerate(s13_cards):
    add_content_card(s13, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(5.0), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 14 : MLOPS ET RÉENTRAÎNEMENT (3 Cartes processus)
# ------------------------------------------------------------------------------
s14 = prs.slides.add_slide(blank_layout)
add_slide_header(s14, "Pipeline de Réentraînement Automatique (MLOps)", "4. DÉPLOIEMENT & MLOPS", 14)

s14_cards = [
    ("Pipeline Dédié (src/retrain.py)", [
        ("Objectif central :", "Prévenir la dérive des données (Data Drift) et la dérive de concept (Concept Drift) face aux nouvelles enquêtes."),
        ("Traitement bout-en-bout :", "Rechargement des données, ré-étalonnage du ColumnTransformer et réentraînement du modèle."),
        ("Traçabilité continue :", "Journalisation systématique dans retraining.log avec date, version et scores obtenus.")
    ], "AUTOMATISATION"),
    ("Quality Gate de Sécurité", [
        ("Garde-fou automatisé :", "Déploiement conditionné à un score de performance strict : ROC-AUC >= 0,75."),
        ("Protection de la production :", "Si le nouveau modèle sous-performe, l'ancien modèle est immédiatement maintenu sans interruption."),
        ("Auditabilité totale :", "Conservation des métriques comparées avant/après chaque cycle.")
    ], "CONTRÔLE QUALITÉ"),
    ("Modes d'Exécution Flexibles", [
        ("Tâche planifiée locale :", "Script Cron (scripts/retrain_cron.sh) pour exécution périodique autonome."),
        ("Webhook API sécurisé :", "Endpoint POST /api/retrain pour intégration avec orchestrateurs externes (ex. Airflow)."),
        ("Rechargement à chaud :", "Mise à jour en mémoire vive sans nécessiter de redémarrage du serveur Uvicorn.")
    ], "OPÉRABILITÉ")
]

for i, (title, items, tag) in enumerate(s14_cards):
    add_content_card(s14, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(5.0), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 15 : DÉMONSTRATION EN PRODUCTION (Carte URL + 3 Cartes fonctionnalités)
# ------------------------------------------------------------------------------
s15 = prs.slides.add_slide(blank_layout)
add_slide_header(s15, "Démonstration de l'Application en Production", "5. DÉMONSTRATION", 15)

# Bannière supérieure URL en ligne
banner = add_card(s15, Inches(0.8), Inches(1.75), Inches(11.7), Inches(1.1), bg_color=COLOR_BLUE_SOFT, border_color=COLOR_BLUE_BORDER)
btb = s15.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(0.9))
btf = btb.text_frame
btf.word_wrap = True
bp1 = btf.paragraphs[0]
bp1.text = "APPLICATION EN LIGNE • STATUT OPÉRATIONNEL SUR RENDER CLOUD"
bp1.font.name = FONT_HEADING
bp1.font.size = Pt(9.5)
bp1.font.bold = True
bp1.font.color.rgb = COLOR_BLUE_ACCENT
bp1.space_after = Pt(2)

bp2 = btf.add_paragraph()
bp2.text = "https://financial-inclusion-africa-4duh.onrender.com"
bp2.font.name = FONT_HEADING
bp2.font.size = Pt(17)
bp2.font.bold = True
bp2.font.color.rgb = COLOR_NAVY

s15_features = [
    ("Simulateur Prédictif", [
        ("Saisie ergonomique :", "Formulaire complet reprenant l'ensemble des 13 variables individuelles."),
        ("Verdict en temps réel :", "Animation semi-circulaire de la jauge et décision binaire instantanée."),
        ("Interprétation :", "Présentation claire de la probabilité de bancarisation estimée.")
    ], "SIMULATION"),
    ("Tableau de Bord EDA", [
        ("Analyses graphiques :", "Visualisations interactives des taux d'inclusion par nation."),
        ("Croisements sociologiques :", "Distribution selon le niveau d'instruction et la catégorie professionnelle."),
        ("Accès immédiat :", "Consultation directe des insights sans prérequis technique.")
    ], "VISUALISATION"),
    ("Monitoring & Retraining", [
        ("Métriques officielles :", "Affichage en direct du ROC-AUC, du F1-Score et du seuil retenu (0,68)."),
        ("Déclenchement réentraînement :", "Bouton d'actualisation connecté à l'API de réentraînement."),
        ("Transparence :", "Matrice de confusion et statut de déploiement en direct.")
    ], "SUPERVISION")
]

for i, (title, items, tag) in enumerate(s15_features):
    add_content_card(s15, Inches(0.8 + i * 3.95), Inches(3.1), Inches(3.75), Inches(3.65), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 16 : LIMITES, PERSPECTIVES ET CONCLUSION
# ------------------------------------------------------------------------------
s16 = prs.slides.add_slide(blank_layout)
add_slide_header(s16, "Limites, Perspectives et Conclusion", "6. CONCLUSION", 16)

s16_left = [
    ("Données purement déclaratives :", "Les enquêtes FinScope reposent sur les déclarations des ménages (biais de mémorisation ou d'approbation sociale)."),
    ("Revenu qualitatif :", "La variable de source de revenu ne quantifie pas le montant monétaire précis des flux financiers."),
    ("Décalage temporel entre pays :", "Les enquêtes nationales ont été collectées entre 2016 et 2018 selon les nations.")
]
add_content_card(s16, Inches(0.8), Inches(1.75), Inches(5.7), Inches(3.3), "Limites Méthodologiques Identifiées", s16_left, tag="LUCIDITÉ SCIENTIFIQUE")

s16_right = [
    ("Flux transactionnels Mobile Money :", "Coupler les enquêtes avec les métriques réelles d'usage (ex. volumes M-Pesa, fréquence des transferts)."),
    ("Explicabilité locale (SHAP) :", "Intégrer les valeurs de Shapley pour justifier chaque score prédictif individuel auprès du client."),
    ("Données géospatiales :", "Intégrer la distance physique aux agences bancaires et aux points de retrait d'argent.")
]
add_content_card(s16, Inches(6.8), Inches(1.75), Inches(5.7), Inches(3.3), "Perspectives d'Amélioration Future", s16_right, tag="ÉVOLUTIONS")

# Bannière de conclusion générale
banner_c = add_card(s16, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.5), bg_color=COLOR_BLUE_SOFT, border_color=COLOR_BLUE_BORDER)
ctb = s16.shapes.add_textbox(Inches(1.05), Inches(5.35), Inches(11.2), Inches(1.3))
ctf = ctb.text_frame
ctf.word_wrap = True

cp1 = ctf.paragraphs[0]
cp1.text = "SYNTHÈSE DU PROJET INTÉGRATEUR"
cp1.font.name = FONT_HEADING
cp1.font.size = Pt(9.5)
cp1.font.bold = True
cp1.font.color.rgb = COLOR_BLUE_ACCENT
cp1.space_after = Pt(2)

cp2 = ctf.add_paragraph()
cp2.text = (
    "Couverture complète du cycle de vie de la Science des Données : de l'audit exploratoire rigoureux "
    "à l'entraînement comparatif et la sélection d'un modèle XGBoost régularisé (ROC-AUC 0,8767, F1 0,5641), "
    "aboutissant à une application conteneurisée déployée en production avec surveillance et réentraînement automatisé."
)
cp2.font.name = FONT_BODY
cp2.font.size = Pt(11)
cp2.font.color.rgb = COLOR_NAVY

# Sauvegarde
output_pptx = "Presentation_Soutenance.pptx"
prs.save(output_pptx)
print(f"Présentation générée avec succès : {output_pptx} ({len(prs.slides)} slides)")

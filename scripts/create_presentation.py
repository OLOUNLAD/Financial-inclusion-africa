"""Générateur de présentation officielle haut de gamme, aérée et visuelle.

Caractéristiques :
- Textes allégés et concis : phrases percutantes, zéro pavé indigeste.
- Vrais SCHÉMAS intégrés :
  * Slide 7  : Schéma de jauge de proportion / ratio de déséquilibre
  * Slide 8  : Schéma comparatif en barres horizontales (Cramér's V)
  * Slide 9  : Schéma de workflow du pipeline de prétraitement (Flowchart 4 étapes)
  * Slide 13 : Schéma d'architecture technique globale (Client -> React -> FastAPI -> Modèle -> Docker/Render)
  * Slide 14 : Schéma de boucle décisionnelle MLOps (Nouvelles données -> Quality Gate -> Prod / Rejet)
- Style : Épuré, élégant, strictement académique et professionnel.
- Format : 16:9 widescreen (13.333" x 7.5").
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# PALETTE DE COULEURS ÉLÉGANTE ET SOBRE
# ==============================================================================
COLOR_BG_DARK = RGBColor(15, 23, 42)        # #0f172a Ardoise nuit
COLOR_NAVY = RGBColor(15, 23, 42)           # #0f172a Titres
COLOR_BLUE_ACCENT = RGBColor(30, 58, 138)   # #1e3a8a Bleu institutionnel
COLOR_BLUE_LINE = RGBColor(37, 99, 235)     # #2563eb Bleu saphir
COLOR_BLUE_SOFT = RGBColor(239, 246, 255)   # #eff6ff Bleu très clair
COLOR_BLUE_BORDER = RGBColor(191, 219, 254) # #bfdbfe Bordure bleue

COLOR_TEXT_PRIMARY = RGBColor(30, 41, 59)   # #1e293b Texte principal
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748b Texte secondaire
COLOR_WHITE = RGBColor(255, 255, 255)

COLOR_CARD_BG = RGBColor(248, 250, 252)     # #f8fafc Fond carte
COLOR_CARD_BORDER = RGBColor(226, 232, 240) # #e2e8f0 Bordure carte

COLOR_SUCCESS_BG = RGBColor(240, 253, 244)  # #f0fdf4 Vert feutré (Quality gate OK)
COLOR_SUCCESS_BORDER = RGBColor(187, 247, 208)
COLOR_SUCCESS_TEXT = RGBColor(22, 101, 52)

COLOR_DANGER_BG = RGBColor(254, 242, 242)   # #fef2f2 Rouge feutré (Rejet)
COLOR_DANGER_BORDER = RGBColor(254, 202, 202)
COLOR_DANGER_TEXT = RGBColor(153, 27, 27)

FONT_HEADING = "Arial"
FONT_BODY = "Arial"


def init_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_slide_header(slide, title_text, category_text, slide_num):
    """En-tête standard épuré avec fil d'Ariane et séparateur bicolore."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
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

    # Ligne d'accent bicolore
    line_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.015))
    line_bg.fill.solid()
    line_bg.fill.fore_color.rgb = COLOR_CARD_BORDER
    line_bg.line.fill.background()

    line_accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(1.2), Inches(0.02))
    line_accent.fill.solid()
    line_accent.fill.fore_color.rgb = COLOR_BLUE_LINE
    line_accent.line.fill.background()

    # Footer
    foot_tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(10.0), Inches(0.3))
    ftf = foot_tb.text_frame
    ftf.word_wrap = True
    ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
    p_foot = ftf.paragraphs[0]
    p_foot.text = "Certification en Science des Données • Travaux Pratiques — Msc. Osias Noël TOSSOU"
    p_foot.font.name = FONT_BODY
    p_foot.font.size = Pt(9)
    p_foot.font.color.rgb = COLOR_TEXT_MUTED

    num_tb = slide.shapes.add_textbox(Inches(11.0), Inches(7.08), Inches(1.5), Inches(0.3))
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
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card


def add_kpi_card(slide, left, top, width, height, value, label, subtext=None, val_color=COLOR_BLUE_ACCENT, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.text = value
    p_val.font.name = FONT_HEADING
    p_val.font.size = Pt(27)
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


def add_concise_card(slide, left, top, width, height, title, items, tag=None, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

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
    p_title.font.size = Pt(13)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY
    p_title.space_after = Pt(8)

    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        if isinstance(item, tuple):
            prefix, text = item
            rp = p.add_run()
            rp.text = "• " + prefix + " "
            rp.font.name = FONT_BODY
            rp.font.size = Pt(10.5)
            rp.font.bold = True
            rp.font.color.rgb = COLOR_NAVY

            rt = p.add_run()
            rt.text = text
            rt.font.name = FONT_BODY
            rt.font.size = Pt(10.5)
            rt.font.color.rgb = COLOR_TEXT_PRIMARY
        else:
            p.text = "• " + item
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_PRIMARY


# ==============================================================================
# GÉNÉRATION DES 16 SLIDES
# ==============================================================================
prs = init_prs()
blank_layout = prs.slide_layouts[6]

# ------------------------------------------------------------------------------
# SLIDE 1 : PAGE DE GARDE INSTITUTIONNELLE
# ------------------------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)

bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = COLOR_BG_DARK
bg1.line.fill.background()

top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = COLOR_BLUE_LINE
top_bar.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.9), Inches(3.0))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_b = tf1.paragraphs[0]
p_b.text = "CERTIFICATION EN SCIENCE DES DONNÉES • TRAVAUX PRATIQUES"
p_b.font.name = FONT_HEADING
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = RGBColor(148, 163, 184)
p_b.space_after = Pt(14)

p_t = tf1.add_paragraph()
p_t.text = "De la Donnée Brute au Déploiement"
p_t.font.name = FONT_HEADING
p_t.font.size = Pt(34)
p_t.font.bold = True
p_t.font.color.rgb = COLOR_WHITE
p_t.space_after = Pt(8)

p_sub = tf1.add_paragraph()
p_sub.text = "Modélisation et Déploiement de l'Inclusion Financière en Afrique de l'Est"
p_sub.font.name = FONT_HEADING
p_sub.font.size = Pt(18)
p_sub.font.color.rgb = RGBColor(191, 219, 254)

cover_cards = [
    ("Encadrement Académique", "Msc. Osias Noël TOSSOU", "Évaluation des travaux pratiques"),
    ("Dépôt GitHub", "OLOUNLAD/Financial-inclusion-africa", "Code source, pipeline et tests"),
    ("Application Active", "financial-inclusion-africa-4duh.onrender.com", "Déploiement en ligne opérationnel")
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
# SLIDE 2 : SOMMAIRE EN 6 BLOCS NUMÉROTÉS
# ------------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_slide_header(s2, "Plan de la Présentation", "STRUCTURE DU PROJET", 2)

agenda_items = [
    ("01", "Contexte & Problématique Métier", [("Enjeu :", "Inclusion financière en Afrique de l'Est"), ("Cadrage :", "Classification binaire supervisée")]),
    ("02", "Analyse Exploratoire des Données", [("Audit :", "23 524 enquêtes, intégrité 100 %"), ("Constats :", "Déséquilibre cible & facteurs clés")]),
    ("03", "Pipeline de Prétraitement", [("Ingénierie :", "ColumnTransformer & Encodages"), ("Protocole :", "Stratification 80/20 étanche")]),
    ("04", "Modélisation & Benchmark", [("Comparatif :", "Évaluation des 4 algorithmes"), ("Sélection :", "XGBoost retenu (ROC-AUC 0,8767)")]),
    ("05", "Architecture & Déploiement", [("Stack :", "FastAPI, React/Vite, Docker"), ("Production :", "Hébergement actif sur Render Cloud")]),
    ("06", "MLOps, Démo & Perspectives", [("Cycle continu :", "Quality Gate & Tâche Cron"), ("Démonstration :", "Application active & Bilan")]),
]

for idx, (num, title, bullets) in enumerate(agenda_items):
    row = idx // 3
    col = idx % 3
    bx = Inches(0.8 + col * 3.95)
    by = Inches(1.75 + row * 2.5)
    bw = Inches(3.75)
    bh = Inches(2.25)

    add_card(s2, bx, by, bw, bh)
    tb = s2.shapes.add_textbox(bx + Inches(0.25), by + Inches(0.2), bw - Inches(0.5), bh - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_num = tf.paragraphs[0]
    p_num.text = num
    p_num.font.name = FONT_HEADING
    p_num.font.size = Pt(17)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_BLUE_ACCENT
    p_num.space_after = Pt(2)

    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY
    p_t.space_after = Pt(6)

    for pref, desc in bullets:
        p_b = tf.add_paragraph()
        p_b.space_after = Pt(3)
        rp = p_b.add_run()
        rp.text = "• " + pref + " "
        rp.font.name = FONT_BODY
        rp.font.size = Pt(10)
        rp.font.bold = True
        rp.font.color.rgb = COLOR_NAVY
        rt = p_b.add_run()
        rt.text = desc
        rt.font.name = FONT_BODY
        rt.font.size = Pt(10)
        rt.font.color.rgb = COLOR_TEXT_PRIMARY

# ------------------------------------------------------------------------------
# SLIDE 3 : CONTEXTE ET ENJEUX MÉTIER (Aéré, 3 cartes concises)
# ------------------------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_slide_header(s3, "Contexte et Enjeux de l'Inclusion Financière", "1. PROBLÉMATIQUE MÉTIER", 3)

s3_cards = [
    ("Enjeu Économique Majeur", [
        ("Levier clé :", "Vecteur direct de réduction de la pauvreté et de résilience des ménages."),
        ("Bénéfices :", "Accès à l'épargne sécurisée, aux micro-crédits et aux assurances."),
        ("Impact :", "Intégration formelle des populations vulnérables dans l'économie.")
    ], "FONDATION"),
    ("Le Paradoxe Est-Africain", [
        ("Périmètre :", "4 nations cibles : Kenya, Rwanda, Tanzanie et Ouganda."),
        ("Boom mobile :", "Adoption massive du Mobile Money (ex. M-Pesa)."),
        ("Défi persistant :", "Faible bancarisation formelle malgré l'essor des téléphones.")
    ], "RÉGION"),
    ("Finalité Opérationnelle", [
        ("Prédiction :", "Identifier les individus à fort potentiel de bancarisation."),
        ("Ciblage :", "Optimiser l'offre des institutions financières et microfinances."),
        ("Politiques publiques :", "Guider les régulateurs pour maximiser l'impact national.")
    ], "OBJECTIF")
]

for i, (title, items, tag) in enumerate(s3_cards):
    add_concise_card(s3, Inches(0.8 + i * 3.95), Inches(1.75), Inches(3.75), Inches(5.0), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 4 : CADRAGE DATA SCIENCE ET ACTEURS (2 grandes cartes aérées)
# ------------------------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_slide_header(s4, "Cadrage Data Science et Parties Prenantes", "1. PROBLÉMATIQUE MÉTIER", 4)

s4_tech = [
    ("Type de problème :", "Classification binaire supervisée."),
    ("Cible Y :", "bank_account (1 = Oui, 0 = Non)."),
    ("Entrées X :", "13 variables socio-démographiques et d'équipement."),
    ("Objectif d'évaluation :", "Optimisation conjointe du ROC-AUC et du F1-score."),
    ("Contrainte de latence :", "Inférence temps réel en production (< 50 ms).")
]
add_concise_card(s4, Inches(0.8), Inches(1.75), Inches(5.7), Inches(5.0), "Cadrage Technique Data Science", s4_tech, tag="CADRAGE ALGORITHMIQUE")

s4_business = [
    ("Banques Commerciales :", "Scoring des prospects et réduction des coûts d'acquisition client."),
    ("Institutions de Microfinance :", "Octroi ciblé de micro-crédits et ouvertures de comptes d'épargne."),
    ("Régulateurs & Banques Centrales :", "Mesure objective et pilotage des politiques publiques d'inclusion."),
    ("Bailleurs & ONG :", "Orientation des programmes d'aide et émancipation économique.")
]
add_concise_card(s4, Inches(6.8), Inches(1.75), Inches(5.7), Inches(5.0), "Parties Prenantes & Cas d'Usage", s4_business, tag="ÉCOSYSTÈME MÉTIER")

# ------------------------------------------------------------------------------
# SLIDE 5 : DESCRIPTION DU JEU DE DONNÉES (4 KPI + 2 Blocs)
# ------------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_slide_header(s5, "Description du Jeu de Données FinScope", "2. ANALYSE EXPLORATOIRE (EDA)", 5)

kpis_s5 = [
    ("23 524", "Observations", "Échantillon officiel consolidé"),
    ("4 Pays", "Afrique de l'Est", "Kenya, Rwanda, Tanzanie, Ouganda"),
    ("13", "Variables", "2 numériques, 7 qualitatives"),
    ("2016-2018", "Période d'Enquête", "Enquêtes FinScope (Zindi)")
]
for i, (v, lbl, sub) in enumerate(kpis_s5):
    add_kpi_card(s5, Inches(0.8 + i * 2.95), Inches(1.75), Inches(2.85), Inches(1.5), v, lbl, sub)

s5_num = [
    ("Âge :", "Variable continue de 16 à 100 ans (médiane : 35 ans)."),
    ("Taille du ménage :", "De 1 à 21 résidents (médiane : 3 membres)."),
    ("Année :", "Année de réalisation de l'enquête (2016 à 2018 selon le pays).")
]
add_concise_card(s5, Inches(0.8), Inches(3.45), Inches(5.7), Inches(3.3), "Variables Numériques", s5_num, tag="DONNÉES QUANTITATIVES")

s5_cat = [
    ("Démographie :", "Genre, statut matrimonial, relation au chef de ménage."),
    ("Capital humain :", "Niveau d'instruction (6 paliers), catégorie professionnelle."),
    ("Milieu & Équipement :", "Zone rurale/urbaine, possession d'un téléphone mobile.")
]
add_concise_card(s5, Inches(6.8), Inches(3.45), Inches(5.7), Inches(3.3), "Variables Catégorielles", s5_cat, tag="PROFILS QUALITATIFS")

# ------------------------------------------------------------------------------
# SLIDE 6 : AUDIT QUALITÉ ET DÉCISION DOUBLONS (2 Grandes cartes)
# ------------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_slide_header(s6, "Audit de Qualité et Décisions d'Ingénierie", "2. ANALYSE EXPLORATOIRE (EDA)", 6)

s6_left = [
    ("Complétude 100 % :", "Zéro valeur manquante sur les 23 524 lignes et 13 colonnes."),
    ("Cohérence des types :", "Aucune incohérence de format ni valeur aberrante."),
    ("Rôle de uniqueid :", "Identifiant local non unique globalement (spécifique au pays)."),
    ("Action d'ingénierie :", "Exclusion de uniqueid pour éviter tout surapprentissage arbitraire.")
]
add_concise_card(s6, Inches(0.8), Inches(1.75), Inches(5.7), Inches(5.0), "Complétude & Intégrité des Données", s6_left, tag="AUDIT D'INTÉGRITÉ")

s6_right = [
    ("Constat :", "4 429 observations partagent un profil socio-démographique identique."),
    ("Analyse rigoureuse :", "Le croisement avec uniqueid prouve qu'il s'agit d'individus réels distincts interrogés lors de l'enquête."),
    ("Décision retenue :", "Conservation intégrale des 4 429 lignes."),
    ("Raison scientifique :", "Préserver fidèlement la distribution et la densité démographique réelle de la population étudiée.")
]
add_concise_card(s6, Inches(6.8), Inches(1.75), Inches(5.7), Inches(5.0), "Gestion des Profils Identiques (4 429 lignes)", s6_right, tag="DÉCISION MÉTHODOLOGIQUE")

# ------------------------------------------------------------------------------
# SLIDE 7 : DÉSÉQUILIBRE DE CLASSES (AVEC SCHÉMA DE PROPORTION VISUEL)
# ------------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_slide_header(s7, "Distribution de la Cible et Déséquilibre de Classes", "2. ANALYSE EXPLORATOIRE (EDA)", 7)

# 3 Cartes KPI
add_kpi_card(s7, Inches(0.8), Inches(1.75), Inches(3.75), Inches(1.4), "85,92 %", "Non Bancarisés (No)", "20 212 individus (Classe majoritaire)", val_color=COLOR_NAVY)
add_kpi_card(s7, Inches(4.75), Inches(1.75), Inches(3.75), Inches(1.4), "14,08 %", "Bancarisés (Yes)", "3 312 individus (Classe cible)", val_color=COLOR_BLUE_LINE)
add_kpi_card(s7, Inches(8.7), Inches(1.75), Inches(3.8), Inches(1.4), "6,1 pour 1", "Ratio de Déséquilibre", "Forte asymétrie statistique", val_color=COLOR_BLUE_ACCENT)

# SCHÉMA VISUEL : BARRE PROPORTIONNELLE
schema_box = add_card(s7, Inches(0.8), Inches(3.3), Inches(11.7), Inches(1.3), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)

# Titre du schéma
stb = s7.shapes.add_textbox(Inches(1.0), Inches(3.4), Inches(11.3), Inches(0.3))
stf = stb.text_frame
stf.margin_top = stf.margin_left = stf.margin_bottom = stf.margin_right = 0
sp = stf.paragraphs[0]
sp.text = "RÉPARTITION VISUELLE DE L'ÉCHANTILLON (23 524 RÉPONDANTS)"
sp.font.name = FONT_HEADING
sp.font.size = Pt(9.5)
sp.font.bold = True
sp.font.color.rgb = COLOR_TEXT_MUTED

# Barre 85.92% (Non bancarisés)
bar_width_total = 11.3
bar_w_no = bar_width_total * 0.8592
bar_w_yes = bar_width_total * 0.1408

b_no = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.8), Inches(bar_w_no), Inches(0.55))
b_no.fill.solid()
b_no.fill.fore_color.rgb = COLOR_NAVY
b_no.line.fill.background()
tf_no = b_no.text_frame
tf_no.word_wrap = True
p_bno = tf_no.paragraphs[0]
p_bno.text = "NON BANCARISÉS : 85,9 % (20 212)"
p_bno.font.name = FONT_HEADING
p_bno.font.size = Pt(11)
p_bno.font.bold = True
p_bno.font.color.rgb = COLOR_WHITE
p_bno.alignment = PP_ALIGN.CENTER

# Barre 14.08% (Bancarisés)
b_yes = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0 + bar_w_no), Inches(3.8), Inches(bar_w_yes), Inches(0.55))
b_yes.fill.solid()
b_yes.fill.fore_color.rgb = COLOR_BLUE_LINE
b_yes.line.fill.background()
tf_yes = b_yes.text_frame
tf_yes.word_wrap = True
p_byes = tf_yes.paragraphs[0]
p_byes.text = "14,1 %"
p_byes.font.name = FONT_HEADING
p_byes.font.size = Pt(11)
p_byes.font.bold = True
p_byes.font.color.rgb = COLOR_WHITE
p_byes.alignment = PP_ALIGN.CENTER

s7_bottom = [
    ("Piège de l'Accuracy :", "Un prédicteur constant 'No' obtiendrait 85,9 % sans rien apprendre."),
    ("Métriques obligatoires :", "Priorité stricte au ROC-AUC et au F1-Score sur la classe minoritaire 'Yes'."),
    ("Ajustements d'apprentissage :", "Pondération scale_pos_weight = 6.1 et recalibration du seuil de décision.")
]
add_concise_card(s7, Inches(0.8), Inches(4.75), Inches(11.7), Inches(2.1), "Conséquences Méthodologiques Directes", s7_bottom, tag="STRATÉGIE ALGORITHMIQUE")

# ------------------------------------------------------------------------------
# SLIDE 8 : FACTEURS DISCRIMINANTS (AVEC SCHÉMA GRAPHIQUE HORIZONTAL CRAMÉR'S V)
# ------------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_slide_header(s8, "Facteurs Clés d'Inclusion (Mesures d'Association)", "2. ANALYSE EXPLORATOIRE (EDA)", 8)

# Schéma comparatif de Cramér's V
schema_v = add_card(s8, Inches(0.8), Inches(1.75), Inches(6.8), Inches(5.0), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)

vtb = s8.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(6.3), Inches(0.4))
vtf = vtb.text_frame
vtf.margin_top = vtf.margin_left = vtf.margin_bottom = vtf.margin_right = 0
vp = vtf.paragraphs[0]
vp.text = "HIÉRARCHIE DES DÉTERMINANTS (V DE CRAMÉR)"
vp.font.name = FONT_HEADING
vp.font.size = Pt(10)
vp.font.bold = True
vp.font.color.rgb = COLOR_BLUE_ACCENT

# Barres horizontales pour Cramér's V
factors = [
    ("Niveau d'instruction", 0.392, "4 % sans instruction -> 57 % supérieur"),
    ("Type d'emploi / activité", 0.361, "77 % fonctionnaires vs <8 % agriculture"),
    ("Téléphone portable", 0.208, "18 % avec téléphone vs 2 % sans"),
    ("Milieu de résidence", 0.119, "Urbain 25 % vs Rural 10 %")
]

max_bar_w = 4.2  # inches
for i, (fname, fval, fcomment) in enumerate(factors):
    by = Inches(2.45 + i * 1.0)
    
    # Label
    ltb = s8.shapes.add_textbox(Inches(1.05), by, Inches(2.2), Inches(0.4))
    ltf = ltb.text_frame
    ltf.margin_top = ltf.margin_left = ltf.margin_bottom = ltf.margin_right = 0
    lp = ltf.paragraphs[0]
    lp.text = fname
    lp.font.name = FONT_HEADING
    lp.font.size = Pt(10.5)
    lp.font.bold = True
    lp.font.color.rgb = COLOR_NAVY
    
    # Barre
    w = max_bar_w * (fval / 0.40)
    bar = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), by + Inches(0.02), Inches(w), Inches(0.28))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_BLUE_LINE if i == 0 else (COLOR_BLUE_ACCENT if i == 1 else COLOR_NAVY)
    bar.line.fill.background()
    
    # Valeur
    val_tb = s8.shapes.add_textbox(Inches(3.35 + w), by, Inches(1.1), Inches(0.3))
    vtf2 = val_tb.text_frame
    vtf2.margin_top = vtf2.margin_left = vtf2.margin_bottom = vtf2.margin_right = 0
    vp2 = vtf2.paragraphs[0]
    vp2.text = f"V = {fval:.3f}"
    vp2.font.name = FONT_HEADING
    vp2.font.size = Pt(10)
    vp2.font.bold = True
    vp2.font.color.rgb = COLOR_NAVY

    # Commentaire sous la barre
    ctb = s8.shapes.add_textbox(Inches(3.3), by + Inches(0.33), Inches(4.0), Inches(0.3))
    ctf = ctb.text_frame
    ctf.margin_top = ctf.margin_left = ctf.margin_bottom = ctf.margin_right = 0
    cp = ctf.paragraphs[0]
    cp.text = fcomment
    cp.font.name = FONT_BODY
    cp.font.size = Pt(9)
    cp.font.color.rgb = COLOR_TEXT_MUTED

# 2 Blocs d'informations complémentaires à droite
s8_age = [
    ("Courbe en cloche :", "Taux minimal chez les jeunes (16-24 ans : 7 %)."),
    ("Pic d'inclusion :", "Culmine entre 35 et 44 ans à 18,2 %."),
    ("Séniors :", "Baisse progressive au-delà de 65 ans.")
]
add_concise_card(s8, Inches(7.8), Inches(1.75), Inches(4.7), Inches(2.4), "Dynamique selon l'Âge", s8_age, tag="RELATION NON LINÉAIRE")

s8_pays = [
    ("Kenya :", "Taux le plus élevé (25 %) grâce à l'écosystème fintech."),
    ("Rwanda :", "Taux intermédiaire (11 %)."),
    ("Tanzanie & Ouganda :", "Faible bancarisation formelle (~9 %).")
]
add_concise_card(s8, Inches(7.8), Inches(4.35), Inches(4.7), Inches(2.4), "Disparités Géographiques", s8_pays, tag="ANALYSE TERRITORIALE")

# ------------------------------------------------------------------------------
# SLIDE 9 : PIPELINE DE PRÉTRAITEMENT (AVEC SCHÉMA FLOWCHART 4 ÉTAPES)
# ------------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
add_slide_header(s9, "Pipeline de Prétraitement et Feature Engineering", "3. MODÉLISATION", 9)

# SCHÉMA DU WORKFLOW EN 4 BLOCS RELIÉS PAR DES FLÈCHES
flow_steps = [
    ("1. Données Brutes", "FinScope Survey\n• 23 524 lignes\n• 13 colonnes\n• Format tabulaire", COLOR_CARD_BG, COLOR_CARD_BORDER),
    ("2. Nettoyage", "Filtrage strict\n• Drop uniqueid\n• Cible binaire (0/1)\n• Typage Pandas", COLOR_CARD_BG, COLOR_CARD_BORDER),
    ("3. Transformations", "ColumnTransformer\n• StandardScaler (Âge, Ménage)\n• OneHot (7 catégories)", COLOR_BLUE_SOFT, COLOR_BLUE_BORDER),
    ("4. Partitionnement", "Split Stratifié 80/20\n• Train : 18 819 (14,1 %)\n• Test : 4 705 (14,1 %)\n• 5-Fold Stratified CV", COLOR_CARD_BG, COLOR_CARD_BORDER)
]

bw = Inches(2.45)
bh = Inches(3.2)
arrow_w = Inches(0.4)

for i, (stitle, sbody, sbg, sbord) in enumerate(flow_steps):
    bx = Inches(0.8 + i * (2.45 + 0.55))
    by = Inches(1.75)
    
    # Carte étape
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
    card.fill.solid()
    card.fill.fore_color.rgb = sbg
    card.line.color.rgb = sbord
    card.line.width = Pt(1)
    
    tb = s9.shapes.add_textbox(bx + Inches(0.2), by + Inches(0.2), bw - Inches(0.4), bh - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0
    
    p1 = tf.paragraphs[0]
    p1.text = stitle
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(8)
    
    for line in sbody.split("\n"):
        p = tf.add_paragraph()
        p.text = line
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(3)
        
    # Flèche de liaison vers le bloc suivant
    if i < 3:
        ax = bx + bw + Inches(0.08)
        ay = by + Inches(1.4)
        arrow = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax, ay, Inches(0.38), Inches(0.25))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLOR_BLUE_LINE
        arrow.line.fill.background()

# Encart inférieur : Garantie méthodologique
s9_sec = [
    ("Ajustement exclusif sur Train :", "Le ColumnTransformer est ajusté (fit) uniquement sur la partition d'entraînement."),
    ("Élimination du Data Leakage :", "Aucune information issue du jeu de test n'est contaminée lors du centrage ou de l'encodage."),
    ("Reproductibilité totale :", "Graine aléatoire fixée (random_state=42) sur l'ensemble du pipeline.")
]
add_concise_card(s9, Inches(0.8), Inches(5.15), Inches(11.7), Inches(1.7), "Garantie d'Étanchéité et Absence de Fuite de Données", s9_sec, tag="RIGUEUR SCIENTIFIQUE")

# ------------------------------------------------------------------------------
# SLIDE 10 : STRATÉGIE DE MODÉLISATION (4 Cartes 2x2 très aérées)
# ------------------------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
add_slide_header(s10, "Stratégie de Modélisation et Algorithmes Évalués", "3. MODÉLISATION", 10)

s10_algos = [
    ("Régression Logistique", [
        ("Famille :", "Modèle linéaire probabiliste de référence (Baseline)."),
        ("Atout :", "Interprétabilité directe des coefficients en odds-ratios."),
        ("Limite :", "Ne capture pas nativement les non-linéarités complexes.")
    ], "BASELINE LINÉAIRE"),
    ("Random Forest", [
        ("Famille :", "Ensemble d'arbres décisionnels par ensachage (Bagging)."),
        ("Atout :", "Réduction de variance, robuste aux valeurs aberrantes."),
        ("Limite :", "Empreinte mémoire importante et coût d'inférence supérieur.")
    ], "BAGGING"),
    ("LightGBM", [
        ("Famille :", "Gradient Boosting leaf-wise sur histogrammes."),
        ("Atout :", "Entraînement ultra-rapide et faible consommation mémoire."),
        ("Limite :", "Sensibilité au surapprentissage sur données déséquilibrées.")
    ], "BOOSTING RAPIDE"),
    ("XGBoost", [
        ("Famille :", "Gradient Boosting régularisé (L1/L2) de pointe."),
        ("Atout :", "Gestion native du déséquilibre via scale_pos_weight."),
        ("Limite :", "Nécessite un calibrage fin des hyperparamètres.")
    ], "BOOSTING RÉGULARISÉ")
]

for idx, (title, items, tag) in enumerate(s10_algos):
    r = idx // 2
    c = idx % 2
    add_concise_card(s10, Inches(0.8 + c * 5.95), Inches(1.75 + r * 2.5), Inches(5.75), Inches(2.3), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 11 : BENCHMARK COMPARATIF DES MODÈLES (Tableau + 3 Badges KPI)
# ------------------------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
add_slide_header(s11, "Benchmark Comparatif des Performances (Test Set)", "3. MODÉLISATION", 11)

rows, cols = 5, 7
left, top, width, height = Inches(0.8), Inches(1.75), Inches(11.7), Inches(2.7)
table_shape = s11.shapes.add_table(rows, cols, left, top, width, height)
tbl = table_shape.table

headers = ["Modèle Évalué", "Accuracy", "Précision", "Rappel", "F1-Score", "ROC-AUC", "Seuil Optimal"]
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
        p.font.size = Pt(11.5)
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
            p.font.size = Pt(11.5)
            p.font.bold = is_winner
            p.font.color.rgb = COLOR_BLUE_ACCENT if is_winner else COLOR_TEXT_PRIMARY
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

kpis_s11 = [
    ("0,8767", "Meilleur ROC-AUC", "XGBoost maximise la séparation probabiliste"),
    ("0,5641", "Meilleur F1-Score", "Équilibre supérieur précision / rappel"),
    ("0,68", "Seuil Optimal", "Calibré par validation croisée à 5 plis sur train")
]

for i, (v, lbl, sub) in enumerate(kpis_s11):
    add_kpi_card(s11, Inches(0.8 + i * 3.95), Inches(4.75), Inches(3.75), Inches(1.9), v, lbl, sub,
                 val_color=COLOR_BLUE_LINE if i == 0 else COLOR_BLUE_ACCENT)

# ------------------------------------------------------------------------------
# SLIDE 12 : SÉLECTION DU MODÈLE FINAL ET SEUIL (KPIs + Carte décisionnelle)
# ------------------------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
add_slide_header(s12, "Sélection Finale du Modèle XGBoost", "3. MODÉLISATION", 12)

add_kpi_card(s12, Inches(0.8), Inches(1.75), Inches(4.0), Inches(1.55), "0,8767", "Score ROC-AUC", "Discrimination probabiliste maximale")
add_kpi_card(s12, Inches(0.8), Inches(3.45), Inches(4.0), Inches(1.55), "0,5641", "Score F1 Minoritaire", "Seuil de décision calibré à 0,68")
add_kpi_card(s12, Inches(0.8), Inches(5.15), Inches(4.0), Inches(1.55), "60,12 %", "Taux de Rappel", "Détection de 6 bancarisés réels sur 10")

s12_justif = [
    ("Pouvoir discriminant n°1 :", "ROC-AUC de 0,8767 garantissant un ordonnancement optimal des probabilités individuelles."),
    ("Équilibre Précision / Rappel :", "53,14 % de précision pour 60,12 % de rappel sur le jeu test indépendant."),
    ("Régularisation pénalisée :", "Résistance éprouvée au bruit statistique limitant fortement tout risque de surapprentissage."),
    ("Rôle du seuil à 0,68 :", "Réduit de 38 % les faux positifs par rapport au seuil naïf de 0,50."),
    ("Artefacts de production :", "Pipeline sérialisé sous models/best_model.joblib et métriques sous models/metrics.json.")
]
add_concise_card(s12, Inches(5.1), Inches(1.75), Inches(7.4), Inches(4.95), "Justification Décisionnelle & Industrialisation", s12_justif, tag="VALIDATION & EXPORT")

# ------------------------------------------------------------------------------
# SLIDE 13 : ARCHITECTURE TECHNIQUE GLOBALE (AVEC SCHÉMA D'ARCHITECTURE EN COUCHES)
# ------------------------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
add_slide_header(s13, "Architecture Technique de Déploiement Full-Stack", "4. DÉPLOIEMENT & MLOPS", 13)

# SCHÉMA D'ARCHITECTURE CONTENEURISÉE
# Cadre global Docker
docker_box = add_card(s13, Inches(0.8), Inches(1.75), Inches(11.7), Inches(3.6), bg_color=COLOR_WHITE, border_color=COLOR_BLUE_LINE)

dtb = s13.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(0.35))
dtf = dtb.text_frame
dtf.margin_top = dtf.margin_left = dtf.margin_bottom = dtf.margin_right = 0
dp = dtf.paragraphs[0]
dp.text = "ENVIRONNEMENT DE PRODUCTION CONTENEURISÉ (DOCKER SUR RENDER CLOUD • HTTPS)"
dp.font.name = FONT_HEADING
dp.font.size = Pt(9.5)
dp.font.bold = True
dp.font.color.rgb = COLOR_BLUE_LINE

# 4 Blocs horizontaux connectés
arch_nodes = [
    ("Navigateur Client", "Utilisateur final\n• Ordinateur / Mobile\n• Saisie des 13 variables\n• Consultation jauge SVG", Inches(1.1), Inches(2.3), Inches(2.4)),
    ("Frontend React", "Interface SPA\n• Vite + TypeScript\n• Tailwind CSS\n• Dashboards Recharts", Inches(3.95), Inches(2.3), Inches(2.4)),
    ("Backend FastAPI", "Moteur REST\n• Validation Pydantic\n• Inférence < 15 ms\n• Endpoints /predict, /retrain", Inches(6.8), Inches(2.3), Inches(2.4)),
    ("Pipeline XGBoost", "Inférence Machine Learning\n• ColumnTransformer\n• Modèle .joblib chargé\n• Verdict & Probabilités", Inches(9.65), Inches(2.3), Inches(2.4))
]

for name, desc, nx, ny, nw in arch_nodes:
    card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, nx, ny, nw, Inches(2.75))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1)

    tb = s13.shapes.add_textbox(nx + Inches(0.15), ny + Inches(0.15), nw - Inches(0.3), Inches(2.45))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0

    p_t = tf.paragraphs[0]
    p_t.text = name
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY
    p_t.space_after = Pt(6)

    for line in desc.split("\n"):
        p = tf.add_paragraph()
        p.text = line
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_after = Pt(2)

# Flèches de communication bidirectionnelle
for ax in [Inches(3.52), Inches(6.37), Inches(9.22)]:
    arrow = s13.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax, Inches(3.4), Inches(0.4), Inches(0.2))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLOR_BLUE_LINE
    arrow.line.fill.background()

# Bandeau de synthèse architecturale
s13_points = [
    ("Build Multi-Stage :", "Étape 1 Node 22 (compilation frontend) -> Étape 2 Python 3.12-slim ultra-légère."),
    ("Reproductibilité :", "Exécution locale ou cloud identique en une commande via docker-compose up."),
    ("Haute Performance :", "Temps de réponse d'inférence < 15 ms avec typage Pydantic asynchrone.")
]
add_concise_card(s13, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.4), "Garanties d'Architecture & Performance", s13_points, tag="INGÉNIERIE LOGICIELLE")

# ------------------------------------------------------------------------------
# SLIDE 14 : MLOPS ET RÉENTRAÎNEMENT (AVEC SCHÉMA DE BOUCLE DE FEEDBACK)
# ------------------------------------------------------------------------------
s14 = prs.slides.add_slide(blank_layout)
add_slide_header(s14, "Pipeline de Réentraînement Automatique (MLOps)", "4. DÉPLOIEMENT & MLOPS", 14)

# SCHÉMA DE LA BOUCLE DE RÉENTRAÎNEMENT ET QUALITY GATE
loop_box = add_card(s14, Inches(0.8), Inches(1.75), Inches(11.7), Inches(3.3), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)

ltb = s14.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(0.3))
ltf = ltb.text_frame
ltf.margin_top = ltf.margin_left = ltf.margin_bottom = ltf.margin_right = 0
lp = ltf.paragraphs[0]
lp.text = "BOUCLE DE FEEDBACK MLOPS & CONTRÔLE QUALITÉ AUTOMATISÉ"
lp.font.name = FONT_HEADING
lp.font.size = Pt(9.5)
lp.font.bold = True
lp.font.color.rgb = COLOR_BLUE_ACCENT

# Bloc 1 : Données
b1 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(2.4), Inches(2.4), Inches(2.3))
b1.fill.solid()
b1.fill.fore_color.rgb = COLOR_CARD_BG
b1.line.color.rgb = COLOR_CARD_BORDER
tf1 = b1.text_frame
tf1.word_wrap = True
tf1.margin_top = tf1.margin_left = tf1.margin_bottom = tf1.margin_right = 0
p = tf1.paragraphs[0]
p.text = "1. Nouvelles Données\n\n• Enquêtes actualisées\n• Dérive surveillée\n• Ingestion automatisée"
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = COLOR_NAVY

# Flèche 1
arr1 = s14.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.55), Inches(3.3), Inches(0.35), Inches(0.2))
arr1.fill.solid()
arr1.fill.fore_color.rgb = COLOR_BLUE_LINE
arr1.line.fill.background()

# Bloc 2 : Script Retrain
b2 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.95), Inches(2.4), Inches(2.4), Inches(2.3))
b2.fill.solid()
b2.fill.fore_color.rgb = COLOR_CARD_BG
b2.line.color.rgb = COLOR_CARD_BORDER
tf2 = b2.text_frame
tf2.word_wrap = True
tf2.margin_top = tf2.margin_left = tf2.margin_bottom = tf2.margin_right = 0
p = tf2.paragraphs[0]
p.text = "2. Script src/retrain.py\n\n• Ré-étalonnage ColumnTransformer\n• Réentraînement XGBoost\n• Calcul métriques CV"
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = COLOR_NAVY

# Flèche 2
arr2 = s14.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.4), Inches(3.3), Inches(0.35), Inches(0.2))
arr2.fill.solid()
arr2.fill.fore_color.rgb = COLOR_BLUE_LINE
arr2.line.fill.background()

# Bloc 3 : Quality Gate (Décision)
b3 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.4), Inches(2.5), Inches(2.3))
b3.fill.solid()
b3.fill.fore_color.rgb = COLOR_BLUE_SOFT
b3.line.color.rgb = COLOR_BLUE_BORDER
tf3 = b3.text_frame
tf3.word_wrap = True
tf3.margin_top = tf3.margin_left = tf3.margin_bottom = tf3.margin_right = 0
p = tf3.paragraphs[0]
p.text = "3. Quality Gate\n\nROC-AUC >= 0,75 ?\n\n• Condition de déploiement\n• Sécurité opérationnelle"
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = COLOR_NAVY

# Flèche vers succès
arr3 = s14.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(9.35), Inches(2.8), Inches(0.35), Inches(0.18))
arr3.fill.solid()
arr3.fill.fore_color.rgb = COLOR_SUCCESS_TEXT
arr3.line.fill.background()

# Bloc Succès
b_ok = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.75), Inches(2.4), Inches(2.5), Inches(1.05))
b_ok.fill.solid()
b_ok.fill.fore_color.rgb = COLOR_SUCCESS_BG
b_ok.line.color.rgb = COLOR_SUCCESS_BORDER
tf_ok = b_ok.text_frame
tf_ok.word_wrap = True
tf_ok.margin_top = tf_ok.margin_left = tf_ok.margin_bottom = tf_ok.margin_right = 0
p = tf_ok.paragraphs[0]
p.text = "OUI : Déploiement\n• Hot-reload en mémoire\n• 0 temps d'arrêt"
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_SUCCESS_TEXT

# Flèche vers échec
arr4 = s14.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(9.35), Inches(3.9), Inches(0.35), Inches(0.18))
arr4.fill.solid()
arr4.fill.fore_color.rgb = COLOR_DANGER_TEXT
arr4.line.fill.background()

# Bloc Rejet
b_no = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.75), Inches(3.6), Inches(2.5), Inches(1.05))
b_no.fill.solid()
b_no.fill.fore_color.rgb = COLOR_DANGER_BG
b_no.line.color.rgb = COLOR_DANGER_BORDER
tf_no = b_no.text_frame
tf_no.word_wrap = True
tf_no.margin_top = tf_no.margin_left = tf_no.margin_bottom = tf_no.margin_right = 0
p = tf_no.paragraphs[0]
p.text = "NON : Rollback\n• Maintien modèle actif\n• Alerte retraining.log"
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_DANGER_TEXT

# 2 Cartes de modes d'exécution en bas
s14_cron = [
    ("Tâche planifiée locale :", "Exécution hebdomadaire autonome via scripts/retrain_cron.sh."),
    ("Auditabilité :", "Horodatage et scores historisés dans retraining.log.")
]
add_concise_card(s14, Inches(0.8), Inches(5.2), Inches(5.7), Inches(1.7), "Mode Planifié (Cron Job)", s14_cron, tag="AUTOMATISATION LOCALE")

s14_api = [
    ("Déclenchement distant :", "Requête sécurisée POST /api/retrain (intégration CI/CD / Airflow)."),
    ("Rechargement à chaud :", "Remplacement immédiat des poids sans coupure de trafic.")
]
add_concise_card(s14, Inches(6.8), Inches(5.2), Inches(5.7), Inches(1.7), "Mode Webhook REST (API)", s14_api, tag="ORCHESTRATION DISTANTE")

# ------------------------------------------------------------------------------
# SLIDE 15 : DÉMONSTRATION EN PRODUCTION (URL + 3 Cartes interactives)
# ------------------------------------------------------------------------------
s15 = prs.slides.add_slide(blank_layout)
add_slide_header(s15, "Démonstration de l'Application en Production", "5. DÉMONSTRATION", 15)

banner = add_card(s15, Inches(0.8), Inches(1.75), Inches(11.7), Inches(1.1), bg_color=COLOR_BLUE_SOFT, border_color=COLOR_BLUE_BORDER)
btb = s15.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(0.9))
btf = btb.text_frame
btf.word_wrap = True
bp1 = btf.paragraphs[0]
bp1.text = "APPLICATION OPÉRATIONNELLE EN LIGNE • HÉBERGÉE SUR RENDER CLOUD"
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
        ("Saisie instantanée :", "Formulaire complet reprenant les 13 variables du modèle."),
        ("Jauge semi-circulaire :", "Animation SVG interactive du score calculé."),
        ("Verdict immédiat :", "Affichage clair du statut (Bancarisé / Non bancarisé).")
    ], "SIMULATION"),
    ("Tableaux de Bord EDA", [
        ("Exploration visuelle :", "Graphiques interactifs des taux par pays et niveau d'étude."),
        ("Croisements sociologiques :", "Distribution selon le secteur professionnel."),
        ("Compréhension directe :", "Insights majeurs accessibles aux non-techniciens.")
    ], "VISUALISATION"),
    ("Monitoring & Retraining", [
        ("Métriques officielles :", "Affichage direct du ROC-AUC, du F1 et du seuil (0,68)."),
        ("Déclenchement direct :", "Bouton d'actualisation connecté à l'API de réentraînement."),
        ("Transparence totale :", "Statut de déploiement et logs vérifiables en ligne.")
    ], "SUPERVISION")
]

for i, (title, items, tag) in enumerate(s15_features):
    add_concise_card(s15, Inches(0.8 + i * 3.95), Inches(3.1), Inches(3.75), Inches(3.65), title, items, tag=tag)

# ------------------------------------------------------------------------------
# SLIDE 16 : LIMITES, PERSPECTIVES ET CONCLUSION
# ------------------------------------------------------------------------------
s16 = prs.slides.add_slide(blank_layout)
add_slide_header(s16, "Limites, Perspectives et Conclusion", "6. CONCLUSION", 16)

s16_lim = [
    ("Données déclaratives :", "Enquêtes FinScope basées sur les déclarations des ménages."),
    ("Revenu qualitatif :", "Absence de montants monétaires précis dans les variables."),
    ("Synchronisation :", "Enquêtes nationales étalées de 2016 à 2018 selon les pays.")
]
add_concise_card(s16, Inches(0.8), Inches(1.75), Inches(5.7), Inches(3.3), "Limites Méthodologiques Identifiées", s16_lim, tag="LUCIDITÉ SCIENTIFIQUE")

s16_persp = [
    ("Transactions Mobile Money :", "Couplage avec les volumes réels de flux (M-Pesa, MTN)."),
    ("Explicabilité locale SHAP :", "Justification des prédictions individuelles par valeurs de Shapley."),
    ("Données géospatiales :", "Intégration de la distance aux points de retrait et agences.")
]
add_concise_card(s16, Inches(6.8), Inches(1.75), Inches(5.7), Inches(3.3), "Perspectives d'Amélioration", s16_persp, tag="ÉVOLUTIONS")

# Bandeau de conclusion générale
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
    "à la sélection d'un modèle XGBoost régularisé (ROC-AUC 0,8767, F1 0,5641), aboutissant à une application "
    "conteneurisée déployée en production avec surveillance et réentraînement automatisé."
)
cp2.font.name = FONT_BODY
cp2.font.size = Pt(11)
cp2.font.color.rgb = COLOR_NAVY

# Sauvegarde
output_pptx = "Presentation_Soutenance.pptx"
prs.save(output_pptx)
print(f"Présentation avec schémas générée avec succès : {output_pptx} ({len(prs.slides)} slides)")

from IPython.display import display
#!/usr/bin/env python
# coding: utf-8

# # EDA — Financial Inclusion in Africa (Zindi)
# 
# **Objectif métier** : prédire si une personne interrogée possède un compte bancaire (`bank_account`) en Afrique de l'Est (Kenya, Rwanda, Tanzanie, Ouganda) afin d'orienter les politiques d'inclusion financière.
# 
# **Plan** : 1) Description du dataset · 2) Qualité des données · 3) Statistiques descriptives · 4) Analyse univariée · 5) Analyse bivariée vs cible · 6) Corrélations / associations · 7) Hypothèses et enseignements.




import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({"figure.dpi": 100, "axes.titleweight": "bold"})
TRAIN = "data/Train.csv"
TEST  = "data/Test.csv"
df = pd.read_csv(TRAIN); test = pd.read_csv(TEST)
print("Train :", df.shape, "| Test :", test.shape)
df.head()


# ## 1. Description du dataset




defs = pd.read_csv("data/VariableDefinitions.csv")
pd.set_option("display.max_colwidth", 200)
defs





df.info()





num_cols = ["household_size", "age_of_respondent"]
cat_cols = [c for c in df.columns if c not in num_cols + ["uniqueid", "year", "bank_account"]]
print("Numériques :", num_cols)
print("Catégorielles :", cat_cols)
print("Années par pays :"); print(pd.crosstab(df.country, df.year))


# ## 2. Qualité des données




print("Valeurs manquantes (train) :", df.isna().sum().sum())
print("Valeurs manquantes (test)  :", test.isna().sum().sum())
print("Lignes dupliquées          :", df.duplicated().sum())
print("uniqueid dupliqués seuls   :", df.uniqueid.duplicated().sum(), "(sur", len(df), ")")
print("(country, uniqueid) dupliqués :", df.duplicated(["country", "uniqueid"]).sum())


# > **Point d'attention** : `uniqueid` n'est **pas** unique globalement (il est réutilisé d'un pays à l'autre) ; c'est le couple `(country, uniqueid)` qui identifie un individu. À ne pas utiliser comme variable explicative.




# Incohérences possibles
print("Âge min/max :", df.age_of_respondent.min(), df.age_of_respondent.max())
print("Taille ménage min/max :", df.household_size.min(), df.household_size.max())
print("\nChefs de ménage de moins de 18 ans :", ((df.relationship_with_head=="Head of Household") & (df.age_of_respondent<18)).sum())
print("Mineurs (<18) :", (df.age_of_respondent<18).sum())
print("Enfants (relation 'Child') de plus de 60 ans :", ((df.relationship_with_head=="Child") & (df.age_of_respondent>60)).sum())
print("Marital 'Married' avec âge < 18 :", ((df.marital_status=="Married/Living together") & (df.age_of_respondent<18)).sum())
print("\nModalités rares (<0.5 %) :")
for c in cat_cols:
    vc = df[c].value_counts(normalize=True)
    r = vc[vc < 0.005]
    if len(r): print(" ", c, "->", {k: f"{v:.2%}" for k, v in r.items()})
# cohérence train/test
print("\nModalités du test absentes du train :")
for c in cat_cols:
    d = set(test[c].unique()) - set(df[c].unique())
    if d: print(" ", c, d)
print("(aucune)" if all(not (set(test[c].unique()) - set(df[c].unique())) for c in cat_cols) else "")


# ## 3. Statistiques descriptives




display(df[num_cols].describe().T.assign(skew=df[num_cols].skew(), kurtosis=df[num_cols].kurt()))
display(df[cat_cols + ["bank_account"]].describe().T)


# ## 4. Analyse univariée




vc = df.bank_account.value_counts()
pct = vc / vc.sum() * 100
fig, ax = plt.subplots(figsize=(5, 3.6))
sns.barplot(x=vc.index, y=vc.values, palette=["#c0504d", "#4f81bd"], ax=ax)
for i, (v, p) in enumerate(zip(vc.values, pct.values)):
    ax.text(i, v, f"{v:,}\n({p:.1f} %)", ha="center", va="bottom")
ax.set_title("Variable cible : bank_account"); ax.set_ylabel("Effectif"); ax.set_ylim(0, vc.max()*1.18)
plt.show()
print(f"Ratio de déséquilibre : {vc['No']/vc['Yes']:.1f} : 1")


# La cible est **fortement déséquilibrée** (~14 % de bancarisés) : on utilisera F1 / AUC-PR plutôt que l'accuracy, une stratification du split et éventuellement un rééquilibrage (class_weight, SMOTE).




fig, axes = plt.subplots(2, 2, figsize=(12, 7))
sns.histplot(df.age_of_respondent, bins=40, kde=True, ax=axes[0,0], color="#4f81bd"); axes[0,0].set_title("Âge")
sns.boxplot(x=df.age_of_respondent, ax=axes[0,1], color="#9bbb59"); axes[0,1].set_title("Âge (boxplot)")
sns.countplot(x=df.household_size, ax=axes[1,0], color="#8064a2"); axes[1,0].set_title("Taille du ménage")
sns.boxplot(x=df.household_size, ax=axes[1,1], color="#f79646"); axes[1,1].set_title("Taille du ménage (boxplot)")
plt.tight_layout(); plt.show()

def iqr_out(s):
    q1, q3 = s.quantile([.25, .75]); i = q3 - q1
    return ((s < q1 - 1.5*i) | (s > q3 + 1.5*i)).sum()
for c in num_cols:
    print(f"{c}: {iqr_out(df[c])} outliers IQR ({iqr_out(df[c])/len(df):.2%}), skew={df[c].skew():.2f}")





order_cols = ["country", "location_type", "cellphone_access", "gender_of_respondent",
              "relationship_with_head", "marital_status", "education_level", "job_type"]
fig, axes = plt.subplots(4, 2, figsize=(14, 18))
for ax, c in zip(axes.ravel(), order_cols):
    o = df[c].value_counts()
    sns.barplot(y=o.index, x=o.values, ax=ax, color="#4f81bd")
    for i, v in enumerate(o.values): ax.text(v, i, f" {v/len(df):.1%}", va="center", fontsize=9)
    ax.set_title(c); ax.set_xlabel("Effectif"); ax.set_ylabel("")
    ax.set_xlim(0, o.max()*1.15)
plt.tight_layout(); plt.show()


# ## 5. Analyse bivariée (variables explicatives vs `bank_account`)




df["y"] = (df.bank_account == "Yes").astype(int)
print(f"Taux global de bancarisation : {df.y.mean():.2%}")

def rate_plot(ax, col, order=None):
    g = df.groupby(col).y.agg(["mean", "count"])
    if order is None: g = g.sort_values("mean")
    else: g = g.loc[order]
    sns.barplot(y=g.index.astype(str), x=g["mean"]*100, ax=ax, color="#4f81bd")
    for i, (m, n) in enumerate(zip(g["mean"], g["count"])): ax.text(m*100, i, f" {m:.1%} (n={n:,})", va="center", fontsize=9)
    ax.axvline(df.y.mean()*100, color="red", ls="--", lw=1)
    ax.set_title(f"Taux de bancarisation par {col}"); ax.set_xlabel("% avec compte bancaire"); ax.set_ylabel("")
    ax.set_xlim(0, max(g["mean"]*100)*1.35)

fig, axes = plt.subplots(4, 2, figsize=(14, 18))
for ax, c in zip(axes.ravel(), order_cols): rate_plot(ax, c)
plt.tight_layout(); plt.show()





# Tests d'association (chi², V de Cramér) pour chaque variable catégorielle
def cramers_v(x, y):
    ct = pd.crosstab(x, y); chi2, p, dof, _ = stats.chi2_contingency(ct)
    n = ct.values.sum(); k = min(ct.shape) - 1
    return np.sqrt(chi2 / (n * k)), chi2, p

rows = []
for c in cat_cols + ["year"]:
    v, chi2, p = cramers_v(df[c], df.bank_account)
    rows.append((c, v, chi2, p))
assoc = pd.DataFrame(rows, columns=["variable", "V_Cramer", "chi2", "p_value"]).sort_values("V_Cramer", ascending=False)
display(assoc.style.format({"V_Cramer": "{:.3f}", "chi2": "{:.1f}", "p_value": "{:.2e}"}))

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=assoc, y="variable", x="V_Cramer", color="#4f81bd", ax=ax)
ax.set_title("Force d'association avec bank_account (V de Cramér)"); plt.show()





# Variables numériques vs cible
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.boxplot(data=df, x="bank_account", y="age_of_respondent", ax=axes[0], palette=["#c0504d", "#4f81bd"]); axes[0].set_title("Âge vs cible")
sns.boxplot(data=df, x="bank_account", y="household_size", ax=axes[1], palette=["#c0504d", "#4f81bd"]); axes[1].set_title("Taille ménage vs cible")
df["age_bin"] = pd.cut(df.age_of_respondent, [15, 25, 35, 45, 55, 65, 75, 101], right=False)
g = df.groupby("age_bin", observed=True).y.mean()*100
sns.lineplot(x=g.index.astype(str), y=g.values, marker="o", ax=axes[2]); axes[2].set_title("Taux de bancarisation par tranche d'âge"); axes[2].set_ylabel("%")
plt.setp(axes[2].get_xticklabels(), rotation=30); plt.tight_layout(); plt.show()

for c in num_cols:
    a, b = df.loc[df.y==1, c], df.loc[df.y==0, c]
    u, p = stats.mannwhitneyu(a, b)
    print(f"{c}: médiane Yes={a.median():.0f} / No={b.median():.0f} | Mann-Whitney p={p:.2e}")





# Interactions clés
fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
t = df.pivot_table(index="country", columns="education_level", values="y", aggfunc="mean")*100
sns.heatmap(t, annot=True, fmt=".0f", cmap="Blues", ax=axes[0], cbar=False); axes[0].set_title("% bancarisés : pays × éducation")
t = df.pivot_table(index="country", columns="job_type", values="y", aggfunc="mean")*100
sns.heatmap(t, annot=True, fmt=".0f", cmap="Blues", ax=axes[1], cbar=False); axes[1].set_title("% bancarisés : pays × emploi")
t = df.pivot_table(index="gender_of_respondent", columns="location_type", values="y", aggfunc="mean")*100
sns.heatmap(t, annot=True, fmt=".1f", cmap="Blues", ax=axes[2], cbar=False); axes[2].set_title("% bancarisés : genre × zone")
plt.tight_layout(); plt.show()





# Pays x année et cellphone x éducation
display(df.groupby(["country", "year"]).agg(n=("y", "size"), taux_bancarise=("y", "mean")).style.format({"taux_bancarise": "{:.1%}"}))
display((df.pivot_table(index="education_level", columns="cellphone_access", values="y", aggfunc="mean")*100).round(1))


# ## 6. Corrélations




# Matrice de corrélation sur variables encodées (numériques + cible + binaires)
enc = pd.DataFrame({
    "bank_account": df.y,
    "age": df.age_of_respondent,
    "household_size": df.household_size,
    "urban": (df.location_type=="Urban").astype(int),
    "cellphone": (df.cellphone_access=="Yes").astype(int),
    "male": (df.gender_of_respondent=="Male").astype(int),
    "educ_ordinal": df.education_level.map({"No formal education":0, "Primary education":1, "Secondary education":2,
                                            "Vocational/Specialised training":3, "Tertiary education":4}),
})
corr = enc.corr(method="spearman")
fig, ax = plt.subplots(figsize=(7, 5.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax); ax.set_title("Corrélations de Spearman")
plt.show()


# ## 7. Hypothèses et enseignements métier




top = lambda c: df.groupby(c).y.mean().sort_values(ascending=False)
edu, job, cty = top("education_level"), top("job_type"), top("country")
print("Pays        :", {k: f"{v:.1%}" for k, v in cty.items()})
print("Éducation   :", {k: f"{v:.1%}" for k, v in edu.items()})
print("Emploi (top 3 / bas 3) :", {k: f"{v:.1%}" for k, v in list(job.items())[:3]}, "|", {k: f"{v:.1%}" for k, v in list(job.items())[-3:]})
for c in ["gender_of_respondent", "location_type", "cellphone_access"]:
    print(c, {k: f"{v:.1%}" for k, v in top(c).items()})


# ### Synthèse (à confirmer en modélisation)
# 
# 1. **Cible très déséquilibrée** (~14 % de comptes) → métriques F1/AUC-PR, `stratify=y`, `class_weight` ou SMOTE.
# 2. **Pays** : effet net (Kenya ≈ 25 % contre 9–12 % ailleurs, V de Cramér ≈ 0,19) ; pays et année sont totalement confondus (une année de collecte par pays), donc leurs effets ne sont pas séparables.
# 3. **Éducation (V ≈ 0,39) et type d'emploi (V ≈ 0,36)** sont les variables les plus discriminantes : emploi formel (gouvernement 77 %, privé 54 %) et formation professionnelle/supérieure (51–57 %) contre 2–9 % pour sans revenu, informel, sans instruction ou primaire.
# 4. **Accès au téléphone** (V ≈ 0,21 ; 18 % vs 2 %) est le 3e facteur ; **genre** (19 % hommes vs 11 % femmes), **zone** (18 % urbain vs 12 % rural) et relation avec le chef de ménage ont des effets plus modestes (V ≈ 0,09–0,12). Ces variables sont corrélées entre elles : à démêler en modélisation.
# 5. **Âge** : relation non linéaire en cloche (7,5 % chez les 16–24 ans, pic ≈ 18 % à 35–44 ans, 9 % après 75 ans) → tranches d'âge / modèles à base d'arbres. L'effet de la taille du ménage est faible.
# 6. **Qualité** : aucun manquant ni doublon, mais `uniqueid` non unique entre pays (à exclure), quelques modalités très rares (`Dont know`, `Other`) à regrouper, et quelques incohérences d'âge/relation à vérifier.
# 7. **Feature engineering suggéré** : tranches d'âge, regroupement des modalités rares, interaction pays × éducation/emploi, éducation ordinale, taille de ménage en classes.

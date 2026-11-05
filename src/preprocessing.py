import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Définition des colonnes du dataset
NUMERICAL_COLS = ['household_size', 'age_of_respondent', 'year']
CATEGORICAL_COLS = [
    'country',
    'location_type',
    'cellphone_access',
    'gender_of_respondent',
    'relationship_with_head',
    'marital_status',
    'education_level',
    'job_type'
]
TARGET_COL = 'bank_account'
DROP_COLS = ['uniqueid']


def load_raw_data(data_path: str = "data/Train.csv") -> pd.DataFrame:
    """Charge les données brutes depuis un fichier CSV."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Le fichier de données '{data_path}' n'existe pas.")
    return pd.read_csv(data_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le DataFrame (suppression des identifiants).

    Remarque : on ne supprime PAS les lignes identiques une fois `uniqueid` retiré.
    Ce sont des individus différents au profil identique, pas de vrais doublons
    (l'EDA n'a trouvé aucun doublon avec `uniqueid`).
    """
    df_clean = df.copy()
    
    # Suppression des colonnes d'identifiant
    for col in DROP_COLS:
        if col in df_clean.columns:
            df_clean = df_clean.drop(columns=[col])
    
    return df_clean


def get_feature_preprocessor() -> ColumnTransformer:
    """Construit et retourne le pipeline de prétraitement (scikit-learn ColumnTransformer)."""
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERICAL_COLS),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_COLS)
        ]
    )
    return preprocessor


def split_features_target(df: pd.DataFrame):
    """Sépare les variables explicatives (X) de la variable cible (y)."""
    df_clean = clean_data(df)
    
    if TARGET_COL in df_clean.columns:
        X = df_clean.drop(columns=[TARGET_COL])
        y = df_clean[TARGET_COL].map({'Yes': 1, 'No': 0})
        return X, y
    else:
        return df_clean, None


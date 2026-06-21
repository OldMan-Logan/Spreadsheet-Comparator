import pandas as pd
from rapidfuzz import fuzz


def normalize_dataframe(df):

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df = df.fillna("")

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def detect_primary_key(df1, df2):

    common_cols = list(
        set(df1.columns).intersection(df2.columns)
    )

    best_col = None
    best_score = -1

    for col in common_cols:

        unique_ratio_1 = df1[col].nunique() / max(len(df1), 1)
        unique_ratio_2 = df2[col].nunique() / max(len(df2), 1)

        score = (
            unique_ratio_1 +
            unique_ratio_2
        ) / 2

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def match_columns(cols1, cols2, threshold=70):

    mapping = {}

    unmatched_a = []
    unmatched_b = set(cols2)

    for col1 in cols1:

        best_match = None
        best_score = 0

        for col2 in cols2:

            score = fuzz.WRatio(
                str(col1).lower(),
                str(col2).lower()
            )

            if score > best_score:
                best_score = score
                best_match = col2

        if best_score >= threshold:

            mapping[col1] = best_match

            if best_match in unmatched_b:
                unmatched_b.remove(best_match)

        else:

            unmatched_a.append(col1)

    return {
        "mapping": mapping,
        "missing_in_b": unmatched_a,
        "new_in_b": list(unmatched_b)
    }
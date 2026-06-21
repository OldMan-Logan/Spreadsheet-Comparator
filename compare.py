import pandas as pd

from pathlib import Path

from file_loader import load_spreadsheet

from utils import (
    normalize_dataframe,
    match_columns
)


def compare_files(file1, file2):

    # Reading file metadata
    file1_name = Path(file1).name
    file2_name = Path(file2).name

    file1_type = Path(file1).suffix
    file2_type = Path(file2).suffix

    # Reading files
    df1 = load_spreadsheet(file1)
    df2 = load_spreadsheet(file2)

    # Normalize data
    df1 = normalize_dataframe(df1)
    df2 = normalize_dataframe(df2)

    # Use first column as primary key
    pk1 = df1.columns[0]
    pk2 = df2.columns[0]


    # Set index
    df1 = df1.set_index(pk1)
    df2 = df2.set_index(pk2)

    # Convert index to string
    df1.index = df1.index.astype(str)
    df2.index = df2.index.astype(str)

    ids1 = set(df1.index)
    ids2 = set(df2.index)

    column_info = match_columns(
        list(df1.columns),
        list(df2.columns)
    )

    column_mapping = column_info["mapping"]

    added_ids = ids2 - ids1
    deleted_ids = ids1 - ids2
    common_ids = ids1.intersection(ids2)

    # ------------------
    # Added rows
    # ------------------

    added_rows = []

    if added_ids:
        added_rows = (
            df2.loc[list(added_ids)]
            .reset_index()
            .to_dict("records")
        )

    # ------------------
    # Deleted rows
    # ------------------

    deleted_rows = []

    if deleted_ids:
        deleted_rows = (
            df1.loc[list(deleted_ids)]
            .reset_index()
            .to_dict("records")
        )

    # ------------------
    # Modified rows
    # ------------------

    modified = []

    common_columns = column_mapping

    for row_id in common_ids:

        row1 = df1.loc[row_id]
        row2 = df2.loc[row_id]

        changes = {}

        for col_a, col_b in common_columns.items():

            old_val = str(row1[col_a]).strip()
            new_val = str(row2[col_b]).strip()

            if old_val != new_val:

                changes[col_a] = {
                    "file_a_column": col_a,
                    "file_b_column": col_b,
                    "old": old_val,
                    "new": new_val
                }

        if changes:

            modified.append({
                "id": row_id,
                "changes": changes
            })

    return {
        "file1_name": file1_name,
        "file2_name": file2_name,
        "file1_type": file1_type,
        "file2_type": file2_type,
        "primary_key_a": pk1,
        "primary_key_b": pk2,
        "column_mapping": column_mapping,
        "missing_columns": column_info["missing_in_b"],
        "new_columns": column_info["new_in_b"],
        "added_count": len(added_rows),
        "deleted_count": len(deleted_rows),
        "modified_count": len(modified),
        "added": added_rows,
        "deleted": deleted_rows,
        "modified": modified
    }
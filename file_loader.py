import pandas as pd
from pathlib import Path


def load_spreadsheet(filepath):

    ext = Path(filepath).suffix.lower()

    if ext == ".csv":
        return pd.read_csv(filepath)

    elif ext in [".xlsx", ".xlsm"]:
        return pd.read_excel(filepath)

    elif ext == ".xls":
        return pd.read_excel(filepath, engine="xlrd")

    elif ext == ".xlsb":
        return pd.read_excel(filepath, engine="pyxlsb")

    elif ext == ".ods":
        return pd.read_excel(filepath, engine="odf")

    elif ext == ".xml":
        return pd.read_xml(filepath)

    elif ext == ".tsv":
        return pd.read_csv(filepath, sep="\t")

    elif ext == ".txt":

        try:
            return pd.read_csv(filepath)

        except:

            return pd.read_csv(
                filepath,
                sep="\t"
            )

    raise ValueError(
        f"Unsupported file type: {ext}"
    )
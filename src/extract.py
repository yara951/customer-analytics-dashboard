import pandas as pd
from src.config import RAW_DIR


def extract_data():
    file_path = RAW_DIR / "Online_Retail.xlsx"

    # Check if the source file exists
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    # Extract raw data
    print("Extracting raw data...")

    df = pd.read_excel(file_path, engine="openpyxl")

    print(f"Rows extracted: {len(df):,}")
    print(f"Columns extracted: {len(df.columns)}")

    return df
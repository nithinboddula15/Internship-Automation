import os

import pandas as pd

from logger import logger

EXCEL_FILE = "data/internships.xlsx"


def load_existing_data():

    logger.info(f"Loading existing data from '{EXCEL_FILE}'...")

    try:

        old_df = pd.read_excel(EXCEL_FILE)

        logger.info(f"Loaded {len(old_df)} existing rows.")
        logger.info(f"Columns: {old_df.columns.tolist()}")

        existing_ids = old_df["internship_id"].tolist()

        logger.info(f"Existing internship IDs count: {len(existing_ids)}")

    except FileNotFoundError:

        logger.info(
            f"'{EXCEL_FILE}' not found. Starting fresh with empty database."
        )
        old_df = pd.DataFrame()
        existing_ids = []

    except Exception as e:

        logger.error(f"Error reading Excel file: {e}. Starting with empty database.")
        old_df = pd.DataFrame()
        existing_ids = []

    return old_df, existing_ids


def save_new_data(old_df, new_internships):

    logger.info(f"Saving {len(new_internships)} new internship(s)...")

    df = pd.DataFrame(new_internships)

    # Convert list columns to readable strings
    list_columns = ["matched_skills", "missing_skills", "internship_skills", "ai_reason"]

    if not df.empty:

        for col in list_columns:

            if col in df.columns:

                df[col] = df[col].apply(
                    lambda x: ", ".join(x) if isinstance(x, list) else x
                )

    # Also convert list columns in old_df if they exist
    if not old_df.empty:

        for col in list_columns:

            if col in old_df.columns:

                old_df[col] = old_df[col].apply(
                    lambda x: ", ".join(x) if isinstance(x, list) else x
                )

    final_df = pd.concat([old_df, df], ignore_index=True)

    # Sort by match_score descending before saving
    if "match_score" in final_df.columns:

        final_df = final_df.sort_values(
            by="match_score",
            ascending=False
        ).reset_index(drop=True)

    try:

        os.makedirs(os.path.dirname(EXCEL_FILE), exist_ok=True)
        final_df.to_excel(EXCEL_FILE, index=False)

        logger.info(
            f"Excel saved: {len(final_df)} total rows in '{EXCEL_FILE}'."
        )

    except Exception as e:

        logger.error(f"Failed to save Excel file: {e}")

    return df, final_df
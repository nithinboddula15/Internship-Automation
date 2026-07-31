import pandas as pd


def load_existing_data():

    try:
        old_df = pd.read_excel("data/internships.xlsx")

        print("Columns in Excel:")
        print(old_df.columns.tolist())

        existing_ids = old_df["internship_id"].tolist()

    except Exception as e:

        print("Error reading Excel:", e)

        old_df = pd.DataFrame()

        existing_ids = []

    return old_df, existing_ids

def save_new_data(old_df, new_internships):

    df = pd.DataFrame(new_internships)
    
    

    # Convert lists to readable strings
    if not df.empty:
        if "matched_skills" in df.columns:
            df["matched_skills"] = df["matched_skills"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

        if "missing_skills" in df.columns:
            df["missing_skills"] = df["missing_skills"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

        if "internship_skills" in df.columns:
            df["internship_skills"] = df["internship_skills"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

    final_df = pd.concat([old_df, df], ignore_index=True)

    final_df.to_excel("data/internships.xlsx", index=False)

    final_df = final_df.sort_values(
    by="match_score",
    ascending=False
    ).reset_index(drop=True)

    final_df.to_excel(
    "data/internships.xlsx",
    index=False
    )

    return df, final_df
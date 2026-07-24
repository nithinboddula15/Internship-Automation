import pandas as pd


def load_existing_data():

    try:
        old_df = pd.read_excel("data/internships.xlsx")
        existing_ids = old_df["internship_id"].tolist()

    except Exception as e:

        print("Error reading Excel:", e)

        old_df = pd.DataFrame()

        existing_ids = []

    return old_df, existing_ids


def save_new_data(old_df, new_internships):

    df = pd.DataFrame(new_internships)

    final_df = pd.concat([old_df, df], ignore_index=True)

    final_df.to_excel("data/internships.xlsx", index=False)

    return df, final_df
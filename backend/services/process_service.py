import pandas as pd
import time

from modules.religion_infer import infer_religion_from_name
from modules.card_ocr import extract_cards_from_pdf


AGE_ORDER = [
    "18-25",
    "26-35",
    "36-45",
    "46-60",
    "60+",
    "Unknown"
]


def age_group(age):

    if pd.isna(age):
        return "Unknown"

    try:
        age = int(age)

    except:
        return "Unknown"

    if age <= 25:
        return "18-25"

    if age <= 35:
        return "26-35"

    if age <= 45:
        return "36-45"

    if age <= 60:
        return "46-60"

    return "60+"


def clean_voter_data(df):

    if df.empty:
        return df

    df = df.copy()

    if "name" in df.columns:

        df["name"] = (
            df["name"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df = df[
            df["name"].str.len() >= 2
        ]

    text_cols = (
        df.select_dtypes(
            include="object"
        ).columns
    )

    for col in text_cols:

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )

    if "age" in df.columns:

        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )

        df = df[
            (
                df["age"].isna()
            )
            |
            (
                (df["age"] >= 18)
                &
                (df["age"] <= 120)
            )
        ]

        df["age_group"] = (
            df["age"]
            .apply(age_group)
        )

    else:

        df["age_group"] = (
            "Unknown"
        )

    duplicate_cols = [

        col

        for col in [
            "name",
            "father_name",
            "age"
        ]

        if col in df.columns
    ]

    if duplicate_cols:

        before = len(df)

        df = df.drop_duplicates(
            subset=duplicate_cols,
            keep="first"
        )

        print(
            f"Removed {before - len(df)} duplicates"
        )

    return (
        df
        .reset_index(drop=True)
    )


def process_pdf_folder(
    pdf_paths,
    constituency_name
):

    all_records = []

    booth_name = "Unknown"

    total_pdfs = len(pdf_paths)

    for idx, pdf_path in enumerate(
        pdf_paths,
        start=1
    ):

        print(
            f"\n📄 [{idx}/{total_pdfs}] Processing: "
            f"{pdf_path}"
        )

        start = time.time()

        records = extract_cards_from_pdf(
            pdf_path
        )

        print(
            f"⏱ OCR Time: "
            f"{time.time() - start:.2f} sec"
        )

        print(
            f"✅ Extracted "
            f"{len(records)} records"
        )

        for record in records:

            record["constituency"] = (
                constituency_name
            )

            record["booth"] = (
                booth_name
            )

        all_records.extend(
            records
        )

    df = pd.DataFrame(
        all_records
    )

    print(
        f"\n📊 Raw Records: {len(df)}"
    )

    if df.empty:

        df["धर्म"] = []

        df["विधानसभा"] = []

        return df

    df = clean_voter_data(df)

    print(
        f"📊 Clean Records: {len(df)}"
    )

    if "name" in df.columns:

        print(
            "🔍 Inferring Religion..."
        )

        df["धर्म"] = (
            df["name"]
            .apply(
                infer_religion_from_name
            )
        )

    else:

        df["धर्म"] = "Unknown"

    df["विधानसभा"] = (
        constituency_name
    )

    age_distribution = (
        df["age_group"]
        .value_counts()
        .reindex(
            AGE_ORDER,
            fill_value=0
        )
        .to_dict()
    )

    gender_distribution = (
        df["gender"]
        .value_counts()
        .to_dict()
        if "gender" in df.columns
        else {}
    )

    religion_distribution = (
        df["धर्म"]
        .value_counts()
        .to_dict()
    )

    print("\n📊 AGE DISTRIBUTION")
    print(age_distribution)

    print("\n📊 GENDER DISTRIBUTION")
    print(gender_distribution)

    print("\n📊 RELIGION DISTRIBUTION")
    print(religion_distribution)

    return df
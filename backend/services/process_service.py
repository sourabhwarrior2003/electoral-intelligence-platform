import pandas as pd

from modules.religion_infer import infer_religion_from_name
from modules.card_ocr import extract_cards_from_pdf


def age_group(age):

    if pd.isna(age):
        return "Unknown"

    age = int(age)

    if age <= 25:
        return "18-25"

    elif age <= 35:
        return "26-35"

    elif age <= 45:
        return "36-45"

    elif age <= 60:
        return "46-60"

    else:
        return "60+"


def clean_voter_data(df):

    df = df.copy()

    # Remove missing names
    if 'name' in df.columns:

        df = df[df['name'].notna()]

        df = df[
            df['name']
            .astype(str)
            .str.len() >= 2
        ]

    # Clean text columns
    for col in df.select_dtypes(include='object'):

        df[col] = (
            df[col]
            .fillna('')
            .astype(str)
            .str.strip()
        )

        df[col] = df[col].str.replace(
            r'\s+',
            ' ',
            regex=True
        )

    # Clean age
    if 'age' in df.columns:

        df['age'] = pd.to_numeric(
            df['age'],
            errors='coerce'
        )

        df = df[
            (df['age'].isna())
            |
            (
                (df['age'] >= 18)
                &
                (df['age'] <= 120)
            )
        ]

        df['age_group'] = (
            df['age']
            .apply(age_group)
        )

    else:

        df['age_group'] = "Unknown"

    # Remove duplicates
    duplicate_cols = []

    for col in [
        'name',
        'father_name',
        'age'
    ]:

        if col in df.columns:
            duplicate_cols.append(col)

    if duplicate_cols:

        df = df.drop_duplicates(
            subset=duplicate_cols,
            keep='first'
        )

    return df


def process_pdf_folder(
    pdf_paths,
    constituency_name
):

    all_records = []

    booth_name = "Unknown"

    for pdf_path in pdf_paths:

        print(
            f"\n📄 Processing: {pdf_path}"
        )

        records = extract_cards_from_pdf(
            pdf_path
        )

        print(
            f"✅ Extracted {len(records)} records"
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

    # Create DataFrame
    df = pd.DataFrame(
        all_records
    )

    print(
        f"\n📊 Raw Records: {len(df)}"
    )

    # Clean Data
    df = clean_voter_data(df)

    print(
        f"📊 Clean Records: {len(df)}"
    )

    # Religion
    if 'name' in df.columns:

        df['धर्म'] = (
            df['name']
            .apply(
                infer_religion_from_name
            )
        )

    else:

        df['धर्म'] = "Unknown"

    # Constituency
    df['विधानसभा'] = (
        constituency_name
    )

    # Statistics
    age_distribution = (
        df['age_group']
        .value_counts()
        .to_dict()
    )

    gender_distribution = (
        df['gender']
        .value_counts()
        .to_dict()
        if 'gender' in df.columns
        else {}
    )

    religion_distribution = (
        df['धर्म']
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
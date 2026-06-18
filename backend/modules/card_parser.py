import re


def parse_card_text(text):

    record = {}

    text = text.replace("\n", " ")

    voter_match = re.search(
        r'([A-Z]{3}\d{7})',
        text
    )

    if voter_match:
        record["voter_id"] = voter_match.group(1)

    name_match = re.search(
        r'निर्वाचक\s*का\s*नाम\s*[:;]?\s*(.*?)(?=(?:पिता|पति|पिला|प्रति|उम्र|गृह|फोटो))',
        text
    )

    if name_match:
        record["name"] = (
            name_match.group(1).strip()
        )

    father_match = re.search(
        r'(?:पिता|पति|पिला|प्रति)\s*का\s*नाम\s*[:;]?\s*(.*?)(?=(?:गृह|उम्र|फोटो))',
        text
    )

    if father_match:
        record["father_name"] = (
            father_match.group(1).strip()
        )

    age_match = re.search(
        r'उम्र\s*[:;]?\s*(\d+)',
        text
    )

    if age_match:

        age = int(
            age_match.group(1)
        )

        if 18 <= age <= 120:
            record["age"] = age

    gender_match = re.search(
        r'लिंग\s*[:;]?\s*(पुरुष|महिला)',
        text
    )

    if gender_match:
        record["gender"] = (
            gender_match.group(1)
        )

    return record
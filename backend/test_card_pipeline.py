from modules.card_ocr import extract_cards_from_pdf
import pandas as pd

pdf_path = input(
    "Enter PDF Path: "
).strip().replace('"', '')

records = extract_cards_from_pdf(
    pdf_path
)

# ADD THIS PART
df = pd.DataFrame(records)

df.to_csv(
    "debug_records.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nCSV Created: debug_records.csv"
)

print("\n")
print("=" * 60)
print(
    f"TOTAL RECORDS = {len(records)}"
)
print("=" * 60)

for rec in records[:10]:
    print(rec)
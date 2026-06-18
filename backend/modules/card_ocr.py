import fitz
import cv2
import pytesseract
import numpy as np
import pandas as pd
import os
from modules.card_parser import parse_card_text



def pdf_page_to_image(page, dpi=300):

    pix = page.get_pixmap(dpi=dpi)

    img = np.frombuffer(
        pix.samples,
        dtype=np.uint8
    ).reshape(
        pix.height,
        pix.width,
        pix.n
    )

    if pix.n == 4:
        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGRA2BGR
        )

    return img


def detect_voter_cards(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        15
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (5, 5)
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    boxes = []

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h

        if area > 50000 and w > 200 and h > 100:
            boxes.append((x, y, w, h))

    boxes = sorted(
        boxes,
        key=lambda b: (b[1], b[0])
    )

    return boxes


def ocr_card(card_img):

    gray = cv2.cvtColor(
        card_img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    text = pytesseract.image_to_string(
        gray,
        config="--oem 3 --psm 11 -l hin+eng"
    )

    return text.strip()


def main():

    pdf_path = input(
        "Enter PDF Path: "
    ).strip().replace('"', '')

    if not os.path.exists(pdf_path):
        print("PDF NOT FOUND")
        return

    doc = fitz.open(pdf_path)

    os.makedirs(
        "ocr_cards",
        exist_ok=True
    )

    rows = []

    total_cards = 0

    for page_no, page in enumerate(doc, start=1):

        print(f"\nProcessing Page {page_no}")

        image = pdf_page_to_image(page)

        boxes = detect_voter_cards(image)

        print(
            f"Cards Detected: {len(boxes)}"
        )

        for card_no, (x, y, w, h) in enumerate(boxes, start=1):

            card = image[
                y:y+h,
                x:x+w
            ]

            text = ocr_card(card)

            total_cards += 1

            txt_path = os.path.join(
                "ocr_cards",
                f"page_{page_no}_card_{card_no}.txt"
            )

            with open(
                txt_path,
                "w",
                encoding="utf-8"
            ) as f:
                f.write(text)

            rows.append(
                {
                    "page": page_no,
                    "card": card_no,
                    "chars": len(text)
                }
            )

            print(
                f"Page {page_no} Card {card_no} -> {len(text)} chars"
            )

    df = pd.DataFrame(rows)

    df.to_csv(
        "card_ocr_summary.csv",
        index=False
    )

    print("\n" + "=" * 60)
    print(
        f"TOTAL CARDS OCR'd = {total_cards}"
    )
    print("=" * 60)

    print(
        "\nCreated:"
    )
    print("card_ocr_summary.csv")
    print("ocr_cards folder")

def extract_cards_from_pdf(pdf_path):

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(pdf_path)

    doc = fitz.open(pdf_path)

    all_records = []

    for page_no, page in enumerate(doc, start=1):

        image = pdf_page_to_image(page)

        boxes = detect_voter_cards(image)

        print(
            f"Page {page_no} -> "
            f"{len(boxes)} cards"
        )

        for x, y, w, h in boxes:

            card = image[
                y:y+h,
                x:x+w
            ]

            text = ocr_card(card)

            if not text.strip():
                continue

            record = parse_card_text(text)

            if record:
                all_records.append(record)

    return all_records

if __name__ == "__main__":
    main()
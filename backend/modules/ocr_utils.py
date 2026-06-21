import fitz
import cv2
import pytesseract
import numpy as np
import os
from datetime import datetime


def log_message(message):
    log_dir = "backend/logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "ocr_log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")


def preprocess_image(img):
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def extract_text_from_image(img, page_number=None):

    processed = preprocess_image(img)

    os.makedirs(
        "backend/output",
        exist_ok=True
    )

    if page_number is not None:

        debug_path = (
            f"backend/output/"
            f"debug_page_{page_number}.jpg"
        )

        cv2.imwrite(
            debug_path,
            processed
        )

    # Improved OCR settings
    config = "--oem 3 --psm 11 -l hin+eng"

    text = pytesseract.image_to_string(
        processed,
        config=config
    )

    return text


def extract_text_from_pdf(pdf_path, max_pages=None):

    log_message(
        f"Started OCR on: {pdf_path}"
    )

    text_results = []

    try:

        pdf_doc = fitz.open(pdf_path)

        print("=" * 60)
        print(f"TOTAL PDF PAGES: {len(pdf_doc)}")
        print("=" * 60)

        for page_number, page in enumerate(
            pdf_doc,
            start=1
        ):

            if (
                max_pages is not None
                and page_number > max_pages
            ):
                break

            print(
                f"Processing Page {page_number}"
            )

            # Increased DPI
            pix = page.get_pixmap(
                dpi=200
            )

            img_data = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            )

            img = img_data.reshape(
                (
                    pix.height,
                    pix.width,
                    pix.n
                )
            )

            if pix.n == 4:

                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_BGRA2BGR
                )

            text = extract_text_from_image(
                img,
                page_number
            )

            print(
                f"Page {page_number} "
                f"Characters = {len(text)}"
            )

            if text.strip():

                log_message(
                    f"Extracted text from page {page_number}"
                )

            else:

                log_message(
                    f"No text on page {page_number}"
                )

            text_results.append(
                f"\n--- PAGE {page_number} ---\n{text}\n"
            )

        final_text = "\n".join(
            text_results
        )

        print("=" * 60)
        print(
            f"TOTAL OCR CHARACTERS: {len(final_text)}"
        )
        print("=" * 60)

        log_message(
            "OCR completed successfully."
        )

        return final_text

    except Exception as e:

        error_msg = str(e)

        print(
            f"OCR ERROR: {error_msg}"
        )

        log_message(
            f"Error during OCR: {error_msg}"
        )

        return ""


def perform_ocr(image_path):

    img = cv2.imread(
        image_path
    )

    if img is None:

        log_message(
            f"Failed to read image: {image_path}"
        )

        return ""

    return extract_text_from_image(img)
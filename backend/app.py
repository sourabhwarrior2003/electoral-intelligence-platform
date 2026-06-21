from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import traceback

from services.process_service import process_pdf_folder
from modules.map_visualizer import generate_religion_map

# ==========================
# PATHS
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = BASE_DIR
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "pdfs")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

os.makedirs(
    os.path.join(BACKEND_DIR, "logs"),
    exist_ok=True
)

# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    filename=os.path.join(
        BACKEND_DIR,
        "logs",
        "app.log"
    ),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# APP
# ==========================

app = Flask(__name__)
CORS(app)

# ==========================
# PROCESS PDF
# ==========================

@app.route('/api/process', methods=['POST'])
def process_constituency():

    constituency = request.form.get(
        "constituency"
    )

    files = request.files.getlist(
        "files"
    )

    if not files:

        return jsonify({
            "error": "No files uploaded"
        }), 400

    save_dir = os.path.join(
        UPLOAD_DIR,
        constituency
    )

    os.makedirs(
        save_dir,
        exist_ok=True
    )

    pdf_paths = []

    for file in files:

        path = os.path.join(
            save_dir,
            file.filename
        )

        file.save(path)

        pdf_paths.append(path)

    try:

        print("\n" + "=" * 60)
        print("STARTING PDF PROCESSING")
        print("=" * 60)

        df = process_pdf_folder(
            pdf_paths,
            constituency
        )

        print("STEP 1 : PROCESSING DONE")

        out_dir = os.path.join(
            OUTPUT_DIR,
            constituency
        )

        os.makedirs(
            out_dir,
            exist_ok=True
        )

        csv_path = os.path.join(
            out_dir,
            "booth_demography.csv"
        )

        df.to_csv(
            csv_path,
            index=False,
            encoding="utf-8-sig"
        )

        print("STEP 2 : CSV CREATED")

        generate_religion_map(
            df,
            out_dir
        )

        print("STEP 3 : MAP CREATED")

        # ======================
        # RELIGION DISTRIBUTION
        # ======================

        religion_distribution = {}

        if "धर्म" in df.columns:

            religion_distribution = (
                df["धर्म"]
                .value_counts()
                .to_dict()
            )

        # ======================
        # AGE DISTRIBUTION
        # ======================

        age_distribution = {}

        if "age_group" in df.columns:

            age_distribution = (
                df["age_group"]
                .value_counts()
                .to_dict()
            )

        # ======================
        # GENDER DISTRIBUTION
        # ======================

        gender_distribution = {}

        if "gender" in df.columns:

            gender_distribution = (
                df["gender"]
                .value_counts()
                .to_dict()
            )

        print("\nReligion Distribution")
        print(religion_distribution)

        print("\nAge Distribution")
        print(age_distribution)

        print("\nGender Distribution")
        print(gender_distribution)

        print("\nSTEP 4 : RETURNING RESPONSE")

        return jsonify({

            "message":
                f"Processed {len(pdf_paths)} PDFs",

            "constituency":
                constituency,

            "booths":
                len(pdf_paths),

            "total_voters":
                len(df),

            "religion_distribution":
                religion_distribution,

            "age_distribution":
                age_distribution,

            "gender_distribution":
                gender_distribution,

            "csv_url":
                f"http://localhost:5000/output/{constituency}/booth_demography.csv",

            "map_url":
                f"http://localhost:5000/output/{constituency}/religion_map.html"
        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500


# ==========================
# SERVE FILES
# ==========================

@app.route(
    '/output/<constituency>/<filename>'
)
def serve_output(
    constituency,
    filename
):

    return send_from_directory(
        os.path.join(
            OUTPUT_DIR,
            constituency
        ),
        filename
    )


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    
    if __name__ == "__main__":

     import multiprocessing

    multiprocessing.freeze_support()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
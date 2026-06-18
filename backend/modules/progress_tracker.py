import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROGRESS_FILE = os.path.join(
    BASE_DIR,
    "progress.json"
)

def update_progress(
    current_page,
    total_pages,
    status
):

    data = {
        "current_page": current_page,
        "total_pages": total_pages,
        "status": status
    }

    with open(
        PROGRESS_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f
        )


def get_progress():

    if not os.path.exists(
        PROGRESS_FILE
    ):

        return {
            "current_page": 0,
            "total_pages": 0,
            "status": "Idle"
        }

    with open(
        PROGRESS_FILE,
        "r"
    ) as f:

        return json.load(f)
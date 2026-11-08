
from fastapi import FastAPI, Path, HTTPException ,Query
import json

a = FastAPI()


def load_json():
    with open("patient.json", "r") as f:
        return json.load(f)


@a.get("/")
def hello():
    return {"message": "Hello World"}


@a.get("/math")
def math():
    return 3.14 * 392 * 829 + 92902992 - 929


@a.get("/view")
def view():
    return load_json()


@a.get("/patient/{patient_id}")
def patient(
    patient_id: str = Path(
        ...,
        description="Enter the patient ID",
        examples=["P001"],
        min_length=4,
        max_length=4,
        pattern=r"^[A-Z][0-9]{3}$"
    )
):
    d = load_json()

    if patient_id in d:
        return d[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )



@a.get("/sort")
def sort(
    sort_by: str = Query(..., description="Sort by height, weight, or bmi"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Choose asc or desc"
        )

    d = load_json()

    try:
        sorted_data = sorted(
            d.values(),
            key=lambda x: float(x[sort_by]),
            reverse=(order == "desc")
        )
        return sorted_data

    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail=f"Patient data has a missing or invalid '{sort_by}' value"
        )

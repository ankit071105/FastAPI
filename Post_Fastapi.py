
from fastapi import FastAPI, HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

a = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Patient ID", examples=["P001"])]
    name: Annotated[str, Field(..., description="Patient Name", examples=["Ankit"])]
    city: Annotated[str, Field(..., description="Patient City", examples=["Delhi"])]
    age: Annotated[int, Field(..., gt=0, lt=120)]
    gender: Annotated[Literal["Male", "Female", "Others"], Field(...)]
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg")]

    # Calculate BMI
    @computed_field
    @property
    def bmi(self) -> float:
        h=self.height
        height = h / 100 if h > 3 else h
        return round(self.weight / (height ** 2), 2)

    # Calculate BMI verdict
    @computed_field
    @property
    def verdict(self) -> str:
        b = self.bmi

        if b < 18.5:
            return "Underweight"
        elif b < 25:
            return "Normal weight"
        elif b < 30:
            return "Overweight"
        else:
            return "Obesity"


# Load JSON data
def load_json():
    with open("patient.json", "r") as f:
        return json.load(f)


# Save JSON data
def save_json(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# Create Patient API
@a.post("/create", status_code=201)
def create_patient(patient: Patient):

    data = load_json()

    # Check duplicate ID
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient ID already exists"
        )

    # Add patient with BMI and verdict
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Save data
    save_json(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient created successfully"}
    )

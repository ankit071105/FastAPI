
from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
import os
import tempfile

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr, HttpUrl
from typing import Optional, Literal

a = FastAPI()


# Main Patient Model
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int = Field(gt=0, lt=120)
    gender: Literal["male", "female", "Male", "Female", "Others"]
    height: float = Field(gt=0, description="Height in meters or cm")
    weight: float = Field(gt=0, description="Weight in kg")

    email: Optional[EmailStr] = None
    linkedin_url: Optional[HttpUrl] = None

    @computed_field
    @property
    def bmi(self) -> float:
        h = self.height / 100 if self.height > 3 else self.height
        return round(self.weight / (h ** 2), 2)

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
            return "Obese"


# Update Model
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[Literal["male", "female", "Male", "Female", "Others"]] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    email: Optional[EmailStr] = None
    linkedin_url: Optional[HttpUrl] = None


# JSON File Path
FILE = Path(__file__).parent / "patient.json"


# Load JSON
def load_data():
    if not FILE.exists() or FILE.stat().st_size == 0:
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid patient.json at line {e.lineno}, column {e.colno}"
        )


# Save JSON safely
def save_data(data):
    temp_file = FILE.with_suffix(".tmp")

    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4, default=str)

    os.replace(temp_file, FILE)


@a.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
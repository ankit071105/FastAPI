# FastAPI

A hands-on Python project for learning **FastAPI** , **Pydantic** , **Docker**. It
contains introductory API routes, JSON-based patient data handling,
request/path/query parameter validation, sorting, and Pydantic model
validation examples.

## Tech Stack

-   **Python 3.11+**
-   **FastAPI** -- building REST API endpoints
-   **Uvicorn** -- running the ASGI application
-   **Pydantic** -- data parsing and validation
-   **JSON** -- sample data storage

## Repository Structure

``` text
FastAPI/
├── Pydantic/          # Pydantic learning examples
├── basic.py           # FastAPI application and API routes
├── patient.json       # Sample patient records used by the API
├── data.json          # Sample JSON data
└── README.md
```

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/ankit071105/FastAPI.git
cd FastAPI
```

### 2. Create a virtual environment

Using Python 3.11:

``` bash
python3.11 -m venv myenv
```

Activate it on macOS/Linux:

``` bash
source myenv/bin/activate
```

On Windows:

``` powershell
myenv\Scripts\activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn "pydantic[email]"
```

`email-validator` is installed through the `pydantic[email]` extra and
is needed when using Pydantic's `EmailStr` type.

### 4. Run the FastAPI application

The FastAPI instance in `basic.py` is named `a`. Start it with:

``` bash
uvicorn basic:a --reload
```

Open the API at:

-   Application: http://127.0.0.1:8000
-   Interactive Swagger documentation: http://127.0.0.1:8000/docs
-   ReDoc documentation: http://127.0.0.1:8000/redoc

> Run the command from the repository root so that `patient.json` can be
> found using the relative path in the application.

## Available API Endpoints

The following routes are implemented in `basic.py`:

  ----------------------------------------------------------------------------------
  Method                  Endpoint                           Description
  ----------------------- ---------------------------------- -----------------------
  `GET`                   `/`                                Returns a Hello World
                                                             message.

  `GET`                   `/math`                            Returns the result of a
                                                             sample arithmetic
                                                             expression.

  `GET`                   `/view`                            Returns the patient
                                                             data loaded from
                                                             `patient.json`.

  `GET`                   `/patient/{patient_id}`            Fetches a patient by
                                                             ID. The ID is validated
                                                             (for example, `P001`).
                                                             Returns 404 if the
                                                             patient is not found.

  `GET`                   `/sort?sort_by=height&order=asc`   Sorts patient records
                                                             by `height`, `weight`,
                                                             or `bmi`, in ascending
                                                             or descending order.
  ----------------------------------------------------------------------------------

### Example requests

``` text
GET http://127.0.0.1:8000/
GET http://127.0.0.1:8000/view
GET http://127.0.0.1:8000/patient/P001
GET http://127.0.0.1:8000/sort?sort_by=height&order=asc
```

The `/sort` endpoint accepts `sort_by` values `height`, `weight`, or
`bmi`. The `order` parameter accepts `asc` or `desc` and defaults to
`asc`.

## Pydantic Concepts Practiced

The Pydantic examples cover common data validation concepts, including:

-   `BaseModel` for defining structured data models.
-   Required fields and default values.
-   `EmailStr` for email validation.
-   `Optional` fields and `None` defaults.
-   `List` and `Dict` type annotations.
-   Automatic conversion of compatible input values (for example, a
    numeric string to an integer).
-   Validation errors when input data does not match the model.

Example model:

``` python
from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    marry: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]
```

## Learning Goals

-   Understand how to create API routes using FastAPI.
-   Work with path and query parameters.
-   Validate input values and handle HTTP errors.
-   Read structured data from JSON files.
-   Define and validate data models with Pydantic.
-   Run and test an API locally using Uvicorn and the interactive API
    documentation.

## Notes

-   This repository is a learning/practice project; the patient records
    are sample data.
-   The current API reads patient records from a local JSON file. It
    does not use a database.
-   Keep the virtual environment active when installing dependencies and
    running the application.

## Author

**Ankit Kumar**

-   GitHub: [@ankit071105](https://github.com/ankit071105)
-   Repository: [FastAPI](https://github.com/ankit071105/FastAPI)

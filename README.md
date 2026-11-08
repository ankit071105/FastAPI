# FastAPI

A hands-on Python project for learning **FastAPI** and **Pydantic** — from basic routes to a full CRUD patient API backed by a JSON file, and finally serving a trained **scikit-learn** model behind a `/predict` endpoint with a **Streamlit** frontend.

## Tech Stack

- **Python 3.11+**
- **FastAPI** — REST API endpoints
- **Uvicorn** — ASGI server
- **Pydantic v2** — validation, `Field` constraints, `computed_field`, custom validators
- **scikit-learn + pandas** — insurance premium category model (`RandomForestClassifier` pipeline)
- **Streamlit** — simple frontend for the ML API
- **JSON** — file-based storage for patient records

## Repository Structure

```text
FastAPI/
├── Get_Fastapi.py        # GET routes: hello, view, patient by ID, sort
├── Post_Fastapi.py       # POST /create — add a patient (auto BMI + verdict)
├── Put_FastAPI.py        # PUT /edit/{id} — partial update with re-validation
├── Delete_FastAPI.py     # DELETE /delete/{id}
├── patient.json          # Sample patient records
├── data.json             # Sample JSON data
├── Fastapi.pdf           # Notes
├── Pydantic/
│   ├── main.py           # field_validator, model_validator, computed_field, EmailStr, AnyUrl
│   ├── nested.py         # Nested models
│   └── export.py         # model_dump / model_dump_json with include/exclude
└── ml/
    ├── main.py           # Complete Patient Management API (all CRUD in one app)
    ├── ml.py             # Insurance premium prediction API (POST /predict)
    ├── frontend.py       # Streamlit UI for /predict
    ├── fastapi_ml_model.ipynb  # Model training notebook
    ├── model.pkl         # Trained sklearn pipeline
    └── patient.json      # Data used by ml/main.py
```

## Getting Started

### 1. Clone

```bash
git clone https://github.com/ankit071105/FastAPI.git
cd FastAPI
```

### 2. Virtual environment

```bash
python3.11 -m venv myenv
source myenv/bin/activate        # macOS/Linux
myenv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn "pydantic[email]" pandas scikit-learn streamlit requests
```

> `pydantic[email]` installs `email-validator`, needed for `EmailStr`.
> `model.pkl` is a pickled sklearn pipeline — if loading fails, install a scikit-learn version close to the one used in the notebook, or re-run the notebook to regenerate it.

## Running the Apps

Every learning file is a separate FastAPI app. Run from the folder that contains the file so `patient.json` is found.

| File | Command (from) | App instance |
|---|---|---|
| `Get_Fastapi.py` | `uvicorn Get_Fastapi:a --reload` (root) | `a` |
| `Post_Fastapi.py` | `uvicorn Post_Fastapi:a --reload` (root) | `a` |
| `Put_FastAPI.py` | `uvicorn Put_FastAPI:a --reload` (root) | `a` |
| `Delete_FastAPI.py` | `uvicorn Delete_FastAPI:a --reload` (root) | `a` |
| `ml/main.py` | `cd ml && uvicorn main:app --reload` | `app` |
| `ml/ml.py` | `cd ml && uvicorn ml:app --reload` | `app` |

Docs: http://127.0.0.1:8000/docs (Swagger) · http://127.0.0.1:8000/redoc

## API Endpoints

### Patient API (root files)

| Method | Endpoint | File | Description |
|---|---|---|---|
| `GET` | `/` | Get | Hello World |
| `GET` | `/math` | Get | Sample arithmetic result |
| `GET` | `/view` | Get | All patients from `patient.json` |
| `GET` | `/patient/{patient_id}` | Get | Patient by ID — validated with regex `^[A-Z][0-9]{3}$` (e.g. `P001`); 404 if missing |
| `GET` | `/sort?sort_by=bmi&order=desc` | Get | Sort by `height` / `weight` / `bmi`, `asc` (default) or `desc`; 400 on invalid input |
| `POST` | `/create` | Post | Create patient; 400 on duplicate ID |
| `PUT` | `/edit/{patient_id}` | Put | Partial update (`exclude_unset`), BMI + verdict recalculated, atomic file save |
| `DELETE` | `/delete/{patient_id}` | Delete | Delete patient; 404 if missing |

`ml/main.py` contains all of the above (`/`, `/about`, `/view`, `/patient/{id}`, `/sort`, `/create`, `/edit/{id}`, `/delete/{id}`) in a single app.

**Create request example:**

```json
POST /create
{
  "id": "P006",
  "name": "Ankit",
  "city": "Delhi",
  "age": 22,
  "gender": "Male",
  "height": 1.72,
  "weight": 68
}
```

`bmi` and `verdict` (Underweight / Normal weight / Overweight / Obese) are computed automatically with `@computed_field`. Height accepts metres or centimetres (values > 3 are treated as cm) in `Post_Fastapi.py`, `Put_FastAPI.py` and `Delete_FastAPI.py`.

### ML Prediction API (`ml/ml.py`)

`POST /predict` — predicts an insurance premium category.

```json
{
  "age": 30,
  "weight": 65,
  "height": 1.7,
  "income_lpa": 10,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Response:

```json
{ "predicted_category": "Low" }
```

Features engineered inside the Pydantic model before prediction:

- `bmi` — weight / height²
- `age_group` — young / adult / middle_aged / senior
- `lifestyle_risk` — low / medium / high (smoker + BMI)
- `city_tier` — 1 / 2 / 3 from built-in city lists

`occupation` must be one of: `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`.

### Streamlit Frontend

```bash
# terminal 1
cd ml && uvicorn ml:app --reload
# terminal 2
cd ml && streamlit run frontend.py
```

## Pydantic Concepts Practiced

- `BaseModel`, required fields, defaults, `Optional`
- `Annotated` + `Field` constraints (`gt`, `lt`, `min_length`, `max_length`, `strict`)
- `Literal` for fixed choices
- `EmailStr`, `AnyUrl`, `HttpUrl`
- `@field_validator` (before/after mode) and `@model_validator`
- `@computed_field` for derived values (BMI, verdict, age group, city tier)
- Nested models
- `model_dump()` / `model_dump_json()` with `include`, `exclude`, `exclude_unset`
- Type coercion (e.g. `"true"` → `True`)

## Known Issues / TODO

- `ml/frontend.py` expects a `response` key with `confidence` and `class_probabilities`, but `ml/ml.py` returns only `{"predicted_category": ...}` — the UI will show an API error until one side is updated.
- In `Pydantic/main.py`, the email validator *allows only* `hdfc.com`, `sbi.com`, `icici.com`, but the error message says the opposite.
- `ml/main.py` maps BMI 25–30 to `"Normal"` instead of `"Overweight"`.
- `Post_Fastapi.py` sets `status_code=201` on the route but returns a `JSONResponse` with 200.
- Storage is a local JSON file — no database, not safe for concurrent writes.

## Learning Goals

- Build REST APIs with FastAPI (GET, POST, PUT, DELETE)
- Use path and query parameters with validation
- Handle errors with `HTTPException`
- Validate and transform data with Pydantic
- Serve an ML model through an API and consume it from a frontend

## Author

**Ankit Kumar**

- GitHub: [@ankit071105](https://github.com/ankit071105)
- Repository: [FastAPI](https://github.com/ankit071105/FastAPI)

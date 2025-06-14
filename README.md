# Take-home Assignment: Virtual Dermatology Clinic API

This application API book appointments with providers, matching patients based on states and insurances. If a patient doesn't exist on the DB, it is created.

## Getting Started

### Prerequisites
- Python 3.12
- Poetry

### Setup
1. Configure Python 3.12 and Poetry
2. Install dependencies:
```
poetry install
```
3. Initialize the DB with the sample data. Note that running populate will destroy the DB and create it again.
```
poetry run populate
```
4. To query the DB:
```
poetry run query
```

## Running the server
Start the server with:
```
poetry run server
```
This will run the Flask application on `http://0.0.0.0:5001`.


## Testing with the service

### POST /appointment
You can use curl to schedule an appointment for a patient.

**Request Body:**
```
curl -X POST http://0.0.0.0:5001/appointment -H "Content-Type: application/json" -d '{
  "patient": {
    "first_name": "Pearl",
    "last_name": "Jam",
    "email": "pearl.jam@example.com",
    "state": "MA",
    "insurance": "Blue Cross"
  }
}
```

**Response:**
```
{
  "patient": "Pearl Jam",
  "scheduled": true,
  "appointment_id": <UUID>,
  "provider": "Dr. Cheryl Crow",
  "time": <datetime>
}
```

### Patient
- `id`: UUID primary key
- `first_name`: Patient's first name
- `last_name`: Patient's last name
- `email`: Patient's email address
- `state`: Two-letter state code
- `insurance`: Insurance provider name

### Provider
- `id`: UUID primary key
- `title`: Provider title (default: "Dr.")
- `first_name`: Provider's first name
- `last_name`: Provider's last name
- `states`: Many-to-many relationship with states where provider is licensed
- `insurances`: Many-to-many relationship with accepted insurance providers

### Appointment
- `id`: UUID primary key
- `provider_id`: Foreign key to Provider
- `patient_id`: Foreign key to Patient
- `insurance_id`: Foreign key to Insurance
- `time`: Appointment datetime

### State
- `id`: UUID primary key
- `state`: Two-letter state code

### Insurance
- `id`: UUID primary key
- `name`: Insurance provider name

## Running Tests
Run the test suite with:
```
poetry run pytest
```

For more verbose output:
```
poetry run pytest -v
```

To run a specific test file:
```
poetry run pytest tests/test_appointment_creation.py
```

## Project Structure
```
├── app.py                     # Main application entry point
├── instance/                  # Configuration files
├── scripts.py                 # CLI commands
├── takehome_api/              # API implementation
│   ├── src/
│       ├── config/            # Application configuration
│       ├── core/              # Business logic
│       ├── models/            # Data models
│       └── main.py            # API routes
└── tests/                     # Test suite
```

## Project Architecture

### Database

As was already present, the app uses SQLAlchemy. `modely.py` has the DB models including a many-to-many relationship between providers and states and providers and insurances.

### Application logic & testing

- `core.py` contains the main application logic, including the appointment scheduling logic. It also contains the logic for matching patients to providers based on states and insurances.
- Pytest is used for testing. `test_appointment_creation.py` tests the appointment creation logic. It writes directly to the DB; not a scalable approach
- Added `populate` and `query` commands to `scripts.py` and `pyproject.toml`
- Added Pydantic response models in `response_model.py`. That allows validation of the data, separates the concern from the database, and allows for easily serializing to JSON
- The scheduling logic is based on the first available appointment in the appointment table. If there is no patient ID populated, then the appointment is available

### For scalability and maintainability
- There is no logic for preferred appointment times - currently, first available appointment is scheduled
- Not accounting for multiple requests for the same patient, provider, or appointment times. Obviously, an RDBMS like postgresql has transactions and would lock, but it is a workflow that would have to be considered
- As mentioned, the Pytest tests write directly to the DB
- There could be a bit better structure to the code including the DB models
- The latest version of SQLAlchemy uses mapped_column instead of Column (see https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column). It provides better type compatibility with Python, provides the same ORM as `Column` but with a more pythonic syntax, and seems to be more inline, in terms of standards, with a library like `SQLModel` 
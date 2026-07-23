# Backend

This document covers the application side of IntelliDoc, including the backend architecture, document extraction pipeline, AI integration, database design, frontend implementation, and the development workflow followed before deploying to AWS.

---

# Application Overview

Before introducing any cloud infrastructure, the application was designed and validated locally. The goal was to ensure that the core document-processing logic worked reliably before adding the complexity of Docker, ECS, Lambda, and other AWS services.

> **Screenshot:** IntelliDoc Homepage


![Homepage](../screenshots/homepage.png)

This approach made it much easier to isolate infrastructure-related issues later in the project because the application logic had already been thoroughly tested.

---

# Development Approach

The application was built incrementally, with each stage fully working before moving to the next.

## Stage 1 — Core Processing Logic

The project began with two standalone Python functions:

* `extract_text()`
* `analyze_with_gemini()`

These functions were tested directly using sample PDF and DOCX documents without any web framework.

At this stage, the focus was purely on proving that document extraction and AI summarization worked correctly.

---

## Stage 2 — FastAPI Integration

Once the core logic was stable, FastAPI was introduced to expose the functionality through REST endpoints.

The upload endpoint simply called the same extraction and analysis functions that had already been tested locally.

---

## Stage 3 — PostgreSQL Persistence

Database support was added using SQLAlchemy and PostgreSQL.

Instead of returning AI results directly, processed documents were stored inside a database and made retrievable through a dedicated API endpoint.

---

## Stage 4 — Dockerization

After the backend was functioning correctly, the application was containerized using Docker.

This ensured that development and deployment environments behaved consistently.

---

# Backend Architecture

The application is built with **FastAPI**, running through **Uvicorn**.

The backend is responsible for:

* Receiving uploaded documents
* Extracting document text
* Sending extracted text to Gemini
* Persisting processed results
* Returning stored documents through the API
* Serving the frontend

The overall request flow is illustrated below.

> **Screenshot:** Upload Workflow


![Upload Workflow](../screenshots/homepage.png)


---

# API Endpoints

| Method | Endpoint          | Description                                                                       |
| ------ | ----------------- | --------------------------------------------------------------------------------- |
| POST   | `/upload`         | Uploads a document, extracts text, analyzes it with Gemini, and stores the result |
| GET    | `/documents/{id}` | Retrieves a processed document                                                    |
| GET    | `/health`         | Health check endpoint                                                             |
| GET    | `/`               | Serves the frontend                                                               |

---

# Document Extraction (`extraction.py`)

Document extraction supports both PDF and Microsoft Word documents.

Supported formats:

* PDF (`pypdf`)
* DOCX (`python-docx`)

Each document type has its own extraction function.

If no readable text is found (for example, image-only PDFs), the extraction layer raises a `ValueError`, allowing the API to return a meaningful **400 Bad Request** instead of crashing.

This separation keeps the extraction logic independent from the API layer.

---

# AI Analysis (`analysis.py`)

After extraction, document text is sent to the Google Gemini API for analysis.

The prompt instructs the model to return structured JSON containing:

* Summary
* Key points
* Document type

A defensive cleanup step removes markdown code fences before parsing the response with `json.loads()`.

Malformed responses raise a clear exception rather than failing silently.

To avoid unnecessarily large requests, extracted text is truncated to approximately **15,000 characters** before being sent to Gemini.

> **Screenshot:** Analysis Result


![Analysis Result](../screenshots/file-analysis.png)


---

# AI Service Decision

The original design targeted **Amazon Bedrock** because of its native AWS integration.

However, during development the available foundation models exceeded the project's free-tier budget.

Rather than tightly coupling the application to a single provider, the AI layer was designed to remain modular.

Google Gemini was adopted for the initial implementation, making it possible to migrate back to Amazon Bedrock in the future with minimal application changes.

---

# Database (`database.py`)

SQLAlchemy is used as the ORM with PostgreSQL as the backing database.

The application stores processed document information in a single table.

```text
documents
├── id
├── filename
├── status
├── result (JSON)
└── created_at
```

`init_db()` creates the required tables during application startup if they do not already exist.

> **Screenshot:** Documents Table


![Database Table](../screenshots/postgres.png)


---

# Notable Backend Challenge

During development, a `DetachedInstanceError` occurred when attempting to access SQLAlchemy model attributes after closing the database session.

The issue was resolved by copying the required values into a standard Python dictionary before closing the session.

This reinforced the importance of understanding SQLAlchemy's session lifecycle when designing backend applications.

---

# Frontend

The user interface was initially developed using **Streamlit**.

Although functional, Streamlit's styling limitations made it difficult to achieve the desired interface, and extensive CSS customization became increasingly difficult to maintain.

The frontend was therefore rebuilt using:

* HTML
* CSS
* Vanilla JavaScript

The static files are served directly by FastAPI using `StaticFiles`, allowing both the frontend and backend to run from a single application.

> **Screenshot:** Homepage


![Homepage](../screenshots/homepage.png)


---

# Deployment Bug

One deployment issue occurred after moving from local development to AWS.

The frontend originally contained the following configuration:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

While this worked locally, browsers attempted to contact their own localhost after deployment, causing every upload request to fail.

The issue was resolved by replacing the hardcoded URL with a relative path:

```javascript
const API_URL = "";
```

This allows the frontend to automatically communicate with whichever server is hosting the application.

---

# Local Development Workflow

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure the environment variables:

```env
GEMINI_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/intellidoc
```

Run the application:

```bash
uvicorn main:app --reload
```

Test the API:

```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@sample.pdf"

curl "http://127.0.0.1:8000/documents/<id>"
```

---

# Testing

The backend was tested throughout development using:

* FastAPI interactive documentation
* cURL
* Postman
* Sample PDF documents
* Sample DOCX documents

Testing included:

* Valid uploads
* Empty documents
* Unsupported file types
* Missing text
* Database persistence
* API response validation

---

# Summary

The backend was intentionally developed in small, verifiable stages before any cloud infrastructure was introduced. This approach ensured that the application's core logic remained stable while infrastructure evolved independently. The result is a modular backend capable of extracting document text, generating AI-powered summaries, persisting results in PostgreSQL, and serving a lightweight frontend through a single FastAPI application.

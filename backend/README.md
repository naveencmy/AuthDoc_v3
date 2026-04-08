## AuthDoc- Backend File structure of the prototype
AuthDoc/
├── backend/
│   ├── node/
│   │   ├── package.json
│   │   ├── nodemon.json
│   │   ├── uploads/
│   │   └── src/
│   │       ├── app.js
│   │       ├── server.js
│   │       ├── config/
│   │       │   └── policies.json
│   │       ├── middleware/
│   │       │   └── upload.middleware.js
│   │       ├── routes/
│   │       │   └── verify.routes.js
│   │       ├── controllers/
│   │       │   └── verify.controller.js
│   │       ├── services/
│   │       │   ├── pythonClient.js
│   │       │   └── verifier.service.js
│   │       ├── store/
│   │       │   └── documentStore.js
│   │       └── utils/
│   │           └── status.util.js
│   │
│   └── python/
│       ├── main.py
│       ├── extractor.py
│       └── requirements.txt
│
└── README.md

 # workflow of the AuthDoc:
 Frontend
   |
   |  (file upload)
   v
Node.js (Express)  ───────────────►  Python (FastAPI)
   |                                      |
   |  verification + policies             |  OCR + extraction
   |                                      |
   |◄──────── extracted JSON ─────────────|
# Service Sturcture of the ML(python-FastAPI):
ocr_service/
├── main.py
├── extractor.py
├── requirements.txt
   ## Requirements:
      fastapi
      uvicorn
      paddleocr
      paddlepaddle
      python-multipart
      opencv-python
README for Frontend + DevOps (Production-Grade)

## 📘 AuthDoc Backend — API & Architecture Guide
Overview

AuthDoc is a verification-first document intelligence backend designed to:

Extract academic data from documents using OCR

Verify extracted data using configurable rule policies

Return explainable, field-level verification results

The backend acts as the single source of truth.
The frontend is a visualization layer only.

## 🧱 Architecture
Frontend
   ↓
Node.js (Express) — API, policies, verification
   ↓
Python (FastAPI) — OCR & field extraction

# Responsibilities
Service	Responsibility
Node.js	API orchestration, rule engine, policies, batch logic
Python	OCR + text parsing only
Frontend	Upload files, display results

OCR output is treated as untrusted candidate data.

# 🚀 Running the Services
Python OCR Service
cd backend/python
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000


# Runs at:

http://127.0.0.1:8000

Node.js Backend
cd backend/node
npm install
npm run dev


# Runs at:

http://localhost:3000

### 🔌 API Endpoints
## 1️⃣ Ingest Document

Uploads a document and triggers OCR extraction.

Endpoint

POST /api/ingest


Request

multipart/form-data

Key: file (PDF / JPG / PNG)

Response

{
  "document_id": "uuid"
}


The document is OCR-processed and stored temporarily in memory.

## 2️⃣ Single Document Verification

Endpoint

POST /api/verify


Request

{
  "document_id": "uuid",
  "policy_id": "strict | lenient"
}


Response

{
  "document_id": "uuid",
  "results": {
    "gpa": {
      "value": 8.691,
      "status": "VERIFIED",
      "reason": "Within allowed range"
    },
    "cgpa": {
      "value": 8.601,
      "status": "VERIFIED",
      "reason": "Difference acceptable"
    },
    "result_status": {
      "value": null,
      "status": "VERIFIED",
      "reason": "Dependency satisfied"
    }
  }
}


VERIFIED ≠ correctness, it means passes verification rules

MISSING is explicitly returned when data is not extracted

## 3️⃣ Batch Verification

Endpoint

POST /api/verify/batch


Request

{
  "policy_id": "strict",
  "document_ids": ["uuid1", "uuid2"]
}


Response

{
  "candidates": [
    {
      "document_id": "uuid1",
      "overall_status": "VERIFIED",
      "fields": {
        "gpa": "VERIFIED",
        "cgpa": "FLAGGED",
        "result_status": "VERIFIED"
      }
    }
  ]
}


Batch responses:

Do NOT include values

Do NOT include reasons

Intended for dashboards and bulk views

## 🧾 Policy Configuration

Policies are defined in:

backend/node/src/config/policies.json


Example:

{
  "strict": {
    "required_fields": ["gpa", "cgpa", "result_status"],
    "rules": [
      { "type": "range", "field": "gpa", "min": 0, "max": 10 },
      { "type": "delta", "field": "cgpa", "compare_with": "gpa", "max_diff": 1.0 },
      { "type": "dependency", "field": "result_status", "depends_on": "subject_grades" }
    ]
  }
}


Rules are configuration-driven, not hard-coded.

## 🛡️ Design Guarantees

OCR output is treated as untrusted

Missing data is never guessed

All verification decisions are explainable

System never crashes on OCR failure

Supports multi-policy organizations

## 📈 Scalability Note

This prototype processes documents synchronously and stores extracted data in memory.
It can be extended to async batch pipelines and persistent storage in production.

## 📎 Notes for Frontend Developers

Always store document_id after upload

Do not compute verification logic in frontend

Frontend should treat status as authoritative

FLAGGED ≠ rejected — it requires review

## 📎 Notes for DevOps

Python and Node services are independent

OCR service must be reachable from Node

Temporary files are stored in OS temp directory

No database required for prototype



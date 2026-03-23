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





INFO:     Started server process [94686]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
[2026/03/09 20:36:20] ppocr DEBUG: dt_boxes num : 81, elapse : 0.21746540069580078
[2026/03/09 20:36:21] ppocr DEBUG: cls num  : 81, elapse : 0.09464526176452637
[2026/03/09 20:36:23] ppocr DEBUG: rec_res num  : 81, elapse : 2.5349879264831543
[{'text': '....', 'confidence': 0.5276982188224792, 'bbox': [[654.0, 600.0], [895.0, 600.0], [895.0, 669.0], [654.0, 669.0]], 'x': 654.0, 'y': 600.0, 'width': 241.0, 'height': 69.0}, {'text': 'Lan mil neuf cent et un, le...akgkaeea.', 'confidence': 0.8051076531410217, 'bbox': [[1451.0, 724.0], [3006.0, 757.0], [3004.0, 844.0], [1450.0, 812.0]], 'x': 1450.0, 'y': 724.0, 'width': 1556.0, 'height': 120.0}, {'text': 'MARIAGE', 'confidence': 0.7858848571777344, 'bbox': [[741.0, 775.0], [1154.0, 775.0], [1154.0, 862.0], [741.0, 862.0]], 'x': 741.0, 'y': 775.0, 'width': 413.0, 'height': 87.0}, {'text': 'jour du mois', 'confidence': 0.9898500442504883, 'bbox': [[3542.0, 775.0], [3956.0, 775.0], [3956.0, 844.0], [3542.0, 844.0]], 'x': 3542.0, 'y': 775.0, 'width': 414.0, 'height': 69.0}, {'text': 'a...a....heres..a....ee...par eoant nous', 'confidence': 0.5212873816490173, 'bbox': [[2167.0, 849.0], [3969.0, 882.0], [3967.0, 969.0], [2166.0, 937.0]], 'x': 2166.0, 'y': 849.0, 'width': 1803.0, 'height': 120.0}, {'text': '1', 'confidence': 0.640700101852417, 'bbox': [[1407.0, 869.0], [1463.0, 869.0], [1463.0, 906.0], [1407.0, 906.0]], 'x': 1407.0, 'y': 869.0, 'width': 56.0, 'height': 37.0}, {'text': "auugashOfcier public de l' Etat-Civil de la", 'confidence': 0.919245719909668, 'bbox': [[2241.0, 968.0], [3956.0, 988.0], [3955.0, 1075.0], [2240.0, 1056.0]], 'x': 2240.0, 'y': 968.0, 'width': 1716.0, 'height': 107.0}, {'text': 'D.CLLL', 'confidence': 0.5145284533500671, 'bbox': [[926.0, 1012.0], [1222.0, 1012.0], [1222.0, 1081.0], [926.0, 1081.0]], 'x': 926.0, 'y': 1012.0, 'width': 296.0, 'height': 69.0}, {'text': 'Commune de', 'confidence': 0.9133532643318176, 'bbox': [[1395.0, 1075.0], [1765.0, 1075.0], [1765.0, 1138.0], [1395.0, 1138.0]], 'x': 1395.0, 'y': 1075.0, 'width': 370.0, 'height': 63.0}, {'text': 'ta.Arrondissement judiciaire de Liege, Province', 'confidence': 0.9300803542137146, 'bbox': [[2414.0, 1074.0], [3956.0, 1107.0], [3955.0, 1194.0], [2412.0, 1162.0]], 'x': 2412.0, 'y': 1074.0, 'width': 1544.0, 'height': 120.0}, {'text': '....', 'confidence': 0.5479162931442261, 'bbox': [[1993.0, 1088.0], [2333.0, 1088.0], [2333.0, 1156.0], [1993.0, 1156.0]], 'x': 1993.0, 'y': 1088.0, 'width': 340.0, 'height': 68.0}, {'text': 'J.Ant.a', 'confidence': 0.5193819403648376, 'bbox': [[558.0, 1105.0], [1106.0, 1126.0], [1102.0, 1239.0], [554.0, 1217.0]], 'x': 554.0, 'y': 1105.0, 'width': 552.0, 'height': 134.0}, {'text': ' de Liége, ont comparu publiquement en notre Maison commune....', 'confidence': 0.9695428609848022, 'bbox': [[1353.0, 1162.0], [3352.0, 1194.0], [3350.0, 1301.0], [1351.0, 1268.0]], 'x': 1351.0, 'y': 1162.0, 'width': 2001.0, 'height': 139.0}, {'text': 'S:e.', 'confidence': 0.6483511924743652, 'bbox': [[599.0, 1281.0], [728.0, 1281.0], [728.0, 1356.0], [599.0, 1356.0]], 'x': 599.0, 'y': 1281.0, 'width': 129.0, 'height': 75.0}, {'text': '.....', 'confidence': 0.8049548864364624, 'bbox': [[2320.0, 1438.0], [2524.0, 1438.0], [2524.0, 1481.0], [2320.0, 1481.0]], 'x': 2320.0, 'y': 1438.0, 'width': 204.0, 'height': 43.0}, {'text': 'Ye....a..', 'confidence': 0.5707662105560303, 'bbox': [[1695.0, 1505.0], [1983.0, 1533.0], [1977.0, 1595.0], [1689.0, 1567.0]], 'x': 1689.0, 'y': 1505.0, 'width': 294.0, 'height': 90.0}, {'text': 'comme il est constaté par lextrait de son acte de naissance ci-joint, domiciliê', 'confidence': 0.9832553267478943, 'bbox': [[1377.0, 1612.0], [3950.0, 1644.0], [3949.0, 1732.0], [1376.0, 1700.0]], 'x': 1376.0, 'y': 1612.0, 'width': 2574.0, 'height': 120.0}, {'text': '..c..o..e.coem', 'confidence': 0.6479067206382751, 'bbox': [[1390.0, 1712.0], [2284.0, 1738.0], [2282.0, 1819.0], [1388.0, 1793.0]], 'x': 1388.0, 'y': 1712.0, 'width': 896.0, 'height': 107.0}, {'text': 'C4a', 'confidence': 0.5163208842277527, 'bbox': [[2563.0, 1730.0], [3012.0, 1745.0], [3010.0, 1832.0], [2560.0, 1818.0]], 'x': 2560.0, 'y': 1730.0, 'width': 452.0, 'height': 102.0}, {'text': 'X -', 'confidence': 0.5801221132278442, 'bbox': [[2407.0, 1756.0], [2536.0, 1756.0], [2536.0, 1800.0], [2407.0, 1800.0]], 'x': 2407.0, 'y': 1756.0, 'width': 129.0, 'height': 44.0}, {'text': 'baie.a', 'confidence': 0.7937344908714294, 'bbox': [[557.0, 1868.0], [1303.0, 1888.0], [1300.0, 2001.0], [554.0, 1980.0]], 'x': 554.0, 'y': 1868.0, 'width': 749.0, 'height': 133.0}, {'text': '.....c...we..e.ce', 'confidence': 0.6475739479064941, 'bbox': [[3147.0, 2100.0], [3703.0, 2100.0], [3703.0, 2144.0], [3147.0, 2144.0]], 'x': 3147.0, 'y': 2100.0, 'width': 556.0, 'height': 44.0}, {'text': '.....', 'confidence': 0.5045576095581055, 'bbox': [[3690.0, 2106.0], [3888.0, 2106.0], [3888.0, 2150.0], [3690.0, 2150.0]], 'x': 3690.0, 'y': 2106.0, 'width': 198.0, 'height': 44.0}, {'text': '..eo.e..e.so.beh.Kombe.', 'confidence': 0.5446963310241699, 'bbox': [[1519.0, 2137.0], [2852.0, 2157.0], [2850.0, 2263.0], [1518.0, 2243.0]], 'x': 1518.0, 'y': 2137.0, 'width': 1334.0, 'height': 126.0}, {'text': '.a.', 'confidence': 0.6433348059654236, 'bbox': [[2841.0, 2180.0], [3210.0, 2201.0], [3207.0, 2270.0], [2837.0, 2249.0]], 'x': 2837.0, 'y': 2180.0, 'width': 373.0, 'height': 90.0}, {'text': '...cx...u.', 'confidence': 0.555298924446106, 'bbox': [[1407.0, 2500.0], [1660.0, 2500.0], [1660.0, 2562.0], [1407.0, 2562.0]], 'x': 1407.0, 'y': 2500.0, 'width': 253.0, 'height': 62.0}, {'text': 'eJe4.cre.ed', 'confidence': 0.5713738203048706, 'bbox': [[2419.0, 2612.0], [3252.0, 2612.0], [3252.0, 2694.0], [2419.0, 2694.0]], 'x': 2419.0, 'y': 2612.0, 'width': 833.0, 'height': 82.0}, {'text': 'Et...ln', 'confidence': 0.5911161303520203, 'bbox': [[1450.0, 2706.0], [1839.0, 2706.0], [1839.0, 2775.0], [1450.0, 2775.0]], 'x': 1450.0, 'y': 2706.0, 'width': 389.0, 'height': 69.0}, {'text': '....e.', 'confidence': 0.7194342613220215, 'bbox': [[2468.0, 2738.0], [2623.0, 2738.0], [2623.0, 2781.0], [2468.0, 2781.0]], 'x': 2468.0, 'y': 2738.0, 'width': 155.0, 'height': 43.0}, {'text': 'A........', 'confidence': 0.5952409505844116, 'bbox': [[1394.0, 2832.0], [1838.0, 2825.0], [1839.0, 2887.0], [1395.0, 2894.0]], 'x': 1394.0, 'y': 2825.0, 'width': 445.0, 'height': 69.0}, {'text': 'tA.As.e', 'confidence': 0.5382478833198547, 'bbox': [[2851.0, 2956.0], [3166.0, 2956.0], [3166.0, 3000.0], [2851.0, 3000.0]], 'x': 2851.0, 'y': 2956.0, 'width': 315.0, 'height': 44.0}, {'text': "comme il est:constaté par l'extrait de son acte de naissance ci-joint, domiciliée", 'confidence': 0.9656440615653992, 'bbox': [[1364.0, 3025.0], [3938.0, 3050.0], [3937.0, 3138.0], [1364.0, 3112.0]], 'x': 1364.0, 'y': 3025.0, 'width': 2574.0, 'height': 113.0}, {'text': 'aKa', 'confidence': 0.5732572674751282, 'bbox': [[2283.0, 3156.0], [2524.0, 3156.0], [2524.0, 3219.0], [2283.0, 3219.0]], 'x': 2283.0, 'y': 3156.0, 'width': 241.0, 'height': 63.0}, {'text': 'e...', 'confidence': 0.7762690782546997, 'bbox': [[3431.0, 3181.0], [3616.0, 3181.0], [3616.0, 3225.0], [3431.0, 3225.0]], 'x': 3431.0, 'y': 3181.0, 'width': 185.0, 'height': 44.0}, {'text': 'Tolumc', 'confidence': 0.8570787906646729, 'bbox': [[580.0, 3606.0], [753.0, 3606.0], [753.0, 3650.0], [580.0, 3650.0]], 'x': 580.0, 'y': 3606.0, 'width': 173.0, 'height': 44.0}, {'text': 'j.c.o.....cs...a.e', 'confidence': 0.512136697769165, 'bbox': [[2803.0, 3706.0], [3864.0, 3725.0], [3862.0, 3794.0], [2801.0, 3775.0]], 'x': 2801.0, 'y': 3706.0, 'width': 1063.0, 'height': 88.0}, {'text': 'fcde.Keacutle-ta', 'confidence': 0.5338476300239563, 'bbox': [[2779.0, 3786.0], [3932.0, 3820.0], [3929.0, 3926.0], [2776.0, 3893.0]], 'x': 2776.0, 'y': 3786.0, 'width': 1156.0, 'height': 140.0}, {'text': 'C.c.uD.cy.c.', 'confidence': 0.5258910059928894, 'bbox': [[1444.0, 3825.0], [1734.0, 3825.0], [1734.0, 3869.0], [1444.0, 3869.0]], 'x': 1444.0, 'y': 3825.0, 'width': 290.0, 'height': 44.0}, {'text': '..ee.', 'confidence': 0.5081313252449036, 'bbox': [[1722.0, 3931.0], [1993.0, 3931.0], [1993.0, 3975.0], [1722.0, 3975.0]], 'x': 1722.0, 'y': 3931.0, 'width': 271.0, 'height': 44.0}, {'text': 'Lesquels nous ont requis de procader á la calebration du mariage projete', 'confidence': 0.9582521915435791, 'bbox': [[1414.0, 4106.0], [3932.0, 4138.0], [3930.0, 4244.0], [1413.0, 4212.0]], 'x': 1413.0, 'y': 4106.0, 'width': 2519.0, 'height': 138.0}, {'text': 'entre eux ct dont la publication a été faite en cette Commune,-azchuz.', 'confidence': 0.9038487672805786, 'bbox': [[1340.0, 4212.0], [3913.0, 4250.0], [3912.0, 4357.0], [1339.0, 4318.0]], 'x': 1339.0, 'y': 4212.0, 'width': 2574.0, 'height': 145.0}, {'text': 'Ceosc. e.0.', 'confidence': 0.6046043038368225, 'bbox': [[1341.0, 4324.0], [1896.0, 4345.0], [1892.0, 4432.0], [1338.0, 4412.0]], 'x': 1338.0, 'y': 4324.0, 'width': 558.0, 'height': 108.0}, {'text': 'lsdte.DcmchegtAuc.cecmmbr', 'confidence': 0.5157123804092407, 'bbox': [[2093.0, 4331.0], [3913.0, 4363.0], [3911.0, 4463.0], [2091.0, 4431.0]], 'x': 2091.0, 'y': 4331.0, 'width': 1822.0, 'height': 132.0}, {'text': 'nrapcet.a.dx.e.es.c.mtTsx.ceiss.cJo', 'confidence': 0.5048163533210754, 'bbox': [[1334.0, 4437.0], [3938.0, 4475.0], [3936.0, 4576.0], [1332.0, 4537.0]], 'x': 1332.0, 'y': 4437.0, 'width': 2606.0, 'height': 139.0}, {'text': "Le futur öpoux étantaentttcamlixee'txagekees.dajpnuafourni", 'confidence': 0.7401266694068909, 'bbox': [[1402.0, 4543.0], [3611.0, 4575.0], [3609.0, 4682.0], [1400.0, 4650.0]], 'x': 1400.0, 'y': 4543.0, 'width': 2211.0, 'height': 139.0}, {'text': '...la preuve', 'confidence': 0.8348543643951416, 'bbox': [[3580.0, 4593.0], [3919.0, 4600.0], [3918.0, 4669.0], [3579.0, 4662.0]], 'x': 3579.0, 'y': 4593.0, 'width': 340.0, 'height': 76.0}, {'text': "qu'il a satisfait & ses obligations.militaires en Belgique par la production d'in", 'confidence': 0.9707731008529663, 'bbox': [[1334.0, 4656.0], [3932.0, 4694.0], [3930.0, 4794.0], [1332.0, 4756.0]], 'x': 1332.0, 'y': 4656.0, 'width': 2600.0, 'height': 138.0}, {'text': 'certificat de M..le Gouverneur.', 'confidence': 0.9847943186759949, 'bbox': [[1340.0, 4768.0], [2364.0, 4782.0], [2363.0, 4869.0], [1339.0, 4856.0]], 'x': 1339.0, 'y': 4768.0, 'width': 1025.0, 'height': 101.0}, {'text': 'Aucune opposition au dit mariage ne nous ayant été signifiéc, faisant droit', 'confidence': 0.9647988677024841, 'bbox': [[1396.0, 4868.0], [3944.0, 4913.0], [3942.0, 5019.0], [1394.0, 4974.0]], 'x': 1394.0, 'y': 4868.0, 'width': 2550.0, 'height': 151.0}, {'text': '-á leur rêquisition, aprés avoir donné lecture des actes fournis par les parties', 'confidence': 0.9584490060806274, 'bbox': [[1316.0, 4974.0], [3926.0, 5019.0], [3924.0, 5126.0], [1314.0, 5081.0]], 'x': 1314.0, 'y': 4974.0, 'width': 2612.0, 'height': 152.0}, {'text': 'contractantes ct du chapitre six, titre cing du Code civil, intitulé : < Du MaRIAGE >,', 'confidence': 0.9459953308105469, 'bbox': [[1328.0, 5093.0], [3907.0, 5138.0], [3905.0, 5226.0], [1326.0, 5181.0]], 'x': 1326.0, 'y': 5093.0, 'width': 2581.0, 'height': 133.0}]
INFO:     127.0.0.1:35454 - "POST /extract HTTP/1.1" 200 OK
^CINFO:     Shutting down

# SecureGraph - Case Management API

A graph-based case management system inspired by Kaseware, built using FastAPI + ArangoDB.

## ✅ Features Implemented

- Graph-based RBAC (users → roles → permissions → resources)
- Case, entity, evidence, incident, and location management
- Graph edge linking (assigned_to, has_evidence, involves_entity, etc.)
- Seed endpoints for demo data
- Dashboard and search support

## 🚀 API Endpoints

### 🧪 Seed Data
- `POST /seed/` — Inserts sample case, entities, evidence, incident, and links
- `POST /seed/rbac` — Inserts roles, permissions, and links user access

### 📁 Case Management
- `POST /cases/` — Create a new case
- `POST /cases/{case_id}/link-entity` — Link suspect/witness to a case
- `POST /cases/{case_id}/add-evidence` — Attach evidence to a case
- `POST /cases/{case_id}/link-incident` — Attach incident to a case
- `GET /cases/{case_id}/graph` — Retrieve full connected graph of the case

### 🔐 Access Control
- `GET /access/users/{user_id}/access` — List resources user has access to

### 🔍 Search
- `GET /search/?query=...` — Search across entities, cases, evidence, etc.

### 📊 Dashboard
- `GET /dashboard/stats` — Return total counts from each major collection

## 📦 Project Structure

```
securegraph/
├── app/
│   ├── db.py
│   ├── graph_setup.py
│   ├── models.py
│   └── routers/
│       ├── __init__.py
│       ├── access.py
│       ├── cases.py
│       ├── dashboard.py
│       ├── search.py
│       └── seed.py
├── main.py
└── README.md
```

## 🛠️ Run Instructions

```bash
# Install dependencies
pip install fastapi uvicorn python-arango jinja2

# Run the app
uvicorn main:app --reload
```

---
Built with ❤️ using FastAPI + ArangoDB.
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.db import db
from uuid import uuid4

app = FastAPI(title="SecureGraph UI")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index(request: Request):
    cases = db.collection("cases")
    case_list = [doc for doc in cases.all()]
    return templates.TemplateResponse("index.html", {"request": request, "cases": case_list})

@app.get("/cases/{case_id}")
def case_detail(request: Request, case_id: str):
    case = db.collection("cases").get(case_id)
    if not case:
        return RedirectResponse("/")
    return templates.TemplateResponse("case_detail.html", {"request": request, "case": case})

print("🚀 UI server booted and route should be visible.")
@app.get("/cases/create/form")
def new_case_form(request: Request):
    print("🚀 GET /cases/new hit")
    return templates.TemplateResponse("case_new.html", {"request": request})

@app.post("/cases/create")
def submit_case_form(request: Request, title: str = Form(...), description: str = Form(None)):
    cases = db.collection("cases")
    key = title.lower().replace(" ", "-") + "-" + str(uuid4())[:6]
    case = {
        "_key": key,
        "title": title,
        "description": description
    }
    cases.insert(case)
    return RedirectResponse(url=f"/cases/{key}", status_code=303)
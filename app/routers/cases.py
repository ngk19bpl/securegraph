from fastapi import APIRouter, HTTPException
from app.db import db
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter(prefix="/cases", tags=["Case Graph"])

@router.get("/{case_id}/graph")
def get_case_graph(case_id: str):
    query = """
    LET case = DOCUMENT("cases", @case_id)

    RETURN {
        case: case,
        entities: (
            FOR v, e IN 1..1 OUTBOUND case._id involves_entity
            RETURN v
        ),
        evidence: (
            FOR v, e IN 1..1 OUTBOUND case._id has_evidence
            RETURN v
        ),
        assigned_users: (
            FOR v, e IN 1..1 INBOUND case._id assigned_to
            RETURN v
        ),
        related_entities: (
            FOR v1 IN 1..1 OUTBOUND case._id involves_entity
                FOR v2, e2 IN 1..1 OUTBOUND v1._id related_to
                RETURN DISTINCT v2
        )
    }
    """
    bind_vars = {"case_id": case_id}
    cursor = db.aql.execute(query, bind_vars=bind_vars)
    result = list(cursor)

    if not result:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return result[0]


# Schema for creating a case
class CaseCreate(BaseModel):
    title: str
    description: str | None = None

@router.post("/")
def create_case(payload: CaseCreate):
    cases = db.collection("cases")
    key = payload.title.lower().replace(" ", "-") + "-" + str(uuid4())[:8]
    case_doc = {
        "_key": key,
        "title": payload.title,
        "description": payload.description
    }
    cases.insert(case_doc)
    return {"message": "Case created", "case": case_doc}


class EntityLinkRequest(BaseModel):
    entity_id: str  # Must be full `_id`, e.g., "entities/john-doe"

@router.post("/{case_id}/link-entity")
def link_entity_to_case(case_id: str, payload: EntityLinkRequest):
    cases = db.collection("cases")
    edge = db.collection("involves_entity")

    case_doc = cases.get(case_id)
    if not case_doc:
        raise HTTPException(status_code=404, detail="Case not found")

    edge.insert({
        "_from": case_doc["_id"],
        "_to": payload.entity_id
    }, overwrite=True)

    return {
        "message": f"Entity {payload.entity_id} linked to case {case_id}"
    }

class EvidenceLinkRequest(BaseModel):
    evidence_id: str  # Full _id like "evidence/cctv-footage"

@router.post("/{case_id}/add-evidence")
def add_evidence_to_case(case_id: str, payload: EvidenceLinkRequest):
    cases = db.collection("cases")
    edge = db.collection("has_evidence")

    case_doc = cases.get(case_id)
    if not case_doc:
        raise HTTPException(status_code=404, detail="Case not found")

    edge.insert({
        "_from": case_doc["_id"],
        "_to": payload.evidence_id
    }, overwrite=True)

    return {
        "message": f"Evidence {payload.evidence_id} linked to case {case_id}"
    }


class IncidentLinkRequest(BaseModel):
    incident_id: str  # Full _id like "incidents/incident-001"

@router.post("/{case_id}/link-incident")
def link_incident_to_case(case_id: str, payload: IncidentLinkRequest):
    cases = db.collection("cases")
    edge = db.collection("happened_at")

    case_doc = cases.get(case_id)
    if not case_doc:
        raise HTTPException(status_code=404, detail="Case not found")

    # Validate the incident exists
    incident = db.collection("incidents").get(payload.incident_id.split("/")[1])
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    # Create edge from case to incident
    edge.insert({
        "_from": case_doc["_id"],
        "_to": payload.incident_id
    }, overwrite=True)

    return {
        "message": f"Incident {payload.incident_id} linked to case {case_id}"
    }
from fastapi import APIRouter
from app.db import db

router = APIRouter(prefix="/seed", tags=["Seed Data"])

@router.post("/")
def seed_data():
    users = db.collection("users")
    cases = db.collection("cases")
    entities = db.collection("entities")
    incidents = db.collection("incidents")
    evidence = db.collection("evidence")
    locations = db.collection("locations")

    edges = {
        "assigned_to": db.collection("assigned_to"),
        "involves_entity": db.collection("involves_entity"),
        "has_evidence": db.collection("has_evidence"),
        "happened_at": db.collection("happened_at"),
        "related_to": db.collection("related_to")
    }

    # Create documents
    alice = users.insert({"_key": "alice-johnson", "name": "Alice Johnson", "role": "Investigator"}, overwrite=True)
    case = cases.insert({"_key": "midtown-bank-burglary", "title": "Burglary at Midtown Bank"}, overwrite=True)
    suspect = entities.insert({"_key": "john-doe", "name": "John Doe", "type": "Suspect"}, overwrite=True)
    witness = entities.insert({"_key": "jane-smith", "name": "Jane Smith", "type": "Witness"}, overwrite=True)
    incident = incidents.insert({"_key": "incident-001", "description": "Bank break-in reported at 2 AM"}, overwrite=True)
    evidence_doc = evidence.insert({"_key": "cctv-footage", "type": "video", "description": "CCTV footage from the bank"}, overwrite=True)
    location = locations.insert({"_key": "midtown-bank-ny", "address": "Midtown Bank, NY"}, overwrite=True)

    # Create edges
    edges["assigned_to"].insert({"_from": alice["_id"], "_to": case["_id"]}, overwrite=True)
    edges["involves_entity"].insert({"_from": case["_id"], "_to": suspect["_id"]}, overwrite=True)
    edges["involves_entity"].insert({"_from": case["_id"], "_to": witness["_id"]}, overwrite=True)
    edges["has_evidence"].insert({"_from": case["_id"], "_to": evidence_doc["_id"]}, overwrite=True)
    edges["happened_at"].insert({"_from": incident["_id"], "_to": location["_id"]}, overwrite=True)
    edges["related_to"].insert({"_from": suspect["_id"], "_to": witness["_id"]}, overwrite=True)

    return {"message": "Seed data inserted successfully."}


@router.post("/rbac")
def seed_rbac():
    users = db.collection("users")
    roles = db.collection("roles")
    permissions = db.collection("permissions")
    resources = db.collection("resources")

    has_role = db.collection("has_role")
    has_permission = db.collection("has_permission")
    can_access = db.collection("can_access")

    resource = resources.insert({
        "_key": "case-evidence-001",
        "title": "Case File #001",
        "type": "document"
    }, overwrite=True)

    permission = permissions.insert({
        "_key": "can_view_case",
        "action": "view",
        "resource_type": "case"
    }, overwrite=True)

    role = roles.insert({
        "_key": "investigator",
        "name": "Investigator"
    }, overwrite=True)

    has_permission.insert({
        "_from": role["_id"],
        "_to": permission["_id"]
    }, overwrite=True)

    can_access.insert({
        "_from": permission["_id"],
        "_to": resource["_id"]
    }, overwrite=True)

    has_role.insert({
        "_from": "users/alice-johnson",
        "_to": role["_id"]
    }, overwrite=True)

    return {"message": "RBAC roles, permissions, and access seeded successfully."}
from fastapi import APIRouter
from app.db import db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_stats():
    def count_docs(coll_name):
        return db.collection(coll_name).count()

    return {
        "cases": count_docs("cases"),
        "entities": count_docs("entities"),
        "evidence": count_docs("evidence"),
        "incidents": count_docs("incidents"),
        "locations": count_docs("locations"),
        "users": count_docs("users")
    }

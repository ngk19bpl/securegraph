from fastapi import APIRouter, Query
from app.db import db

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_all(query: str = Query(..., min_length=1)):
    results = {}

    results["cases"] = list(db.aql.execute("""
        FOR doc IN cases
            FILTER CONTAINS(LOWER(doc.title), LOWER(@q)) 
                OR CONTAINS(LOWER(doc.description), LOWER(@q))
            RETURN doc
    """, bind_vars={"q": query}))

    results["entities"] = list(db.aql.execute("""
        FOR doc IN entities
            FILTER CONTAINS(LOWER(doc.name), LOWER(@q)) 
                OR CONTAINS(LOWER(doc.type), LOWER(@q))
            RETURN doc
    """, bind_vars={"q": query}))

    results["evidence"] = list(db.aql.execute("""
        FOR doc IN evidence
            FILTER CONTAINS(LOWER(doc.description), LOWER(@q))
            RETURN doc
    """, bind_vars={"q": query}))

    results["locations"] = list(db.aql.execute("""
        FOR doc IN locations
            FILTER CONTAINS(LOWER(doc.address), LOWER(@q))
            RETURN doc
    """, bind_vars={"q": query}))

    return results

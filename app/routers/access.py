from fastapi import APIRouter
from fastapi import HTTPException
from app.db import db

router = APIRouter(prefix="/access", tags=["Access Control"])

@router.get("/ping")
def ping():
    return {"message": "Access API is up"}


@router.get("/users/{user_id}/access")
def get_user_access(user_id: str):
    query = """
    LET user = DOCUMENT("users", @user_id)
    LET resources = (
        FOR v IN 1..3 OUTBOUND user._id GRAPH "access_graph"
            OPTIONS { bfs: true, uniqueVertices: "global" }
            FILTER IS_SAME_COLLECTION("resources", v)
            RETURN v
    )
    RETURN {
        user: user,
        accessible_resources: resources
    }
    """
    bind_vars = {"user_id": user_id}
    cursor = db.aql.execute(query, bind_vars=bind_vars)
    result = list(cursor)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or no access")
    return result[0]
from fastapi import APIRouter

router = APIRouter(prefix="/access", tags=["Access Control"])

@router.get("/ping")
def ping():
    return {"message": "Access API is up"}
from fastapi import FastAPI
from app.graph_setup import initialize_graph
from app.routers import access

app = FastAPI(title="SecureGraph")

@app.on_event("startup")
def setup():
    initialize_graph()

app.include_router(access.router)
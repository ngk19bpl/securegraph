from fastapi import FastAPI
from app.graph_setup import initialize_graph
from app.routers import access, seed, cases, search, dashboard
app = FastAPI(title="SecureGraph")

@app.on_event("startup")
def setup():
    initialize_graph()

app.include_router(access.router)
app.include_router(seed.router)
app.include_router(cases.router)
app.include_router(search.router)
app.include_router(dashboard.router)
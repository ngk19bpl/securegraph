from app.db import db
from app.models import collections, edge_definitions

def initialize_graph():
    for name in collections:
        if not db.has_collection(name):
            db.create_collection(name)

    for edge_def in edge_definitions:
        edge_name = edge_def["edge"]
        if not db.has_collection(edge_name):
            db.create_collection(edge_name, edge=True)

    if not db.has_graph("access_graph"):
        db.create_graph(
            "access_graph",
            edge_definitions=[
                {
                    "edge_collection": e["edge"],
                    "from_vertex_collections": e["from"],
                    "to_vertex_collections": e["to"]
                }
                for e in edge_definitions
            ]
        )
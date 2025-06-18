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

    if db.has_graph("access_graph"):
        graph = db.graph("access_graph")
        existing_edges = set(e["edge_collection"] for e in graph.edge_definitions())
        for e in edge_definitions:
            if e["edge"] not in existing_edges:
                graph.create_edge_definition(
                    edge_collection=e["edge"],
                    from_vertex_collections=e["from"],
                    to_vertex_collections=e["to"]
                )
    else:
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

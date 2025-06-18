collections = [
    "users", "roles", "permissions", "resources",
    "cases", "incidents", "entities", "evidence", "locations"
]

edge_definitions = [
    {"edge": "has_role", "from": ["users"], "to": ["roles"]},
    {"edge": "has_permission", "from": ["roles"], "to": ["permissions"]},
    {"edge": "can_access", "from": ["permissions"], "to": ["resources"]},
    {"edge": "assigned_to", "from": ["users"], "to": ["cases"]},
    {"edge": "involves_entity", "from": ["cases"], "to": ["entities"]},
    {"edge": "has_evidence", "from": ["cases"], "to": ["evidence"]},
    {"edge": "happened_at", "from": ["incidents"], "to": ["locations"]},
    {"edge": "related_to", "from": ["entities"], "to": ["entities"]}
]

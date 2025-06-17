collections = [
    "users", "roles", "permissions", "resources", "cases", "evidence"
]

edge_definitions = [
    {"edge": "has_role", "from": ["users"], "to": ["roles"]},
    {"edge": "has_permission", "from": ["roles"], "to": ["permissions"]},
    {"edge": "can_access", "from": ["permissions"], "to": ["resources"]},
    {"edge": "assigned_to", "from": ["users"], "to": ["cases"]},
    {"edge": "owns", "from": ["users"], "to": ["evidence"]},
]
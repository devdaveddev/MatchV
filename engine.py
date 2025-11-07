
from db import names_collection
from utils.scoring import final_score


records = list(names_collection.find({}))


search_pool = [
    (f"{r.get('First Name', '')} {r.get('Last Name', '')}".strip(), r)
    for r in records
]

def search_names(query: str, top_k: int = 10):
    """Return top-k matched persons for given name query."""
    scored = []

    for full_name, doc in search_pool:
        score = final_score(query, full_name)
        scored.append((score, doc))

    
    scored.sort(key=lambda x: x[0], reverse=True)

    
    return [
        {
            **doc,
            "match_score": round(score, 4)
        }
        for score, doc in scored[:top_k]
    ]


def add_person(data: dict):
    """Insert new person into DB and update search pool live."""
    
    first = (data.get("first") or "").strip()
    last  = (data.get("last") or "").strip()

    if not first or not last:
        raise ValueError("first and last name required")

    new_doc = {
        "First Name": first,
        "Last Name": last,
        "Age": data.get("age"),
        "Phone": data.get("phone"),
        "Address": data.get("address"),
    }

    
    names_collection.insert_one(new_doc)

    
    search_pool.append((f"{first} {last}", new_doc))

    return new_doc

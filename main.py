from fastapi import FastAPI


app = FastAPI()


notes = [
    {
        "id": 1,
        "term": "variable",
        "definition": "A name that stores a value.",
        "js_equivalent": "let / const",
        "tags": ["python", "basics"],
        "learned": True,
    },
    {
        "id": 2,
        "term": "list",
        "definition": "An ordered collection of items.",
        "js_equivalent": "array",
        "tags": ["python", "data"],
        "learned": True,
    },
    {
        "id": 3,
        "term": "loop",
        "definition": "Repeats a block of code multiple times.",
        "js_equivalent": "for / while",
        "tags": ["python", "basics"],
        "learned": False,
    },
    {
        "id": 4,
        "term": "function",
        "definition": "A reusable block of code defined with def.",
        "js_equivalent": "function",
        "tags": ["python", "data"],
        "learned": False,
    },
]


@app.get("/")
def root():
    return {"message": "Learning Notebook API is Running!"}


# @app.get("/terms")
# def get_terms():
#     return notes

@app.get("/terms")
def get_terms(tag: str | None = None, q: str | None = None):
    result = []
    for note in notes:
        if tag and tag not in note["tags"]:
            continue
        if q and q.lower() not in note["term"].lower():
            continue
        result.append(note)
    return result   


@app.get("/terms/{term_id}")
def get_term(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            return note
    return {"message": "Term not found!"}


@app.post("/terms", status_code=201)
def add_term(note: dict):
    new_note = {"id": len(notes) +1}
    new_note.update(note)
    notes.append(new_note)
    return new_note
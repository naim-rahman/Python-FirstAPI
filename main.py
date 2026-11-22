from fastapi import FastAPI
from pydantic import BaseModel


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


class Note(BaseModel):
    term: str
    definition: str
    js_equivalent: str | None = None
    tags: list[str] = []
    learned: bool = False
    
    
class NoteUpdate(BaseModel):
    term: str | None = None
    definition: str | None = None
    js_equivalent: str | None = None
    tags: list[str] | None = None
    learned: bool | None = None
    
    

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
def add_term(note: Note):
    new_note = {"id": len(notes) +1}
    new_note.update(note.model_dump())
    notes.append(new_note)
    return new_note


@app.patch("/terms/{term_id}")
def update_term(term_id: int, changes: NoteUpdate):
    for note in notes:
        if note["id"] == term_id:
            note.update(changes.model_dump(exclude_unset=True))
            return note
    return {"message": "Term not found"}


@app.delete("/terms/{term_id}", status_code=204)
def delete_term(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            notes.remove(note)
            return
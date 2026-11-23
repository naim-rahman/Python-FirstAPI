import random
from fastapi import FastAPI, HTTPException
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
    {
        "id": 5,
        "term": "dict",
        "definition": "A collection of key-value pairs.",
        "js_equivalent": "Object / Map",
        "tags": ["dict", "python"],
        "learned": True,
    },
    {
        "id": 6,
        "term": "f-string",
        "definition": 'A string with embedded {expressions}, written f"Hi {name}".',
        "js_equivalent": "Template literal (`Hi ${name}`)",
        "tags": ["f-string", "python"],
        "learned": True,
    },
    {
        "id": 7,
        "term": "indentation",
        "definition": "Leading spaces that mark code blocks.",
        "js_equivalent": "Curly braces { } for blocks",
        "tags": ["indentation", "python"],
        "learned": True,
    },
    {
        "id": 8,
        "term": "pydantic",
        "definition": "A library that validates data using type hints.",
        "js_equivalent": "Zod / Joi",
        "tags": ["pydantic", "python"],
        "learned": False,
    },
    {
        "id": 9,
        "term": "uv",
        "definition": "A fast Python package and project manager.",
        "js_equivalent": "npm / pnpm",
        "tags": ["uv", "python"],
        "learned": True,
    },
    {
        "id": 10,
        "term": "decorator",
        "definition": "A function that wraps another function to add behavior.",
        "js_equivalent": "Higher-order function",
        "tags": ["decorator", "python"],
        "learned": False,
    },
]


## define default class
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


## route start here
@app.get("/")
def root():
    return {"message": "Learning Notebook API is Running!"}


# @app.get("/terms")
# def get_terms():
#     return notes


@app.get("/terms")
def get_terms(
    tag: str | None = None, q: str | None = None, learned: bool | None = None
):
    result = []
    for note in notes:
        if tag and tag not in note["tags"]:
            continue
        if q and q.lower() not in note["term"].lower():
            continue
        if learned is not None and note["learned"] != learned:
            continue
        result.append(note)
    return result


@app.get("/terms/random")
def random_term():
    if len(notes) == 0:
        raise HTTPException(status_code=404, detail="No terms yet!")
    return random.choice(notes)


@app.get("/terms/progress")
def progress():
    total = len(notes)
    learned = sum(1 for note in notes if note["learned"])
    remain = total - learned
    percent = round(learned / total * 100) if total else 0
    return {"Total": total, "Learned": learned, "Remain": remain, "Percent": f"{percent}%"}


@app.get("/terms/{term_id}")
def get_term(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            return note
    raise HTTPException(status_code=404, detail="Term not found!")


# @app.post("/terms", status_code=201)
# def add_term(note: Note):
#     new_note = {"id": len(notes) +1}
#     new_note.update(note.model_dump())
#     notes.append(new_note)
#     return new_note


@app.post("/terms", status_code=201)
def add_term(note: Note):
    for existing in notes:
        if existing["term"].lower() == note.term.lower():
            raise HTTPException(status_code=409, detail="Term already exist!")
    new_id = 1
    for existing in notes:
        if existing["id"] >= new_id:
            new_id = existing["id"] + 1
    new_note = {"id": new_id}
    new_note.update(note.model_dump())
    notes.append(new_note)
    return new_note


@app.patch("/terms/{term_id}")
def update_term(term_id: int, changes: NoteUpdate):
    for note in notes:
        if note["id"] == term_id:
            note.update(changes.model_dump(exclude_unset=True))
            return note
    raise HTTPException(status_code=404, detail="Term not found!")


@app.delete("/terms/{term_id}", status_code=204)
def delete_term(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            notes.remove(note)
            return
    raise HTTPException(status_code=404, detail="Term not found!")


@app.post("/terms/{term_id}/learn")
def mark_learned(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            if note["learned"]:
                raise HTTPException(status_code=409, detail="Already learned!")
            note["learned"] = True
            return note
    raise HTTPException(status_code=404, detail="Term not found!")


@app.post("/terms/{term_id}/unlearn")
def mark_unlearned(term_id: int):
    for note in notes:
        if note["id"] == term_id:
            if not note["learned"]:
                raise HTTPException(status_code=409, detail="Already unlearned!")
            note["learned"] = False
            return note
    raise HTTPException(status_code=404, detail="Term not found!")


@app.get("/stats")
def get_stats():
    learned = 0
    by_tag = {}
    for note in notes:
        if note["learned"]:
            learned += 1
        for tag in note["tags"]:
            by_tag[tag] = by_tag.get(tag, 0) + 1
    return {"total": len(notes), "learned": learned, "by_tag": by_tag}

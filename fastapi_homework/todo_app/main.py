from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import sqlite3
from pathlib import Path

app = FastAPI(title="TODO Service")

DATA_DIR = Path("/app/data")
DB_PATH = DATA_DIR / "todo.db"

def get_conn():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

@app.on_event("startup")
def on_startup():
    init_db()

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    completed: bool = False

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None

class ItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO items (title, description, completed) VALUES (?, ?, ?)",
            (item.title, item.description, int(item.completed)),
        )
        conn.commit()
        item_id = cur.lastrowid
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return ItemOut(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@app.get("/items", response_model=List[ItemOut])
def list_items():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM items ORDER BY id").fetchall()
        return [ItemOut(id=r["id"], title=r["title"], description=r["description"], completed=bool(r["completed"])) for r in rows]

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemOut(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemUpdate):
    with get_conn() as conn:
        existing = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Item not found")

        new_title = item.title if item.title is not None else existing["title"]
        new_desc = item.description if item.description is not None else existing["description"]
        new_completed = int(item.completed) if item.completed is not None else int(existing["completed"])

        conn.execute(
            "UPDATE items SET title = ?, description = ?, completed = ? WHERE id = ?",
            (new_title, new_desc, new_completed, item_id),
        )
        conn.commit()

        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return ItemOut(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"status": "deleted", "id": item_id}


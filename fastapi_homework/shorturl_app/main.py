from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
import sqlite3
from pathlib import Path
import secrets
import string

app = FastAPI(title="Short URL Service")

DATA_DIR = Path("/app/data")
DB_PATH = DATA_DIR / "shorturl.db"

def get_conn():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS links (
                short_id TEXT PRIMARY KEY,
                full_url TEXT NOT NULL
            )
        """)
        conn.commit()

@app.on_event("startup")
def on_startup():
    init_db()

class ShortenIn(BaseModel):
    url: AnyUrl

class ShortenOut(BaseModel):
    short_id: str
    short_url: str
    full_url: str

def generate_id(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

@app.post("/shorten", response_model=ShortenOut)
def shorten(payload: ShortenIn):
    with get_conn() as conn:
        for _ in range(10):
            sid = generate_id()
            exists = conn.execute("SELECT 1 FROM links WHERE short_id = ?", (sid,)).fetchone()
            if not exists:
                conn.execute("INSERT INTO links (short_id, full_url) VALUES (?, ?)", (sid, str(payload.url)))
                conn.commit()
                return ShortenOut(short_id=sid, short_url=f"/{sid}", full_url=str(payload.url))
    raise HTTPException(status_code=500, detail="Could not generate short id")

@app.get("/{short_id}")
def redirect(short_id: str):
    with get_conn() as conn:
        row = conn.execute("SELECT full_url FROM links WHERE short_id = ?", (short_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Short link not found")
        return RedirectResponse(url=row["full_url"], status_code=307)

@app.get("/stats/{short_id}")
def stats(short_id: str):
    with get_conn() as conn:
        row = conn.execute("SELECT short_id, full_url FROM links WHERE short_id = ?", (short_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Short link not found")
        return {"short_id": row["short_id"], "full_url": row["full_url"]}


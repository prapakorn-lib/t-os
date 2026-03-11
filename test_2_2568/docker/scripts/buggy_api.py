"""
buggy_api.py  —  FastAPI App ที่มี bug (Lab 3.3)
-------------------------------------------------
โปรแกรมนี้มี bug อยู่ 2 จุด
นักศึกษา: รัน → อ่าน error → แก้ทีละจุด → ทดสอบจนใช้ได้

วิธีรัน:
    uvicorn buggy_api:app --port 8001

ทดสอบ:
    curl http://localhost:8001/items
"""

from fastapi import FastAPI, HTTPException
import psycopg2
import psycopg2.extras

app = FastAPI(title="Buggy API - Fix Me!", version="0.1.0")


# ============================================================
# BUG #1: DB_NAME ผิด — แก้ให้ตรงกับ database ที่สร้างไว้
# ============================================================
DB_CONFIG = {
    "host":     "localhost",
    "dbname":   "wrongdbname",     # ← BUG: ชื่อ database ผิด
    "user":     "labuser",
    "password": "labpass123",
    "port":     5432,
}


def get_conn():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")


@app.get("/")
def root():
    return {"status": "running", "hint": "Try GET /items"}


@app.get("/items")
def get_items():
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # ============================================================
        # BUG #2: SQL syntax error — FORM ควรเป็น FROM
        # ============================================================
        cur.execute("SELECT id, name, price, stock FORM products")   # ← BUG: FORM ควรเป็น FROM
        rows = cur.fetchall()
        return {"items": rows}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"SQL Error: {e}")
    finally:
        conn.close()


@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM products WHERE id = %s", (item_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        return row
    finally:
        conn.close()

"""
main.py  —  FastAPI Application (Lab Part 3)
--------------------------------------------
โปรแกรมนี้เตรียมไว้ให้แล้ว
นักศึกษาต้องแก้ไขเฉพาะส่วน DATABASE CONFIG ด้านล่างให้ตรงกับที่ตั้งค่าไว้
จากนั้นติดตั้ง dependencies และรัน server
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
import psycopg2.extras

# ============================================================
#  DATABASE CONFIG  ←  นักศึกษาต้องแก้ไขส่วนนี้
# ============================================================
DB_HOST     = "localhost"
DB_NAME     = "???"          # ← แก้เป็นชื่อ database ที่สร้างไว้
DB_USER     = "???"          # ← แก้เป็นชื่อ user ที่สร้างไว้
DB_PASSWORD = "???"          # ← แก้เป็น password ที่ตั้งไว้
DB_PORT     = 5432
# ============================================================

app = FastAPI(title="Products API", version="1.0.0")


# ----- Pydantic Model -----

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int


class Product(ProductCreate):
    id: int


# ----- DB Helper -----

def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


# ----- Endpoints -----

@app.get("/")
def root():
    return {
        "message": "Welcome to Products API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/products")
def get_all_products():
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM products ORDER BY id")
        rows = cur.fetchall()
        return {"products": rows, "total": len(rows)}
    finally:
        conn.close()


@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product id={product_id} not found")
        return row
    finally:
        conn.close()


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s) RETURNING *",
            (product.name, product.price, product.stock)
        )
        new_row = cur.fetchone()
        conn.commit()
        return {"message": "Product created", "product": new_row}
    finally:
        conn.close()

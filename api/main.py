# ============================================
# Fred Baker's Automations
# api/main.py — FastAPI REST API
# Nigeria Business Intelligence API
# ============================================

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# ---- APP ----
app = FastAPI(
    title="Fred Baker's Automations API",
    description="Nigeria Business Intelligence API — LexAI, EstateIQ, OpsGuard",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "projects/nigeria-business-db/nigeria_businesses.db"

# ---- DATABASE ----
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def rows_to_list(rows):
    return [dict(row) for row in rows]

# ---- ROUTES ----
@app.get("/")
def root():
    return {
        "company": "Fred Baker's Automations",
        "api": "Nigeria Business Intelligence",
        "version": "1.0.0",
        "location": "Abuja, Nigeria",
        "products": ["LexAI", "EstateIQ", "OpsGuard"]
    }

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM businesses")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM businesses
        GROUP BY city ORDER BY count DESC
    """)
    cities = rows_to_list(cursor.fetchall())

    cursor.execute("""
        SELECT prospect_for, COUNT(*) as count
        FROM businesses
        GROUP BY prospect_for ORDER BY count DESC
    """)
    products = rows_to_list(cursor.fetchall())

    conn.close()
    return {
        "total_records": total,
        "by_city": cities,
        "by_product": products
    }

@app.get("/businesses")
def get_businesses(
    city: Optional[str] = None,
    sector: Optional[str] = None,
    product: Optional[str] = None,
    limit: int = Query(default=10, le=100)
):
    conn = get_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM businesses WHERE 1=1"
    params = []

    if city:
        sql += " AND city LIKE ?"
        params.append(f"%{city}%")
    if sector:
        sql += " AND sector LIKE ?"
        params.append(f"%{sector}%")
    if product:
        sql += " AND prospect_for = ?"
        params.append(product)

    sql += f" LIMIT {limit}"
    cursor.execute(sql, params)
    results = rows_to_list(cursor.fetchall())
    conn.close()

    return {
        "count": len(results),
        "businesses": results
    }

@app.get("/businesses/{business_id}")
def get_business(business_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses WHERE id = ?", (business_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return {"error": "Business not found"}
    return dict(result)

@app.get("/prospects/lexai")
def get_lexai_prospects(limit: int = 20):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM businesses
        WHERE prospect_for = 'LexAI'
        AND contacted = 0
        ORDER BY city
        LIMIT ?
    """, (limit,))
    results = rows_to_list(cursor.fetchall())
    conn.close()
    return {"product": "LexAI", "count": len(results), "prospects": results}

@app.get("/prospects/estateiq")
def get_estateiq_prospects(limit: int = 20):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM businesses
        WHERE prospect_for = 'EstateIQ'
        AND contacted = 0
        ORDER BY city
        LIMIT ?
    """, (limit,))
    results = rows_to_list(cursor.fetchall())
    conn.close()
    return {"product": "EstateIQ", "count": len(results), "prospects": results}

@app.get("/prospects/opsguard")
def get_opsguard_prospects(limit: int = 20):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM businesses
        WHERE prospect_for = 'OpsGuard'
        AND contacted = 0
        ORDER BY city
        LIMIT ?
    """, (limit,))
    results = rows_to_list(cursor.fetchall())
    conn.close()
    return {"product": "OpsGuard", "count": len(results), "prospects": results}

@app.get("/search")
def search_businesses(
    q: str = Query(..., description="Search term"),
    limit: int = 10
):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM businesses
        WHERE company_name LIKE ?
        OR summary LIKE ?
        LIMIT ?
    """, (f"%{q}%", f"%{q}%", limit))
    results = rows_to_list(cursor.fetchall())
    conn.close()
    return {"query": q, "count": len(results), "results": results}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import datetime

app = FastAPI()

# THIS IS THE VITAL PART:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/status")
def get_status():
    # Gets the last time the .db file was modified
    mod_time = os.path.getmtime('brick_archive.db')
    dt_m = datetime.datetime.fromtimestamp(mod_time)
    return {"last_update": dt_m.isoformat()}


@app.get("/search")
def search_sets(q: str, page: int = 1):
    limit = 20
    offset = (page - 1) * limit

    conn = sqlite3.connect('brick_archive.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Lowercase + wildcards makes it much more general
    search_query = f"%{q.lower()}%"

    # 1. Get the TOTAL count for pagination buttons
    count_query = """
        SELECT COUNT(*) FROM sets 
        JOIN themes ON sets.theme_id = themes.id
        WHERE (LOWER(sets.name) LIKE ? OR sets.set_num LIKE ?)
        AND themes.name NOT IN ('Books', 'Gear', 'Keychains')
    """
    total_results = cursor.execute(count_query, (search_query, search_query)).fetchone()[0]

    # 2. Get the actual page of results
    query = """
        SELECT sets.set_num, sets.name, sets.year, themes.name as theme, sets.img_url
        FROM sets
        JOIN themes ON sets.theme_id = themes.id
        WHERE (LOWER(sets.name) LIKE ? OR sets.set_num LIKE ?)
        AND themes.name NOT IN ('Books', 'Gear', 'Keychains')
        ORDER BY sets.year DESC
        LIMIT ? OFFSET ?
    """

    results = cursor.execute(query, (search_query, search_query, limit, offset)).fetchall()
    conn.close()

    return {
        "results": [dict(row) for row in results],
        "total": total_results,
        "page": page,
        "pages": (total_results // limit) + 1
    }

@app.get("/details/{set_num}")
def get_details(set_num: str):
    conn = sqlite3.connect('brick_archive.db')
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT * FROM sets WHERE set_num = ?", (set_num,)).fetchone()
    conn.close()
    return dict(res) if res else {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    import os
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
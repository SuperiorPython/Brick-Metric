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
def search_sets(q: str, page: int = Query(1, ge=1)):
    limit = 5  # Small limit for terminal testing
    offset = (page - 1) * limit

    conn = sqlite3.connect('brick_archive.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fuzzy search: %term% matches anything containing the term
    search_term = f"%{q}%"

    # Get total count for pagination info
    count_sql = "SELECT COUNT(*) FROM sets WHERE name LIKE ? OR set_num LIKE ?"
    total_count = cursor.execute(count_sql, (search_term, search_term)).fetchone()[0]

    # Get the specific page of data
    data_sql = "SELECT set_num, name, year FROM sets WHERE name LIKE ? OR set_num LIKE ? LIMIT ? OFFSET ?"
    rows = cursor.execute(data_sql, (search_term, search_term, limit, offset)).fetchall()
    conn.close()

    return {
        "total_results": total_count,
        "current_page": page,
        "total_pages": (total_count + limit - 1) // limit,
        "results": [dict(row) for row in rows]
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

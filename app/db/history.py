from app.db.database import get_connection

def save_search(filename: str, question: str, answer: str, confidence: float):
    conn = get_connection()
    conn.execute(
        "INSERT INTO search_history (filename, question, answer, confidence) VALUES (?, ?, ?, ?)",
        (filename, question, answer or "—", confidence)
    )
    conn.commit()
    conn.close()

def get_history(limit: int = 50) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM search_history ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_history():
    conn = get_connection()
    conn.execute("DELETE FROM search_history")
    conn.commit()
    conn.close()

def get_history_by_file(filename: str, limit: int = 50) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM search_history WHERE filename = ? ORDER BY created_at DESC LIMIT ?",
        (filename, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
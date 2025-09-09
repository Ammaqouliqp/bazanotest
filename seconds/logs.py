from .database import get_db_connection

def log_event(username, action, status, message=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO auth_logs (username, action, status, message) VALUES (?, ?, ?, ?)",
        (username, action, status, message)
    )
    conn.commit()
    conn.close()

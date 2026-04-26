import sqlite3
import os

DB_PATH = 'backend/veritas.db'

def check_db():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("Applications Table:")
    apps = cursor.execute('SELECT * FROM applications').fetchall()
    for app in apps:
        print(dict(app))
    
    print("\nClient Applications Table:")
    capps = cursor.execute('SELECT * FROM client_applications').fetchall()
    for capp in capps:
        print(dict(capp))
        
    conn.close()

if __name__ == "__main__":
    check_db()

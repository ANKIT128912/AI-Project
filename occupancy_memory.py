
import sqlite3
from datetime import datetime

DATABASE_PATH = "data/classroom.db"


def initialize_database():
    """Create the occupancy history table if it doesn't exist."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS occupancy_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                classroom_id TEXT NOT NULL,
                student_count INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)


def save_occupancy(classroom_id, student_count):
    """Save one occupancy observation."""
    timestamp = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            INSERT INTO occupancy_history
                (classroom_id, student_count, timestamp)
            VALUES (?, ?, ?)
            """,
            (classroom_id, student_count, timestamp)
        )


def get_recent_history(classroom_id, limit=10):
    """Return the latest occupancy observations."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT student_count, timestamp
            FROM occupancy_history
            WHERE classroom_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (classroom_id, limit)
        )
        return cursor.fetchall()


if __name__ == "__main__":
    initialize_database()

    save_occupancy("CLASS-101", 18)
    save_occupancy("CLASS-101", 20)
    save_occupancy("CLASS-101", 19)

    print("Recent occupancy history:")
    for count, timestamp in get_recent_history("CLASS-101"):
        print(f"{timestamp} | Students detected: {count}")

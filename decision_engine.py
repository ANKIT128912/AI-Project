
import sqlite3
from timetable import get_class_status, load_classrooms

DATABASE_PATH = "data/classroom.db"


def get_latest_occupancy(classroom_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT student_count
            FROM occupancy_history
            WHERE classroom_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (classroom_id,)
        )
        result = cursor.fetchone()

    return result[0] if result else 0


def evaluate_classroom(classroom_id):
    detected_count = get_latest_occupancy(classroom_id)

    classrooms = load_classrooms()
    room = classrooms[
        classrooms["classroom_id"] == classroom_id
    ]

    if room.empty:
        return {
            "classroom_id": classroom_id,
            "alert": "Unknown classroom"
        }

    capacity = int(room.iloc[0]["capacity"])
    schedule = get_class_status(classroom_id)

    alerts = []

    if detected_count > capacity:
        alerts.append("OVERcrowding detected")

    if (
        schedule["status"] == "No class scheduled"
        and detected_count > 0
    ):
        alerts.append("Possible unscheduled room usage")

    if not alerts:
        alerts.append("Normal occupancy")

    return {
        "classroom_id": classroom_id,
        "detected_count": detected_count,
        "capacity": capacity,
        "timetable_status": schedule["status"],
        "alerts": alerts
    }


if __name__ == "__main__":
    print(evaluate_classroom("C101"))

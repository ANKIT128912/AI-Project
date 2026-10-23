
import pandas as pd
from datetime import datetime

CLASSROOMS_FILE = "data/classrooms.csv"
TIMETABLE_FILE = "data/timetable.csv"


def load_classrooms():
    """Load classroom details from CSV."""
    return pd.read_csv(CLASSROOMS_FILE)


def load_timetable():
    """Load scheduled classes from CSV."""
    return pd.read_csv(TIMETABLE_FILE)


def get_class_status(classroom_id, current_time=None):
    """Compare a classroom with its timetable."""

    if current_time is None:
        current_time = datetime.now()

    classrooms = load_classrooms()
    timetable = load_timetable()

    room = classrooms[
        classrooms["classroom_id"] == classroom_id
    ]

    if room.empty:
        return {"status": "Unknown classroom"}

    today = current_time.strftime("%A")
    now = current_time.strftime("%H:%M")

    scheduled = timetable[
        (timetable["classroom_id"] == classroom_id)
        & (timetable["day"].str.lower() == today.lower())
        & (timetable["start_time"] <= now)
        & (timetable["end_time"] > now)
    ]

    if scheduled.empty:
        return {
            "status": "No class scheduled",
            "classroom_id": classroom_id
        }

    class_info = scheduled.iloc[0]

    return {
        "status": "Class scheduled",
        "classroom_id": classroom_id,
        "subject": class_info["subject"],
        "expected_students": int(class_info["expected_students"]),
        "start_time": class_info["start_time"],
        "end_time": class_info["end_time"]
    }


if __name__ == "__main__":
    print("CLASSROOM TIMETABLE STATUS")
    print("-" * 35)

    classrooms = load_classrooms()

    for classroom_id in classrooms["classroom_id"]:
        result = get_class_status(classroom_id)
        print(f"{classroom_id}: {result}")

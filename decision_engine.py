
from timetable import get_class_status, load_classrooms


def evaluate_classroom(classroom_id, detected_count):
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
    # Test values only; these are not live detections.
    for room_id, count in [
        ("C101", 25),
        ("C201", 65),
        ("C301", 10)
    ]:
        print(evaluate_classroom(room_id, count))

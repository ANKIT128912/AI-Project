
import cv2
import time
from ultralytics import YOLO
from occupancy_memory import initialize_database, save_occupancy

VIDEO_PATH = "videos/sectionK.mp4"
CLASSROOM_ID = "CLASS-101"
SAVE_INTERVAL = 5  # Save one observation every 5 seconds


def detect_people():
    initialize_database()

    model = YOLO("yolo11n.pt")
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"Error: Could not open {VIDEO_PATH}")
        return

    print("Classroom AI started!")
    last_saved = 0

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Video finished.")
                break

            results = model(frame, verbose=False)

            people_count = sum(
                1
                for box in results[0].boxes
                if int(box.cls[0]) == 0
            )

            current_time = time.time()

            # Save actual detections every 5 seconds
            if current_time - last_saved >= SAVE_INTERVAL:
                save_occupancy(CLASSROOM_ID, people_count)
                print(f"Saved occupancy: {people_count}")
                last_saved = current_time

            annotated_frame = results[0].plot()

            cv2.putText(
                annotated_frame,
                f"People detected: {people_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Intelligent Classroom Occupancy Agent",
                annotated_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    print("Detection stopped.")


if __name__ == "__main__":
    detect_people()

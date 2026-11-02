
import streamlit as st
import pandas as pd
from decision_engine import evaluate_classroom
from occupancy_memory import get_recent_history
from room_recommender import recommend_room

st.set_page_config(
    page_title="Classroom Occupancy Agent",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 Intelligent Classroom Occupancy Agent")
st.caption("AI-powered classroom monitoring and utilization")

classrooms = pd.read_csv("data/classrooms.csv")

st.sidebar.header("Classroom Selection")

room_ids = classrooms["classroom_id"].tolist()
selected_room = st.sidebar.selectbox("Select classroom", room_ids)

accessible_required = st.sidebar.checkbox(
    "Require accessible classroom"
)

# Get latest YOLO occupancy from SQLite
history = get_recent_history(selected_room, limit=1)

if history:
    detected_count = history[0][0]
    last_detection_time = history[0][1]
else:
    detected_count = 0
    last_detection_time = "No detection recorded"

# Decision Engine reads occupancy from SQLite
result = evaluate_classroom(selected_room)

room_info = classrooms[
    classrooms["classroom_id"] == selected_room
].iloc[0]

capacity = int(room_info["capacity"])

col1, col2, col3 = st.columns(3)

col1.metric("People detected", detected_count)
col2.metric("Room capacity", capacity)

utilization = (
    detected_count / capacity * 100
    if capacity > 0 else 0
)

col3.metric(
    "Capacity utilization",
    f"{utilization:.1f}%"
)

st.caption(f"Last detection: {last_detection_time}")

st.subheader("Classroom status")
st.write("**Timetable:**", result["timetable_status"])

for alert in result["alerts"]:
    if "OVERcrowding" in alert:
        st.error(alert)
    elif "unscheduled" in alert:
        st.warning(alert)
    else:
        st.success(alert)

st.subheader("Alternative classroom recommendations")

if detected_count > capacity:
    recommendations = recommend_room(
        current_room=selected_room,
        required_capacity=detected_count,
        accessible_required=accessible_required
    )

    if recommendations:
        st.dataframe(
            pd.DataFrame(recommendations),
            use_container_width=True
        )
    else:
        st.info("No suitable alternative found.")
else:
    st.info("No capacity-based room change is needed.")

st.subheader("Occupancy History")

if history:
    st.write("Latest occupancy observation from SQLite:")
    st.dataframe(
        pd.DataFrame(
            history,
            columns=["People detected", "Timestamp"]
        ),
        use_container_width=True
    )
else:
    st.info("No occupancy records available for this classroom.")

st.subheader("All classrooms")
st.dataframe(classrooms, use_container_width=True)

st.caption(
    "Occupancy is retrieved from SQLite. "
    "Building distances are simulated."
)

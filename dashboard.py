
import streamlit as st
import pandas as pd
from decision_engine import evaluate_classroom
from room_recommender import recommend_room

st.set_page_config(
    page_title="Classroom Occupancy Agent",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 Intelligent Classroom Occupancy Agent")
st.caption("AI-powered classroom monitoring and utilization")

classrooms = pd.read_csv("data/classrooms.csv")

st.sidebar.header("Detection Simulator")
st.sidebar.caption("Use sample counts to test the dashboard.")

room_ids = classrooms["classroom_id"].tolist()
selected_room = st.sidebar.selectbox("Select classroom", room_ids)
detected_count = st.sidebar.number_input(
    "Detected people",
    min_value=0,
    max_value=500,
    value=25
)
accessible_required = st.sidebar.checkbox(
    "Require accessible classroom"
)

result = evaluate_classroom(selected_room, detected_count)
room_info = classrooms[
    classrooms["classroom_id"] == selected_room
].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("People detected", detected_count)
col2.metric("Room capacity", int(room_info["capacity"]))
col3.metric(
    "Capacity utilization",
    f"{detected_count / int(room_info['capacity']) * 100:.1f}%"
)

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

if detected_count > int(room_info["capacity"]):
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

st.subheader("All classrooms")
st.dataframe(classrooms, use_container_width=True)

st.caption(
    "Demo mode: counts are manually entered, and building distances "
    "are simulated. Live YOLO integration comes next."
)

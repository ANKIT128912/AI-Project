
import pandas as pd
import networkx as nx

CLASSROOMS_FILE = "data/classrooms.csv"


def build_building_graph():
    """Example walking connections between classrooms."""
    graph = nx.Graph()

    connections = [
        ("C101", "C102", 10),
        ("C101", "C201", 15),
        ("C102", "C202", 12),
        ("C201", "C202", 8),
        ("C201", "C301", 20),
        ("C202", "C302", 18),
        ("C301", "C401", 14),
        ("C302", "C401", 10),
    ]

    graph.add_weighted_edges_from(connections)
    return graph


def recommend_room(
    current_room,
    required_capacity,
    accessible_required=False
):
    classrooms = pd.read_csv(CLASSROOMS_FILE)
    graph = build_building_graph()

    if current_room not in graph:
        return None

    candidates = classrooms[
        (classrooms["capacity"] >= required_capacity)
        & (classrooms["classroom_id"] != current_room)
    ]

    if accessible_required:
        candidates = candidates[
            candidates["accessible"].astype(str).str.lower() == "true"
        ]

    recommendations = []

    for _, room in candidates.iterrows():
        room_id = room["classroom_id"]

        if room_id not in graph:
            continue

        try:
            distance = nx.shortest_path_length(
                graph,
                source=current_room,
                target=room_id,
                weight="weight"
            )
        except nx.NetworkXNoPath:
            continue

        recommendations.append({
            "classroom_id": room_id,
            "capacity": int(room["capacity"]),
            "distance": distance,
            "building": room["building"],
            "floor": int(room["floor"])
        })

    recommendations.sort(key=lambda item: item["distance"])
    return recommendations


if __name__ == "__main__":
    results = recommend_room(
        current_room="C101",
        required_capacity=45,
        accessible_required=True
    )

    if results:
        print("Recommended alternative classrooms:")
        for room in results:
            print(room)
    else:
        print("No suitable alternative classroom found.")

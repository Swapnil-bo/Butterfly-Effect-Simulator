def calculate_positions(nodes: list, spacing_y: int = 200) -> list:
    for i, node in enumerate(nodes):
        node["position"] = {"x": 250, "y": i * spacing_y}
    return nodes


def generate_edges(nodes: list) -> list:
    if len(nodes) < 2:
        raise ValueError("Need at least 2 nodes to generate edges.")
    return [
        {"id": f"e{i+1}-{i+2}", "source": nodes[i]["id"], "target": nodes[i+1]["id"]}
        for i in range(len(nodes) - 1)
    ]

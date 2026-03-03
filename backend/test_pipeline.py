"""
Phase 1 end-to-end test: user decision → LLM → nodes + positions + edges.
Usage: python test_pipeline.py "I bought a cheap guitar at a thrift store"
"""
import sys
import json
from ai_service import generate_timeline
from graph_math import calculate_positions, generate_edges

VALID_IMPACTS = {"low", "medium", "high", "life-changing"}


def run_pipeline(user_decision: str) -> dict:
    print(f'Input: "{user_decision}"')
    print("Calling Qwen 2.5 3B...\n")

    # Step 1: LLM generates raw nodes
    raw_nodes = generate_timeline(user_decision)

    # Step 2: Assign positions
    positioned_nodes = calculate_positions(raw_nodes)

    # Step 3: Generate edges
    edges = generate_edges(positioned_nodes)

    return {"nodes": positioned_nodes, "edges": edges}


def validate(result: dict) -> None:
    nodes = result["nodes"]
    edges = result["edges"]

    assert isinstance(nodes, list), "nodes is not a list"
    assert 5 <= len(nodes) <= 7, f"Expected 5-7 nodes, got {len(nodes)}"
    assert len(edges) == len(nodes) - 1, f"Expected {len(nodes)-1} edges, got {len(edges)}"

    for node in nodes:
        assert "id" in node, f"Missing id: {node}"
        assert "position" in node, f"Missing position: {node}"
        assert "year" in node.get("data", node), f"Missing year: {node}"
        assert "event" in node.get("data", node), f"Missing event: {node}"
        impact = node.get("data", node).get("impact")
        assert impact in VALID_IMPACTS, f"Invalid impact '{impact}' in {node['id']}"

    print("VALIDATION PASSED")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Impacts: {[n.get('data', n).get('impact') for n in nodes]}")


if __name__ == "__main__":
    decision = sys.argv[1] if len(sys.argv) > 1 else "I bought a cheap acoustic guitar at a thrift store"
    result = run_pipeline(decision)
    print(json.dumps(result, indent=2))
    print()
    validate(result)

"""
Milestone 3: JSONL Extraction → Graph Data Converter
=====================================================
Converts LangExtract JSONL output to {nodes, links} graph JSON
for 3D force-graph visualization.
"""
from __future__ import annotations
import json
import pathlib
import re
from collections import defaultdict

# Non-causal entity classes
ENTITY_CLASSES = {"person", "animal", "object", "place", "event", "emotion", "concept"}

# Group color mapping (for the 3D globe)
GROUP_COLORS = {
    "person": "#FF6B6B",    # Coral red
    "animal": "#4ECDC4",    # Teal
    "object": "#FFD93D",    # Gold
    "place": "#6BCB77",     # Green
    "event": "#FF8C42",     # Orange
    "emotion": "#C77DFF",   # Purple
    "concept": "#48B5E4",   # Blue
    "causal_chain": "#AAAAAA",  # Gray (for link-only)
}


def parse_causal_text(text: str) -> tuple[str, str, str] | None:
    """Parse '(因) A —[desc]→ (果) B' into (cause, relation, effect)."""
    # Pattern: (因) cause —[relation]→ (果) effect
    m = re.match(
        r'\(因\)\s*(.+?)\s*[—\-]\s*\[(.+?)\]\s*[→>]\s*\(果\)\s*(.+?)$',
        text.strip(),
    )
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    return None


def find_entity_node_id(name: str, node_ids: set[str], node_aliases: dict[str, str]) -> str:
    """Find best matching node ID for an entity name."""
    if name in node_ids:
        return name
    if name in node_aliases:
        return node_aliases[name]
    # Try fuzzy: if name contains a known entity or vice versa
    for nid in node_ids:
        if len(name) >= 2 and len(nid) >= 2:
            if name in nid or nid in name:
                return nid
    return name


def convert(jsonl_path: str, output_path: str) -> dict:
    """Convert JSONL to graph data."""
    docs = list(load_jsonl(jsonl_path))
    if not docs:
        raise ValueError("No documents in JSONL")

    doc = docs[0]
    extractions = doc.get("extractions", [])

    # Pass 1: Build entity nodes
    nodes: dict[str, dict] = {}
    node_aliases: dict[str, str] = {}  # alt_name → canonical_id

    for ext in extractions:
        cls = ext.get("extraction_class", "")
        if cls not in ENTITY_CLASSES:
            continue

        text = ext.get("extraction_text", "").strip()
        if not text:
            continue

        char_interval = ext.get("char_interval", {})
        attrs = ext.get("attributes", {}) or {}

        if text in nodes:
            # Update with additional context if available
            existing = nodes[text]
            if attrs and not existing.get("attributes"):
                existing["attributes"] = attrs
            continue

        nodes[text] = {
            "id": text,
            "group": cls,
            "color": GROUP_COLORS.get(cls, "#AAAAAA"),
            "char_interval": char_interval,
            "attributes": attrs,
            "connections": 0,
        }

    node_ids = set(nodes.keys())

    # Pass 2: Build links from causal chains
    links: list[dict] = []
    link_set = set()  # (source, target, relation) for dedup

    for ext in extractions:
        cls = ext.get("extraction_class", "")
        if cls != "causal_chain":
            continue

        text = ext.get("extraction_text", "").strip()
        parsed = parse_causal_text(text)
        if not parsed:
            continue

        cause_text, relation, effect_text = parsed
        char_interval = ext.get("char_interval", {})
        attrs = ext.get("attributes", {}) or {}

        # Find node IDs
        source_id = find_entity_node_id(cause_text, node_ids, node_aliases)
        target_id = find_entity_node_id(effect_text, node_ids, node_aliases)

        # Create nodes if they don't exist (for compound event names)
        for node_text, node_cls in [(source_id, attrs.get("cause_type", "event")),
                                     (target_id, attrs.get("effect_type", "event"))]:
            if node_text not in nodes:
                nodes[node_text] = {
                    "id": node_text,
                    "group": node_cls if node_cls in ENTITY_CLASSES else "event",
                    "color": GROUP_COLORS.get(node_cls if node_cls in ENTITY_CLASSES else "event", "#AAAAAA"),
                    "char_interval": char_interval,
                    "attributes": {},
                    "connections": 0,
                }
                node_ids.add(node_text)

        link_key = (source_id, target_id, relation)
        if link_key in link_set:
            continue
        link_set.add(link_key)

        nodes[source_id]["connections"] = nodes[source_id].get("connections", 0) + 1
        nodes[target_id]["connections"] = nodes[target_id].get("connections", 0) + 1

        links.append({
            "source": source_id,
            "target": target_id,
            "relation": relation,
            "description": f"(因) {cause_text} —[{relation}]→ (果) {effect_text}",
            "char_interval": char_interval,
        })

    # Pass 3: Create entity-event participation links
    entity_ids = {nid for nid, nd in nodes.items() if nd["group"] in ENTITY_CLASSES}
    event_ids = {nid for nid, nd in nodes.items() if nd["group"] == "event"}

    for event_id in sorted(event_ids):
        for entity_id in sorted(entity_ids):
            if entity_id in event_id:
                link_key = (entity_id, event_id, "participates_in")
                if link_key not in link_set:
                    link_set.add(link_key)
                    nodes[entity_id]["connections"] = nodes[entity_id].get("connections", 0) + 1
                    nodes[event_id]["connections"] = nodes[event_id].get("connections", 0) + 1
                    # Get char_interval from event node
                    ci = nodes[event_id].get("char_interval", {})
                    links.append({
                        "source": entity_id,
                        "target": event_id,
                        "relation": "participates_in",
                        "description": f'{entity_id} participates in {event_id}',
                        "char_interval": ci,
                    })

    # Pass 4: Calculate node sizes based on connections
    node_list = list(nodes.values())
    max_conn = max((n.get("connections", 0) for n in node_list), default=1)
    for n in node_list:
        conn = n.get("connections", 0)
        n["size"] = max(3, 3 + (conn / max(max_conn, 1)) * 8)

    graph = {
        "nodes": node_list,
        "links": links,
        "metadata": {
            "total_nodes": len(node_list),
            "total_links": len(links),
            "entity_types": list(
                sorted(set(n["group"] for n in node_list))
            ),
            "source_text": doc.get("text", ""),
        },
    }

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"Graph data saved to: {output_path}")
    print(f"Nodes: {len(node_list)}")
    print(f"Links: {len(links)}")
    print(f"\nNodes by group:")
    groups = defaultdict(int)
    for n in node_list:
        groups[n["group"]] += 1
    for g, c in sorted(groups.items()):
        print(f"  {g}: {c}")

    return graph


def load_jsonl(path: str) -> list[dict]:
    """Load JSONL file, returns list of parsed JSON objects."""
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    return docs


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert JSONL to graph data")
    parser.add_argument("--input", default="extraction_results.jsonl", help="Input JSONL file")
    parser.add_argument("--output", default="graph_data.json", help="Output graph JSON file")
    args = parser.parse_args()

    convert(args.input, args.output)


if __name__ == "__main__":
    main()

"""
Milestone 5: Quality Check & Data Cleaning
==========================================
Validates graph_data.json quality:
- Checks for duplicate nodes
- Identifies isolated nodes (no links)
- Validates all link references
- Reports statistics
- Optionally auto-cleans issues
"""
from __future__ import annotations
import json
import pathlib
from collections import Counter, defaultdict


def quality_check(graph_path: str, auto_fix: bool = False) -> dict:
    """Run quality checks on graph data."""
    g = json.loads(pathlib.Path(graph_path).read_text(encoding="utf-8"))
    nodes = g.get("nodes", [])
    links = g.get("links", [])

    report = {
        "total_nodes": len(nodes),
        "total_links": len(links),
        "issues": [],
        "warnings": [],
        "stats": {},
    }

    node_ids = set()
    node_id_list = []

    # ── Check 1: Duplicate nodes ──
    seen_ids = {}
    dups = []
    for i, n in enumerate(nodes):
        nid = n.get("id", "")
        if nid in seen_ids:
            dups.append((nid, seen_ids[nid], i))
        else:
            seen_ids[nid] = i
        node_ids.add(nid)
        node_id_list.append(nid)

    if dups:
        report["issues"].append({
            "type": "duplicate_nodes",
            "count": len(dups),
            "details": [{"id": d[0], "first_index": d[1], "dup_index": d[2]} for d in dups],
        })

    # ── Check 2: Broken links ──
    broken = []
    for i, l in enumerate(links):
        sid = l.get("source", "")
        tid = l.get("target", "")
        if sid not in node_ids:
            broken.append({"link_index": i, "missing_source": sid, "target": tid})
        if tid not in node_ids:
            broken.append({"link_index": i, "source": sid, "missing_target": tid})

    if broken:
        report["issues"].append({
            "type": "broken_links",
            "count": len(broken),
            "details": broken,
        })

    # ── Check 3: Isolated nodes ──
    connected = set()
    for l in links:
        connected.add(l.get("source", ""))
        connected.add(l.get("target", ""))

    isolated = [nid for nid in node_ids if nid not in connected]
    if isolated:
        report["warnings"].append({
            "type": "isolated_nodes",
            "count": len(isolated),
            "details": isolated,
        })

    # ── Check 4: Nodes with same name but different IDs ──
    name_counts = Counter(node_id_list)
    similar_names = {k: v for k, v in name_counts.items() if v > 1}
    if similar_names:
        report["warnings"].append({
            "type": "reused_names",
            "details": dict(similar_names),
        })

    # ── Stats ──
    group_dist = Counter(n.get("group", "unknown") for n in nodes)
    conn_dist = [n.get("connections", 0) for n in nodes]
    report["stats"] = {
        "groups": dict(group_dist.most_common()),
        "max_connections": max(conn_dist) if conn_dist else 0,
        "min_connections": min(conn_dist) if conn_dist else 0,
        "avg_connections": round(sum(conn_dist) / len(conn_dist), 1) if conn_dist else 0,
        "nodes_without_connections": sum(1 for c in conn_dist if c == 0),
        "density": round(len(links) / (len(nodes) * (len(nodes) - 1) / 2), 4) if len(nodes) > 1 else 0,
    }

    # ── Auto-fix ──
    if auto_fix and (dups or broken):
        # Remove duplicate nodes
        if dups:
            dup_indices = {d["dup_index"] for d in dups}
            g["nodes"] = [n for i, n in enumerate(nodes) if i not in dup_indices]
            print(f"  Removed {len(dup_indices)} duplicate node(s)")

        # Remove broken links
        if broken:
            broken_indices = {b["link_index"] for b in broken}
            g["links"] = [l for i, l in enumerate(links) if i not in broken_indices]
            print(f"  Removed {len(broken_indices)} broken link(s)")

        # Update metadata
        g["metadata"]["total_nodes"] = len(g["nodes"])
        g["metadata"]["total_links"] = len(g["links"])

        pathlib.Path(graph_path).write_text(
            json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  Cleaned graph saved to: {graph_path}")

    return report


def print_report(report: dict):
    """Pretty-print quality report."""
    print("=" * 55)
    print("  Graph Data Quality Report")
    print("=" * 55)
    print(f"  Nodes: {report['total_nodes']}")
    print(f"  Links: {report['total_links']}")
    print(f"  Issues: {sum(len(i.get('details',[])) for i in report['issues'])}")
    print(f"  Warnings: {sum(len(w.get('details',[])) for w in report['warnings'])}")
    print()

    for issue in report["issues"]:
        print(f"  [ISSUE] {issue['type']}: {issue['count']} occurrences")
        for d in issue.get("details", [])[:5]:
            print(f"    - {d}")

    for warn in report["warnings"]:
        print(f"  [WARN] {warn['type']}: {warn['count']} occurrences")

    print()
    print("  Statistics:")
    stats = report["stats"]
    print(f"    Group distribution: {stats['groups']}")
    print(f"    Connections: max={stats['max_connections']}, min={stats['min_connections']}, avg={stats['avg_connections']}")
    print(f"    Isolated nodes: {stats['nodes_without_connections']}")
    print(f"    Graph density: {stats['density']}")
    print("=" * 55)

    if report["issues"]:
        print("\n  ⚠ Graph has issues. Run with --fix to auto-clean.")
    else:
        print("\n  [OK] Graph data is clean.")


def main():
    import argparse
    p = argparse.ArgumentParser(description="Quality check graph data")
    p.add_argument("--input", default="graph_data.json", help="Graph JSON file")
    p.add_argument("--fix", action="store_true", help="Auto-fix issues")
    args = p.parse_args()

    report = quality_check(args.input, auto_fix=args.fix)
    print_report(report)


if __name__ == "__main__":
    main()

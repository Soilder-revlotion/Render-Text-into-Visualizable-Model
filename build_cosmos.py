"""
Build cosmos.html from template, and graph_data.js from graph_data.json.
graph_data.js is loaded via <script> tag (no CORS issues with file://).
"""
import json, pathlib

def build():
    # Generate graph_data.js
    g = json.loads(pathlib.Path("graph_data.json").read_text(encoding="utf-8"))
    js = "var FULL_GRAPH = " + json.dumps(g, ensure_ascii=False) + ";"
    pathlib.Path("graph_data.js").write_text(js, encoding="utf-8")
    print(f"Generated graph_data.js ({len(js)} bytes, {len(g['nodes'])} nodes, {len(g['links'])} links)")

    # Generate cosmos.html from template
    template = pathlib.Path("cosmos_template.html").read_text(encoding="utf-8")
    out = pathlib.Path("cosmos.html")
    out.write_text(template, encoding="utf-8")
    print(f"Generated cosmos.html ({len(template)} bytes)")

if __name__ == "__main__":
    build()

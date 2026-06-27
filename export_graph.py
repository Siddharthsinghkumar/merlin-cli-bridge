from pathlib import Path


def export_graph(graph, export_html):
    output_dir = Path("graphify-out")
    output_dir.mkdir(parents=True, exist_ok=True)
    export_html(graph, str(output_dir / "graph.html"))

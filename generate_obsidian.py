import json
import os
import re

def safe_filename(name):
    # Replace invalid filename characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def main():
    graph_path = "/home/sidd/project/merlin-cli-bridge/graphify-out/graph.json"
    vault_dir = "/home/sidd/project/merlin-cli-bridge/obsidian_vault"
    
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)
        
    with open(graph_path, 'r') as f:
        data = json.load(f)
        
    nodes = data.get('nodes', [])
    links = data.get('links', [])
    
    # Map node id to node data for easy lookup
    node_map = {n['id']: n for n in nodes}
    
    for node in nodes:
        node_id = node['id']
        filename = safe_filename(node_id) + ".md"
        filepath = os.path.join(vault_dir, filename)
        
        # Find related links
        outgoing = [link for link in links if link['source'] == node_id]
        incoming = [link for link in links if link['target'] == node_id]
        
        with open(filepath, 'w') as f:
            f.write(f"# {node.get('label', node_id)}\n\n")
            f.write("## Metadata\n")
            f.write(f"- **Type:** {node.get('file_type', 'unknown')}\n")
            f.write(f"- **File:** {node.get('source_file', 'unknown')}\n")
            f.write(f"- **Location:** {node.get('source_location', 'unknown')}\n")
            f.write(f"- **Origin:** {node.get('_origin', 'unknown')}\n")
            
            f.write("\n## Outgoing Links (Dependencies)\n")
            if not outgoing:
                f.write("None\n")
            for link in outgoing:
                target_id = link['target']
                target_name = safe_filename(target_id)
                edge_type = link.get('type', 'relates to')
                f.write(f"- {edge_type} [[{target_name}]]\n")
                
            f.write("\n## Incoming Links (Dependents)\n")
            if not incoming:
                f.write("None\n")
            for link in incoming:
                source_id = link['source']
                source_name = safe_filename(source_id)
                edge_type = link.get('type', 'relates to')
                f.write(f"- {edge_type} from [[{source_name}]]\n")

if __name__ == '__main__':
    main()

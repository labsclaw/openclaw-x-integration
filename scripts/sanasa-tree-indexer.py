import asyncio
import json
import os
import re
from pageindex.page_index_md import md_to_tree

"""
sanasa-tree-indexer.py
Indexer estrutural de especificações e requisitos (RFs) da SANASA baseado na arquitetura PageIndex / Tree-RAG.
Elimina o chunking arbitrário e preserva a rastreabilidade hierárquica de cada requisito para os agentes de teste.
"""

def extract_rf_metadata(text):
    rfs = re.findall(r"(RF\d{3})", text)
    return list(set(rfs))

async def index_sanasa_specifications():
    spec_files = [
        "memory/segments/x-testing-sanasa-operation.md",
        "memory/segments/x-testing-sanasa-contract.md",
        "memory/segments/x-testing-standards-metrics.md"
    ]
    
    combined_index = {
        "project": "X-Testing SANASA ALM Test Factory",
        "indexer": "PageIndex Tree-RAG",
        "timestamp": "2026-09-18",
        "domains": []
    }
    
    for file_path in spec_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"[*] Indexando especificação estrutural: {file_path}")
        tree_res = await md_to_tree(
            md_path=file_path,
            if_add_node_id='yes',
            if_add_node_text='yes',
            if_thinning=False
        )
        
        structure = tree_res.get("structure", []) if isinstance(tree_res, dict) else tree_res
        
        def enrich_nodes(nodes):
            enriched = []
            for node in nodes:
                text = node.get("text", "")
                rfs = extract_rf_metadata(text)
                entry = {
                    "node_id": node.get("node_id"),
                    "title": node.get("title"),
                    "line_num": node.get("line_num"),
                    "char_count": len(text),
                    "associated_rfs": rfs,
                    "summary_preview": text.strip().split("\n")[0][:150] if text else "",
                }
                if "nodes" in node and node["nodes"]:
                    entry["children"] = enrich_nodes(node["nodes"])
                enriched.append(entry)
            return enriched
            
        domain_tree = enrich_nodes(structure)
        combined_index["domains"].append({
            "source_file": file_path,
            "tree": domain_tree
        })
        
    os.makedirs("artifacts/x-testing", exist_ok=True)
    out_path = "artifacts/x-testing/sanasa-requirements-tree.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined_index, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Árvore de requisitos SANASA consolidada com sucesso em: {out_path}")
    return combined_index

if __name__ == "__main__":
    asyncio.run(index_sanasa_specifications())

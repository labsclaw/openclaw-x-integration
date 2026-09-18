import asyncio
import json
import time
import os
from pageindex.page_index_md import md_to_tree

async def run_benchmark():
    print("==========================================================")
    print("   BENCHMARK / TESTE DE BANCADA: PAGEINDEX (TREE RAG)   ")
    print("==========================================================")
    
    target_doc = "memory/segments/x-testing-sanasa-operation.md"
    if not os.path.exists(target_doc):
        target_doc = "README.md"
        
    print(f"[*] Documento alvo de teste: {target_doc}")
    doc_size = os.path.getsize(target_doc)
    print(f"[*] Tamanho do documento: {doc_size} bytes")
    
    t0 = time.time()
    tree_result = await md_to_tree(
        md_path=target_doc,
        if_add_node_id='yes',
        if_add_node_text='yes',
        if_thinning=False
    )
    t1 = time.time()
    
    gen_time_ms = (t1 - t0) * 1000
    print(f"\n[+] Árvore hierárquica gerada com sucesso em {gen_time_ms:.2f} ms")
    
    # Extract structure list
    structure = tree_result.get("structure", []) if isinstance(tree_result, dict) else tree_result
    
    flat_nodes = []
    def traverse(nodes, depth=0):
        for n in nodes:
            node_id = n.get("node_id", "N/A")
            title = n.get("title", "Sem título")
            text = n.get("text", "")
            flat_nodes.append({
                "depth": depth,
                "node_id": node_id,
                "title": title,
                "char_length": len(text),
                "line_num": n.get("line_num", 0)
            })
            if "nodes" in n and n["nodes"]:
                traverse(n["nodes"], depth + 1)

    traverse(structure)
    total_nodes = len(flat_nodes)
    max_depth = max([n["depth"] for n in flat_nodes]) if flat_nodes else 0
    
    print(f"[+] Total de nós na árvore: {total_nodes}")
    print(f"[+] Profundidade máxima da hierarquia: {max_depth}")
    print("\n--- Estrutura Hierárquica Extraída (Amostra) ---")
    for s in flat_nodes[:15]:
        indent = "  " * s["depth"]
        print(f"{indent}├─ [{s['node_id']}] {s['title']} ({s['char_length']} chars, linha {s['line_num']})")
    if len(flat_nodes) > 15:
        print(f"  ... e mais {len(flat_nodes) - 15} nós estruturados.")
        
    # Test reasoning-based retrieval simulation (locating exact section without vector similarity)
    print("\n==========================================================")
    print("   SIMULAÇÃO DE RECUPERAÇÃO POR RACIOCÍNIO NA ÁRVORE      ")
    print("==========================================================")
    queries = [
        "Quais são as ordens de serviço e regras de negócio da SANASA?",
        "Qual é o organograma e os papéis dos agentes da X-Testing?",
        "Métricas de performance e TestLink"
    ]
    
    query_results = []
    for query in queries:
        print(f"\nQuery: \"{query}\"")
        keywords = [w.lower() for w in query.replace("?", "").replace(",", "").split() if len(w) > 3]
        matches = []
        for s in flat_nodes:
            score = sum(1 for kw in keywords if kw in s["title"].lower())
            if score > 0:
                matches.append((score, s))
        matches.sort(key=lambda x: x[0], reverse=True)
        top_matches = [m[1] for m in matches[:3]]
        for r in top_matches:
            indent = "  " * r["depth"]
            print(f"{indent}★ Rota de Navegação: [{r['node_id']}] {r['title']} (Nível {r['depth']})")
        query_results.append({
            "query": query,
            "top_nodes": top_matches
        })
        
    report = {
        "benchmark": "PageIndex Tree-RAG Spike",
        "document": target_doc,
        "document_bytes": doc_size,
        "generation_time_ms": gen_time_ms,
        "total_nodes": total_nodes,
        "max_depth": max_depth,
        "structure": flat_nodes,
        "queries_simulated": query_results,
        "status": "SUCCESS"
    }
    
    os.makedirs("memory/reports", exist_ok=True)
    report_path = "memory/reports/pageindex-bench-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"\n[+] Relatório de benchmark salvo em: {report_path}")
    print("==========================================================")

if __name__ == "__main__":
    asyncio.run(run_benchmark())

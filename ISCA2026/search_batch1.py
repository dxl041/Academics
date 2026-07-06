#!/usr/bin/env python3
"""Search arxiv for remaining ISCA 2026 papers - batch 1: Security + PIM"""
import urllib.request, urllib.parse, json, re, time, os, sys

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

PAPERS = [
    # Security 3C
    ("Security","3C","Interrupt Side-Channel Attacks macOS Apple Silicon"),
    ("Security","3C","Helium Quantifying Microarchitectural Side-Channel Leakage Probabilistic Guarantees"),
    ("Security","3C","LAEGIS Pinpointing Performance Overheads GPU Confidential Computing"),
    ("Security","3C","MC-ORAM Mask-Assisted Counter-Based Non-Deterministic ORAM VM-Based TEE"),
    ("Security","3C","TimeGaps Channels Exploiting CPU Halted Time"),
    # Security 5C
    ("Security","5C","muRNG Framework Assessing Randomness Intermittent Computing Devices"),
    ("Security","5C","IroKnight Ownership-Preserving Neural Acceleration Inference Serving"),
    ("Security","5C","Intermittence-aware Speculative Page Coloring Secure NVM"),
    ("Security","5C","LIPPEN Lightweight In-Place Pointer Encryption Architecture Pointer Integrity"),
    ("Security","5C","DarkStream Exploiting Internal Throughput Contention Data Streaming Accelerator"),
    # Security 6D
    ("Security","6D","ColumnKeeper Efficient Solutions ColumnDisturb Vulnerability DRAM"),
    ("Security","6D","PVAC RowHammer Mitigation Architecture Per-victim-row Counting"),
    ("Security","6D","Loaded Dice Solving Non-Selection Problem Probabilistic RowHammer Defense"),
    ("Security","6D","PRowhammer Propagating Bit-flips CPU GPU"),
    ("Security","6D","DejaVu Why You Should Write DRAM Rows Twice Carefully"),
    # PIM/PNM
    ("PIM","2B","ECC Enabled Reliable Performant Processing-in-Memory"),
    ("PIM","2B","HBM-CASO Coordinated Approach HBM System-Level On-Die ECC"),
    ("PIM","2B","ATX Accelerator Task Extensions"),
    ("PIM","3B","Taking Analytic Databases Bank DRAM near-memory"),
    ("PIM","3B","PuDGhost Experimental Analysis Computation Result Corruption DRAM real chips"),
    ("PIM","3B","MERIDIAN In-Memory Acceleration RAG Document Attention Decomposition"),
    ("PIM","3B","PipeIMC Pipelined In-SRAM Computing Architecture"),
    ("PIM","3B","BAAP Coupling Compute-in-SRAM DRAM Banks Near-Memory Processing"),
    ("PIM","10C","AXLE Coordinated Offloading Asynchronous Back-Streaming Computational Memory"),
    ("PIM","10C","DCC Data-Centric Compilation Machine Learning Kernels Processing-In-Memory"),
    ("PIM","10C","Optimizing Spatial Data Structure Near-Cache Acceleration Physical Locality"),
    ("PIM","10C","Bridging Efficiency Scalability LLM 3D Hybrid PIM 2D In-Transit"),
    ("PIM","10C","Early Silicon Raptor First 3D-DRAM Accelerator Generative Inference"),
]

def search(query):
    encoded = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=ti:{encoded}&max_results=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode()
    except Exception as e:
        return None

def find_match(xml_data, target):
    entries = re.findall(r'<entry>(.*?)</entry>', xml_data, re.DOTALL)
    if not entries:
        return None
    target_w = set(w.lower() for w in re.findall(r'\w+', target) if len(w)>2)
    best, best_s = None, 0
    for e in entries:
        tm = re.search(r'<title>(.*?)</title>', e)
        if not tm: continue
        tw = set(w.lower() for w in re.findall(r'\w+', tm.group(1)) if len(w)>2)
        if not target_w or not tw: continue
        s = len(target_w & tw) / max(len(target_w | tw), 1)
        if 'ISCA 2026' in e or 'isca 2026' in e.lower(): s += 0.3
        if s > best_s and s > 0.15:
            best_s = s
            im = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', e)
            am = re.search(r'<summary>(.*?)</summary>', e, re.DOTALL)
            best = {"id": im.group(1) if im else "", "title": tm.group(1), "abstract": am.group(1).replace('\n',' ') if am else "", "score": round(s,3)}
    return best

results = []
for cat, sess, q in PAPERS:
    print(f"[{cat}/{sess}] {q[:60]}...", flush=True)
    xml = search(q[:120])
    if xml:
        m = find_match(xml, q)
        if m:
            m["cat"] = cat; m["sess"] = sess
            results.append(m)
            print(f"  ✓ arxiv:{m['id']} score={m['score']}", flush=True)
        else:
            # fallback: search with 'all' field
            xml2 = search(f"all:{q[:120]}")
            if xml2:
                m2 = find_match(xml2, q)
                if m2:
                    m2["cat"] = cat; m2["sess"] = sess
                    results.append(m2)
                    print(f"  ✓(all) arxiv:{m2['id']} score={m2['score']}", flush=True)
                else:
                    print("  ✗", flush=True)
            else:
                print("  ✗", flush=True)
    else:
        print("  ✗", flush=True)
    time.sleep(2.5)  # Conservative rate limiting

with open("/home/dxl/Academics/ISCA2026/arxiv_batch1.json", "w") as f:
    json.dump({"found": len(results), "papers": results}, f, ensure_ascii=False, indent=2)
print(f"\nDone: {len(results)} found")

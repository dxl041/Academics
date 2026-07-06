#!/usr/bin/env python3
"""Search arxiv for remaining ISCA 2026 papers - batch 2: ML Accel + Quantum + FHE + remaining LLM"""
import urllib.request, urllib.parse, json, re, time, os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

PAPERS = [
    # ML Accelerators 3A
    ("ML","3A","Shining Light Silicon Photonic DNN Accelerators"),
    ("ML","3A","TensorPrism Rethinking Sparse High-order Tensor Acceleration Co-occurrence Graph"),
    ("ML","3A","OASIS Outlier-Aware LUT-Based GEMM Dual-Side Quantization LLM"),
    ("ML","3A","Omni-LUT Energy-Efficient LUT-based Accelerator KV Cache Quantization"),
    ("ML","3A","QiMeng-Tensify Scaling Tensor Computation Optimization LLM-Guided MCTS"),
    # ML Accelerators 10B  
    ("ML","10B","Dynamic Scheduling AI Accelerators TISA"),
    ("ML","10B","MXFFP Microscaling Flexible Floating Point Format AI Model Acceleration"),
    ("ML","10B","UniCore Bit-Width Scalable GEMM Unit Unified LLM Inference"),
    ("ML","10B","XtraMAC Efficient MAC Architecture Mixed-Precision LLM Inference FPGA"),
    ("ML","10B","ELSA Elastic SNN Inference Architecture Efficient Neuromorphic Computing"),
    # Quantum 4D
    ("Quantum","4D","Triage Adaptive Parallel Window Decoding Scheduler Real-time Fault-Tolerant Quantum"),
    ("Quantum","4D","Coset Ensemble Decoder Quantum Error Correction Algorithm-Hardware Co-Design"),
    ("Quantum","4D","Streaming Architecture Quantum Error Syndrome Compression 4 Kelvin"),
    ("Quantum","4D","Transpiler-Architecture Co-Design Curb Clifford Costs Fault-Tolerant Quantum"),
    ("Quantum","4D","Kernpiler Compiler Optimization Quantum Hamiltonian Simulation Partial Trotterization"),
    # Quantum 8C
    ("Quantum","8C","Distilling Magic States Bicycle Architecture"),
    ("Quantum","8C","O3LS Optimizing Lattice Surgery Automatic Layout Searching Loose Scheduling"),
    ("Quantum","8C","Leveraging Phase Polynomials Quantum Circuit Optimization"),
    # Quantum 9C
    ("Quantum","9C","Unifying Qubit Routing Diverse Quantum ISAs Canonical Representation"),
    ("Quantum","9C","TUSQ Tracking Uncomputation Sampling Noisy Quantum Simulation"),
    ("Quantum","9C","Photonic Quantum Computing Spin Memory Architecture Tree-Encoded Fusion"),
    ("Quantum","9C","SATIC Optimizing Ising Compiler SATisfiability"),
    # FHE 7D
    ("FHE","7D","FEnc2 Unifying Data Packing Efficient Private Inference Fragment Encoding"),
    ("FHE","7D","FlashTFHE Scalable Architecture Efficient Multi-bit Fully Homomorphic Encryption"),
    ("FHE","7D","Unlocking Pipeline Parallelism Bootstrapping Pipelined Multi-Chiplet TFHE"),
    ("FHE","7D","HE2 Communication-Light Heterogeneous Architecture Efficient FHE"),
    ("FHE","7D","HyperDrive Hierarchical Exploitation Memory Efficiency GPU-Based FHE"),
    ("FHE","7D","MNEMOS GPU-based TFHE Acceleration Framework Memory Access Optimization"),
    # Remaining LLM papers not yet found
    ("LLM","1A","MLX Multi-Layer Execution Structured LLM Workload Acceleration Spatial"),
    ("LLM","4A","HybridSpec Exploiting Hybrid-bonding Memory Accelerate LLM Serving Heterogeneous"),
    ("LLM","4A","CHIME Efficient Long-Context Attention-FC Disaggregated Inference DIMM-PIM"),
    ("LLM","4A","SMOOTH Hardware-Assisted Fine-Grained On-Chip Memory Management LLM"),
    ("LLM","4A","SHyLA 3D-Stacked NVM-DRAM Hybrid LLM-Inference Architecture"),
    ("LLM","5A","ConServe Contiguity-Preserving Memory Management Multi-Turn LLM Serving"),
    ("LLM","5A","Mapping Communication Optimizations Fault Tolerance Wafer-Scale LLM Inference"),
    ("LLM","5A","DynoPipe Heterogeneous Edge-Cloud LLM Serving Pipeline Boundaries"),
    ("LLM","5A","DIAMoND Dynamic Inference Adaptive Edge MoE Heterogeneous In-NAND"),
    ("LLM","5A","SingularBit Exploiting Synergy SVD Low-Bit Quantization LLM Inference"),
    ("LLM","6A","Tetris Efficient Long-context LLM Serving Chunkwise Dynamic Sequence Parallelism"),
    ("LLM","6A","SMoE Algorithm-System Co-Design Pushing MoE Edge Expert Substitution"),
    ("LLM","6A","ENEC Lossless AI Model Compression Fast Inference Ascend NPUs"),
    ("LLM","6A","STEP Adaptive Spatio-Temporal Expert Prefetching MoE Inference"),
    ("LLM","6A","EVA Accelerating LLM Decoding Efficient Vector Quantization Architecture"),
    ("LLM","10A","Scalable Synthesis Distributed LLM Workloads Symbolic Tensor Graphs"),
    ("LLM","10A","DisDP Disaggregating Compute Network Storage Model-Sharded Data-Parallel"),
    ("LLM","10A","MoE-Hub Taming Software Complexity Seamless MoE Overlap Communication"),
    ("LLM","10A","Symbiotic MLLM Serving Dynamically Balancing Parallelism GPUs"),
]

def search(query, field="ti"):
    encoded = urllib.parse.quote(query[:150])
    url = f"https://export.arxiv.org/api/query?search_query={field}:{encoded}&max_results=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode()
    except:
        return None

def find_match(xml_data, target):
    entries = re.findall(r'<entry>(.*?)</entry>', xml_data, re.DOTALL)
    if not entries: return None
    target_w = set(w.lower() for w in re.findall(r'\w+', target) if len(w)>2)
    best, best_s = None, 0
    for e in entries:
        tm = re.search(r'<title>(.*?)</title>', e)
        if not tm: continue
        tw = set(w.lower() for w in re.findall(r'\w+', tm.group(1)) if len(w)>2)
        if not target_w or not tw: continue
        s = len(target_w & tw) / max(len(target_w | tw), 1)
        if 'ISCA 2026' in e: s += 0.4
        if s > best_s and s > 0.12:
            best_s = s
            im = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', e)
            am = re.search(r'<summary>(.*?)</summary>', e, re.DOTALL)
            best = {"id": im.group(1) if im else "", "title": tm.group(1), "abstract": am.group(1).replace('\n',' ') if am else "", "score": round(s,3)}
    return best

results = []
for cat, sess, q in PAPERS:
    short = q[:60]
    print(f"[{cat}/{sess}] {short}...", flush=True)
    # Try title search first
    xml = search(q, "ti")
    m = None
    if xml: m = find_match(xml, q)
    if not m:
        # Fall back to all-field search
        xml = search(q, "all")
        if xml: m = find_match(xml, q)
    
    if m:
        m["cat"] = cat; m["sess"] = sess
        results.append(m)
        tag = "ISCA" if "ISCA 2026" in str(m) else ""
        print(f"  ✓ arxiv:{m['id']} score={m['score']} {tag}", flush=True)
    else:
        print("  ✗", flush=True)
    time.sleep(2.0)

path = "/home/dxl/Academics/ISCA2026/arxiv_batch2.json"
with open(path, "w") as f:
    json.dump({"found": len(results), "papers": results}, f, ensure_ascii=False, indent=2)
print(f"\nDone: {len(results)}/{len(PAPERS)} found. Saved to {path}")

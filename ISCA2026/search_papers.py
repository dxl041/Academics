#!/usr/bin/env python3
"""Search arxiv for ISCA 2026 hot-session papers and extract abstracts."""
import urllib.request, urllib.parse, json, re, time, sys, os

# Proxy configuration
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

# Short unique search queries for each paper
PAPERS = [
    # === LLM Sessions (1A, 2A, 4A, 5A, 6A, 10A) ===
    ("LLM", "1A", "MLX: Multi-Layer Execution Structured LLM Workload Acceleration Spatial Architectures"),
    ("LLM", "1A", "CODO: Automated Compiler Comprehensive Dataflow Optimization"),
    ("LLM", "1A", "COSM: Cooperative Scheduling Framework Concurrent PIM CPU Execution Mobile"),
    ("LLM", "1A", "Cerberus: Cross-Layer ECC Co-Design Robust Efficient Memory Protection"),
    ("LLM", "1A", "Patterns Behind Chaos: Forecasting Data Movement Efficient MoE LLM Inference"),
    ("LLM", "2A", "Cassandra: Enabling Reasoning LLMs Edge Self-Speculative Decoding"),
    ("LLM", "2A", "Combating Memory Walls: Optimization Pathways Long-Context Agentic LLM Inference"),
    ("LLM", "2A", "Approaching Shannon Bound Lossless LLM Weight Compression"),
    ("LLM", "4A", "HybridSpec: Exploiting Hybrid-bonding Memory Accelerate LLM Serving"),
    ("LLM", "4A", "P3-LLM: Integrated NPU-PIM Accelerator Edge LLM Inference Hybrid Numerical"),
    ("LLM", "4A", "CHIME: Efficient Long-Context Attention-FC Disaggregated Inference DIMM-PIM"),
    ("LLM", "4A", "SMOOTH: Hardware-Assisted Fine-Grained On-Chip Memory Management LLM"),
    ("LLM", "4A", "SHyLA: 3D-Stacked NVM-DRAM Hybrid LLM-Inference Architecture"),
    ("LLM", "5A", "Accelerating MoE Dynamic In-Switch Computing Multi-GPUs"),
    ("LLM", "5A", "ConServe: Contiguity-Preserving Memory Management Multi-Turn LLM Serving"),
    ("LLM", "5A", "Mapping Communication Optimizations Fault Tolerance Wafer-Scale LLM Inference"),
    ("LLM", "5A", "DynoPipe: Heterogeneous Edge-Cloud LLM Serving Pipeline Boundaries"),
    ("LLM", "5A", "DIAMoND: Dynamic Inference Adaptive Edge MoE Heterogeneous In-NAND Near-DRAM"),
    ("LLM", "5A", "SingularBit: Exploiting Synergy SVD Low-Bit Quantization LLM Inference"),
    ("LLM", "6A", "Tetris: Efficient Long-context LLM Serving Chunkwise Dynamic Sequence Parallelism"),
    ("LLM", "6A", "SMoE: Algorithm-System Co-Design Pushing MoE Edge Expert Substitution"),
    ("LLM", "6A", "ENEC: Lossless AI Model Compression Fast Inference Ascend NPUs"),
    ("LLM", "6A", "STEP: Adaptive Spatio-Temporal Expert Prefetching MoE Inference"),
    ("LLM", "6A", "EVA: Accelerating LLM Decoding Efficient Vector Quantization Architecture"),
    ("LLM", "10A", "Scalable Synthesis Distributed LLM Workloads Symbolic Tensor Graphs"),
    ("LLM", "10A", "DisDP: Disaggregating Compute Network Storage Model-Sharded Data-Parallel"),
    ("LLM", "10A", "MoE-Hub: Taming Software Complexity Seamless MoE Overlap Communication"),
    ("LLM", "10A", "Symbiotic MLLM Serving Dynamically Balancing Parallelism GPUs"),
    
    # === Security Sessions (3C, 5C, 6D) ===
    ("Security", "3C", "Practical Interrupt Side-Channel Attacks macOS Apple Silicon"),
    ("Security", "3C", "Helium: Quantifying Microarchitectural Side-Channel Leakage Probabilistic"),
    ("Security", "3C", "LAEGIS: Pinpointing Addressing Performance Overheads GPU Confidential Computing"),
    ("Security", "3C", "MC-ORAM: Mask-Assisted Counter-Based Non-Deterministic ORAM VM-Based TEE"),
    ("Security", "3C", "TimeGaps Channels: Exploiting CPU Halted Time Fun Profit"),
    ("Security", "5C", "muRNG: Framework Assessing Randomness Intermittent Computing Devices"),
    ("Security", "5C", "IroKnight: Ownership-Preserving Neural Acceleration Inference Serving"),
    ("Security", "5C", "Intermittence-aware Speculative Page Coloring Secure NVM"),
    ("Security", "5C", "AutoFHE: Automatic Hardware Generation Framework Domain-Specific FHE Accelerator"),
    ("Security", "5C", "LIPPEN: Lightweight In-Place Pointer Encryption Architecture Pointer Integrity"),
    ("Security", "5C", "DarkStream: Exploiting Internal Throughput Contention Data Streaming Accelerator"),
    ("Security", "6D", "ColumnKeeper: Efficient Solutions ColumnDisturb Vulnerability DRAM-based"),
    ("Security", "6D", "PVAC: RowHammer Mitigation Architecture Per-victim-row Counting"),
    ("Security", "6D", "Loaded Dice: Solving Non-Selection Problem Scalable Probabilistic RowHammer"),
    ("Security", "6D", "PRowhammer: Propagating Bit-flips CPU GPU"),
    ("Security", "6D", "DejaVu: Why Write DRAM Rows Twice Carefully"),
    
    # === PIM/PNM Sessions (2B, 3B, 10C) ===
    ("PIM/PNM", "2B", "ECC Enabled Reliable Performant Processing-in-Memory"),
    ("PIM/PNM", "2B", "HBM-CASO: Coordinated Approach HBM System-Level On-Die ECC"),
    ("PIM/PNM", "2B", "ATX: Accelerator Task Extensions"),
    ("PIM/PNM", "3B", "Taking Analytic Databases Bank DRAM"),
    ("PIM/PNM", "3B", "PuDGhost: Experimental Analysis Computation Result Corruption DRAM"),
    ("PIM/PNM", "3B", "MERIDIAN: In-Memory Acceleration RAG Document Attention Decomposition"),
    ("PIM/PNM", "3B", "PipeIMC: Pipelined In-SRAM Computing Architecture"),
    ("PIM/PNM", "3B", "BAAP: Coupling Compute-in-SRAM DRAM Banks Near-Memory Processing"),
    ("PIM/PNM", "10C", "AXLE: Coordinated Offloading Asynchronous Back-Streaming Computational Memory"),
    ("PIM/PNM", "10C", "DCC: Data-Centric Compilation Machine Learning Kernels Processing-In-Memory"),
    ("PIM/PNM", "10C", "Optimizing Spatial Data Structure Near-Cache Acceleration Physical Locality"),
    ("PIM/PNM", "10C", "Bridging Efficiency Scalability LLM 3D Hybrid PIM 2D In-Transit"),
    ("PIM/PNM", "10C", "Early Silicon Raptor First 3D-DRAM Accelerator Generative Inference"),
    
    # === ML Accelerator Sessions (3A, 10B) ===
    ("ML Accel", "3A", "Shining Light Silicon Photonic DNN Accelerators"),
    ("ML Accel", "3A", "TensorPrism: Rethinking Sparse High-order Tensor Acceleration Co-occurrence"),
    ("ML Accel", "3A", "OASIS: Outlier-Aware LUT-Based GEMM Dual-Side Quantization LLM Inference"),
    ("ML Accel", "3A", "Omni-LUT: Energy-Efficient LUT-based Accelerator KV Cache Quantization"),
    ("ML Accel", "3A", "QiMeng-Tensify: Scaling Tensor Computation Optimization LLM-Guided MCTS"),
    ("ML Accel", "10B", "Dynamic Scheduling AI Accelerators TISA"),
    ("ML Accel", "10B", "MXFFP: Microscaling Flexible Floating Point Format AI Model Acceleration"),
    ("ML Accel", "10B", "UniCore: Bit-Width Scalable GEMM Unit Unified LLM Inference"),
    ("ML Accel", "10B", "XtraMAC: Efficient MAC Architecture Mixed-Precision LLM Inference FPGA"),
    ("ML Accel", "10B", "ELSA: Elastic SNN Inference Architecture Efficient Neuromorphic Computing"),
    
    # === Quantum Sessions (4D, 8C, 9C) ===
    ("Quantum", "4D", "Triage: Adaptive Parallel Window Decoding Scheduler Real-time Fault-Tolerant Quantum"),
    ("Quantum", "4D", "Coset Ensemble Decoder Quantum Error Correction Algorithm-Hardware Co-Design"),
    ("Quantum", "4D", "Streaming Architecture Quantum Error Syndrome Compression 4 Kelvin"),
    ("Quantum", "4D", "Transpiler-Architecture Co-Design Curb Clifford Costs Fault-Tolerant Quantum"),
    ("Quantum", "4D", "Kernpiler: Compiler Optimization Quantum Hamiltonian Simulation Partial Trotterization"),
    ("Quantum", "8C", "Distilling Magic States Bicycle Architecture"),
    ("Quantum", "8C", "O3LS: Optimizing Lattice Surgery Automatic Layout Searching Loose Scheduling"),
    ("Quantum", "8C", "Leveraging Phase Polynomials Quantum Circuit Optimization"),
    ("Quantum", "9C", "Unifying Qubit Routing Diverse Quantum ISAs Canonical Representation"),
    ("Quantum", "9C", "TUSQ: Tracking Uncomputation Sampling Noisy Quantum Simulation"),
    ("Quantum", "9C", "Photonic Quantum Computing Spin Memory Architecture Tree-Encoded Fusion"),
    ("Quantum", "9C", "SATIC: Optimizing Ising Compiler SATisfiability"),
    
    # === FHE Sessions (7D) ===
    ("FHE", "7D", "FEnc2: Unifying Data Packing Efficient Private Inference Fragment Encoding"),
    ("FHE", "7D", "FlashTFHE: Scalable Architecture Efficient Multi-bit Fully Homomorphic Encryption"),
    ("FHE", "7D", "Unlocking Pipeline Parallelism Bootstrapping Pipelined Multi-Chiplet TFHE"),
    ("FHE", "7D", "HE2: Communication-Light Heterogeneous Architecture Efficient FHE"),
    ("FHE", "7D", "HyperDrive: Hierarchical Exploitation Memory Efficiency GPU-Based FHE"),
    ("FHE", "7D", "MNEMOS: GPU-based TFHE Acceleration Framework Memory Access Optimization"),
]

def search_arxiv(query):
    encoded = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded}&max_results=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode()
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None

def extract_best_match(xml_data, target_title):
    entries = re.findall(r'<entry>(.*?)</entry>', xml_data, re.DOTALL)
    if not entries:
        return None
    
    target_words = set(w.lower() for w in re.findall(r'\w+', target_title) if len(w) > 2)
    
    best = None
    best_score = 0
    for entry_xml in entries:
        title_m = re.search(r'<title>(.*?)</title>', entry_xml)
        if not title_m:
            continue
        t = title_m.group(1).strip()
        t_words = set(w.lower() for w in re.findall(r'\w+', t) if len(w) > 2)
        
        if not target_words or not t_words:
            continue
        score = len(target_words & t_words) / max(len(target_words | t_words), 1)
        
        # Also check if arxiv comment mentions ISCA 2026
        is_isca = 'ISCA 2026' in entry_xml or 'isca 2026' in entry_xml.lower()
        if is_isca:
            score += 0.3
        
        if score > best_score and score > 0.15:
            best_score = score
            id_m = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry_xml)
            abstract_m = re.search(r'<summary>(.*?)</summary>', entry_xml, re.DOTALL)
            best = {
                "arxiv_id": id_m.group(1).strip() if id_m else "",
                "title": t,
                "abstract": abstract_m.group(1).strip().replace('\n', ' ') if abstract_m else "",
                "score": round(best_score, 3),
                "is_isca": is_isca,
            }
    return best

results = []
found_count = 0

for i, (category, session, query) in enumerate(PAPERS):
    short_title = query.split(":")[0] if ":" in query else query[:60]
    print(f"[{i+1}/{len(PAPERS)}] {category}/{session}: {short_title}...", flush=True)
    
    xml_data = search_arxiv(query[:150])
    
    if xml_data:
        match = extract_best_match(xml_data, query)
        if match:
            found_count += 1
            match["category"] = category
            match["session"] = session
            match["query"] = query
            results.append(match)
            status = "✓" if match["is_isca"] else "?"
            print(f"  {status} arxiv:{match['arxiv_id']} (score={match['score']})", flush=True)
        else:
            print(f"  ✗ No match", flush=True)
    else:
        print(f"  ✗ API error", flush=True)
    
    time.sleep(0.3)  # Rate limiting

# Sort by category, session
results.sort(key=lambda r: (r["category"], r["session"]))

# Save results
output_path = "/home/dxl/Academics/ISCA2026/arxiv_results.json"
with open(output_path, "w") as f:
    json.dump({"found": found_count, "total": len(PAPERS), "papers": results}, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"DONE: {found_count}/{len(PAPERS)} papers found on arxiv")
print(f"Results saved to: {output_path}")

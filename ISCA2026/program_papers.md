# ISCA 2026 — Main Conference Paper Sessions

**Date**: June 29 – July 1, 2026  
**Location**: Raleigh, NC  
**Source**: https://iscaconf.org/isca2026/program/

---

## 汇总总览

| 日期 | Sessions | Papers |
|------|----------|--------|
| Monday, June 29 | 13 | 57 |
| Tuesday, June 30 | 8 | 44 |
| Wednesday, July 1 | 16 | 75 |
| **TOTAL** | **37** | **176** |

### 热点领域分布

| 领域 | Sessions | 约论文数 |
|------|----------|---------|
| LLM 推理/训练 | 1A, 2A, 4A, 5A, 6A, 10A | ~29 |
| Security/Rowhammer | 3C, 5C, 6D | ~16 |
| ML Accelerators | 3A, 10B + Industry tracks | ~16 |
| PIM/PNM (存内计算) | 2B, 3B, 10C | ~13 |
| Quantum Computing | 4D, 8C, 9C | ~12 |
| FHE (全同态加密) | 5C(部分), 7D | ~12 |
| Domain-Specific Accelerators | 4C, 7C, 10D | ~16 |
| Prefetching/Cache/Microarch | 3D, 8B, 9B | ~15 |
| Sustainability | 2C, 9D | ~7 |
| Other (GPU, Storage, HPC, etc.) | 2D, 6B, 6C, 7B, 8A, 8D, 9A, 7A | ~28 |

---

## Monday, June 29 (57 papers)

### Session 1A: Best Paper Candidate Session (Plenary) — 5 papers
Location: Ballroom A | Chair: José F. Martínez (Cornell University)

1. **MLX: Multi-Layer Execution for Structured LLM Workload Acceleration on Spatial Architectures**
   - Haibin Wu, Wenming Li, Zhihua Fan, Zirui Ma, Yuqun Liu, Tengfei Xia, Yanhuan Liu, Kunming Zhang, Xiaochun Ye, Dongrui Fan (ICT, CAS), Jian Weng (KAUST)

2. **CODO: An Automated Compiler for Comprehensive Dataflow Optimization**
   - Weichuang Zhang, Yiquan Wang, Xinzhou Zhang, Chi Zhang, Yu Feng, Xiaofeng Hou, Chao Li, Jieru Zhao, Minyi Guo (Shanghai Jiao Tong University)

3. **COSM: A Cooperative Scheduling Framework for Concurrent PIM and CPU Execution on Mobile Devices**
   - Yilong Zhao, Fangxin Liu (SJTU), Onur Mutlu (ETH Zurich), Mingyu Gao (Tsinghua), Jian Liu (BUAA), Haibing Guan, Li Jiang (SJTU)

4. **Cerberus: Cross-Layer ECC Co-Design for Robust and Efficient Memory Protection**
   - Junhwan Kim, Seunghyun Kim, Yesin Ryu, Jungrae Kim (Sungkyunkwan University), Saeid Gorgin (Univ. of Hertfordshire)

5. **Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference**
   - Zhongkai Yu, Yue Guan (UC San Diego), Zihao Yu (Indiana Univ.), Chenyang Zhou (Columbia), Zhengding Hu (UC San Diego), Shuyi Pei, Yangwook Kang (Samsung), Yufei Ding (UC San Diego), Po-An Tsai (NVIDIA)

---

### Session 2A: LLM 1 — 3 papers
Location: Ballroom A | Chair: Ramyad Hadidi (d-Matrix)

1. **Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding**
   - Soongyu Choi, Yuntae Kim, Muyoung Son, Joo-Young Kim (KAIST)

2. **Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference**
   - Haoran Wu, Jiayi Nie (Cambridge), Can Xiao, Xuan Guo, Binglei Lou, Jeffrey T.H. Wong, Zhiwen Mo, Cheng Zhang, Przemyslaw Forys, Hongxiang Fan, Aaron Zhao (Imperial), Chengyang Ai, Jianyi Cheng (Edinburgh), Timi Adeniran, Timothy M. Jones, Rika Antonova, Robert Mullins (Cambridge), Wayne Luk (Imperial)

3. **Approaching Shannon Bound with Lossless LLM Weight Compression**
   - Hongshi Tan, Yao Chen, Weng-Fai Wong, Bingsheng He (NUS), Gustavo Alonso (ETH Zurich)

### Session 2B: Memory Systems and PIM/PNM — 3 papers
Location: Room 302 | Chair: Tamara Lehman (CU Boulder)

1. **ECC Enabled Reliable and Performant Processing-in-Memory**
   - Jeageun Jung, Margaret Lee, Mattan Erez (UT Austin)

2. **HBM-CASO: A Coordinated Approach to HBM System-Level and On-Die ECC**
   - Ruizhi Zhu, Huize Li, Qian Lou, Xin Xin (UCF), Yanan Guo (Rochester), Weidong Cao (GWU)

3. **ATX: Accelerator Task Extensions**
   - Gerasimos Gerogiannis, Josep Torrellas (UIUC), Stijn Eyerman, Wim Heirman (Intel)

### Session 2C: Sustainability — 3 papers
Location: Room 402 | Chair: Yan Solihin (UCF)

1. **RHODES: Robust Optimization for Uncertainty-Aware Design of CO2-Efficient Computing Systems**
   - Mariam Elgamal, Gu-Yeon Wei, David Brooks, Gage Hills (Harvard), Abdulrahman Mahmoud (MBZUAI)

2. **Rearchitecting the Datacenter Lifecycle for AI**
   - Jovan Stojkovic (UT Austin), Chaojie Zhang, Íñigo Goiri, Ricardo Bianchini (Microsoft Azure)

3. **CAPA: Manufacturing Carbon Estimation for Advanced-Packaged Architectures**
   - Jingyang Liu, Gwenith Bowker-Bafna, Yuke Zhang, Natalie Enright Jerger (Univ. of Toronto)

### Session 2D: Storage — 3 papers
Location: Room 301 | Chair: Mark D. Hill (UW-Madison)

1. **Five-Minute Rule 40 Years Later: A First-Principles Revisit for Modern Memory Hierarchy**
   - Tong Zhang, Fei Sun, Linsen Ma, Yang Liu, Jiangpeng Li, Hao Zhong (ScaleFlux), Vikram Sharma Mailthody, Chris J. Newburn, Wen-Mei W. Hwu (NVIDIA), Teresa Zhang (Stanford)

2. **LOONG: Utilizing Long-Stride Reprogram to Enhance the Performance of SSDs**
   - Congming Gao, Jiancong Zheng, Xufeng Yang, Zheng Wan, Yina Lv, Jiwu Shu (Xiamen Univ.), Qiao Li, Chun Jason Xue (MBZUAI), Jian Chen, Tianyu Ren (Tsinghua), Xin Xin (UCF), Min Ye (CityU HK)

3. **Don't Surrender to Low QPS/$: Fast and Cost-Efficient ANNS with TridentANN**
   - Yuchen Huang, Baiteng Ma, Chuliang Weng (ECNU), Erci Xu (SJTU)

---

### Session 3A: ML Accelerators 1 — 5 papers
Location: Ballroom A | Chair: Bahar Asgari (UMD)

1. **Shining Light on Silicon Photonic DNN Accelerators**
   - Avilash Mukherjee, Mieszko Lis, Sudip Shekhar (UBC)

2. **TensorPrism: Rethinking Sparse High-order Tensor Acceleration via Co-occurrence Graph**
   - Fangzhou Ye, Shilin Tian, Amir Ghazizadeh Ahsaei, Hao Zheng (UCF)

3. **OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration**
   - Xueying Wu, Baijun Zhou, Zhihui Gao, Yuzhe Fu, Qilin Zheng, Yintao He, Hai Li (Duke)

4. **Omni-LUT: Energy-Efficient LUT-based Accelerator with Hardware-Aware KV Cache Quantization**
   - Cheng-Han Tsai, Kuan-Chen Chou, Yu-Hsin Wang, Chieh-Dun Wen, Tsung Tai Yeh (NYCU)

5. **QiMeng-Tensify: Scaling up Tensor Computation Optimization via Architecture-Aware LLM-Guided MCTS**
   - Shouyang Dong, Xiyue Yu, Jianxing Xu, Xuehai Zhou (USTC), Jun Bi, Yuanbo Wen, Guanglin Xu, Qi Guo (ICT, CAS), Ling Li (ISCAS), Tianshi Chen (Cambricon)

### Session 3B: DRAM and SRAM PIM/PNM — 5 papers
Location: Room 302 | Chair: Xun (Steve) Jian (Virginia Tech)

1. **Taking Analytic Databases to the Bank**
   - Alexandar Devic, Anand Sivasubramaniam (Penn State), Martin Prammer, Jignesh Patel (CMU), Kevin Gaffney (Microsoft), Siddhartha Balakrishna Rai (AMD), Ameen Akel (Micron)

2. **PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips**
   - Daichi Tokuda, Tatsuya Kubo, Shinya Takamaeda-Yamazaki (U. Tokyo / RIKEN), Ismail Emir Yuksel, Ataberk Olgun, Haocong Luo, Nisa Bostanci, Jikun Wang, Onur Mutlu (ETH Zurich), Abdullah Giray Yağlıkçı (CISPA)

3. **MERIDIAN: In-Memory Acceleration for RAG with Document Attention Decomposition**
   - Chaoqiang Liu, Yu Huang, Haifeng Liu, Yi Zhang, Qihang Qiu, Long Zheng, Xiaofei Liao, Hai Jin (HUST), Xueqi Li (ICT, CAS), Jingling Xue (UNSW)

4. **PipeIMC: a Pipelined In-SRAM Computing Architecture**
   - Yikai Cui, Renhao Fan, Weike Li, Zhaolin Li (Tsinghua), Mingzhao Li (Suzhou Taihao), Mingyu Wang (SYSU)

5. **BAAP: Coupling Compute-in-SRAM with DRAM Banks for Near-Memory Processing**
   - Cecilio C. Tamarit, Socrates Wong, Akshati Vaishnav, José Martínez (Cornell)

### Session 3C: Security — 5 papers
Location: Room 402 | Chair: Wenjie Xiong (Virginia Tech)

1. **Towards Practical Interrupt Side-Channel Attacks on macOS for Apple Silicon**
   - Xin Zhang, Jiajun Zou, Yi Yang, Qingni Shen (PKU), Chang Liu (Tsinghua), Zhi Zhang (UWA), Trevor E. Carlson (NUS)

2. **Helium: Quantifying Microarchitectural Side-Channel Leakage with Probabilistic Guarantees**
   - Samantha Archer, Caroline Trippel (Stanford), Mohammad Rahmani Fadiheh (LUBIS EDA, RPTU)

3. **LÆGIS: Pinpointing and Addressing Performance Overheads of GPU-based Confidential Computing**
   - (Authors TBD — GPU TEE performance analysis)

4. **MC-ORAM: A Mask-Assisted and Counter-Based Non-Deterministic ORAM inside VM-Based TEEs**
   - (Authors TBD)

5. **TimeGaps Channels: Exploiting CPU Halted Time for Fun and Profit**
   - (Authors TBD)

### Session 3D: Microarchitecture — 5 papers
Location: Room 301 | (Chair TBD)

1. **Dorado: Clustered Hardware Cache Coherence for 1,000+ Cores**
   - (Authors TBD)

2. **Hierarchical Wakeup Logic of the Issue Queue for High Scalability**
   - (Authors TBD)

3. **RUNLTS: Branch Prediction with Register-Value Correlations and Hierarchical Table Orchestration**
   - (Authors TBD)

4. **Augmenting the Branch Predictor with a Squashed-Branch Reuse Buffer**
   - (Authors TBD)

5. **Revisiting Global Value Prediction: A Resurgent Complement to Local Predictors**
   - (Authors TBD)

---

### Session 4A: LLM 2 — 5 papers
Location: Ballroom A | (Chair TBD)

1. **HybridSpec: Exploiting Hybrid-bonding Memory to Accelerate LLM Serving through Heterogeneous Architecture and Speculative Decoding**
   - (Authors TBD)

2. **P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats**
   - (Authors TBD)

3. **CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM**
   - (Authors TBD)

4. **SMOOTH: Hardware-Assisted Fine-Grained On-Chip Memory Management for Efficient On-Device LLM Inference**
   - (Authors TBD)

5. **SHyLA: 3D-Stacked NVM-DRAM Hybrid LLM-Inference Architecture Exploiting Data and Memory Heterogeneity**
   - (Authors TBD)

### Session 4B: Industry Track 1 — 5 papers
Location: Room 302 | (Chair TBD)

1. **SPEC CPU: The Next Generation**
   - (Authors TBD)

2. **A Silicon-Proven Unified Low-Latency CXL Controller and Port-Based Routing Switch for Memory-Centric Fabrics**
   - (Authors TBD)

3. **Vistara: Making CXL Real—Full Path from ASIC Design and OS Support to Hyperscale Deployment**
   - (Authors TBD)

4. **From Lab to Fleet: Building and Deploying a Practical Rowhammer Defense in Cloud SoCs**
   - (Authors TBD)

5. **KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta**
   - (Authors TBD)

### Session 4C: Domain Specific Accelerators 1 — 5 papers
Location: Room 402 | (Chair TBD)

1. **Graph.hls: A Compiler Framework for Composable Graph Accelerator Design**
   - (Authors TBD)

2. **Accelerator Polymorphism: Transcending Domain-Specific Architectures with Robotics**
   - (Authors TBD)

3. **GRAINS: Enabling High-Performance and Low-Cost Graph-Based Genome Analysis via Storage-Aware Algorithm-Architecture Co-Design**
   - (Authors TBD)

4. **Lembas: An Appliance for Scalable Genome Alignment**
   - (Authors TBD)

5. **LoRA: Towards Improved Applicability of Reconfigurable Architecture for Versatile Nonlinear Functions**
   - (Authors TBD)

### Session 4D: Quantum 1 — 5 papers
Location: Room 301 | (Chair TBD)

1. **Triage: An Adaptive Parallel Window Decoding Scheduler for Real-time Fault-Tolerant Quantum Computation**
   - (Authors TBD)

2. **Coset Ensemble Decoder for Quantum Error Correction with Algorithm-Hardware Co-Design**
   - (Authors TBD)

3. **A Streaming Architecture for Quantum Error Syndrome Compression at 4 Kelvin**
   - (Authors TBD)

4. **Transpiler-Architecture Co-Design to Curb Clifford Costs in Fault-Tolerant Quantum Computing**
   - (Authors TBD)

5. **Kernpiler: Compiler Optimization for Quantum Hamiltonian Simulation with Partial Trotterization**
   - (Authors TBD)

---

## Tuesday, June 30 (44 papers)

### Session 5A: LLM 3 — 6 papers
Location: Ballroom A | (Chair TBD)

1. **Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs**
2. **ConServe: Contiguity-Preserving Memory Management for Multi-Turn LLM Serving**
3. **Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference**
4. **DynoPipe: Heterogeneous Edge-Cloud LLM Serving with Dynamically Orchestrated Pipeline Boundaries**
5. **DIAMoND: Dynamic Inference for Adaptive Edge MoE with Heterogeneous In-NAND and Near-DRAM Compute Architecture**
6. **SingularBit: Exploiting Synergy of SVD and Low-Bit Quantization for Weight and KV Compression in LLM Inference**

### Session 5B: Industry Track 2 — 6 papers
Location: Room 302 | (Chair TBD)

1. **Optimized Memory Tagging on AmpereOne® Processors**
2. **BoostX™-NTI: Fast, Scalable and Flexible Storage Architecture with NVMe/TCP Initiator Acceleration**
3. **M100: An Orchestrated Dataflow Architecture Powering General AI Computing**
4. **Prometheus: Toward Resilient Datacenters through Optimized Cooling Infrastructure**
5. **Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles**
6. **MTIA 300: Meta's First Training Chip Featuring Built-in NICs and Collective Offloading Engines**

### Session 5C: Crypto and Security — 6 papers
Location: Room 402 | (Chair TBD)

1. **μRNG: A Framework for Assessing Randomness in Intermittent Computing Devices**
2. **IroKnight: Ownership-Preserving Neural Acceleration for Inference Serving**
3. **Intermittence-aware Speculative Page Coloring for Secure NVM**
4. **AutoFHE: An Automatic Hardware Generation Framework for Domain-Specific FHE Accelerator**
5. **LIPPEN: A Lightweight In-Place Pointer Encryption Architecture for Pointer Integrity**
6. **DarkStream: Exploiting Internal Throughput Contention in Data Streaming Accelerator for Timing Attacks**

### Session 5D: Potpourri — 6 papers
Location: Room 301 | (Chair TBD)

1. **L-PCN: A Point Cloud Accelerator Exploiting Spatial Locality through Octree-based Islandization**
2. **NS-FPS: Accelerating Farthest Point Sampling via Neighbor Search in Large-Scale Point Clouds**
3. **RoCC: Harnessing Raster Operations Pipeline for Efficient Tensor Collective Communication**
4. **STEP: Spatial Footprint Prefetcher with Multi-Point Temporal Triggers**
5. **TDMSim: Enabling High-Density and Energy-Efficient GPU DRAM Caches with 2D-Materials for Data-Intensive Applications**
6. **RangeGuard: Efficient, Bounded Approximate Error Correction for Reliable DNNs**

---

### Session 6A: LLM 4 — 5 papers
Location: Ballroom A | (Chair TBD)

1. **Tetris: Efficient Long-context LLM Serving with Chunkwise Dynamic Sequence Parallelism**
2. **SMoE: An Algorithm-System Co-Design for Pushing MoE to the Edge via Expert Substitution**
3. **ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs**
4. **STEP: Adaptive Spatio-Temporal Expert Prefetching for Low-Latency and Memory-Efficient MoE Inference**
5. **EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture**

### Session 6B: Deep Learning / Memory Acceleration — 5 papers
Location: Room 302 | (Chair TBD)

1. **LoKA: Low-precision Kernel Applications for Recommendation Models At Scale**
2. **Bringing Near Data Processing into the Low-Bit Floating-Point Era**
3. **NasZip: Software and Hardware Co-design to Accelerate ANN Search with DIMM-based Near-Data Processing**
4. **AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization**
5. **Random-Access Hardware Sequence Compression**

### Session 6C: GPUs and Compilation — 5 papers
Location: Room 402 | (Chair TBD)

1. **Observability-aided GPU Memory Oversubscription**
2. **Coarse-Grained Duplication First, Fine-Grained Deduplication Later: Duplication-Centric Multi-GPU Memory Management**
3. **Reducing Page Faults via Invalidation-based Mapping Propagation in Multi-GPU Systems**
4. **sCROOGe: Circuit-level Design and Optimization Framework for RISC-V Out-of-Order GPUs**
5. **æSIP: μArch-aware ASIP-ISA Co-Design via Program Synthesis, Equality Saturation, and External Don't Cares**

### Session 6D: Rowhammer and Security — 5 papers
Location: Room 301 | (Chair TBD)

1. **ColumnKeeper: Efficient Solutions to the ColumnDisturb Vulnerability in DRAM-based Systems**
2. **PVAC: A RowHammer Mitigation Architecture Exploiting Per-victim-row Counting**
3. **Loaded Dice: Solving the Non-Selection Problem for Scalable Probabilistic RowHammer Defense**
4. **PRowhammer: Propagating Bit-flips from CPU to GPU**
5. **DejaVu: Why You Should Write to Your DRAM Rows Twice, Carefully**

---

## Wednesday, July 1 (75 papers)

### Session 7A: Emerging Technologies: Chiplet, Wafer-Scale, etc. — 6 papers
Location: Ballroom A | (Chair TBD)

1. **DICE: Detailed Inter-Chiplet End-to-End PHY Modeling for Accurate Chiplet Simulation**
2. **Omelet: A Packaging-Aware Hierarchical Interconnect Simulator for 2.5D/3D Chiplet Architectures**
3. **PhaseWeave: Phase-Aware Execution on Heterogeneous Chiplet Architectures for Datacenters**
4. **ConBin: A Performance-Convergence Framework for Wafer-Scale Chip Binning**
5. **WaferBRAIN: Whole-Brain Scale Neuromorphic Architecture Based on Wafer-Scale Integration**
6. **DS-ISA: Instruction Set Architecture for Dynamical System Units**

### Session 7B: Performance Modeling / Datacenter — 6 papers
Location: Room 302 | (Chair TBD)

1. **NeRArch-Sim: A Unified Simulator for Benchmarking and DSE of Neural Rendering Accelerators**
2. **BULLET TIME: Time Dilation for High-Fidelity Tracing**
3. **PIPEWEAVE: Synergizing Analytical and Learning Models for Unified GPU Performance Prediction**
4. **SSBench: Automated Characterization of Memory Dependence Predictors on Modern CPUs**
5. **R2D2: Robotized Reconfigurable Network for Disaggregated Datacenters**
6. **Lotus: A Task Dataflow Architecture for Cycle-Level Simulation**

### Session 7C: Domain Specific Accelerators 2 — 6 papers
Location: Room 402 | (Chair TBD)

1. **SegFold: Accelerating Sparse GEMM with a Fine-Grained Dynamic Dataflow**
2. **ParetoES: Hardware-Accelerated Sparse Embedding Similarity via Pareto-Optimal Pruning**
3. **ECHO: Efficient Head-Orientation-Guided Real-Time Sound Spatialization for Virtual Reality**
4. **DESSCam: An Event-Driven Architecture with In-Sensor Epitopological Sparse Sampling to Break the Latency-Power Tradeoff in Eye Tracking**
5. **SLICE: A Selective Local Inference Framework with Codec Exploitation for Accelerating Video Super-Resolution**
6. **Enabling Continuous, In-Field Introspection: The Programmable IPU Architecture**

### Session 7D: FHE — 6 papers
Location: Room 301 | (Chair TBD)

1. **FEnc2: Unifying Data Packing for Efficient Private Inference via Convolution and Architecture-Aware Fragment Encoding**
2. **FlashTFHE: A Scalable Architecture for Efficient Multi-bit Fully Homomorphic Encryption**
3. **Unlocking Pipeline Parallelism for Bootstrapping: A Pipelined Multi-Chiplet TFHE Accelerator**
4. **HE^2: A Communication-Light Heterogeneous Architecture for Efficient Fully Homomorphic Encryption**
5. **HyperDrive: Hierarchical Exploitation of Memory Efficiency for GPU-Based FHE Acceleration**
6. **MNEMOS: A GPU-based TFHE Acceleration Framework with Memory Access Optimization**

---

### Session 8A: Rendering — 3 papers
Location: Ballroom A | (Chair TBD)

1. **GauTracer: Extending Ray Tracing Accelerator for Gaussian-based Scene Representation**
2. **TTP: A Hardware-Efficient Design for Precise Prefetching in Ray Tracing**
3. **Optimizing 3D Gaussian Splatting with Axis-Shared Rasterization and Order-independent Transmittance**

### Session 8B: Prefetching and Caches 1 — 3 papers
Location: Room 302 | (Chair TBD)

1. **Bumper: Hinting Instruction Usefulness for Robust Unified Caches**
2. **ICP: Exploiting Instruction Correlation for Prefetching Irregular Memory Accesses**
3. **Revelator: Rapid Data Fetching via OS-Guided Hash-based Speculative Address Translation**

### Session 8C: Quantum 2 — 3 papers
Location: Room 402 | (Chair TBD)

1. **Distilling Magic States in the Bicycle Architecture**
2. **O3LS: Optimizing Lattice Surgery via Automatic Layout Searching and Loose Scheduling**
3. **Leveraging Phase Polynomials for Quantum Circuit Optimization**

### Session 8D: HPC — 3 papers
Location: Room 301 | (Chair TBD)

1. **Harmonia: A Unified Hierarchical Scheduling Framework for Sparse Matrix Multiplication**
2. **PipeComm: Maximizing Link Utilization through Pipeline-Aware Collective Communication Synthesis**
3. **Breaking Barriers in Atomic Scaling: A Hardware–Software-Collaborated Framework to Deconstruct RDMA Atomic**

---

### Session 9A: Verification and Robustness — 4 papers
Location: Ballroom A | (Chair TBD)

1. **Democratizing and Accelerating Hardware Verification with Software-Native Optimization**
2. **HartBreaker: Deterministic Fuzzing of Multi-Hart RISC-V CPUs with Non-Deterministic Programs**
3. **QED: Scalable Consistency Verification of Memory Instruction Reordering in Hardware**
4. **tākōFormal: Enabling Robust Software for Programmable Memory Hierarchies**

### Session 9B: Prefetching and Caches 2 — 4 papers
Location: Room 302 | (Chair TBD)

1. **LIBRA: A High-Accuracy, Cost-Aware, and Coordinated Multi-GPU Page Prefetcher**
2. **Enhancing Instruction Prefetching via Cache and TLB Management**
3. **R-Max: Extending Bélády's MIN with Prefetching to Bound Realistic Cache Performance**
4. **From Memorization to Generalization: A Practical Neural Network Prefetching Framework**

### Session 9C: Quantum 3 — 4 papers
Location: Room 402 | (Chair TBD)

1. **Unifying Qubit Routing Across Diverse Quantum ISAs via Canonical Representation**
2. **TUSQ: Tracking, Uncomputation, and Sampling for Noisy Quantum Simulation**
3. **Photonic Quantum Computing on Spin Memory Architecture with Tree-Encoded Fusion**
4. **SATIC: An Optimizing Ising Compiler for SAT(isfiability)**

### Session 9D: Sustainability and Energy Efficiency — 4 papers
Location: Room 301 | (Chair TBD)

1. **PowerGrad: Hierarchical Power Management for Power-Limited ML Inference Clusters**
2. **Power Sloshing in Compound Servers for Large-Scale AI Inference Workloads**
3. **PowerWeave: Unlocking Energy-Efficient ML on GPUs with OS-Level Spatial Power Management**
4. **Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs**

---

### Session 10A: LLM 5 — 4 papers
Location: Ballroom A | (Chair TBD)

1. **Scalable Synthesis of Distributed LLM Workloads Through Symbolic Tensor Graphs**
2. **DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training**
3. **MoE-Hub: Taming Software Complexity for Seamless MoE Overlap with Hardware-Accelerated Communication on Multi-GPU Systems**
4. **Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs**

### Session 10B: ML Accelerators 2 — 5 papers
Location: Room 302 | (Chair TBD)

1. **Dynamic Scheduling for AI Accelerators via TISA**
2. **MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration**
3. **UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference**
4. **XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA**
5. **ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing**

### Session 10C: PIM/PNM, cont. — 5 papers
Location: Room 402 | (Chair TBD)

1. **AXLE: Coordinated Offloading with Asynchronous Back-Streaming in Computational Memory Systems**
2. **DCC: Data-Centric Compilation of Machine Learning Kernels for Processing-In-Memory Architectures**
3. **Optimizing Spatial Data Structure with Near-Cache Acceleration by Exploiting Physical Locality**
4. **Bridging Efficiency and Scalability in LLM System via 3D Hybrid PIM with 2D In-Transit Computation**
5. **Early Silicon of Raptor: The First 3D-DRAM Accelerator for Generative Inference**

### Session 10D: Domain Specific Accelerators 3 — 5 papers
Location: Room 301 | (Chair TBD)

1. **DICE: Enabling Efficient General-Purpose SIMT Execution with Statically Scheduled Coarse-Grained Reconfigurable Arrays**
2. **TAGT: An Efficient Graph Transformer Accelerator with Topology-aware Sparsification and Merging**
3. **GenZA: A General and Efficient Accelerator for Diverse Zero-Knowledge Proof Protocols**
4. **HiT: A Unified Sparsity-Adaptive Architecture for High-Throughput Matrix Multiplication**
5. **DiTPA: A DiT-based Action Planner Accelerator Exploiting Action–Denoising–Multimodality Redundancy for Embodied AI**

---

## 领域关键词索引

- **LLM**: 1A, 2A, 4A, 5A, 6A, 10A (6 sessions)
- **PIM/PNM/存内计算**: 2B, 3B, 10C (3 sessions)
- **Security/安全**: 3C, 5C, 6D (3 sessions)
- **FHE/全同态加密**: 5C(部分), 7D (2 sessions)
- **Quantum/量子**: 4D, 8C, 9C (3 sessions)
- **ML Accelerators/ML加速器**: 3A, 10B (2 sessions)
- **Domain-Specific Accelerators**: 4C, 7C, 10D (3 sessions)
- **Microarchitecture/微架构**: 3D, 8B, 9B (3 sessions)
- **Sustainability/绿色计算**: 2C, 9D (2 sessions)
- **GPU/Compilation**: 6C (1 session)
- **Chiplet/Wafer-Scale**: 7A (1 session)
- **Industry Track**: 4B, 5B (2 sessions)

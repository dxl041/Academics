# ISCA 2026 热点领域论文分析

> 基于会议日程（June 29 – July 1, 2026）的标题级分析
> 分析日期: 2026-07-06

---

## 一、LLM 推理/训练（6 sessions, ~29 papers）

这是ISCA 2026最大的热点领域，横跨6个session，且 Best Paper Candidate Session (1A) 中5篇有2篇直接与LLM推理相关。反映出体系结构社区对LLM推理效率的极度关注。

### 1.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **LLM推理加速硬件** | ~8篇 | MLX, P3-LLM, CHIME, HybridSpec, SMOOTH, SHyLA |
| **LLM模型压缩** | ~5篇 | Approaching Shannon Bound (lossless), SingularBit (SVD+quant), ENEC (Ascend NPU) |
| **MoE推理优化** | ~5篇 | Patterns Behind Chaos (MoE data movement), Accelerating MoE with In-Switch, SMoE (edge MoE), DIAMoND (heterogeneous edge MoE), STEP (MoE prefetching) |
| **LLM Serving系统** | ~5篇 | Tetris (chunkwise DP), ConServe (contiguity memory), DynoPipe (edge-cloud pipeline), Symbiotic MLLM Serving, Combating Memory Walls (agentic LLM) |
| **Speculative Decoding** | ~2篇 | Cassandra (edge), HybridSpec (hybrid-bonding memory) |
| **分布式训练** | ~3篇 | Scalable Synthesis (symbolic tensor graphs), DisDP (disaggregated DP), MoE-Hub (MoE overlap) |
| **Wafer-Scale LLM** | ~1篇 | Mapping and Communication Opt. w/ Fault Tolerance |

### 1.2 关键趋势

1. **从单芯片到异构混合架构**：多篇论文将NPU、PIM、DIMM-PIM、Hybrid-bonding Memory等不同计算范式混合起来做LLM推理（P3-LLM, CHIME, SMOOTH, DIAMoND），说明单一架构已无法满足LLM的memory bandwidth和compute需求。

2. **MoE成为独立子方向**：5篇论文专门针对MoE，涵盖data movement预测、in-switch加速、边缘MoE、expert prefetching。MoE特有的all-to-all通信和expert load imbalance正在催生新的体系结构创新。

3. **Speculative Decoding走向边缘**：Cassandra将self-speculative decoding推向edge设备，说明token-by-token的自回归解码延迟问题已从云端蔓延到边缘场景。

4. **Long-context是新战场**：Combating Memory Walls 针对agentic long-context场景，Tetris 用chunkwise DP解决长序列，CHIME 做long-context attention-FC disaggregation。上下文窗口变长带来的KV cache压力正在成为核心瓶颈。

5. **中国团队主导力强**：ICT CAS (MLX), SJTU (HybridSpec, COSM), HUST (MERIDIAN), Tsinghua (PipeIMC), NUS/ETH合作频繁。

### 1.3 值得关注的论文

- **MLX (1A, Best Paper Candidate)**：ICT CAS提出多层执行框架用于结构化LLM workload在空间架构上的加速，大概率涉及算子融合+数据流调度
- **Approaching Shannon Bound (2A)**：声称无损LLM权重压缩逼近香农界，如果属实将是weight compression的重大突破
- **Patterns Behind Chaos (1A, Best Paper Candidate)**：MoE数据移动预测——名字暗示了MoE路由的混沌特性中寻找可预测的模式
- **Combating the Memory Walls (2A)**：Cambridge+Imperial+Edinburgh大联合作，17位作者，针对long-context agentic LLM，industrial paper风格

---

## 二、Security / Rowhammer（3 sessions, ~16 papers）

### 2.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **Rowhammer攻防** | 5篇 | ColumnKeeper, PVAC, Loaded Dice, PRowhammer (CPU→GPU), DejaVu |
| **侧信道攻击** | 3篇 | macOS Apple Silicon interrupt side-channel, Helium (量化侧信道泄露), TimeGaps (CPU halted time) |
| **TEE/机密计算** | 2篇 | LÆGIS (GPU TEE overhead), MC-ORAM (ORAM in VM-based TEE) |
| **Pointer/内存安全** | 2篇 | LIPPEN (pointer encryption), Optimized Memory Tagging (AmpereOne) |
| **NVM安全** | 1篇 | Intermittence-aware Speculative Page Coloring |
| **加速器安全** | 1篇 | DarkStream (data streaming accelerator timing attack) |

### 2.2 关键趋势

1. **Rowhammer热度不减**：从2014年至今已12年，仍在ISCA有独立session（6D），且研究从DRAM row拓展到column（ColumnKeeper/ColumnDisturb）、从CPU拓展到GPU（PRowhammer）。Onur Mutlu系工作量很大。

2. **GPU TEE开销成为新焦点**：LÆGIS专门分析GPU-based confidential computing的性能开销——随着LLM在GPU TEE中部署，这将成为实际瓶颈。

3. **Apple Silicon安全研究兴起**：macOS Apple Silicon的中断侧信道攻击表明Apple Silicon已成为安全研究的重要平台。

4. **概率性防御是Rowhammer主流**：Loaded Dice（概率性防御中的"非选择问题"）、DejaVu（"为什么你应该对DRAM row写两次"）都是概率性/随机化防御思路。

---

## 三、PIM/PNM 存内计算（3 sessions, ~13 papers）

### 3.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **DRAM PIM** | ~4篇 | Taking Analytic Databases to the Bank, PuDGhost (real chip corruption), BAAP, AXLE |
| **SRAM PIM** | ~2篇 | PipeIMC (pipelined In-SRAM), BAAP (Compute-in-SRAM + DRAM) |
| **DIMM-PIM/Near-Data** | ~3篇 | NasZip (ANN search), CHIME (attention-FC with DIMM-PIM), 3D Hybrid PIM |
| **PIM编译/编程** | ~2篇 | DCC (data-centric compilation for PIM), 3D Hybrid PIM with 2D In-Transit |
| **3D-DRAM加速器** | ~1篇 | Raptor (first 3D-DRAM accelerator for generative inference, early silicon!) |

### 3.2 关键趋势

1. **从仿真走向硅验证**：Raptor号称"第一个3D-DRAM accelerator for generative inference的early silicon"，PuDGhost在真实DRAM芯片上实验分析computation result corruption——PIM研究正在从simulation走向real hardware。

2. **PIM+分析数据库是新兴交叉点**：Taking Analytic Databases to the Bank 将分析数据库放到DRAM bank上，这是PIM+数据库的新方向。

3. **PIM可靠性成为独立问题**：PuDGhost直接在真实DRAM上验证PIM计算结果的corruption问题，ECC Enabled Reliable PIM关注PIM的ECC支持——可靠性不再是事后的"future work"。

4. **PIM与LLM深度融合**：MERIDIAN (in-memory RAG), CHIME (DIMM-PIM for attention-FC), 3D Hybrid PIM for LLM——PIM正从通用加速走向LLM专用部署。

5. **Onur Mutlu系占据半壁江山**：ETH Zurich团队(PuDGhost, HBM-CASO相关)和合作者在DRAM PIM领域持续高产出。

---

## 四、ML Accelerators（2 sessions, ~10 papers）

### 4.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **LUT-Based加速** | 2篇 | OASIS (outlier-aware LUT GEMM), Omni-LUT (KV cache quant) |
| **新型数值格式** | 2篇 | MXFFP (microscaling flexible FP), UniCore (bit-width scalable GEMM) |
| **FPGA加速** | 1篇 | XtraMAC (mixed-precision LLM on FPGA) |
| **光计算** | 1篇 | Shining Light on Silicon Photonic DNN |
| **稀疏加速** | 1篇 | TensorPrism (high-order tensor via co-occurrence graph) |
| **SNN/神经形态** | 1篇 | ELSA (elastic SNN inference) |
| **LLM-Guided优化** | 1篇 | QiMeng-Tensify (LLM-guided MCTS for tensor optimization) |
| **调度** | 1篇 | Dynamic Scheduling via TISA |

### 4.2 关键趋势

1. **LUT-based加速是新兴方向**：OASIS和Omni-LUT都基于LUT（查找表）做GEMM/量化加速，这是对传统MAC阵列的替代方案，适合低精度/非均匀量化场景。

2. **混合精度/灵活位宽成为标配**：MXFFP、UniCore、XtraMAC都关注混合精度或位宽可伸缩——不同layer/operator需要不同精度已从paper走向architecture。

3. **用LLM辅助硬件设计**：QiMeng-Tensify用LLM-guided MCTS搜索tensor computation optimization，代表了"AI for Architecture"的新范式。

4. **光计算回归视野**：Silicon Photonic DNN Accelerators作为3A首篇，光计算在AI加速领域的探索仍在继续。

---

## 五、Quantum Computing（3 sessions, ~12 papers）

### 5.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **量子纠错/解码器** | 4篇 | Triage (parallel window decoder), Coset Ensemble Decoder, Streaming Syndrome Compression @4K, Distilling Magic States |
| **量子编译/Transpiler** | 3篇 | Transpiler-Arch Co-Design (Clifford cost), Kernpiler (Hamiltonian simulation), Unifying Qubit Routing |
| **量子架构** | 2篇 | Bicycle Architecture (magic state distillation), Photonic Quantum w/ Spin Memory |
| **量子模拟** | 1篇 | TUSQ (noisy quantum simulation) |
| **Ising编译** | 1篇 | SATIC (Ising compiler for SAT) |
| **Lattice Surgery** | 1篇 | O3LS (optimizing lattice surgery) |

### 5.2 关键趋势

1. **量子纠错是最大子方向**：12篇中至少4篇直接涉及纠错解码——从实时调度(Triage)、硬件协同(Coset)、4K压缩到Magic State蒸馏。FTQC（容错量子计算）的工程化挑战已成为体系结构社区的核心关注点。

2. **编译与架构协同设计**：Transpiler-Architecture Co-Design直接提出transpiler和架构需要协同优化来减少Clifford gate开销——量子编译不再只是软件问题。

3. **光量子+自旋存储混合架构**：Photonic Quantum Computing on Spin Memory Architecture，光子量子计算与传统固态存储的结合。

4. **从算法走向系统工程**：Triage（实时调度）、Streaming Compression @4K（低温压缩）——量子计算正从理论走向可部署系统。

---

## 六、FHE 全同态加密（2 sessions, ~12 papers）

### 6.1 子方向分布

| 子方向 | 论文数 | 代表论文 |
|--------|--------|---------|
| **TFHE加速器** | 3篇 | FlashTFHE (multi-bit), Pipelined Multi-Chiplet TFHE, MNEMOS (GPU TFHE) |
| **通用FHE架构** | 2篇 | HE^2 (communication-light heterogeneous), HyperDrive (GPU memory) |
| **FHE硬件生成** | 1篇 | AutoFHE (automatic hardware generation for domain-specific FHE) |
| **Private Inference** | 1篇 | FEnc2 (fragment encoding for private inference) |

### 6.2 关键趋势

1. **TFHE方案占据主流**：12篇中多数围绕TFHE（全同态加密的一种scheme），说明TFHE因其bootstrapping效率被体系结构社区广泛认可。

2. **从单芯片到多Chiplet**：Pipelined Multi-Chiplet TFHE Accelerator——FHE的巨大计算量正在推动chiplet方案。

3. **GPU-FHE融合**：MNEMOS (GPU-based TFHE)、HyperDrive (GPU memory optimization for FHE)——利用已有GPU硬件加速FHE而非设计专用ASIC。

4. **自动化设计流程**：AutoFHE自动生成domain-specific FHE硬件——FHE的应用场景多样化（医疗、金融、ML），需要自动化的硬件生成工具。

5. **FHE从密码学会议走向体系结构顶会**：ISCA有2个session共12篇FHE论文，说明体系结构社区已将FHE视为重要的加速目标。

---

## 七、跨领域交叉观察

### 7.1 LLM × PIM
CHIME (DIMM-PIM for attention-FC), MERIDIAN (in-memory RAG), 3D Hybrid PIM for LLM——PIM正被定位为解决LLM memory wall的关键技术。

### 7.2 LLM × FHE
FEnc2 (private inference via FHE)——虽然目前在FHE session，但private LLM inference正在成为连接两个领域的桥梁。

### 7.3 Security × GPU
LÆGIS (GPU TEE overhead), PRowhammer (CPU→GPU bit-flip propagation)——GPU不再是安全的"孤岛"。

### 7.4 AI for Architecture
QiMeng-Tensify (LLM-guided MCTS for tensor optimization)——利用AI技术辅助硬件设计，代表了"AI for Architecture"的交叉趋势。

### 7.5 中国团队活跃度
LLM加速领域中国团队特别活跃：ICT CAS（MLX）、SJTU（HybridSpec/COSM/CODO）、HUST（MERIDIAN）、Tsinghua/SYSU、PKU（Apple Silicon security）、Xiamen/ECNU（Storage）。

---

## 八、总结：ISCA 2026 体系结构研究的六大主题

| 主题 | 权重 | 核心问题 |
|------|------|---------|
| **LLM全栈优化** | ★★★★★ | Memory wall, MoE通信, Long-context KV cache, Edge部署 |
| **PIM/近存计算落地** | ★★★★ | 可靠性、编程模型、与LLM workload的适配 |
| **安全无处不在** | ★★★★ | Rowhammer不死，侧信道泛化，TEE性能开销 |
| **量子纠错工程化** | ★★★ | 实时解码、低温压缩、编译-架构协同 |
| **FHE加速实用化** | ★★★ | TFHE主导，多Chiplet/GPU方案，自动化生成 |
| **混合精度与新型加速范式** | ★★★ | LUT-based, Photonic, Flexible FP, SNN |

**最大变化**: LLM已从"一个方向"膨胀为整个会议的最大主题，占据了6个session（~16%的论文），且深入到了PIM、FHE、Security等其他领域形成交叉。

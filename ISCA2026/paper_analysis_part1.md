# ISCA 2026 热点领域论文逐篇四要素分析

> 每篇论文提炼四个要素（各≤50字）：研究背景、要解决的问题、现有方案不足、本文解决思路
> 标注 ★ 的论文已获取arxiv原文摘要，分析基于摘要+Introduction
> 标注 ☆ 的论文基于标题信息分析
> 分析日期: 2026-07-06

---

## 一、LLM 推理/训练（6 sessions, 28 papers）

### Session 1A: Best Paper Candidate Session (Plenary)

---

#### ★ 1. MLX: Multi-Layer Execution for Structured LLM Workload Acceleration on Spatial Architectures
- **研究背景**: LLM推理对算力和访存需求激增，空间架构（如CGRA/Systolic Array）成为主流加速方案
- **要解决的问题**: 空间架构上结构化LLM workload（attention/FFN/路由）的执行效率不足
- **现有方案不足**: 单层优化忽略层间数据复用与流水，算子融合策略未考虑空间架构的bank冲突
- **本文解决思路**: 提出多层协同执行框架MLX，跨层调度+数据流重排，最大化空间架构利用率

---

#### ★ 2. CODO: An Automated Compiler for Comprehensive Dataflow Optimization
- **研究背景**: FPGA数据流架构适合流式/流水处理高计算密度应用，但大规模数据流设计仍需人工HLS调优
- **要解决的问题**: 面向FPGA的数据流加速器自动化编译生成，需要消除粗/细粒度数据流冲突
- **现有方案不足**: 现有HLS框架缺乏系统性数据流违规检测和自动调度，片上/片外数据传输效率低
- **本文解决思路**: CODO编译器自动检测消除数据流冲突，联合优化片上片外数据移动，自动调度平衡资源与性能

---

#### ★ 3. COSM: A Cooperative Scheduling Framework for Concurrent PIM and CPU Execution on Mobile Devices
- **研究背景**: 端侧LLM隐私和低延迟需求驱动PIM部署，但移动设备DRAM成本受限、CPU-PIM共享内存
- **要解决的问题**: CPU与PIM在共享内存空间并发执行时的bank冲突和总线拥塞，削弱PIM性能收益
- **现有方案不足**: 现有调度方案将PIM与CPU顺序执行或简单时分复用，无法充分利用空闲窗口隐藏延迟
- **本文解决思路**: COSM低干扰PIM控制接口+空闲感知调度，将PIM命令插入CPU访存空闲窗口，PIM吞吐提升2.8x

---

#### ★ 4. Cerberus: Cross-Layer ECC Co-Design for Robust and Efficient Memory Protection
- **研究背景**: DRAM制程微缩和高速I/O使数据可靠性更严峻，业界采用On-Die/Link/System三层ECC独立演进
- **要解决的问题**: 三层ECC独立设计导致冗余重复、覆盖盲区和层间干扰，浪费纠错预算且无法协同修复
- **现有方案不足**: O-ECC/L-ECC/S-ECC各自为政，冗余信息不共享，miscorrection放大，联合故障无法恢复
- **本文解决思路**: Cerberus提出"一次编码多次解码"(EODM)架构，单一编码冗余被三层复用，协同分配纠错预算

---

#### ★ 5. Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference
- **研究背景**: MoE大模型成为开源前沿模型主流，但随机的expert选择机制引入巨大数据移动开销
- **要解决的问题**: MoE推理中expert选择看似混沌，但缺乏对其数据移动模式的系统性理解以指导系统设计
- **现有方案不足**: 缺乏从数据和时空维度系统分析MoE数据移动规律的工作，无法为硬件/调度设计提供指导
- **本文解决思路**: 对4款200B-1000B MoE模型做24K+请求的profiling，提炼6条insight，wafer-scale上加速6.6x

---

### Session 2A: LLM 1

---

#### ★ 6. Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding
- **研究背景**: Speculative Decoding是LLM无损加速主流方案，推理LLM解码开销突出，近似方法降低精度
- **要解决的问题**: 现有speculative decoding在低batch场景性能不足且需要额外训练，限制消费设备端侧部署
- **现有方案不足**: 基于layer skipping或结构化KV压缩的自投机解码效率低，格式转换开销大
- **本文解决思路**: Cassandra算法-硬件协同，训练无关draft模型构建+剪枝尾数截断+轻量编解码硬件模块，2.41x加速

---

#### ★ 7. Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference (PLENA)
- **研究背景**: Agentic LLM推理与对话bot推理本质不同，长上下文（网页DOM/工具调用轨迹）产生巨量片外访存
- **要解决的问题**: Agentic LLM面临带宽墙和容量墙双重memory wall，计算单元利用率极低
- **现有方案不足**: 现有GPU/TPU针对chatbot场景优化，缺乏针对agentic长上下文memory wall的专用架构
- **本文解决思路**: PLENA扁平Systolic Array+非对称量化+FlashAttention原生支持，吞吐达A100的2.23x/TPUv6e的4.70x

---

#### ★ 8. Approaching Shannon Bound with Lossless LLM Weight Compression
- **研究背景**: LLM参数量达万亿级，权重存储进入TB级别，与GPU显存容量严重不匹配
- **要解决的问题**: LLM权重的内在信息熵远低于存储位宽，理论上可达10x无损压缩，但系统级实现缺失
- **现有方案不足**: 有损量化牺牲精度，无损压缩在LLM推理系统中未实际部署，解压速度未对齐GEMM tiling
- **本文解决思路**: 基于Asymmetric Numeral Systems的tile级即时解压框架，码率逼近Shannon限，Mixtral-176B batch扩至4.8x

---

### Session 4A: LLM 2

---

#### ☆ 9. HybridSpec: Exploiting Hybrid-bonding Memory to Accelerate LLM Serving through Heterogeneous Architecture and Speculative Decoding
- **研究背景**: LLM serving对显存带宽和容量需求巨大，Hybrid-bonding 3D堆叠内存提供高带宽新途径
- **要解决的问题**: 如何利用3D混合键合内存的高带宽特性，结合异构架构与推测解码加速LLM serving
- **现有方案不足**: 现有方案未充分利用3D堆叠内存的近存带宽优势，推测解码与异构架构分离设计
- **本文解决思路**: Hybrid-bonding内存+异构计算单元+推测解码协同，利用近存高带宽降低解码延迟

---

#### ★ 10. P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats
- **研究背景**: 端侧LLM推理面临巨大带宽和算力挑战，NPU+PIM异构方案兴起但高精度PIM单元面积功耗大
- **要解决的问题**: DRAM工艺下高精度PIM计算单元面积功耗开销大，限制有效算力密度
- **现有方案不足**: 现有PIM量化方案精度-效率权衡不佳，混合数值格式的PIM架构协同设计缺失
- **本文解决思路**: 混合数值格式量化方案+低精度PIM计算单元+算子融合去量化优化，平均4.9x加速于HBM-PIM

---

#### ☆ 11. CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM
- **研究背景**: 长上下文LLM推理中Attention和FC模块计算/访存特征迥异，统一架构效率低
- **要解决的问题**: 长上下文场景下Attention与FC模块的分离推理，利用DIMM-PIM处理不同特征的计算
- **现有方案不足**: 单一架构难以同时高效处理Attention的memory-bound和FC的compute-bound特征
- **本文解决思路**: CHIME将Attention-FC disaggregate到DIMM-PIM与计算单元，根据计算特征异构部署

---

#### ☆ 12. SMOOTH: Hardware-Assisted Fine-Grained On-Chip Memory Management for Efficient On-Device LLM Inference
- **研究背景**: 端侧LLM推理on-chip memory容量极度受限，KV cache和权重竞争SRAM空间
- **要解决的问题**: 如何在有限的片上SRAM中细粒度管理LLM推理的中间数据与权重，减少片外访存
- **现有方案不足**: 现有缓存管理策略粗粒度（整层/整tensor），未能利用LLM推理的token级局部性
- **本文解决思路**: SMOOTH硬件辅助的细粒度片上内存管理，token/tile级数据留存策略，最小化片外访问

---

#### ☆ 13. SHyLA: 3D-Stacked NVM-DRAM Hybrid LLM-Inference Architecture Exploiting Data and Memory Heterogeneity
- **研究背景**: LLM推理中权重（只读、大容量）和KV cache（读写、动态）访存模式截然不同
- **要解决的问题**: 如何利用3D堆叠NVM+DRAM混合存储，根据数据访问特征异构部署权重和KV cache
- **现有方案不足**: 统一DRAM存储忽略权重和KV截然不同的读写/容量需求，NVM的高密度优势未被利用
- **本文解决思路**: SHyLA将权重映射到高密度NVM层、KV cache到低延迟DRAM层，3D堆叠提升带宽

---

### Session 5A: LLM 3

---

#### ★ 14. Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs
- **研究背景**: MoE模型的多GPU部署中expert路由引发all-to-all通信，成为推理和训练的主要瓶颈
- **要解决的问题**: MoE多GPU场景下expert间数据移动的通信瓶颈，传统网络交换仅转发不计算
- **现有方案不足**: 现有方案依赖GPU间NVLink/IB直接通信，all-to-all通信量与expert数成平方增长
- **本文解决思路**: 在交换机中嵌入动态计算能力（in-switch computing），边路由边聚合，减少跨GPU通信量

---

#### ☆ 15. ConServe: Contiguity-Preserving Memory Management for Multi-Turn LLM Serving
- **研究背景**: 多轮对话LLM serving中KV cache随对话增长，内存碎片化导致分配失败和利用率下降
- **要解决的问题**: 多轮LLM serving中KV cache的连续性碎片化，导致大块连续内存无法分配、提前eviction
- **现有方案不足**: 现有vLLM等系统的page-based分配忽略多轮对话的KV cache连续性需求，碎片率高
- **本文解决思路**: ConServe连续性保持内存管理，根据对话轮次预分配连续KV cache空间，减少碎片和eviction

---

#### ☆ 16. Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference
- **研究背景**: Wafer-Scale芯片（如Cerebras）提供超大算力但存在制造缺陷，LLM推理映射需容错
- **要解决的问题**: Wafer-Scale芯片上LLM推理的算子映射与通信优化，同时需容忍制造缺陷导致的故障单元
- **现有方案不足**: 现有映射策略未同时考虑通信优化和容错，缺陷芯片的算力损失大
- **本文解决思路**: 通信感知的容错映射策略，结合冗余计算和动态重路由，最大化缺陷wafer的有效算力

---

#### ☆ 17. DynoPipe: Heterogeneous Edge-Cloud LLM Serving with Dynamically Orchestrated Pipeline Boundaries
- **研究背景**: 边缘-云协同LLM serving兴起，但网络波动和设备异构性使静态pipeline划分低效
- **要解决的问题**: 边缘-云异构环境中pipeline并行的边界如何动态调整以适应网络和设备状态变化
- **现有方案不足**: 静态pipeline划分无法响应网络波动，边界固定导致边缘/云资源利用不均衡
- **本文解决思路**: DynoPipe动态编排pipeline边界，根据实时网络延迟和设备负载在线调整切分点

---

#### ☆ 18. DIAMoND: Dynamic Inference for Adaptive Edge MoE with Heterogeneous In-NAND and Near-DRAM Compute Architecture
- **研究背景**: 端侧MoE推理受限于算力和内存，异构近存计算（In-NAND/Near-DRAM）提供新可能
- **要解决的问题**: 如何结合In-NAND和Near-DRAM异构近存计算，动态适配不同MoE expert的计算需求
- **现有方案不足**: 单一近存计算架构无法覆盖MoE中不同expert的差异化计算/容量需求
- **本文解决思路**: DIAMoND动态推理框架，根据expert特征自适应分配到In-NAND或Near-DRAM计算单元

---

#### ☆ 19. SingularBit: Exploiting Synergy of Singular Value Decomposition and Low-Bit Quantization for Weight and KV Compression in LLM Inference
- **研究背景**: LLM权重和KV cache占据大量内存，SVD和低位宽量化是两种主要压缩手段
- **要解决的问题**: SVD和量化各自有损，如何协同利用两者实现更高的压缩比而不增加精度损失
- **现有方案不足**: SVD和量化独立使用，未利用SVD的奇异值分布指导量化位宽的非均匀分配
- **本文解决思路**: SingularBit将SVD与低bit量化协同，利用奇异值分布指导混合精度量化，压缩权重+KV

---

### Session 6A: LLM 4

---

#### ☆ 20. Tetris: Efficient Long-context LLM Serving with Chunkwise Dynamic Sequence Parallelism
- **研究背景**: 长上下文LLM serving中序列并行是分布推理关键，但固定chunk大小忽略attention稀疏性
- **要解决的问题**: 长序列推理中如何动态调整sequence parallelism的chunk划分以适配不同位置的attention密度
- **现有方案不足**: 固定大小chunk造成attention密度高的位置计算瓶颈、稀疏位置算力浪费
- **本文解决思路**: Tetris chunkwise动态序列并行，根据attention score分布在线调整chunk边界，负载均衡

---

#### ☆ 21. SMoE: An Algorithm-System Co-Design for Pushing MoE to the Edge via Expert Substitution
- **研究背景**: MoE模型参数大但每次推理仅激活少量expert，有潜力部署到边缘但总参数量超边缘内存
- **要解决的问题**: 如何将大MoE模型压缩部署到边缘设备，在有限内存下保持推理质量
- **现有方案不足**: 简单剪枝expert丢失知识，知识蒸馏需要大量训练数据和算力
- **本文解决思路**: SMoE算法-系统协同，通过expert替换策略在边缘保留最关键的expert子集，无需重训练

---

#### ☆ 22. ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs
- **研究背景**: 华为昇腾NPU生态需要高效模型压缩方案，无损压缩对精度敏感的推理任务至关重要
- **要解决的问题**: 面向昇腾NPU的无损AI模型压缩，需兼顾高压缩比和NPU上的快速解压推理
- **现有方案不足**: 通用无损压缩算法未适配NPU的DaVinci架构计算模式，解压成为推理瓶颈
- **本文解决思路**: ENEC面向昇腾NPU的无损压缩方法，压缩格式对齐NPU矩阵计算单元，解压与GEMM融合

---

#### ☆ 23. STEP: Adaptive Spatio-Temporal Expert Prefetching for Low-Latency and Memory-Efficient MoE Inference
- **研究背景**: MoE推理中expert的加载延迟影响端到端推理延迟，prefetching可隐藏加载但预测不准
- **要解决的问题**: 如何准确预测下一个token所需的expert以实现及时prefetch，降低MoE推理延迟
- **现有方案不足**: 基于历史频率的静态prefetch忽略token间的时序依赖和空间局部性，预测准确率低
- **本文解决思路**: STEP自适应时空expert预取，结合spatial（层间）和temporal（token间）特征预测expert需求

---

#### ☆ 24. EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture
- **研究背景**: LLM解码阶段的矩阵向量乘法（GEMV）受限于权重访存带宽，量化可压缩权重但需高效解压
- **要解决的问题**: 如何设计高效的向量量化硬件架构，使解压延迟不成为GEMV的瓶颈
- **现有方案不足**: 标量量化压缩比低，K-means等向量量化解压查表延迟高，无法与GEMV流水线匹配
- **本文解决思路**: EVA高效VQ架构，设计低延迟码本查表单元与GEMV流水线深度耦合

---

### Session 10A: LLM 5

---

#### ☆ 25. Scalable Synthesis of Distributed LLM Workloads Through Symbolic Tensor Graphs
- **研究背景**: LLM分布式训练的并行策略（DP/TP/PP）组合空间巨大，手工设计无法穷举最优方案
- **要解决的问题**: 如何自动搜索和合成最优的分布式LLM训练/推理并行策略组合
- **现有方案不足**: 现有自动并行方案基于规则或受限搜索空间，无法表达复杂的符号化张量变换
- **本文解决思路**: 基于符号化张量图的分布式workload合成，自动推导最优DP/TP/PP组合

---

#### ☆ 26. DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training
- **研究背景**: 大模型数据并行训练中计算、网络和存储资源耦合分配，导致资源利用率低
- **要解决的问题**: 如何将模型分片的数据并行训练中的计算、网络和存储资源解耦，提高资源利用率
- **现有方案不足**: 资源耦合分配造成GPU等待梯度同步时空闲、存储I/O与计算串行
- **本文解决思路**: DisDP分离式架构，计算/网络/存储独立弹性伸缩，异步流水化三者的执行

---

#### ☆ 27. MoE-Hub: Taming Software Complexity for Seamless MoE Overlap with Hardware-Accelerated Communication on Multi-GPU Systems
- **研究背景**: 多GPU MoE训练/推理中计算-通信重叠是隐藏all-to-all延迟的关键，但软件实现复杂
- **要解决的问题**: MoE中expert计算与all-to-all通信的重叠在软件层面实现复杂，难以无缝利用硬件加速通信
- **现有方案不足**: 手工编写计算-通信重叠代码易出错，无法透明利用NCCL/RDMA等硬件加速
- **本文解决思路**: MoE-Hub软件框架，自动分析MoE计算图并插入通信-计算重叠，透明利用硬件加速通信

---

#### ☆ 28. Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs
- **研究背景**: 多模态LLM服务需要同时处理文本和图像，不同模态的计算/访存特征差异大
- **要解决的问题**: 多模态LLM serving中如何动态平衡GPU间的并行度和GPU内SM/带宽资源的分配
- **现有方案不足**: 静态资源分配无法适应多模态请求的动态混合，GPU间和GPU内的负载不均衡
- **本文解决思路**: Symbiotic动态平衡框架，跨GPU并行度和GPU内资源细粒度动态调度

---

## 二、Security / Rowhammer（3 sessions, 16 papers）

### Session 3C: Security

---

#### ☆ 29. Towards Practical Interrupt Side-Channel Attacks on macOS for Apple Silicon
- **研究背景**: Apple Silicon Mac市场份额快速增长，其安全特性与传统x86不同，侧信道威胁有待揭示
- **要解决的问题**: Apple Silicon上macOS中断机制的侧信道泄露，探讨实用化攻击的可行性
- **现有方案不足**: 现有侧信道研究集中在x86/ARM Linux，对Apple Silicon的中断子系统缺乏分析
- **本文解决思路**: 首次系统性分析Apple Silicon中断侧信道，利用中断时序差异构建实用攻击

---

#### ☆ 30. Helium: Quantifying Microarchitectural Side-Channel Leakage with Probabilistic Guarantees
- **研究背景**: 微架构侧信道是CPU安全的长期威胁，但缺乏量化的泄露度量框架来评估防御效果
- **要解决的问题**: 如何量化微架构侧信道的泄露程度，给出概率性保证而非二元的"安全/不安全"
- **现有方案不足**: 现有方法定性分析或经验性评估，缺乏形式化的概率泄露上界
- **本文解决思路**: Helium概率性侧信道泄露量化框架，建模微架构状态竞争，给出泄露比特数上界

---

#### ☆ 31. LÆGIS: Pinpointing and Addressing Performance Overheads of GPU-based Confidential Computing
- **研究背景**: GPU TEE（如NVIDIA Confidential Computing）为LLM推理提供安全环境，但引入性能开销
- **要解决的问题**: GPU机密计算的性能开销来源不明确，缺乏系统性分析和针对性优化方案
- **现有方案不足**: 对GPU TEE开销的认知停留在黑盒benchmark，未定位具体微架构层面的瓶颈
- **本文解决思路**: LÆGIS精确定位GPU TEE性能开销的微架构来源（加密/认证/页表遍历），提出针对性优化

---

#### ☆ 32. MC-ORAM: A Mask-Assisted and Counter-Based Non-Deterministic ORAM inside VM-Based TEEs
- **研究背景**: VM-based TEE（如AMD SEV/Intel TDX）中访存模式泄露敏感信息，ORAM可隐藏但开销大
- **要解决的问题**: VM级TEE中ORAM的性能开销过高，需要轻量级方案保护访存模式隐私
- **现有方案不足**: 确定性的Path ORAM带宽开销大，且无法利用VM级TEE的大页和嵌套页表特性
- **本文解决思路**: MC-ORAM掩码辅助+计数器驱动的非确定性ORAM，利用TEE大页降低元数据开销

---

#### ☆ 33. TimeGaps Channels: Exploiting CPU Halted Time for Fun and Profit
- **研究背景**: 现代CPU在空闲时进入halt状态以节能，但halt/唤醒的时序差异可能构成新的隐蔽信道
- **要解决的问题**: CPU halt/唤醒的时间间隔（TimeGaps）是否可被利用为跨核心的隐蔽信道
- **现有方案不足**: 现有侧信道研究关注cache/分支预测器等微架构状态，未关注CPU电源管理状态
- **本文解决思路**: TimeGaps首次揭示CPU halted time可构成隐蔽信道，分析其带宽和跨核心可靠性

---

### Session 5C: Crypto and Security

---

#### ☆ 34. μRNG: A Framework for Assessing Randomness in Intermittent Computing Devices
- **研究背景**: 间歇计算设备（能量采集IoT）依赖随机数生成器做安全通信，但上电状态的不确定性影响RNG质量
- **要解决的问题**: 间歇计算场景下随机数生成器的随机性质量如何评估，上电/掉电循环是否削弱熵
- **现有方案不足**: 标准RNG测试套件假设持续供电，未考虑间歇供电下SRAM上电值的熵退化
- **本文解决思路**: μRNG框架专门评估间歇计算RNG质量，分析上电/掉电循环对SRAM PUF熵的影响

---

#### ☆ 35. IroKnight: Ownership-Preserving Neural Acceleration for Inference Serving
- **研究背景**: 模型推理即服务中，模型所有者担心模型被盗，用户担心输入泄露
- **要解决的问题**: 如何在云端推理服务中同时保护模型所有权和用户数据隐私
- **现有方案不足**: TEE保护计算但无法完全防止模型参数通过侧信道泄露，水印可证明所有权但不够强
- **本文解决思路**: IroKnight所有权保持的神经加速方案，模型参数加密+运行时认证，防止窃取和滥用

---

#### ☆ 36. Intermittence-aware Speculative Page Coloring for Secure NVM
- **研究背景**: 非易失内存(NVM)的持久性引入新的安全威胁，数据残留和磨损均衡与安全着色冲突
- **要解决的问题**: NVM上如何实现安全的页着色(Page Coloring)以防止缓存侧信道，同时考虑磨损均衡
- **现有方案不足**: DRAM的页着色方案未考虑NVM写入耐久性和持久数据残留问题
- **本文解决思路**: 间歇感知的投机性页着色，动态调整着色策略以平衡安全性、磨损均衡和持久性

---

#### ☆ 37. AutoFHE: An Automatic Hardware Generation Framework for Domain-Specific FHE Accelerator
- **研究背景**: FHE应用场景多样化（医疗/金融/ML），各场景算子和参数差异大，手工设计加速器效率低
- **要解决的问题**: 如何自动生成面向特定FHE应用场景的定制化硬件加速器，降低设计门槛
- **现有方案不足**: 通用FHE加速器效率不如领域定制，手工设计每个加速器耗时且需要跨领域专家
- **本文解决思路**: AutoFHE自动硬件生成框架，输入FHE算子和参数规格，输出优化的RTL加速器

---

#### ☆ 38. LIPPEN: A Lightweight In-Place Pointer Encryption Architecture for Pointer Integrity
- **研究背景**: 内存安全漏洞（use-after-free/buffer overflow）主要利用指针篡改，指针加密是轻量防御
- **要解决的问题**: 如何实现轻量级指针原地加密，不修改指针宽度和内存布局，兼容现有软件
- **现有方案不足**: ARM PAC需要额外指令和指针空间，软指针加密性能开销大，不兼容遗留代码
- **本文解决思路**: LIPPEN轻量原地指针加密架构，利用未使用的指针高位bit做加密，无需修改内存布局

---

#### ☆ 39. DarkStream: Exploiting Internal Throughput Contention in Data Streaming Accelerator for Timing Attacks
- **研究背景**: 数据流加速器（如DMA/数据搬移引擎）在多租户环境中共享，内部吞吐争用可能泄露信息
- **要解决的问题**: 数据流加速器内部吞吐争用是否构成新的计时侧信道，攻击者如何跨租户提取信息
- **现有方案不足**: 现有共享加速器安全研究集中在GPU和NPU，数据流搬移引擎的安全被忽视
- **本文解决思路**: DarkStream展示数据流加速器内部吞吐争用的计时攻击，利用DMA通道带宽竞争泄露信息

---

### Session 6D: Rowhammer and Security

---

#### ☆ 40. ColumnKeeper: Efficient Solutions to the ColumnDisturb Vulnerability in DRAM-based Systems
- **研究背景**: ColumnDisturb是继RowHammer之后新型DRAM扰动漏洞，激活同一row的多个column导致邻居column数据翻转
- **要解决的问题**: DRAM ColumnDisturb漏洞的高效防御方案，需兼顾性能开销和安全性
- **现有方案不足**: RowHammer防御方案无法直接移植到ColumnDisturb，列粒度的追踪开销更大
- **本文解决思路**: ColumnKeeper轻量ColumnDisturb防御，利用列访问计数器+自适应刷新策略

---

#### ☆ 41. PVAC: A RowHammer Mitigation Architecture Exploiting Per-victim-row Counting
- **研究背景**: RowHammer仍是DRAM最主要的安全威胁，JEDEC标准刷新窗口内的多次激活可翻转邻居行
- **要解决的问题**: 如何以极低硬件开销精确追踪每行的激活次数，避免假阳性刷新浪费性能
- **现有方案不足**: 概率性方案存在安全窗口，确定性计数器方案SRAM开销大，现有per-row追踪硬件成本高
- **本文解决思路**: PVAC per-victim-row计数架构，仅追踪被攻击的victim行而非所有行，大幅降低硬件成本

---

#### ☆ 42. Loaded Dice: Solving the Non-Selection Problem for Scalable Probabilistic RowHammer Defense
- **研究背景**: 概率性RowHammer防御（随机选择行刷新）硬件开销低，但"非选择问题"导致某些行长期未被刷新
- **要解决的问题**: 概率性防御中部分行长期未被选中刷新，在足够长的攻击窗口下仍有可能被攻破
- **现有方案不足**: 纯随机选择无法保证每行在安全窗口内被刷新，确定性的表计数器开销高
- **本文解决思路**: Loaded Dice解决非选择问题，biased随机策略确保每行在概率上被及时刷新

---

#### ☆ 43. PRowhammer: Propagating Bit-flips from CPU to GPU
- **研究背景**: 异构系统中CPU和GPU共享DRAM控制器，但RowHammer研究长期聚焦单一处理器类型
- **要解决的问题**: CPU侧的RowHammer攻击是否可以跨处理器传播到GPU侧的内存空间
- **现有方案不足**: CPU和GPU的RowHammer防御独立，未考虑跨处理器类型的攻击传播
- **本文解决思路**: PRowhammer首次展示CPU-GPU间RowHammer bit-flip传播，揭示统一内存的跨处理器安全风险

---

#### ☆ 44. DejaVu: Why You Should Write to Your DRAM Rows Twice, Carefully
- **研究背景**: RowHammer的根本原因是多次激活相邻行导致电荷泄露，写操作可以"重置"行状态
- **要解决的问题**: 利用写操作缓解RowHammer，但普通写操作可能不够精确，需要"小心地写两次"
- **现有方案不足**: 现有刷新方案是被动防御，未利用主动写操作来"修复"被扰动的行
- **本文解决思路**: DejaVu提出对DRAM行"仔细写两次"的策略，精确恢复被RowHammer扰动的电荷状态

---

## 三、PIM/PNM 存内计算（3 sessions, 13 papers）

### Session 2B: Memory Systems and PIM/PNM

---

#### ☆ 45. ECC Enabled Reliable and Performant Processing-in-Memory
- **研究背景**: PIM在DRAM内部执行计算，但DRAM工艺的bit错误率高于逻辑工艺，PIM计算可靠性堪忧
- **要解决的问题**: PIM计算单元在DRAM工艺下的可靠性保障，需将ECC与PIM计算高效整合
- **现有方案不足**: 现有PIM设计假设DRAM可靠性足够，或简单复用存储ECC但对计算延迟影响大
- **本文解决思路**: ECC使能的高性能可靠PIM，设计可同时保护存储和计算的统一ECC方案

---

#### ☆ 46. HBM-CASO: A Coordinated Approach to HBM System-Level and On-Die ECC
- **研究背景**: HBM的高带宽和堆叠架构使数据可靠性面临独特挑战，System-Level和On-Die ECC需协调
- **要解决的问题**: HBM中系统级ECC和片上ECC如何协同工作，避免冗余和覆盖盲区
- **现有方案不足**: SL-ECC和OD-ECC独立设计导致保护重叠和覆盖缺口，纠错能力未被最大化
- **本文解决思路**: HBM-CASO协同方案，协调系统级和片上ECC的纠错分工，统一纠错预算分配

---

#### ☆ 47. ATX: Accelerator Task Extensions
- **研究背景**: 近存/存内加速器缺乏统一的编程和接口模型，CPU与加速器之间的任务调度效率低
- **要解决的问题**: 如何设计通用加速器任务扩展接口，使CPU能高效offload任务到近存/存内加速器
- **现有方案不足**: 各加速器有专有接口，缺乏统一的指令集扩展，调度开销大且不可移植
- **本文解决思路**: ATX加速器任务扩展ISA，定义统一的offload/同步/数据移动原语

---

### Session 3B: DRAM and SRAM PIM/PNM

---

#### ☆ 48. Taking Analytic Databases to the Bank
- **研究背景**: 分析数据库的扫描/聚合/Join操作为memory-bound，PIM在DRAM bank内计算可消除数据搬移
- **要解决的问题**: 如何将分析型数据库的核心算子直接部署到DRAM bank内的PIM单元中
- **现有方案不足**: 现有PIM大数据工作仅限于简单向量运算，未覆盖数据库完整的算子集
- **本文解决思路**: 首次将分析数据库全栈部署到DRAM bank级别，设计scan/aggregate/join的PIM实现

---

#### ☆ 49. PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips
- **研究背景**: Processing-using-DRAM(PuD)在不修改DRAM芯片的情况下实现存内计算，但结果正确性缺乏真实芯片验证
- **要解决的问题**: 真实DRAM芯片上PuD操作的计算结果是否存在corruption，影响程度和机理是什么
- **现有方案不足**: PuD研究依赖模拟器或理想化假设，从未在真实DRAM芯片上大规模测试计算正确性
- **本文解决思路**: PuDGhost首次在真实DRAM芯片上实验分析PuD计算腐败，揭示工艺偏差和时序margin影响

---

#### ☆ 50. MERIDIAN: In-Memory Acceleration for RAG with Document Attention Decomposition
- **研究背景**: RAG(检索增强生成)中长文档的注意力计算成为新瓶颈，文档长度可达数万token
- **要解决的问题**: RAG中文档注意力的高计算和访存需求，如何利用存内计算高效加速
- **现有方案不足**: GPU/TPU处理长文档注意力时KV cache访存成为瓶颈，PIM方案未针对文档注意力设计
- **本文解决思路**: MERIDIAN存内加速RAG，将文档注意力分解后在PIM单元中并行计算，减少KV搬移

---

#### ☆ 51. PipeIMC: a Pipelined In-SRAM Computing Architecture
- **研究背景**: In-SRAM计算利用SRAM的bit-cell阵列做模拟计算，但计算延迟限制了吞吐率
- **要解决的问题**: SRAM存内计算的流水线化，使不同计算阶段可重叠执行以提升吞吐
- **现有方案不足**: 现有SRAM存内计算为单周期或固定多周期，无流水线导致吞吐受限
- **本文解决思路**: PipeIMC流水线化SRAM存内计算架构，将ADC/移位/累加分阶段流水执行

---

#### ☆ 52. BAAP: Coupling Compute-in-SRAM with DRAM Banks for Near-Memory Processing
- **研究背景**: DRAM-based PIM算力有限（每bank仅少量ALU），SRAM-based CIM算力高但容量小
- **要解决的问题**: 如何将SRAM存算(高算力)与DRAM近存(大容量)耦合，发挥两者优势
- **现有方案不足**: SRAM-CIM和DRAM-PIM独立设计，缺乏统一的数据流调度和容量-算力权衡
- **本文解决思路**: BAAP将Compute-in-SRAM与DRAM Bank耦合为近存处理层级，SRAM做计算DRAM做存储

---

### Session 10C: PIM/PNM, cont.

---

#### ☆ 53. AXLE: Coordinated Offloading with Asynchronous Back-Streaming in Computational Memory Systems
- **研究背景**: 计算型内存系统中CPU与PIM的offload为同步阻塞模式，CPU等待PIM完成再取结果
- **要解决的问题**: PIM offload改为异步模式，PIM计算结果边产生边回传，CPU无需等待全完成
- **现有方案不足**: 同步offload造成CPU空转，PIM结果的回传无法与后续计算overlap
- **本文解决思路**: AXLE异步回流传输，PIM边计算边将结果流式传回CPU，实现offload与计算重叠

---

#### ☆ 54. DCC: Data-Centric Compilation of Machine Learning Kernels for Processing-In-Memory Architectures
- **研究背景**: PIM架构的编程模型与GPU/CPU截然不同，数据位置决定计算位置，传统编译器未适配
- **要解决的问题**: 如何编译ML kernel到PIM架构上，以数据为中心自动决定哪些算子放到哪些PIM单元
- **现有方案不足**: 现有PIM编程依赖手工标注或简单规则，无法自动做数据-计算的最优映射
- **本文解决思路**: DCC以数据为中心的PIM编译框架，基于数据流图自动推导数据放置和算子映射

---

#### ☆ 55. Optimizing Spatial Data Structure with Near-Cache Acceleration by Exploiting Physical Locality
- **研究背景**: 空间数据结构（树/图/哈希）的指针追逐导致cache miss率高，近cache加速可减少访存延迟
- **要解决的问题**: 利用物理局部性（物理地址相邻）和近cache计算加速空间数据结构的遍历
- **现有方案不足**: 现有prefetcher对无规律指针追逐效果差，PIM方案粒度太粗无法处理单指针解引用
- **本文解决思路**: 近cache加速单元拦截指针追逐，利用物理地址局部性在cache侧完成遍历

---

#### ☆ 56. Bridging Efficiency and Scalability in LLM System via 3D Hybrid PIM with 2D In-Transit Computation
- **研究背景**: 3D堆叠PIM提供高带宽但众核PIM间的数据交换是瓶颈，2D In-Transit计算提供横向通信
- **要解决的问题**: 如何在3D混合PIM系统中结合垂直高带宽和水平数据交换，高效支持LLM推理
- **现有方案不足**: 纯3D PIM层间通信好但层内横向通信差，难以处理LLM的all-reduce/all-to-all
- **本文解决思路**: 3D混合PIM + 2D传输中计算，垂直和水平维度各司其职，Bridging效率与规模

---

#### ☆ 57. Early Silicon of Raptor: The First 3D-DRAM Accelerator for Generative Inference
- **研究背景**: 3D-DRAM堆叠加速器从学术界概念走向硅验证，生成式推理是首个目标场景
- **要解决的问题**: 首个3D-DRAM AI加速器的实际硅验证结果，展示真实性能、功耗和良率
- **现有方案不足**: 3D-DRAM加速器停留在模拟阶段，缺乏实际芯片数据无法评估真实可行性
- **本文解决思路**: Raptor首个3D-DRAM生成式推理加速器early silicon，报告实测性能/功耗/面积

---


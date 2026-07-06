# ISCA 2026 热点领域论文逐篇四要素分析 (Part 2)

> 每篇论文提炼四个要素（各≤50字）：研究背景、要解决的问题、现有方案不足、本文解决思路
> ☆ 标注：基于标题信息分析（ISCA 2026论文尚未在arxiv公开）
> 分析日期: 2026-07-06

---

## 四、ML Accelerators（2 sessions, 10 papers）

### Session 3A: ML Accelerators 1

---

#### ☆ 58. Shining Light on Silicon Photonic DNN Accelerators
- **研究背景**: 硅光子计算利用光干涉实现矩阵乘法，能效比电子计算高几个数量级，但工程化挑战大
- **要解决的问题**: 硅光子DNN加速器的实际可实现性、精度限制和系统集成挑战的系统性分析
- **现有方案不足**: 光计算研究停留在理论或小规模demo，缺乏对大规模DNN部署的实际约束分析
- **本文解决思路**: 系统性"照亮"硅光子DNN加速器，从器件到系统层面分析精度/能效/扩展性瓶颈与出路

---

#### ☆ 59. TensorPrism: Rethinking Sparse High-order Tensor Acceleration via Co-occurrence Graph
- **研究背景**: 高阶稀疏张量在推荐系统/图神经网络中普遍存在，但稀疏模式无规则导致加速困难
- **要解决的问题**: 高阶稀疏张量的不规则稀疏模式如何通过共现图（Co-occurrence Graph）重新组织和加速
- **现有方案不足**: 现有稀疏加速器针对1D/2D稀疏设计，高阶张量展开后稀疏模式被打散
- **本文解决思路**: TensorPrism用共现图捕获高阶稀疏模式，基于图结构设计专用的乘法/累加调度

---

#### ☆ 60. OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration
- **研究背景**: LLM权重和激活值存在大量异常值(outlier)，均匀量化严重损失精度，LUT是替代MAC的新范式
- **要解决的问题**: 如何设计outlier感知的LUT-based GEMM，在保持精度的同时利用双侧量化提高效率
- **现有方案不足**: LUT-based方案对outlier敏感，单侧量化无法同时压缩权重和激活
- **本文解决思路**: OASIS outlier感知的LUT-GEMM，对outlier和正常值分别LUT编码，双侧量化最大化压缩

---

#### ☆ 61. Omni-LUT: Energy-Efficient LUT-based Accelerator with Hardware-Aware KV Cache Quantization
- **研究背景**: LLM推理中KV cache是主要内存瓶颈，LUT-based计算天然适合低精度非均匀量化
- **要解决的问题**: 如何结合硬件感知的KV cache量化和LUT-based计算架构，最大化端侧LLM能效
- **现有方案不足**: KV cache量化与计算架构分离设计，量化格式的选择未与LUT硬件特性对齐
- **本文解决思路**: Omni-LUT硬件感知KV cache量化+LUT加速器，量化格式与LUT硬件深度协同

---

#### ☆ 62. QiMeng-Tensify: Scaling up Tensor Computation Optimization via Architecture-Aware LLM-Guided MCTS
- **研究背景**: 张量计算的优化空间（算子融合/tiling/调度）巨大，传统自动调优难以规模化
- **要解决的问题**: 如何利用LLM的推理能力引导蒙特卡洛树搜索(MCTS)，自动发现大规模张量优化策略
- **现有方案不足**: AutoTVM等基于模板搜索空间有限，RL-based方案采样效率低，无法利用领域知识
- **本文解决思路**: QiMeng-Tensify用LLM引导MCTS搜索张量优化空间，架构感知的reward设计

---

### Session 10B: ML Accelerators 2

---

#### ☆ 63. Dynamic Scheduling for AI Accelerators via TISA
- **研究背景**: AI加速器需要同时处理多种不同形状和资源的算子，静态调度无法适应动态workload
- **要解决的问题**: 如何设计任务指令集架构(TISA)实现AI加速器的动态调度，提高资源利用率
- **现有方案不足**: 静态编译调度无法适应运行时变化，动态调度的硬件复杂度高
- **本文解决思路**: TISA任务指令集架构，定义动态调度原语使加速器运行时自适应workload变化

---

#### ☆ 64. MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration
- **研究背景**: AI训练推理需要比IEEE754更灵活的浮点格式，Microscaling(共享指数)是主流方向
- **要解决的问题**: 设计一种灵活的Microscaling浮点格式，在动态范围和精度间取得最优权衡
- **现有方案不足**: FP8/MX格式的指数/尾数位宽固定，不能按layer/tensor动态调整精度分配
- **本文解决思路**: MXFFP灵活的Microscaling浮点格式，运行时可配置指数共享粒度和尾数位宽

---

#### ☆ 65. UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference
- **研究背景**: LLM推理需要支持多种精度（FP16/INT8/INT4），各自使用不同GEMM单元浪费面积
- **要解决的问题**: 设计统一的可伸缩位宽GEMM单元，在单一硬件上高效支持多种精度
- **现有方案不足**: 多套精度单元面积冗余，精度切换开销大，无法动态组合低精度实现高吞吐
- **本文解决思路**: UniCore位宽可伸缩GEMM单元，通过可重构MAC阵列统一支持INT4到FP16

---

#### ☆ 66. XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA
- **研究背景**: FPGA的DSP资源有限，LLM推理的混合精度需求需要高效的MAC架构设计
- **要解决的问题**: 如何在FPGA有限的DSP上设计高效的混合精度MAC，最大化LLM推理吞吐
- **现有方案不足**: FPGA DSP固定位宽映射效率低，混合精度方案无法灵活适配不同量化配置
- **本文解决思路**: XtraMAC高效MAC架构，利用FPGA DSP的级联特性实现混合精度packing计算

---

#### ☆ 67. ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing
- **研究背景**: 脉冲神经网络(SNN)以事件驱动和稀疏计算著称，但不同输入产生不同脉冲数导致负载不均衡
- **要解决的问题**: SNN推理中脉冲数的弹性变化需要弹性架构，避免固定timestep造成算力浪费
- **现有方案不足**: 固定timestep架构在低脉冲输入时空转，无法根据输入动态调整计算资源
- **本文解决思路**: ELSA弹性SNN推理架构，根据脉冲密度动态伸缩计算阵列，空闲单元进入低功耗

---

## 五、Quantum Computing（3 sessions, 12 papers）

### Session 4D: Quantum 1

---

#### ☆ 68. Triage: An Adaptive Parallel Window Decoding Scheduler for Real-time Fault-Tolerant Quantum Computation
- **研究背景**: 容错量子计算(FTQC)需要实时解码纠错Syndrome，解码延迟直接影响逻辑量子比特保真度
- **要解决的问题**: 量子纠错解码的实时调度——如何并行处理多个解码窗口，优先处理最紧迫的syndrome
- **现有方案不足**: FIFO或固定窗口解码无法根据错误严重程度做优先级调度，关键syndrome被延迟
- **本文解决思路**: Triage自适应并行窗口解码调度器，根据错误密度和逻辑比特紧急度动态优先级排序

---

#### ☆ 69. Coset Ensemble Decoder for Quantum Error Correction with Algorithm-Hardware Co-Design
- **研究背景**: 量子纠错码(QEC)解码是FTQC的核心瓶颈，解码算法复杂度高且需要硬件加速
- **要解决的问题**: 如何算法-硬件协同设计QEC解码器，在解码精度和硬件延迟间取得最优
- **现有方案不足**: 算法和硬件独立优化，解码算法未考虑硬件的并行度约束和存储限制
- **本文解决思路**: Coset Ensemble Decoder算法-硬件协同，将陪集分解与硬件并行度对齐

---

#### ☆ 70. A Streaming Architecture for Quantum Error Syndrome Compression at 4 Kelvin
- **研究背景**: 量子处理器工作在mK级温度，纠错syndrome数据从低温传到室温的带宽是关键瓶颈
- **要解决的问题**: 如何在4K低温环境下对syndrome数据流式压缩，减少低温到室温的数据传输量
- **现有方案不足**: 原始syndrome数据不经压缩传输，I/O带宽成为扩展瓶颈，且压缩电路需耐低温
- **本文解决思路**: 4K低温流式syndrome压缩架构，设计低温CMOS兼容的轻量压缩电路

---

#### ☆ 71. Transpiler-Architecture Co-Design to Curb Clifford Costs in Fault-Tolerant Quantum Computing
- **研究背景**: Clifford门在QEC中消耗大量物理量子比特和时间，但其经典可模拟性可被利用
- **要解决的问题**: 如何通过Transpiler与架构协同设计，减少FTQC中Clifford门的物理代价
- **现有方案不足**: Transpiler优化不考虑底层架构的Clifford执行特性，两者独立导致次优
- **本文解决思路**: Transpiler-架构协同缩减Clifford开销，Transpiler感知架构特性重组Clifford序列

---

#### ☆ 72. Kernpiler: Compiler Optimization for Quantum Hamiltonian Simulation with Partial Trotterization
- **研究背景**: 量子哈密顿量模拟是量子计算核心应用，Trotterization分解精度与深度的权衡是编译关键
- **要解决的问题**: 如何对哈密顿量模拟做部分Trotterization编译优化，不同term用不同Trotter步数
- **现有方案不足**: 统一Trotter步数导致简单term被过度分解(浪费深度)或复杂term精度不足
- **本文解决思路**: Kernpiler部分Trotterization编译框架，根据term复杂度自适应分配Trotter步数

---

### Session 8C: Quantum 2

---

#### ☆ 73. Distilling Magic States in the Bicycle Architecture
- **研究背景**: Magic State蒸馏是FTQC的非Clifford门实现方式，但蒸馏开销大，Bicycle码是新平台
- **要解决的问题**: 如何在Bicycle量子LDPC码架构上高效蒸馏Magic State
- **现有方案不足**: 现有Magic State蒸馏方案针对surface code设计，未适配Bicycle码的连通性
- **本文解决思路**: 在Bicycle架构上重新设计Magic State蒸馏流程，利用LDPC的高编码率减少物理qubit需求

---

#### ☆ 74. O3LS: Optimizing Lattice Surgery via Automatic Layout Searching and Loose Scheduling
- **研究背景**: Lattice Surgery是surface code上多量子比特操作的核心技术，布局和调度影响操作延迟
- **要解决的问题**: 如何自动搜索最优Lattice Surgery布局和宽松调度，在不牺牲保真度前提下减少延迟
- **现有方案不足**: 手工布局和紧调度限制优化空间，缺乏对布局空间的形式化搜索
- **本文解决思路**: O3LS自动布局搜索+宽松调度，形式化Lattice Surgery约束并自动推导最优plan

---

#### ☆ 75. Leveraging Phase Polynomials for Quantum Circuit Optimization
- **研究背景**: 量子电路优化是编译的关键环节，相位多项式(Phase Polynomial)是描述Clifford+T电路的有力工具
- **要解决的问题**: 如何利用相位多项式表示进行量子电路优化，超越基于门的传统优化方法
- **现有方案不足**: 基于门的优化规则（合并/消除）只能做局部变换，无法发现全局相位抵消机会
- **本文解决思路**: 利用相位多项式全局表示电路，在多项式层面做优化变换再映射回门电路

---

### Session 9C: Quantum 3

---

#### ☆ 76. Unifying Qubit Routing Across Diverse Quantum ISAs via Canonical Representation
- **研究背景**: 多样化量子ISA（超导/离子阱/中性原子）的连通性差异大，qubit routing各自实现
- **要解决的问题**: 如何用统一的正则表示(Canonical Representation)为不同量子ISA做qubit routing
- **现有方案不足**: 各平台有专用router，换平台需重新实现，无法跨ISA复用routing优化
- **本文解决思路**: 将各ISA连通图映射到统一的正则表示，routing算法一次编写跨平台部署

---

#### ☆ 77. TUSQ: Tracking, Uncomputation, and Sampling for Noisy Quantum Simulation
- **研究背景**: 含噪量子模拟是评估NISQ算法和纠错码的重要工具，但计算量和内存消耗巨大
- **要解决的问题**: 如何通过追踪(Tracking)、反计算(Uncomputation)和采样(Sampling)降低噪声模拟开销
- **现有方案不足**: 全状态向量模拟内存指数增长，张量网络收缩忽略噪声追踪
- **本文解决思路**: TUSQ三管齐下：追踪噪声传播、反计算回收内存、采样近似，降低模拟复杂度

---

#### ☆ 78. Photonic Quantum Computing on Spin Memory Architecture with Tree-Encoded Fusion
- **研究背景**: 光子量子计算的优势在室温操作和长距离传输，但光子-光子纠缠概率性限制了规模化
- **要解决的问题**: 如何利用自旋存储(Spin Memory)和树编码融合(Tree-Encoded Fusion)提升光子量子计算规模
- **现有方案不足**: 概率性纠缠门成功率低导致计算图构建失败率高，线性光学的确定性门受限
- **本文解决思路**: Spin Memory存储光子态等待纠缠+Tree-Encoded Fusion树形编码提升融合成功概率

---

#### ☆ 79. SATIC: An Optimizing Ising Compiler for SAT(isfiability)
- **研究背景**: Ising机(量子退火/CMOS Ising)求解组合优化问题，SAT是核心应用但映射到Ising模型效率低
- **要解决的问题**: 如何将SAT问题高效编译到Ising模型（二次无约束二值优化QUBO），减少辅助变量
- **现有方案不足**: 直接映射产生大量辅助spin变量，超出Ising机容量
- **本文解决思路**: SATIC优化Ising编译，利用SAT子句结构做逻辑-物理联合优化减少辅助变量

---

## 六、FHE 全同态加密（1 sessions + AutoFHE, ~7 papers）

### Session 7D: FHE

---

#### ☆ 80. FEnc2: Unifying Data Packing for Efficient Private Inference via Convolution and Architecture-Aware Fragment Encoding
- **研究背景**: FHE的私人推理(Private Inference)需要将神经网络算子编码为FHE密文，编码效率决定推理速度
- **要解决的问题**: 如何统一卷积和全连接层的数据打包编码，减少FHE密文数量和乘法深度
- **现有方案不足**: 卷积和FC使用不同编码方案，切换开销大，加密参数未与架构对齐
- **本文解决思路**: FEnc2统一打包编码，卷积和FC用同一套编码框架，架构感知的片段编码优化

---

#### ☆ 81. FlashTFHE: A Scalable Architecture for Efficient Multi-bit Fully Homomorphic Encryption
- **研究背景**: TFHE支持快速自举(bootstrapping)但门级（单bit）操作效率低，多bit操作需要可扩展架构
- **要解决的问题**: 如何设计可扩展的多bit TFHE加速架构，提高密文计算的吞吐量
- **现有方案不足**: 现有TFHE加速器bit-serial吞吐低，多bit并行面临密文膨胀和存储瓶颈
- **本文解决思路**: FlashTFHE可扩展多bit TFHE架构，并行处理多位密文+层次化存储优化

---

#### ☆ 82. Unlocking Pipeline Parallelism for Bootstrapping: A Pipelined Multi-Chiplet TFHE Accelerator
- **研究背景**: TFHE的自举(bootstrapping)是计算最密集的操作，占据FHE推理90%以上的时间
- **要解决的问题**: 如何通过流水线化和多Chiplet并行加速TFHE bootstrapping，突破单芯片算力瓶颈
- **现有方案不足**: 单芯片bootstrapping吞吐有限，多芯片方案缺乏对bootstrapping流水线特性的利用
- **本文解决思路**: 多Chiplet流水线TFHE加速，将bootstrapping各阶段分配到不同chiplet流水执行

---

#### ☆ 83. HE^2: A Communication-Light Heterogeneous Architecture for Efficient Fully Homomorphic Encryption
- **研究背景**: FHE计算的不同阶段（NTT/自举/密钥切换）具有不同计算特征，统一架构效率低
- **要解决的问题**: 如何设计通信轻量的异构FHE架构，将不同算子分配到最合适的计算单元
- **现有方案不足**: 同构架构处理所有FHE算子效率不一，异构方案芯片间通信成为瓶颈
- **本文解决思路**: HE^2通信轻量异构FHE架构，算子映射到专用单元+低开销跨单元数据交换

---

#### ☆ 84. HyperDrive: Hierarchical Exploitation of Memory Efficiency for GPU-Based FHE Acceleration
- **研究背景**: GPU的大规模并行和HBM带宽适合FHE加速，但FHE密文的多级存储层次利用不足
- **要解决的问题**: 如何在GPU上层次化利用register/shared/HBM各级存储，最大化FHE内存效率
- **现有方案不足**: GPU FHE实现未精细管理存储层次，频繁的HBM访问成为瓶颈
- **本文解决思路**: HyperDrive层次化GPU FHE内存优化，register缓存RNS残差、shared缓存NTT twiddle

---

#### ☆ 85. MNEMOS: A GPU-based TFHE Acceleration Framework with Memory Access Optimization
- **研究背景**: GPU TFHE加速面临不规则访存模式（密钥切换的随机访问、自举的跨bank访问）
- **要解决的问题**: 如何优化GPU上TFHE的访存模式，减少bank conflict和不规则访存延迟
- **现有方案不足**: 直接映射TFHE到GPU导致大量随机访存和shared memory bank conflict
- **本文解决思路**: MNEMOS GPU TFHE访存优化框架，数据布局重组+访问顺序重排消除bank conflict

---

## 附录：已获取arxiv原文摘要的论文列表

以下论文已成功从arxiv获取摘要（基于ISCA 2026标签确认），分析基于原文内容：

| # | 论文 | arxiv ID |
|---|------|----------|
| 2 | CODO: Automated Compiler for Dataflow Optimization | 2604.12618 |
| 3 | COSM: Cooperative Scheduling for PIM+CPU on Mobile | 2606.30553 |
| 4 | Cerberus: Cross-Layer ECC Co-Design | 2605.02220 |
| 5 | Patterns Behind Chaos: MoE Data Movement | 2510.05497 |
| 6 | Cassandra: Self-Speculative Decoding at Edge | 2605.26558 |
| 7 | Combating Memory Walls (PLENA) | 2509.09505 |
| 8 | Approaching Shannon Bound: Lossless LLM Compression | 2606.15789 |
| 10 | P3-LLM: NPU-PIM Accelerator for Edge LLM | 2511.06838 |
| 14 | Accelerating MoE with In-Switch Computing | 2605.05607 |

> 其余论文因ISCA 2026刚结束(7月1日)，论文尚未上传arxiv或未标注ISCA 2026标签，分析基于论文标题。
> 待论文公开后可补充基于原文的详细分析。

---

## 总结：分析方法论说明

1. **★ 标注**：已从arxiv获取原文摘要，四要素基于摘要+标题提炼
2. **☆ 标注**：论文尚未在arxiv公开，四要素基于标题+领域知识推断
3. 每篇论文的四个要素严格控制在50字以内
4. "研究背景"描述该领域大方向，"要解决的问题"聚焦论文核心挑战
5. "现有方案不足"指出当前方法的gap，"本文解决思路"提炼标题暗示的创新点

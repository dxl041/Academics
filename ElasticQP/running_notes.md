# Elastic QP (SID) 论文分析笔记

> 状态：分析中（§1-§3 已翻译确认，§4-§9 待翻译）

## 0. 论文概述

## 论文一页版总结

### 基本信息
- **标题**: Efficient and Flexible Datapaths for Fine-Grained Rack-Scale Interconnects with Elastic QP
- **会议**: SIGCOMM'26（2026年8月17-21，Denver, CO, USA）
- **作者**: Chenxingyu Zhao（赵宸兴宇，UW 博士），通讯作者 Arvind Krishnamurthy（UW）+ Ming Liu（UW-Madison）
- **DOI**: 10.1145/3789240.3829160（CC-BY 4.0）
- **资助**: ACE（JUMP 2.0/SRC/DARPA）+ NSF CNS-2212193 等多项

### 一句话标题
UW 提出 Software-Interposed Datapath（SID）用 Elastic QP 实现 WQE 级并行，解决 RDMA 小消息低效与硬件固化问题

### 主要观点
- 背景+问题：机架级互连是 scale-up 关键通路，但 RDMA 小消息速率停滞（400GbE 仍瓶颈）且逻辑固化 ASIC 不灵活
- 方案：E-QP 数据机构 + DPA 插接处理器，实现有序 intra-QP 并行（WLP），主机保持无状态单 QP
- 效果：56.50 Mpps（RDMA 的 11.03x），应用最高 12.2x 加速，支持 CPU/GPU-Direct
- [洞察] 留白

### AS-IS（研究背景、问题、现有方案的详细分析）
机架级互连为大数据/HPC/ML 等通信密集型系统提供 scale-up 数据通路。Ethernet 方案（ESUN/SUE、UEC、RoCEv2、Falcon、SRD）竞争激烈，RDMA 商用成熟。但 RDMA 两大局限：1) 逻辑固化 ASIC，不灵活（PCIe 交互、传输协议、操作集均不可编程）；2) 小消息效率低——实测从 100GbE CX5 升到 400GbE CX8，小消息速率停滞，根因不是 NIC 处理能力不足，而是缺乏利用 intra-QP WQE 级并行（WLP）的机制。现有方案靠 QLP（多 QP 多核）榨性能，代价是主机承担有状态分发与排序管理（多 QP 协调、CQE 轮询开销），GPU-Direct 场景负担更重。

### TO-BE（解决方案、效果、不足的详细分析 + 高价值研究点）
SID 将并行与排序管理下沉到 on-NIC 插接处理器（DPA，256 RISC-V 硬件线程），主机保持无状态单 QP 透明抽象。核心思想类比 CPU ILP：请求 FIFO 提交、episode 内乱序执行、完成按序提交。E-QP 用 Billboard 无锁免拷贝分发机制实现 SPMC 并行。FlexOp Engine 提供可扩展操作集（OpenSHMEM + 消息队列）。效果：56.50 Mpps（11.03x），应用 12.2x。不足待分析：依赖 DPA 编程、RX 侧 incast 两级扩展复杂度、与现有 RDMA 生态兼容性。高价值点：WLP 与 QLP 联合（多 E-QP + grant 机制）、PCIe 交互可编程化（batching/MMIO/DMA 切换/request shrinking）。

## 0. 摘要（≤350字中文总结）
机架级互连是新兴通信密集型系统 scale-up 的关键数据通路，Ethernet 方案创新层出不穷，但 RDMA 等硬件方案小消息性能不佳且不灵活。本文提出 Software-Interposed Datapath（SID），高效、软件灵活、低成本，专为细粒度内存访问优化。核心洞察：现有 NIC 主要依赖 QP 级并行（QLP），未充分利用 QP 内 WQE 级并行（WLP）。SID 基于 on-NIC 数据通路处理器（CX8/BF3 DPA）构建 Elastic QP 数据结构，实现有序 intra-QP 并行并最小化协调开销；FlexOp Engine 支持 OpenSHMEM（ML/HPC）与 Message Queue（云服务）可扩展操作集；基于 Ethernet/PCIe/DPA 商用组件低成本构建。评估：小消息 56.50 Mpps，比 RDMA 基线高 11.03x（后者需 8 核 8 QP 才能匹配）；YCSB/SpMM/HPC/ML 应用最高 12.2x 加速；完整支持 CPU 与 GPU-Direct。

## 1. 引言（§1）
- 机架级互连处于网络系统甜点：大于单服务器（可组合更多 GPU），小于集群（拓扑简单，细粒度通信可行，如内存语义 OpenSHMEM）
- RDMA 两局限：ASIC 固化不灵活；小消息效率低（根因非处理能力，而是缺 intra-QP 并行利用机制）
- **RMA Queue Buildup**：本地内存带宽 > 网络带宽 → 远程访问队列堆积；堆积不是缺陷，而是并行机会
- **WLP 类比 ILP**：ILP 硬件吸收并行/排序复杂性、应用透明受益；TLP 应用管线程。WLP 将排序与并行管理下沉 NIC，单 QP 内透明并行；WLP 与 QLP 正交可联合
- **插接处理器三能力**：主机内存 load/store、可编程核+on-NIC 内存、与 Ethernet MAC 紧耦合；DPA 因广泛可及性被选
- **E-QP 原理**：请求 FIFO 提交，但 barrier 之间大多无需严格顺序 → 乱序执行、按序提交（同 CPU OoO）；完成信号按提交顺序暴露，应用感知顺序执行
- 效果预告：56.50 Mpps（11.03x）、应用 12.2x、CPU/GPU-Direct、OpenSHMEM + 消息队列双模型

## 2. 背景（§2）
### 2.1 机架级互连
- 机架 = 数十服务器 ×（多 PE + 匹配 NIC），机架内低直径（1 跳）无过订阅（1:1）交换
- **网络语义**（MPI）：显式 send/receive，粗粒度（64KB）高效；**内存语义**（DSM/PGAS）：load/store 共享内存抽象，细粒度（缓存行级）
- DSM 一致性难扩展 → PGAS 显式分区、无全局一致性，实用可扩展
- OpenSHMEM 分离远程访问（shmem_put）与排序（shmem_fence），排序控制显式 API
### 2.2 ESUN/SUE
- SUE 将 XPU 事务（load/store）转 Ethernet 包；**Packing 模块**：节点内接口带宽 > Ethernet 链路 → 事务在 per-destination 队列累积（图 1b，优化机会）
- SID 与 ESUN 关系：遵循 SUE 部署模型；三点差异贡献：①弹性请求级并行机制（规范未覆盖）②XPU-NIC 交互/传输协议/操作集灵活性 ③真实硬件原型（规范只有抽象描述）
### 2.3 On-NIC 可编程性
- ASIC NIC（CX8）与 SoC SmartNIC（BF3）都含可编程单元；多核处理器位于机内/机间互连桥梁 = **on-NIC 插接处理器**
- BF3：on-path NIC 子系统 + off-path ARM 子系统；本文聚焦 on-path（与基础 NIC 集成更紧）；DPA 有 256 RISC-V 硬件线程 + DPA 可访问 cache/DRAM，适合高并行低 IPC（load/store）I/O 场景

## 3. 动机（§3）
### 3.1 RDMA 小消息速率停滞（阿喀琉斯之踵）
- 实测（CX5 100GbE / CX7 200GbE / CX8 400GbE，64B ib_write_bw）：大消息饱和带宽，小消息远低于线速；**升级网卡小消息速率停滞**（图 4a），直接限 OpenSHMEM PUT/GET 应用 IOPS（图 4b）
- **榨干速率之旅**（图 3）：单 QP 受 MMIO doorbell 限制 → 加 QP 无效（MMIO 瓶颈仍在）→ 开 batching（摊销 doorbell、改善 DMA WQE 效率）→ 多 QP 激活多 PU → 再加主机核心并发触发 MMIO
- **QLP 的代价**：多 QP 增加 WQE 提交/CQE 轮询开销；跨 QP 分发+跟踪完成 = 高度有状态操作；GPU-Direct Async 下负担落到 GPU 线程
- WLP 动机：透明保持无状态单 QP FIFO 抽象，弹性利用 NIC 并行；与 QLP 互补
### 3.2 硬件固化互连的不灵活
- **PCIe 交互固定**：MMIO doorbell/DMA WQE/CQE 通知优化刚性，host driver 与 ASIC 交互无法重编程
- **传输协议固定**：RoCEv2 为机架内+跨机架双场景设计，机架级（1 跳）下可简化但 ASIC 不支持
- **操作集固定**：verbs 固定（READ/WRITE/SEND/RECV），MPI/PGAS 的复合操作（alltoall 等）需主机 PE 实现；负载快速演化下可扩展/可编程操作集日益重要

## Q&A：WQE 并行（WLP）如何实现？（§4-5 提前解答）
核心 = E-QP 数据结构（§5.1）+ SID Ordering Model（§4.1），三层机制：
1. **排序模型**：FIFO 提交 → episode（两个 barrier/fence 之间）内允许乱序执行 → 完成严格按提交顺序暴露（OoO + in-order commit）。episode 越长 WLP 越适用（RMA Queue Buildup：内存带宽>网络带宽、细粒度 episodic 模式、集合操作三者致队列堆积）
2. **Billboard 无锁免拷贝分发**（图 7）：dispatcher 轮询 SQ head/tail（①）→ 分配请求槽写入 Billboard（version counter + completion counter + per-thread index array），递增 version 发布（②）→ 线程查 version（③）读自己槽位直接从 SQ 抓请求（④，免拷贝）→ 并行处理写 CQ（⑤）→ 各线程递增 completion counter（⑥）→ 全完成后 dispatcher 更新 CQ tail（⑦）主机才感知。SPMC + 无锁 + 免拷贝（O(N) 拷贝会瓶颈化 dispatcher）
3. **否掉的 strawman**：Partitioned SPSC（多 QP = QLP，主机有状态）vs Centralized SPMC（消费者间锁开销大）→ 理想模型 = 主机无状态单 E-QP + offloaded dispatcher
- **RX 侧两级扩展**（§5.2）：一级硬件 RSS 分发到 RX L1 线程（1:1）；incast 时 L1 作 root 用 E-QP 机制批量分发包描述符到 L2 线程池（免拷贝）；L2 处理后委托回 ACK
- **多 E-QP（WLP+QLP 联合）**：多 dispatcher 各管 E-QP，集中式 grant 机制协调共享线程池（grant 期内可处理发布大量请求，开销极小）
- **PCIe 优化**（§5.3）：批量通知（MMIO 摊销）；WQE 抓取默认 DMA、线程多（128）时改 MMIO（DMA 有 μs setup）；同批同 opcode 做 request shrinking（后续请求去 opcode）；抓取与处理流水化

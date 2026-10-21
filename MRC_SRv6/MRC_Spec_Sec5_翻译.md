# MRC Specification §5 Overview — 中英对照精译

> 源：`MRC_Specification.pdf` p.18–20（§5 Overview，含 §5.1 Description、§5.2 Goals, Visions and Objectives）
> 排版约定：`>` 引用块为**规范英文原文**（逐字保留），其下为**中文译文**。译文中的方括号 `[ ]` 为译者补充，帮助理解，不属于原文。
> 术语约定见文末「译名对照」；**译注**在每节末尾。

---

# 5. Overview 概述

> The MRC specification defines a transport for AI/ML systems that operates over standard best-effort Ethernet and existing software interfaces. MRC extends the reliable connection (RC) model with explicit multipath support, congestion control, path health tracking, and failure recovery mechanisms to maintain high goodput in the presence of congestion and link or path failures. The specification describes endpoint behavior, protocol state machines, control- and data-plane semantics, and the software APIs required to implement MRC in NICs, accelerators, and host stacks.

**译**：MRC 规范定义了一种面向 AI/ML 系统的传输协议，它运行在标准的尽力而为（best-effort）以太网与既有软件接口之上。MRC 在可靠连接（RC）模型的基础上，扩展了显式多路径支持、拥塞控制、路径健康跟踪与故障恢复机制，以便在存在拥塞以及链路故障或路径故障时维持高有效吞吐量（goodput）。本规范描述了端点行为、协议状态机、控制面与数据面语义，以及在 NIC、加速器与主机协议栈中实现 MRC 所需的软件 API。

**译注**
- **goodput（有效吞吐量）** 是全文的核心指标，注意它与 throughput（吞吐率）不同：goodput 只计**真正被有效交付的有用数据**，已剔除重传、协议开销与无效流量。MRC 的整个设计目标就是"拥塞与故障下不塌 goodput"，这与论文里 tail latency 主导性能的论断互为表里。
- 第一句就点明前提：**标准 best-effort 以太网 + 既有软件接口**。这意味着 MRC 不要求无损网络（即禁用 PFC），也不要求更换物理层——这是它相对 RDMA/RoCE 正统方案的根本取舍。
- **"explicit multipath"（显式多路径）** 的"explicit"是关键词：多路径不是靠交换机 ECMP 被动哈希得到，而是由端点显式掌握并主动选择（见 §9 EV）。

---

## 5.1. Description 描述

> MRC is a transport protocol designed to provide reliable, high-goodput connectivity for large-scale AI/ML workloads over standard best-effort Ethernet. MRC extends RC transport with explicit multipath operation, path health monitoring, and failure recovery so that endpoints can sustain effective throughput in the presence of congestion, link failures, and other fabric impairments.

**译**：MRC 是一种传输协议，旨在为标准尽力而为以太网上的大规模 AI/ML 工作负载提供可靠的、高有效吞吐量的连接。MRC 在 RC 传输之上扩展了显式多路径操作、路径健康监测与故障恢复，使端点能够在拥塞、链路故障以及其他网络（fabric）损伤的情况下维持有效吞吐。

> Within the larger system stack, MRC sits between existing protocol layers and AI/ML frameworks or runtime libraries, exposing APIs that allow NICs, accelerators, and host software to utilize multiple network paths while preserving ordered, reliable delivery semantics where required.

**译**：在更大的系统栈中，MRC 位于既有协议层与 AI/ML 框架或运行时库之间，对外暴露 API，使 NIC、加速器与主机软件能够利用多条网络路径，同时在**需要之处**保持有序、可靠的交付语义。

> MRC addresses problems such as underutilized network capacity, job failures or stalls due to transient fabric issues, and tight coupling between endpoint behavior and specific network topologies.

**译**：MRC 所解决的问题包括：网络容量利用不足、因瞬时网络问题导致的作业失败或停滞，以及端点行为与特定网络拓扑之间的紧耦合。

> In the Open Compute Project ecosystem, MRC provides an open, implementation-ready specification that enables interoperable, multi-vendor AI/ML fabrics, improves effective accelerator utilization on commodity Ethernet infrastructure, and supports scalable, fault-tolerant deployments from small clusters to hyperscale systems.

**译**：在开放计算项目（OCP）生态中，MRC 提供了一份开放的、可直接落地实现的规范，它使多厂商 AI/ML 网络能够互操作，提升加速器在商用（commodity）以太网基础设施上的有效利用率，并支持从小型集群到超大规模系统的可扩展、容错部署。

> MRC uses ECMP hashing or source-based routing for multipath load balancing. It achieves high transport efficiency through:
> - Entropy-based rotation of request packets
> - Responder-side tracking of out-of-order packets
> - Direct placement of payload into target memory
> - Distinct traffic classes for data, retransmissions, and control messages

**译**：MRC 使用 ECMP 哈希或基于源的路由来实现多路径负载均衡。它通过以下方式获得高传输效率：

- **基于熵值的请求包轮转**（Entropy-based rotation of request packets）
- **响应端乱序包跟踪**（Responder-side tracking of out-of-order packets）
- **载荷直接放置到目标内存**（Direct placement of payload into target memory）
- **为数据、重传与控制消息划分不同的流量类别**（Distinct traffic classes for data, retransmissions, and control messages）

> Supported source-routing modes:
> - Structured EV: Combines IPv6 flow label and UDP source port into a single entropy field for deterministic path selection from the sender to the spine switch
> - SRv6: Uses uSID-based addressing with optional CSID encoded Segment Routing Header

**译**：支持的源路由模式：

- **结构化 EV（Structured EV）**：把 IPv6 流标签（flow label）与 UDP 源端口合并为单一的熵字段，用于从发送方到**脊交换机（spine switch）**的确定性选路。
- **SRv6**：使用基于 uSID 的寻址，并可选使用 CSID 编码的段路由头（Segment Routing Header, SRH）。

> For congestion control, reliability, and scalability, MRC provides:
> - Independent Reliability SACKs: Separate from RDMA Transport ACKs, SACKs convey packet reception state and fabric and responder congestion signals for transport and CC algorithms
> - Dynamic PSN Window: Responder can adjust the maximum in-flight packet range at runtime
> - NSCC Congestion Control: Implements UltraEthernet sender-based algorithm with support for trimmed and untrimmed packet flows
> - Reliability Probes: Allow requestors to query responder packet reception state
> - Entropy Value Probes: Measure path health and latency across network paths
> - Port Status Mask: Communicates local port reachability to peers

**译**：为满足拥塞控制、可靠性与可扩展性，MRC 提供：

- **独立的可靠性 SACK（Independent Reliability SACKs）**：与 RDMA 传输 ACK 相互独立；SACK 既承载包接收状态，也承载网络侧与响应端侧的拥塞信号，供传输算法与拥塞控制（CC）算法使用。
- **动态 PSN 窗口（Dynamic PSN Window）**：响应端可以在运行时调整最大在途包范围。
- **NSCC 拥塞控制**：实现 UltraEthernet 的基于发送端的算法，并支持被裁剪（trimmed）与未被裁剪（untrimmed）的包流。
- **可靠性探测（Reliability Probes）**：允许请求端查询响应端的包接收状态。
- **熵值探测（Entropy Value Probes）**：测量各网络路径的健康状况与时延。
- **端口状态掩码（Port Status Mask）**：把本地端口可达性告知对端。

> MRC exposes two APIs:
> - Application API: Mirrors libibverbs semantics for creating and managing MRC queue pairs
> - Control-Plane API: Enables administrators to configure per-QP multipath policies, adjust load-balancing dynamically and query path reachability

**译**：MRC 对外暴露两个 API：

- **应用 API（Application API）**：镜像 libibverbs 的语义，用于创建和管理 MRC 队列对（QP）。
- **控制面 API（Control-Plane API）**：使管理员能够配置每个 QP 的多路径策略、动态调整负载均衡，并查询路径可达性。

> MRC connections implement the following core capabilities:
> - Multipath Transmission: Distributes request and reliability control packets (SACKs) across multiple network paths using ECMP or source routing, with ECN marking support
> - Reliability Control: Uses selective acknowledgments (SACKs) and negative acknowledgments (NACKs) to ensure timely packet delivery and convey congestion state
> - WriteIMM Limiting: Enforces a user-defined maximum number of in-flight Write-with-Immediate operations per connection
> - Congestion Control: Implements NSCC, a sender-based congestion control algorithm specified in the UltraEthernet Transport Specification [UESPEC]
> - Selective Retransmission: Allows retransmission of specific packets based on SACK/NACK feedback.

**译**：MRC 连接实现以下核心能力：

- **多路径传输（Multipath Transmission）**：使用 ECMP 或源路由，把请求包与可靠性控制包（SACK）分散到多条网络路径上，并支持 ECN 标记。
- **可靠性控制（Reliability Control）**：使用选择性确认（SACK）与否定确认（NACK）确保包及时交付，并传递拥塞状态。
- **WriteIMM 限制（WriteIMM Limiting）**：对每条连接上在途的 Write-with-Immediate 操作数量施加上限，上限由用户定义。
- **拥塞控制（Congestion Control）**：实现 NSCC——UltraEthernet 传输规范 [UESPEC] 中定义的基于发送端的拥塞控制算法。
- **选择性重传（Selective Retransmission）**：允许依据 SACK/NACK 反馈对特定包进行重传。

> Implementations MAY support the following optional features:
> - Dynamic Maximum PSN Range (MPR): Enables responders to adjust the maximum number of outstanding request packets in-flight during connection runtime
> - Trim NACK: Responders generate trim notifications when packets are truncated in the network
> - Service Time: Responders report local request service time

**译**：**实现可以选择（MAY）**支持以下可选特性：

- **动态最大 PSN 范围（Dynamic Maximum PSN Range, MPR）**：使响应端能够在连接运行期间调整在途未完成请求包的最大数量。
- **裁剪 NACK（Trim NACK）**：当包在网络中被截断（truncated）时，由响应端生成裁剪通知。
- **服务时间（Service Time）**：响应端上报本地的请求服务时间。

> Limitations of MRC Compared to RC:
> - Restricted Operations: Supports only RDMA Write and Write-with-Immediate (WriteIMM); Read, Send, and Atomic operations are not supported
> - WriteIMM Resource Bound: The number of in-flight WriteIMM operations is limited by responder-side tracking resources
> - No RNR-NAK Semantics: RDMA transport-level Receiver Not Ready (RNR-NAK) flow-control is not supported

**译**：MRC 相较于 RC 的局限：

- **操作受限（Restricted Operations）**：仅支持 RDMA Write 与 Write-with-Immediate（WriteIMM）；不支持 Read、Send 与 Atomic 操作。
- **WriteIMM 受资源约束（WriteIMM Resource Bound）**：在途 WriteIMM 操作的数量受响应端跟踪资源限制。
- **无 RNR-NAK 语义（No RNR-NAK Semantics）**：不支持 RDMA 传输层的接收端未就绪（Receiver Not Ready, RNR-NAK）流控。

**译注（§5.1）**
1. **"where required" 是有意限定。** 规范说"在需要之处保持有序、可靠交付"，而非无条件有序——因为 MRC 允许接收端乱序放置（见 §6.3.2），只要求 WR 在请求端按序完成（§6.2.1）。这个限定词值得在你的笔记里标出来。
2. **"spine switch" 需要和论文的拓扑术语对齐。** 规范在 Structured EV 模式里说选路是"从发送方到脊交换机"，而论文使用的是 T0/T1 两层多平面 Clos。二者对应关系（spine ≈ T1？）建议在读完 §9.3.5 后再回头确认。
3. **"Distinct traffic classes"** 具体映射规则在 §7.5.5.1 Class of Service Mapping (p.44)。
4. **"truncated" 与 "trimmed"** 是同一件事的两种表述（交换机裁剪载荷、保留包头转发），规范在此处用 truncated，在 Trim NACK 条目用 trim。
5. **本节唯一的规范性关键词是 `MAY`**（三个可选特性）。除它之外，§5 全部是描述性与愿景性文字，**不构成强制要求**——真正的 MUST 集中在 §6–§9。所以：§5 用来建立全局图景，不能作为一致性要求的引用来源。
6. **三条 Limitations 值得单独记入笔记**，因为它们界定了 MRC 的适用边界。其中 **"No RNR-NAK"** 在论文里并未强调，但它很关键：RC 里接收端缓冲区不足会回 RNR-NAK 让发送端重试，MRC 取消了这个机制，转而依赖 WriteIMM 限制 + 响应端流控（§7.5.1）。

---

## 5.2. Goals, Visions and Objectives 目标、愿景与目的

> The long-term vision of MRC is to provide an open, transport-level mechanism, inclusive of application and management APIs, that enables large-scale AI/ML systems to achieve high goodput, resilience to fabric impairments, and efficient accelerator utilization over standard best-effort Ethernet. MRC is intended to serve as a common foundation for interoperable, multi-vendor AI/ML fabrics within the Open Compute Project ecosystem, reducing dependence on proprietary transports and specialized networks.

**译**：MRC 的长期愿景是提供一种开放的、传输层机制（并包含应用与管理 API），使大规模 AI/ML 系统能够在标准尽力而为以太网上实现高有效吞吐、对网络损伤的韧性以及高效的加速器利用率。MRC 旨在成为 OCP 生态内可互操作、多厂商 AI/ML 网络的共同基础，降低对专有传输协议与专用网络的依赖。

> The primary goals are:
> - Reliable multipath operation over Ethernet: Provide a transport that supports multipath communication, maintains reliable delivery semantics where required, and continues to make progress in the presence of congestion, intermittent faults, and link or path failures
> - High effective utilization of existing infrastructure: Increase usable network capacity and accelerator utilization without requiring changes to underlying physical layers or wholesale replacement of deployed Ethernet fabrics
> - Interoperability and openness: Enable consistent endpoint behavior, control-plane integration, and observability across NICs, accelerators, and switches from different vendors, using a publicly available, implementation-ready specification
> - Operational scalability: Support deployments ranging from small clusters to hyperscale fabrics with minimal operator intervention through well-defined control-plane APIs and integration hooks for monitoring, orchestration, and automated remediation

**译**：首要目标为：

- **以太网上的可靠多路径运行**：提供一种支持多路径通信、在需要之处维持可靠交付语义、并且在拥塞、间歇性故障以及链路或路径故障下仍能持续取得进展（make progress）的传输协议。
- **既有基础设施的高效利用**：在不改变底层物理层、也不整体更换已部署以太网网络的前提下，提升可用网络容量与加速器利用率。
- **互操作性与开放性**：借助一份公开可用、可直接实现的规范，实现不同厂商的 NIC、加速器与交换机之间一致的端点行为、控制面集成与可观测性。
- **运维可扩展性**：通过定义良好的控制面 API，以及面向监控、编排与自动化修复的集成钩子，支持从小型集群到超大规模网络的部署，且仅需最少的运维人员干预。

> Measurable objectives guiding the design and evolution of MRC include:
> - Improving realized goodput and network utilization for representative AI/ML workloads compared to single-path reliable transports operating over the same Ethernet fabric
> - Reducing job failures, stalls, or restarts attributable to transient or localized fabric impairments
> - Demonstrating interoperable implementations across multiple independent vendors and system configurations
> - Enabling incremental, non-disruptive deployment of MRC endpoints into existing Ethernet-based environments

**译**：指导 MRC 设计与演进的可度量目标包括：

- 在与单路径可靠传输相同的以太网网络条件下，为有代表性的 AI/ML 工作负载提升**实际达成的有效吞吐量与网络利用率**。
- 减少因瞬时或局部网络损伤而导致的作业失败、停滞或重启。
- 在多个独立厂商与多种系统配置上验证实现的互操作性。
- 使 MRC 端点能够**渐进式、非中断地**部署进既有以太网环境。

**译注（§5.2）**
1. §5.2 通篇是**设计目标陈述，没有任何规范性关键词**（无 MUST/SHOULD/MAY），纯属意图声明。在规范里它的作用是解释 §6–§9 各机制"为什么长这样"，不能引用为要求。
2. **"without wholesale replacement"（不整体更换）** 与 **"incremental, non-disruptive deployment"（渐进、非中断部署）** 是 MRC 相对 UET/专有方案的核心卖点，也是论文里"多平面拓扑用商用交换机"论述的规范侧表述。
3. **"continue to make progress"** 对应论文的核心韧性主张：故障期间吞吐可以下降，但**任务不能中断**（论文里 50K GPU 任务扛过 transceiver flap、吞吐波动 25% 即此意）。
4. 注意目标里用的是 **"realized goodput"（实际达成的有效吞吐）**，而非理论带宽——评价基线明确是"同一以太网网络上的单路径可靠传输"，即 RoCEv2 单路径 ECMP。

---

## 译名对照

| 英文 | 本译文采用 | 说明 |
|---|---|---|
| goodput | 有效吞吐量 | 区别于 throughput（吞吐率） |
| best-effort | 尽力而为 | 对应有损、无 PFC 的网络 |
| fabric | 网络 / 组网 | **不译作"光纤"**；指整个交换网络 |
| fabric impairment | 网络损伤 | 含丢包、抖动、链路抖动、交换机异常 |
| requestor / responder | 请求端 / 响应端 | 不用"发起方/响应方"以保持术语唯一 |
| endpoint | 端点 | NIC / 加速器侧 |
| spray / rotation | 喷洒 / 轮转 | "rotation"此处即逐包轮转绕行 |
| entropy / EV | 熵 / 熵值 | EV = Entropy Value |
| Structured EV | 结构化 EV | §9.1 定义其位结构 |
| spine switch | 脊交换机 | 与论文 T1 的对应关系待核对 |
| source-based routing | 基于源的路由（源路由） | |
| trim / truncated | 裁剪 / 截断 | 交换机丢弃载荷、仅转发包头 |
| in-flight / outstanding | 在途 / 未完成 | |
| SACK / NACK | 选择性确认 / 否定确认 | 缩写保留 |
| NSCC | （网络信号拥塞控制） | 译名保留缩写 NSCC，不硬译 |
| WriteIMM | WriteIMM | Write-with-Immediate |
| reachability | 可达性 | |
| orchestrator / orchestration | 编排 | |
| remediation | 修复 | automated remediation = 自动化修复 |
| observability | 可观测性 | |
| RNR-NAK | 接收端未就绪 | Receiver Not Ready |
| commodity | 商用 / 通用 | commodity Ethernet = 商用以太网 |

---

## 与论文 / 你的疑问的对应关系

| §5 提到的能力 | 规范展开处 | 你的 `疑问.md` 关联 |
|---|---|---|
| Entropy-based rotation of request packets | §9.4 EV Generation (p.67) | 疑问 3、3.1 |
| Structured EV / SRv6 两种源路由模式 | §9.3.4 / §9.3.5 (p.64–67) | **疑问 3** |
| Independent Reliability SACKs | §7.2 (p.30)、§7.5.2 (p.38–41) | **疑问 4** |
| Dynamic PSN Window / MPR | §7.5.4 (p.43) | — |
| NSCC Congestion Control | **§8 全章 (p.54–59)** | **疑问 3.2** |
| Reliability Probes / EV Probes | §7.4.6 / §7.4.7 (p.35) | **疑问 2、3.1** |
| Port Status Mask | §7.4.8 (p.36) | 论文 §3 运维实践 |
| Selective Retransmission | §7.4.4 (p.32–34) | **疑问 2、4** |
| Trim NACK | §7.5.3 (p.41–43) | **疑问 4** |
| Distinct traffic classes | §7.5.5.1 (p.44) | — |
| 三条 Limitations | §6.2.2 支持的操作 (p.21)、§7.5.1 流控 (p.37) | 论文"不足"一节 |

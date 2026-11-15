# MetaRoCE 分析笔记（博客 + 规范 v1.0）

> 分析对象: Meta 2026-08-24 工程博客《MetaRoCE: A New RDMA Transport Built for AI-Scale Ethernet》
> + 《Meta-RoCE Protocol for AI Accelerators》v1.0（2026-10-12，随 OCP 提交，GitHub facebookincubator/metaroce）
> 笔记日期: 2026-11-12　｜　所有判断按【原文】/【推论】标注，数字出处标到章节号或图号

本地文件（都在 `D:/Academics/MetaRoCE/`）：

```
MetaRoCE/
├── MetaRoCE-Spec-1.0.pdf              ← 规范原文（1.0 MB，10 章，6095 行 markdown 等价）
├── blog-01-Meta-Engineering-2026-08-24.md   ← Meta 博客英文全文（11 KB）
├── blog-02-AMD-2026-08-25.md                ← AMD 博客英文全文（合作方视角，待用户确认是否为"第二篇"）
├── running_notes.md                   ← 本文件
├── 疑问.md
└── .pages/                            ← 中间产物（Obsidian 不索引）
    ├── MetaRoCE-Spec-1.0.md           ← 规范 markdown 源（便于 grep，PDF 的母本）
    ├── blog_raw.html                  ← 博客原始 HTML
    ├── img/                           ← 博客 3 张插图（含唯一性能图 Figure-1）
    └── repo/                          ← 完整仓库快照（spec + libsoftmetaroce + rdma_gen + wireshark dissector，11 MB）
```

---

## 一页版总结

### 基本信息
- **性质**: 工业博客 + 协议规范 + 开源参考实现，**不是会议论文**，无同行评审、无摘要/致谢/Shepherd。
- **作者**: Arvind Srinivasan、Neil Spring、Omar Baldonado、Rajiv Krishnamurthy（Meta 网络组）；规范为 Meta + OCP ESUN 名义发布。
- **版本**: Spec 1.0（October 12, 2026），Apache-2.0；2026-08-24 博客承诺"10 月 OCP Global Summit 放出规范 + DPDK 软件实现 + 合规框架"。
- **硬件**: AMD Pensando Pollara 400（研发验证）→ Vulcano 800（800G 生产）【AMD 博客】；Meta 侧万卡级部署口径未公开数据。

### 一句话标题
MetaRoCE：Meta 用一个无 PFC 的乱序 RDMA 传输，把可靠性/多路径/拥塞控制全搬到网卡，在商品以太网上支撑百万级 GPU。

### 主要观点（3 行）
- 背景：PFC 在十万卡规模上制造 pause storm、headroom 吃光 buffer；RoCEv2 单流 + 按序交付使 ECMP 哈希冲突和多平面喷洒都用不起来，而 QP scaling 换来的是 O(N) 网卡状态。
- 方案：一条 QP 里塞多个 Tag（独立 MSN/CSN 空间）+ 多条 Flow（独立 FSN/窗口/RTT），包走到哪个 flow 由网卡按 entropy 决定；数据乱序落地、完成按 Tag 有序，配 per-flow SACK 精确重传与接收端 TargetRate 限速。
- 定位：不要求交换机做任何新功能（只吃 ECN + ECMP），换来拓扑无关性；规范开源 + 合规套件，赌的是"以太网传输层标准化"的话语权。

### 四要素
1. **研究背景**: AI 集群规模跨机架/跨楼/跨地域，集合通信的最慢传输决定整任务时长。
2. **要解决的问题**: 如何在不依赖无损网络的前提下，同时拿到高吞吐、低尾延迟、与并行度无关的网卡状态。
3. **现有方案不足**: PFC 随速率扩张的 headroom、按 TC 而非按流的阻塞、单流 ECMP 哈希冲突、QP scaling 的状态与 CC 碎片化。
4. **本文解决思路**: 分层序列号（MSN/POSN/CSN/FSN）把"乱序到达"与"有序完成"解耦，多流多 Tag 把并行度从连接里剥出来。

### AS-IS（现状与问题，来自 §1.1）
- PFC 三个失效模式（§1.1）：① headroom 随链路速率与距离线性增长，吃掉本可用于吸收突发的 buffer；② 单拥塞端口把 pause 帧往上推，形成 pause storm 停掉无关流量；③ PFC 作用于 TC 而非流，一个慢接收端能堵住整个 class 的所有发送方。
- 单流连接：ECMP 按 5 元组哈希到固定路径，多连接撞同一链路时并行链路闲置；要打散必须"交换机喷洒（需交换机 reorder buffer）"或"端点多流"，而传统 RDMA 都不给（§1.1）。
- QP scaling 的代价：连接状态随 QP 线性占用网卡内存（加速器旁挂网卡受功耗/面积限制）；CC 被切碎成几十个互不知情的小窗口；集合库还要自己做流量切分（§1.1）。

### TO-BE（方案与效果）
- **四层序列号**（§2.1）：MSN（QP+Tag 内消息号，可回绕）、POSN（消息内包偏移，16 bit，不回绕→消息上限 256 MB）、CSN（QP+Tag 内消耗 RWQE 的消息号，可回绕）、FSN（flow 内包号，16 bit，可回绕）。RoCE 的 PSN 与 first/middle/last 都不存在（§2.1 末）。
- **乱序落地 + 有序完成**（§3）：写包自带地址/长度/rkey，Send 靠 CSN 匹配已 post 的 RWQE，数据到哪写哪，网卡无需 reorder buffer；completion 在 ordered 模式按 WQ 顺序 post，unordered 模式按到达顺序。
- **可靠性**（§4）：per-flow RTO（RFC6298 改造）+ 256 bit 选择性 ACK 位图 + MaxFSN + snd.cur 重传游标；六条 ACK 丢弃条件；RNR 三级（B-RNR / H-RNR / RNR-Cancel）。
- **拥塞控制**（§6）：QWND（QP 级，带分数部分做 AIMD）/ FWND（流级）层次化窗口；baseline AIMD（ε=1, β=1/2, λ=1）+ Fast Start + 接收端 TargetRate（RCN）→ `QWND_max = max(QWND_min, γ·TargetRate·(RWeightedRTT+ω))`。
- **多路径**（§7）：Flow ID 固定、entropy（默认 UDP 源端口 49152–65535 计数器）可变；超时重传换熵换路径；多端口/多平面（≤16 plane）带端口失败与放空（draining）。

---

## 1. 博客精炼

### 1.1 六个机制（博客正文章节顺序）
| 机制 | 博客说法 | 规范对应 |
|---|---|---|
| Native Out-of-Order Delivery | 每包自带目的地，落地即写内存；无 reorder buffer、无 HOL；Send 也无需在途往返匹配 | §2.3 / §3 / §8.3 |
| Native Multipathing | 每连接多条一等公民 path，逐包喷洒；每 path 独立窗口与 RTT → 能区分"拥塞"与"故障"，坏链路只拖慢一条 path | §7.1–7.4 / §6.1 |
| Loss Tolerance by Design | 不要 PFC/暂停帧；每 path 独立有序序列 → 256 bit SACK 的"洞"就是丢包证据，洞一出现就按 path 精确重传"缺的那一个包" | §4.2.3 / §4.6 |
| Congestion Control From Both Sides | 发送端 ECN+AIMD，接收端在**每个 ACK 里**回自己给它分配的入向带宽份额 → incast 一到两轮 RTT 收敛 | §6.3 |
| Topology Independence | 只要交换机已有 ECN + ECMP；不要求 packet trimming / INT / credit / 交换机喷洒，也不因对端提供而失效 | §1.2 |
| Unified Connections at Scale | 一条 QP 承载多条有序流（每 communicator/collective 一条 Tag）+ 多条 path（一个拥塞控制器）；连接状态不再随并行度增长；verbs API 不变 | §1.3 / §10 |

### 1.2 博客里的实测口径（唯一性能证据）
- 平台：**64 节点 AMD GPU 集群 + RCCL**，MetaRoCE vs **RoCEv2**，all-reduce / all-to-all。
- 丢包：1% 丢包下维持 **~86%** 吞吐；10% 丢包下仍可用，"优雅收敛而非崩塌"。
- 多平面：4-plane 与 8-plane，最多 **4000 并发连接**，吞吐随 plane 数线性。
- 故障：模拟 plane 失败，流量自主重分布，无应用/运维介入。
- 注意：这些是博客断言，仓库里没有任何 trace/脚本能复现；图只有一张 delta% 柱状图（见 §6 数字核对）。

### 1.3 开放与路线
- 开放三件套：OCP 规范 + 多厂商 NIC 实现（已证 AMD，其他在途）+ 生产合规套件 + `libsoftmetaroce` 软件参考实现（Linux 上跑标准 UDP socket，作为"权威行为模型"）。
- Road ahead 自认未完成：**scale-up**（机架内 P2P 小消息，正在优化短内存操作的快速信令路径）、**scale-across**（跨数据中心、毫秒级 RTT、按 path 逐级公平）、**存储/KV-cache**（incast 与变速率网络下的 TargetRate 精度）。

---

## 2. 规范结构地图（10 章）

| 章 | 内容 | 值得注意的点 |
|---|---|---|
| §1 Introduction | 动机、fabric 需求、设计总览、支持操作 | 明确列出"不需要"的交换机能力：PFC、交换机喷洒、packet trimming、INT、链路 credit（§1.2） |
| §2 Sequence Numbers | MSN / POSN / CSN / FSN | 明确"没有 QP 级 PSN、没有 first/middle/last"；POSN 16 bit + 4096B MTU → 消息上限 2^28 B = 256 MB（§2.3） |
| §3 Ordering | 术语、支持的消息序列、有序/无序完成、CSN 实现语义、SRQ | ordered 模式下 atomic 只有"前序全部完成"后才执行（§3.3.1 表）；明确"轮询写尾地址永不合法"（§3.3.1） |
| §4 Reliable Delivery | mCRC、ACK 生成/内容、packet tracker、RTO、SACK 判丢、tail/alt-flow 重传、UNA、RNR | 规范最"硬"的一章：六条 ACK 丢弃条件 + MaxAckAge 与 FSN 回绕的别名分析（§4.2.3） |
| §5 Error Handling | 可重试错误、message-fatal、requester/responder 侧 | 目标写成"实现简单优先于理论可恢复"（§5 开头） |
| §6 Congestion Control | baseline AIMD、可编程 CC 的输入/输出、RCN 限速 | QWND 带分数部分把"每 RTT 加 ε 包"摊到每 ACK（§6.1.1）；RCN 与 ECN 同时生效时的优先规则（§6.3.4） |
| §7 Multipath & Flow Selection | entropy 选择、发送调度、流数与生命周期、多端口/多平面 | entropy 用设备级计数器而非随机数（§7.1）；ACK 源端口镜像数据源端口（§7.1.1） |
| §8 Packet Headers | base/METH/RETH/ImmDt/ACK/RNR-Cancel/Control/Atomic | base 12 B + METH 20 B = **32 B** 协议头 + 4 B mCRC；UDP 目的端口默认 **2766**（§4.1） |
| §9 Conformance Tables | MUST/Should/may 全表 + 报文合法性规则 | 约 400 条可勾选条目 + 大量计数器要求，是合规套件的规格来源 |
| §10 Verbs Integration | QP 类型、profile、初始 MSN/CSN、RTO/retry_cnt、MTU、Tag、多端口 | `qp_type = IBV_QPT_DRIVER (0xFF)`；初始 CSN/MSN 塞进 `sq_psn/rq_psn`（高 16 位 CSN，低 16 位 MSN） |

---

## 3. 关键机制详解

### 3.1 四层序列号（§2）
| 序列号 | 作用域 | 递增单位 | 回绕 | 作用 |
|---|---|---|---|---|
| MSN | QP+Tag | 消息（含 read/atomic 响应沿用请求 MSN） | 可 | 消息唯一标识 + 完成顺序 |
| POSN | 消息内 | 包（4 KB 步长） | **不可** | 直接当内存写偏移 —— 所以数据能乱序落地 |
| CSN | QP+Tag | 消耗 RWQE 的消息 | 可 | 把 Send/Write-imm 绑到"第几个已 post 的接收 buffer" |
| FSN | Flow | 包 | 可 | 被 ACK/重传的粒度 |

要点：`(Flow,FSN)` 在回绕前唯一确定 `(Tag,Opcode,MSN,POSN)`，且同一份数据同一时刻只能挂在一个 `(Flow,FSN)` 下（§2.5）——这就是"每 FSN 恰好交付一次"能替代消息级去重的原因；RNR 后同一数据换新 FSN，旧 FSN 不再分配。

### 3.2 乱序落地、有序完成（§3）
- **ordered 模式**：Send / Write-imm / Read-imm 的完成必须等"所有前序消息完成"；纯 Write / Read / atomic 生成 virtual completion（不进 CQ）但仍参与排序判断（§3.1 术语表、§3.3.1 表）。atomic 的执行本身就是交付，所以"持锁"语义仍成立。
- **unordered 模式**：按到达顺序完成，需要顺序时用 execution fence / completion fence bit（§3.3.2–3.3.3）。
- **明确不保证**：并发写同一地址、并发读写同一地址、atomic-before-access 的顺序（§3.2.5）——这是"没有 reorder buffer"的必然代价，规范把它写成"用户不应依赖"而不是缺陷。
- **SRQ**：CSN 仍把消息的每个包绑到同一个 buffer，但 buffer 取用按消息到达顺序；规范给出两种防死锁实现（限制越过 next-expected CSN 的准入 / 私下预留被跳过 CSN 的 RWQE）（§3.4.1）。

### 3.3 可靠性：判丢、重传与 ACK 防腐（§4）
- **RTO**：RFC6298 结构 + 三个改造：`RTO = clamp(RTT + 4·mdev + ρ, lower, upper, ≥RTT_meas)`；Karn 不需要（全用回显时间戳测 RTT）；ACK 到达只在"会更早到期"时重置定时器；每 flow 一个定时器、每发一个包就重置（§4.5.2）。ρ 用来补"DMA 取包体到打时间戳"这段落差 —— 这种细节只有做出过芯片的人才会写进规范。
- **SACK**：256 bit 位图 + `CumulativeFSN` + `MaxFSN`；MaxFSN 可以超出位图窗口，用于窗口 >256 的恢复期（§4.2.3）。发送端维护 `snd.cur` 游标：同一缺口收到重复 SACK 不会重复重传（§4.6, Fig 4.8/4.9）。部分 RTO 突发后 `snd.cur` 停在突发端点，后续由 ACK 驱动继续（§4.6, Fig 4.10）。
- **ACK 丢弃六条件**（§4.2.3）：MaxFSN < snd.una（陈旧，正常可发生）、CumulativeFSN ≥ snd.nxt、MaxFSN ≥ snd.nxt、CDMSN 越过本端 Next Tx MSN、MaxFSN < CumulativeFSN、以及 `RTT_meas > min(2·MaxRTO, MaxAckAge·(RTT+mdev))`。最后一条是为 16 bit FSN 的回绕别名（aliasing）设计的：被网络扣住太久的 ACK 可能携带"回绕前"的 FSN，误用会把没送达的包退休掉；规范还给出 `MaxAckAge < 32768/FWND_max` 的取值约束（默认 64，256 包窗口下上限 128）。这一段是全篇最见功力的地方【推论】。
- **换路径重传**（§4.8）：RTO 后可以立刻换 entropy（同 Flow ID、同 FSN），后续 RTO 还可以换输出端口 —— 对应 blog 说的"能区分拥塞与故障"。
- **UNA 字段**（§4.9）：数据包里带 snd.una，接收端据此释放 per-FSN 状态；规范特意警告"把 UNA 当接收上限会丢弃好数据"，因为多路径下 UNA 落后是常态而不是异常。

### 3.4 协议头与封装（§4.1, §8）
- 封装矩阵（Fig 4.1）：IPv6/UDP（MUST）、IPv4/UDP（Should）、PSP（Should，不重复带 mCRC）、纯以太网（may，用 FCS）、ESUN（may，必须带 mCRC，因为帧内 CRC 逐跳更新）。
- mCRC = CRC-32，与以太网 CRC 同多项式、同预/后取反，覆盖从 Meta-RoCE 头到数据尾；**不含** IP/UDP 头（比 RoCEv2 的 iCRC 范围小，§4.1）。
- UDP 目的端口 **2766**（不是 RoCEv2 的 4791），说明它把自己当成"新传输"而非 RoCE 扩展；opcode 高 3 bit 用 `110`（IB 保留给厂商的编码）以便与 RoCEv2 在同一网卡上共存（§8.1.1）。
- METH 里塞了两个 RoCE 没有的字段：**Rate Hints**（发送端申报期望速率，供接收端算 fair share）与 **Transmit Timestamp**（回显测 RTT，纳秒粒度、32 bit≈4 s）（§8.2）。

### 3.5 拥塞控制（§6）
- 层次：`QWND = Σ FWND[f]` 恒成立；QWND 带整数+分数部分，每 ACK 分数 +ε/QWND，攒满一整包才让某条 flow "认领"一次 FWND 增长；被 ECN 标记则分数 −β·QWND（§6.1.1–6.1.2）。默认 ε=1, β=1/2, λ=1，可配范围见 Table 6.1。
- 增量分配有两个巧思：① 拥塞的 flow 会错过跨过整数边界的那一刻，于是窗口概率性地从热点流挪走；② 允许 flow 在"自己 RTT 高于平滑 RTT"时放弃认领（必须实现，可关）（§6.1.2 第 3 条）—— 这是个很便宜的负载均衡偏置。
- **Fast Start**（§6.1.3）：空闲 QP 有新消息时 QWND/FWND 归零、按发送而非按 ACK 增长，直到收到 ACK / 收到 CNP / QWND 达上限 / 一个 RTT 到期。给出三种逐包到 flow 的调度图案（burst=4 轮询、多端口轮询、交错"lazy caterer"式），本质是"消息小就自动少用几条流"。
- **RCN**（§6.3）：接收端每个 ACK 都带 `TargetRate = ceil(链路速率/估计并发发送者) + offset`，发送端换算成 `QWND_max = max(QWND_min, γ·TargetRate·(RWeightedRTT+ω))`；超过上限后按三区间递减（>2× 每 ACK 减 1 包、在 1×–2× 之间每 ACK 减半包、否则不减速），并用 `fwnd_floor` 保护低编号流不被削到 0（§6.3.3）。RCN 生效期间**忽略 ECN 减速**，避免双重惩罚（§6.3.4）。
- 可编程 CC（§6.2）：只开放"改 ε/β/λ/γ/ω、直接改 QWND/FWND、读 20+ 个信号（QWND、AWND、MINRTT、SRTT、CE 计数、重传计数…）+ 16 B per-QP scratch + 64 个设备级计数器"。规范明确"**不应**按流跑独立 CC 协议"（§6.2.1）—— 层次化窗口是硬约束。

### 3.6 多路径（§7）
- **Tag 与 Flow 正交**：Tag 管"消息流/完成顺序"，Flow 管"网络路径/可靠性窗口"；一个 Tag 的包撒在多个 Flow 上（§3.1）。
- **entropy**：默认 UDP 源端口；设备级 14 bit 计数器映射到 49152–65535，创建/换流时 +1，明确"不要用随机数"（§7.1）。
- **ACK 反向熵**：ACK 源端口复制数据包源端口，让回程路径跟着换（§7.1.1）。
- **多端口/多平面**：区分 multi-port（每个 flow 可用不同目的地址）与 multi-plane（每平面一对一，地址可相同），本版最多 16 个可寻址端口/平面（§7.5）；要求支持放空 plane、多交换机/端口同时故障对 QP 不可见、失败后不得"确定性跳到失败端口+1"（§7.5.4）。
- **流数**：控制面给 QP 分配最大流数，收发可不同；溢出时对方回 Flow ID Unsupported NAK（§7.3, §5.2.1）；流数永不为 0，flow 0 恒在。

### 3.7 RNR 三级（§4.10）
- 接收端状态三分：not-seen / delivered / rnr；RNR 的 FSN 进 RNR 位图，`CumulativeFSN` **冻结**在第一个 RNR 之前，窗口被"锁住"直到发送端用 UNA 声明放弃这些 FSN。
- 发送端动作：定位受影响 `{Tag, MSN}` → 停该 Tag 的新流量 → 起 BRNR 退避定时器（线性或指数）→ 用 UNA 推进 → 接收端释放 per-FSN 状态并推进 CumulativeFSN。
- **RNR-Cancel**（§4.10.1）：接收端就绪时主动告知（BRNR 按 Tag 各发一个；HRNR 只发一个且 Tag=0），使默认退避可以设得很长而不牺牲恢复速度；不重传、不确认，丢了就靠探测。

### 3.8 合规与实现（§9, §10 + 仓库）
- §9.1 用 MUST/Should/may 三档穷举 **469 条**要求（258 MUST / 121 Should / 90 may），含"必须能配 FWND_max=64/128/256"、"必须支持 4096 B MTU"、"必须实现 execution fence"等；§9.2 另给 **97 条**"发射端应满足的报文规则"，明确它是抓包可检验的规格，而**不是**接收端丢弃依据（保留字段非零不得丢包）（§9.2 开头）。
- verbs 集成刻意最小侵入：`IBV_QPT_DRIVER`、复用 `path_mtu`（扩到 8192）、复用 `timeout/retry_cnt`（明确乘积当"时长"读，不是重传次数）、Tag 用 `qp_num` 的**高 8 bit** 承载（低 24 bit 仍放 QPN，`ibv_create_qp_ex()` 以原 QPN 为父创建子 QP；CC/MTU/PD/RTO 由 QP 共享，队列与初始 MSN/CSN 按 Tag 独立）（§10.6）。
- 仓库另有 `libsoftmetaroce`（用户态软件传输 + verbs provider）、`rdma_gen`（流量生成器/驱动示例）、`wireshark` Lua 解析器 —— 约 11 万行（含 build 脚手架），软件实现的存在是"可复现性"这一项比绝大多数工业白皮书强的地方。

---

## 4. 与相邻方案的定位（推论，需按各自规范核实细节）

- **vs RoCEv2 + DCQCN**：DCQCN 也是 ECN 驱动的 AIMD，但前提是"无损 fabric + 按序到达 + 单流"；MetaRoCE 把这三条全拆了：去 PFC、接受乱序、单连接多流。真正的差异不在 CC 公式，而在**状态布局**（per-flow 16 bit FSN + 256 bit SACK + 分数窗口）与**完成语义**（Tag 级有序）。
- **vs Ultra Ethernet (UEC)**：UEC 1.0 同样采用逐包喷洒 + 柔性排序 + 端点拥塞控制，方向一致；Meta 这篇只挂 OCP/ESUN 而**未提 UEC 兼容**，说明 2026 年传输层标准仍在分叉【推论，需查 UEC 1.1/OCP 公告】。
- **vs MRC（Multipath Reliable Connection）**：同属 Meta/OCP 生态，MRC 的着力点是多平面寻址与 EV/SRv6 承载，MetaRoCE 是端点传输本体；两者是否组合部署、谁承载谁的包，博客与规范都未交代 —— 这是最值得追的一条线（见 疑问.md）。

---

## 5. 深度分析（我的判断，非原文）

1. **贡献在机制层是"序列号分层 + 状态可算"**：把"乱序到达/有序完成/每流精确重传/与并行度无关的连接状态"四个目标，用 MSN/POSN/CSN/FSN 四个计数器 + Tag/Flow 正交解耦实现（§2.1, §3, §7）。真正难的部分不是想法，而是 §4.2.3 那类 ACK 防腐与 `MaxAckAge < 32768/FWND_max` 的边界推导——它决定了 16 bit FSN 在 800G×长肥管道下不会别名失控。
2. **最该打折扣的是性能证据**：全部实测只有 64 节点 AMD 集群 vs RoCEv2（blog §"in practice"），无基线调优说明、无大规模生产数据、无独立复现；且唯一性能图本身存在多处回退（见下节）。"1% 丢包保 86% 吞吐"这类数字在规范的 400 条 MUST 之外，没有任何可核对载体。
3. **最该追问的失效点是"同一 flow 内网络不得重排"这一隐含契约**：SACK 判丢依赖 per-flow 有序（§4.6.1 明说），而规范同时要求实现支持"网络逐包喷洒"下的两种降级模式（关掉 SACK 判丢 / 只对 MaxFSN 减去若干窗口的部分重传）。也就是说，一旦 fabric 开了交换机喷洒，MetaRoCE 会退回接近 timeout 驱动的恢复，其性能代价规范**没有给**量化，而这恰好是下一代 fabric（UEC 风格）的默认行为。

## 6. 数字口径问题（博客断言 vs 图中读数）

博客原文："MetaRoCE consistently delivers higher throughput and lower flow completion times than RoCEv2. / maintains ~86% throughput at 1% packet loss"。
但唯一性能图（`MetaRoCE-Figure-1.png`，双面板柱状图，纵轴 = Completion Time Delta % vs baseline，负值=更快，无数据标签、无图例）【读图估计，误差约 ±1–2 pp】：

| 面板 | 表现 |
|---|---|
| All Reduce（64 GPU） | 全部为负（更快），8B–16GiB 区间约 −3% ~ −29%，峰值在 64–128 KiB（≈ −29%），大消息端 2/4/8/16 GiB 只有 −3% ~ −7% |
| All To All（64 GPU） | **混合**：128B–512 KiB 多为 −12% ~ −20%，但 **0B ≈ +20%**、**1 MiB ≈ +17%**、**32 MiB ≈ +11%**、8–16 GiB 转正（+5.5% / +7.5%）；512 MiB–2 GiB ≈ 0 |

即：至少 4 个消息尺寸比 RoCEv2 baseline **更慢**，"consistently higher" 与图不符；而图中"baseline"未标注是 RoCEv2 的什么配置（DCQCN 参数、PFC 开关、ECN 门限均未给），因此无法判断这些回退是协议本身还是配置/实现所致。建议向作者核对的点已记入 `疑问.md`。

## 7. 后续可做

- 用 `.pages/repo/libsoftmetaroce` 在 Linux 上跑 `rdma_gen` + `wireshark` dissector，做一次"规范条款 ↔ 实际报文"的交叉验证（本机为 Windows，需 WSL 或另一台 Linux）。
- 若写论文/组会材料：可对比 MRC（已有的 `D:/Academics/MRC_SRv6`）与 veRoCE，做"端点传输 vs 承载/寻址"的分层对照。
- 需要中文逐章译文时再说：规范 10 章可按 skill 约定写到 `.pages/MetaRoCE-Spec-1.0/译文_中英对照.md`，不塞进本文件。

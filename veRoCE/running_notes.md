# ByteDance veRoCE Transport Protocol — 分析笔记
## 0 文档概述
### 基本信息
- **标题**: ByteDance veRoCE Transport Protocol
- **类型**: 技术规范文档 (Specification)，非学术会议论文
- **版本**: v2.0.4
- **日期**: December 18, 2025
- **组织**: ByteDance Ltd.
- **联系人**: Huichen Dai (daihuichen@bytedance.com)
- **许可**: CC BY-NC-ND 4.0
- **页数**: 44页
### 一句话标题
ByteDance提出veRoCE协议在RoCEv2基础上引入多路径+选择性重传以消除RDMA对无损网络的依赖
### 主要观点
- AI时代RDMA受限于无损网络要求，丢包和乱序成为大规模AI集群（百万级GPU）的必然挑战
- veRoCE向后兼容RoCEv2，通过SACK乱序确认+快速选择性重传+独立PSN空间消除对无损网络的依赖
- 引入灵活拥塞控制框架(FCC)、RTT探测、慢路径检测和Packet Trimming，支持连接级/路径级控制
## 0. 文档概述（中文摘要，~300字）
veRoCE是ByteDance发布的RDMA传输协议规范（v2.0.4, 2025年12月），旨在解决AI/ML大规模集群中RoCEv2对无损网络的强依赖问题。当AI集群扩展到数十万乃至百万GPU时，多路径传输下的丢包和乱序不可避免，而传统IB/RoCE协议对此束手无策。
veRoCE在RoCEv2基础上引入四项核心扩展：(1) 多路径传输，通过修改报文熵值利用ECMP或交换机报文喷洒实现；(2) 原生支持乱序数据交付（Direct Data Placement），Send/Recv操作也支持DDP；(3) 选择性确认机制（SACK），使发送端快速检测丢包并触发硬件友好的选择性重传；(4) 将Read Response的PSN空间独立于Send Queue，统一了Send/Write和Read的丢包检测与重传机制。
此外，veRoCE提供灵活拥塞控制框架（FCC），支持路径级/连接级、窗口/速率模式；速率模式下拥塞信号与ACK解耦，不影响ACK合并。提供了Base(P0)到P3四个Feature Profile以满足不同场景的硬件复杂度需求。通信接口使用libibverbs，通过独立配置API扩展，无需修改现有应用。
---
## 第1章 Overview
### 翻译摘要
在AI时代，RDMA广泛用于GPU/AI加速器间的高速低延迟数据传输。InfiniBand RDMA和RoCEv2均要求无损网络，难以处理丢包和乱序。随着AI网络将扩展到数十万乃至百万GPU，丢包和乱序成为不可避免的"事实"。
veRoCE保持与RoCEv2的向后兼容性，同时引入关键扩展来增强RDMA对丢包和乱序的适应能力，从而消除RDMA对无损网络的依赖。具体特性包括：
- **多路径传输**：源端点修改报文熵值（依赖ECMP）或交换机侧报文喷洒
- **乱序交付**：数据报文携带扩展头支持DDP（含Send/Recv）
- **SACK**：选择性确认通知发送方乱序到达，快速检测丢包
- **快速选择性重传**：高效恢复丢失报文，最小化不必要重传
- **独立PSN空间**：Read Response单独PSN空间，统一丢包检测和重传
- **FCC框架**：支持自定义拥塞控制算法，路径级/连接级，窗口/速率模式
- **解耦拥塞信号**：速率控制下拥塞信号独立于ACK，不中断ACK合并
- libibverbs原生支持，可在此基础上构建高层API
### 精炼笔记
veRoCE的核心目标：让RDMA在有损网络（丢包+乱序）下正常工作。关键洞察是——与其依赖昂贵的无损网络基础设施，不如让传输协议本身具备容错能力。All existing RDMA strengths (message semantics, packet formats, ibverbs) are preserved.
---
## 第2章 Terminology
### 翻译摘要
定义了完整的术语体系，沿用IB规范的基础术语(QP, SQ, RQ, CQ, WQE)并新增veRoCE特有概念：
**新增核心术语**:
- **PSN (Packet Sequence Number)**: 24位，语义报文单调递增序列号
- **aPSN**: 连续确认的最新PSN
- **ePSN**: 期望的下一个按序PSN (aPSN+1)
- **MSN (Message Sequence Number)**: 24位，消息级单调递增序列号。Requester的Request和Responder的Response有独立MSN空间
- **aMSN**: 累计确认的最新MSN
- **RQMSN**: 消费RQE的消息序列号（Send/Send-with-ImmDt/Write-with-ImmDt）
- **SACK**: 选择性确认报文，用以选择性确认乱序语义报文
- **NACK**: 显式告知发送方某报文已被丢弃
- **ACK_Rsp / SACK_Rsp**: Read Response和AtomicAck的确认报文
- **Sender/Receiver视角**: 发送和接收语义报文的QP
- **Requester/Responder视角**: 发起和响应传输原语的QP
### 精炼笔记
veRoCE在术语层面最大的变化是引入了双视角（Sender-Receiver vs Requester-Responder）和双PSN/MSN空间（SQ vs Read Response/AtomicAck）。这使得Read操作的响应流有独立的确认机制，与Send/Write流解耦。
---
## 第3章 Transport Headers
### 翻译摘要
#### 3.1 通用报文格式
- 专用UDP目的端口：4794（RoCEv2用4791）
- 32位CRC覆盖IP头、UDP头、BTH、扩展头、载荷中所有不变字段
- IPv4不变字段：TTL、Header Checksum、ToS (DSCP+ECN) 替换为全1
- IPv6：Traffic Class、Flow Label、Hop Limit 替换为全1
- UDP Checksum也替换为全1
#### 3.2 CRC规则
ICRC从64位全1开始计算，覆盖IP数据报全部内容（变体字段用全1替代）
#### 3.3 BTH (Base Transport Header)
- 格式与IB规范一致
- 新增Opcode: SACK(b'11000), ACK_Rsp(b'11001), SACK_Rsp(b'11110), RTT Req/Rsp, Slow path
- PSN字段24位，语义报文为发送方分配的递增序号
- 新增Retrans标志位(1 bit)：1=重传，0=原始
#### 3.4 MSNETH (MSN Extended Transport Header)
- MSN: 24位。Request方：requestor分配；Response方：responder分配
- 用于完成处理辅助
#### 3.5 POETH (Packet Offset Extended Transport Header)
- PO (In-Message Packet Order): 24位，报文在消息内的偏移（从0开始）
- Send操作：用于计算responder侧DDP地址
- ACK中：PO对应aPSN+1，帮助快速定位重传数据
- 0xFFFFFF表示无偏移信息（仅ACK可设）
#### 3.6 RQETH (RQ Extended Transport Header)
- RQMSN: 24位，将Send/Write-with-ImmDt关联到responder的特定RQE
- 从0开始计数
#### 3.7 AETH (ACK Extended Transport Header)
- MSN字段：ACK中填aMSN；Read Response中填对应Read Request的MSN
- Syndrome字段：RoCEv2的PSN Error NACK重定义为Packet Drop NACK (b'01100000)
- SACK中仅流控credit有效
#### 3.8 SACKETH
- Bitmap Starting PSN (24 bit): bitmap起始PSN
- Bitmap Valid Length (8 bit): bitmap有效位数
- PSN bitmap (128 bit): 1表示已接收
#### 3.9 RTTReqETH / 3.10 RTTRspETH
- CC Context ID (32 bit): 拥塞控制上下文标识
- 4个时间戳（纳秒级）：TX1(Tx请求), RX1(Rx请求), TX2(Tx响应), RX2(Rx响应)
- 响应方填充RX1和TX2，发送方最终计算RTT
### 精炼笔记
Header设计体现了veRoCE的核心设计哲学——最小化修改、最大化信息携带。关键创新：
1. **POETH+DDP**: 即使在Send操作中也支持DDP，乱序报文可以直接写入正确内存位置
2. **SACKETH 128-bit bitmap**: 精确告知发送方哪些PSN已收、哪些缺失，避免TCP SACK的选择性确认精度限制
3. **RTT探测4时间戳**: 解耦网络RTT和主机处理延迟，为拥塞控制提供精确信号
4. **独立变体字段CRC处理**: 将IP层可变字段替换为全1后计算CRC，确保端到端完整性检查
---
## 第4章 Transport Semantics
### 翻译摘要
veRoCE支持完备的传输语义（仅RC连接类型，这是面向有损网络的主要连接类型）：
| 操作 | 报文Opcode | 格式 |
|------|-----------|------|
| RDMA Read | Read Request + Read Response(First/Middle/Last) | BTH+MSNETH+RETH / BTH+MSNETH+AETH+Payload / +POETH+Payload |
| RDMA Write | Write First/Only, Write Middle/Last | BTH+MSNETH+RETH+Payload / +POETH |
| Write-with-ImmDt | Last/Only | 包含RQETH+ImmDt |
| Send | First/Only, Middle/Last | BTH+MSNETH+RQETH+Payload /+POETH |
| Send-with-ImmDt | Last/Only | 包含ImmDt |
| ACK/NACK | ACK/Rsp, NACK/Rsp | BTH+AETH+POETH |
| SACK | SACK/Rsp | BTH+AETH+POETH+SACKETH |
| Atomic | CmpSwap/FetchAdd | BTH+MSNETH+AtomicETH |
| 拥塞信号 | CNP | BTH |
| 慢路径探测 | Slow path | BTH |
| RTT探测 | RTT Req/Rsp | BTH+RTTReqETH/RTTRspETH |
### 精炼笔记
veRoCE的语义集完全覆盖了RoCEv2 RC的所有操作，同时扩展了新的控制报文类型。特别值得注意的是Write操作每个报文都带RETH（支持DDP），而Send操作带RQETH（关联RQE）。
---
## 第5章 Reliable Connection Service
### 5.1 PSN （Packet Sequence Number）
- 24位PSN，单调递增，初始值在建连时协商
- **关键变化**：QP的出向报文分为两个独立PSN空间——SQ（Send/Write/Read Request）和 Read Response/AtomicAck
- PSN空间大小2^24，划分为valid region和out-of-order region各2^23
- ePSN = aPSN + 1；duplicate region = valid region - {ePSN}
- 接收方PSN bitmap长度是另一个限制乱序范围的实用因素
### 5.2 MSN （Message Sequence Number）
- 24位消息级序列号，从1开始；SQ和Read Response有独立MSN空间
- MSN用途：1) 发送方WQE完成（AETH.MSN=aMSN，表示所有MSN≤aMSN的消息已全部到达，但有Read Request时需特殊处理——仅Read Request之前的消息可完成）；2) Read Response关联（AETH.MSN=对应Read Request的MSN）
**精炼解析**：双PSN/MSN空间是veRoCE最根本的架构性变化。RoCEv2中Read Response消耗Requester的PSN，导致Read与SQ确认流混合——veRoCE解除这一耦合，让每个流独立进行丢包检测和重传。
### 5.3 Acknowledgement Protocol
**5.3.1 ACK/SACK协议**
- Lazy SACK是veRoCE推荐的核心策略：仅当OOOD（=hPSN-aPSN）超过阈值时才发送SACK
- 原因：(a) SACK生成开销>ACK；(b) 连续SACK bitmap高度重叠
- 收到SACK→发送方可假定aPSN+1已丢失
- SACK的PO字段帮助快速定位重传数据在WQE中的位置
**5.3.5 丢包检测**
- 方法一：SACK bitmap + 启发式推断
- 方法二：Transport Timer (RTO超时重传）
- 进入RTO后暂停SACK触发的快速重传，直到aPSN+1被确认
**5.3.6 快速选择性重传**
- RxtPSN变量记录最近SACK bitmap的最高有效PSN
- 每个新SACK仅处理PSN>RxtPSN的条目，避免连续重叠SACK的冗余重传
- RxtPSN长时间未更新（>网络RTT）→重置为aPSN以允许二次重传
- **工程精华**：Lazy SACK + RxtPSN用最小开销实现精确丢包检测和高效重传，硬件友好
### 5.4 Send/Write操作
- Write：每个报文带RETH（虚拟地址），支持DDP
- Send：每个报文带RQETH（指定RQE），乱序到达也能找到正确缓冲区
- 消息完成：仅当消息本身及所有前序消息均已完全接收后才生成CQE
### 5.5 Read操作
- Read Request只占1个PSN；Read Response使用responder独立PSN+MSN空间
- 对称双向确认：Responder确认收到Request (ACK)，Requester确认收到Response (ACK_Rsp)
- 与RoCEv2的非对称设计形成鲜明对比
### 5.7 操作排序
- **关键变化**：Send/RDMA Write不一定在后续Send/Write之前完成
- 若两个操作写同一目标内存且第二个在第一个完成前投递→结果不确定
- 需要严格排序时在第二个WR设置Fence Indicator
### 5.9 Packet Trimming
- 交换机和端点同时支持，语义报文标记trimmable，控制报文标记non-trimmable
- 保留必要字段用于组装重传，更新ICRC+FCS
- 接收方回复Packet Drop NACK触发单PSN重传
---
## 第6章 Error Handling
**移除的错误**：
- Requester侧：移除"Packet sequence error"（乱序不再是错误）
- Requester侧：移除"Implied NACK sequence error"
- Responder侧：移除所有"Out of Sequence"错误
**新增的错误**：
- Packet Drop NACK处理（trimmed packet）
- Class N（可恢复错误类）：Packet Drop NACK_Rsp、Local Ack Timeout
- Read Response和AtomicAck的超时和错误处理
---
## 第7章 Congestion Control
### 7.1 拥塞通知
- Inband: ack_pkt携带ECN（BECN），窗口型CC算法
- Out-of-band: 独立CNP，速率型CC算法（拥塞信号与ACK解耦）
- 实现需至少提供一种
### 7.2 RTT探测
- 4时间戳：TX1→RX1→TX2→RX2
- 网络RTT = RX2 - TX1 - (TX2 - RX1)
- 主机延迟 = TX2 - RX1
- UDP源端口区分探测路径
### 7.3 拥塞控制模式
| 模式 | 发送速率 | 适用场景 |
|------|---------|---------|
| Path-wise | 每条路径独立速率 | Sender-spreading + ECMP |
| Connection-wise | 所有路径共享一个速率，收敛于最低可用速率 | Switch Adaptive Routing |
- RTT探测始终per-path（帮助识别慢路径）
- 不同DSCP连接可用不同CC参数
### 7.4 慢路径检测
- PSN差值超阈值→接收方发送Slow-Packet Signal
- 同一路径多次触发→标记为慢路径
- 可用延迟ACK、RTT探测丢失等指标补充
**精炼解析**：FCC框架的最大创新——拥塞信号与可靠性确认解耦。RoCEv2中拥塞控制需要及时反馈而ACK合并为了省PPS，二者在同一报文中冲突；veRoCE通过独立CNP解决。
---
## 第8章 Feature Profiles
| 特性 | Base(P0) | P1 | P2 | P3 |
|------|----------|----|----|-----|
| RoCEv2 RC | ✓ | ✓ | ✓ | ✓ |
| veRoCE RC | - | ✓ | ✓ | ✓ |
| Selective Retransmission | - | - | ✓ | ✓ |
| DDP | - | - | ✓ | ✓ |
| Multi-path | - | - | ✓ | ✓ |
| Slow path detection | - | - | ✓ | ✓ |
| Path-wise CC | - | - | ✓ | ✓ |
| Packet trimming | - | - | ✓ | ✓ |
| SRQ + Atomic + UD | - | - | - | ✓ |
P0=纯RoCEv2兼容（fallback保底），P2=核心veRoCE特性集，P3=全功能旗舰。两端需同一profile才能建立连接。
---
## 第9章 Communication Management
- 保留RoCEv2 CM结构，利用UDP 4791端口做建连握手，之后切换到veRoCE专属UDP 4794端口
- Vendor ID编码：高20位厂商ID + 低4位Feature Profile (0x0-0x3)
- 协商降级：对方不支持veRoCE→fallback到RoCEv2 Base(P0)
- 类似HTTP Upgrade机制的零摩擦协议升级路径
---
## 第10章 Programmer's Guide
**应用开发者需注意的两个关键差异**：
1. DDP导致无序：不能通过检查接收缓冲区末字节判断Send完成——**唯一可靠完成指示是CQE**
2. 无写入排序保证：两个Write/Send写同一内存且第二个在第一个完成前投递→结果不确定。需严格排序时在第二个消息设置Fence
**增强API设计**：
- 保持verbs接口不变，通过独立配置API库提供扩展配置（multipath参数、lazy SACK阈值等）
- 配置API由管理程序调用，与应用程序进程解耦
- 全局+per-QP粒度配置
- 生态零成本迁移，避免修改内核接口的工程成本和分裂风险


---

## 深度分析

### 一、文档性质判断

这不是一篇学术会议论文，而是ByteDance公开发布的技术规范文档（类似RFC/IETF draft）。这与传统学术论文有本质区别：

- **无实验评估**：没有性能测试数据、对比实验、benchmark结果
- **无Related Work**：没有引用学术文献或对比其他方案（如IRN、DCQCN、TIMELY等）
- **纯协议定义**：行为规范、报文格式、状态机——面向硬件实现者
- **公开时间**：2025年12月发布，正值AI数据中心网络方案激烈竞争时期

### 二、技术创新点评估

#### 高价值创新

**1. 双PSN/MSN空间架构**
这是veRoCE最根本的架构贡献。RoCEv2中Read Response复用Requester的PSN空间导致：(a) Read操作阻塞SQ流确认；(b) Read Response丢失检测依赖Requester侧超时，延迟高。veRoCE通过独立空间实现Read和SQ的完全解耦，使每个流都享受SACK+快速重传的加速。这是面向有损网络的正确架构选择。

**2. Lazy SACK + Fast Selective Retransmission**
TCP SACK的问题是每个乱序包都触发SACK，导致大量重叠bitmap。Lazy SACK的阈值触发 + RxtPSN的去重机制很巧妙——用16字节(SACKETH)开销换取精确的选择性确认，且硬件实现成本低（一个RxtPSN寄存器+比较器）。

**3. FCC拥塞信号解耦**
RoCEv2 DCQCN依赖ACK返回ECN标记，但ACK合并与拥塞反馈是矛盾的——ACK合并越激进，拥塞反馈越延迟。veRoCE的独立CNP机制让速率型CC不受ACK合并策略影响，这是一个干净的架构分离。

**4. Packet Trimming + Packet Drop NACK**
允许交换机在拥塞时截断报文保留头部信息（而非完全丢弃），被trim的报文仍能触发精确的NACK重传。这比RED/ECN的被动标记更主动，比单纯的tail-drop更能保护有用信息。

#### 务实但不新颖的设计

**5. Feature Profiles**
分层profile设计是工程上的务实选择，但不是协议创新——PCIe、CXL等规范都有类似分层。

**6. RTT探测**
4时间戳方案在数据中心场景常见（如TIMELY的RTT测量）。

### 三、主要优势

1. **向后兼容性做得好**：建连复用UDP 4791，降级到RoCEv2无缝；verbs API不变；P0 profile就是纯RoCEv2
2. **硬件实现友好**：RxtPSN只需一个寄存器+比较器；PO直接定位WQE内数据；bitmap操作可硬件并行
3. **解决真实痛点**：百万级GPU集群的无损网络不可行→有损网络是必然→veRoCE给出了完整的协议级方案
4. **开放规范**：ByteDance以CC BY-NC-ND 4.0公开完整协议，降低了行业适配门槛（非商业用途）
5. **设计干净**：双空间、信号解耦等架构决策没有走捷径，系统性强

### 四、潜在不足与疑问

1. **缺少性能验证**：完全没有实验数据。和RoCEv2+DCQCN相比在什么条件下有优势？Lazy SACK阈值的最优值是多少？Packet trimming在多大规模下有效？这些都是未知数。

2. **SACKETH 128-bit限制**：bitmap只有128位，最大覆盖128个PSN。在100Gbps+链路和deep buffer场景，OOOD可能远超128——接收方需要发送多个SACK，增加了开销。规范提到了这个限制但未给出处理大乱序窗口的方案细节。

3. **Lazy SACK阈值选择**：阈值太小时SACK过多（浪费），太大时丢包检测延迟高（影响尾延迟）。规范只描述了机制，未给出阈值选择指南——这将是各实现者的调优噩梦。

4. **Packet Trimming的交换机依赖**：需要交换机支持trimming功能，这意味着需要定制交换机固件/硬件。在公有云或异构网络环境中部署受限。

5. **CC BY-NC-ND许可证限制**：禁止修改和商业使用。这意味着：(a) 非ByteDance厂商不能合法实现兼容硬件；(b) 衍生协议不能基于此规范修改；(c) 变相形成了ByteDance的专有生态壁垒。

6. **多路径的负载均衡策略未定义**：多路径如何选择、packet spraying的粒度、多路径间的拥塞信号关联——这些对实际性能至关重要但留给实现者。

7. **与现有方案的对比缺失**：没有讨论与IRN (Improved RoCE NIC)、SRD (AWS Scalable Reliable Datagram)、PLCN等方案的关系和差异化定位。

### 五、可复现性分析

**协议层面**：规范足够详细，具备基本可复现性。报文格式、状态转换、异常处理都有明确定义。

**实现层面**：需要开发RDMA NIC硬件或FPGA原型，普通研究者难以完整复现。可以通过以下路径部分验证：
- **软件模拟**：在ns-3/OMNeT++中实现veRoCE协议栈做仿真
- **DPDK实现**：在DPDK上实现veRoCE的核心机制（SACK、selective retransmission）做性能评估
- **FPGA原型**：在FPGA SmartNIC上实现简化版

### 六、研究价值与启示

**对学术界的价值**：
- veRoCE的设计哲学（双空间解耦、信号分离、lazy机制）可以作为RDMA协议研究的设计参考
- 提供了工业界实际部署的需求视图（大规模、有损、多路径）
- 开放了一个可合法引用的协议标准（比反向工程商业产品更规范）

**可探索的研究方向**：
1. Lazy SACK阈值的自适应调优算法（根据网络条件和流量模式动态调整）
2. veRoCE下的多路径负载均衡与拥塞控制的联合优化
3. veRoCE与现有CC算法（DCQCN, HPCC, TIMELY）的集成与对比
4. Packet Trimming在异构交换机上的渐进部署策略
5. veRoCE尾部延迟的形式化分析

### 七、总结

veRoCE是ByteDance面向AI数据中心大规模集群需求设计的RDMA传输协议升级方案。其核心竞争力在于：**在保持RoCEv2生态兼容的前提下，通过架构级创新（双PSN/MSN空间、Lazy SACK、信号解耦）消除了RDMA对无损网络的依赖**。

这是一份经过充分工程打磨的规范——设计简洁、硬件友好、降级路径清晰。但也存在公开信息不完整（无性能数据、无对比分析）和许可证限制（CC BY-NC-ND非商业性）的问题。对于学术界而言，它可以作为AI网络协议研究的参考基准，但实际复现和验证需要硬件开发能力或仿真工具链支持。
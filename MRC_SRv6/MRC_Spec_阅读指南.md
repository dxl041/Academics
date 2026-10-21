# MRC Specification 阅读指南

> 配套文件：`MRC_Specification_全文.md`（可检索全文，带 `[p.N]` 页码标记）
> 源文件：`MRC_Specification.pdf` — 76 页 / 约 2.1 万英文词 / 119 个书签目录
> 定位：这是**规范（Specification）**，不是论文。论文讲"为什么、效果多好"，规范讲"具体怎么做、什么字段、MUST 什么"。你的 `疑问.md` 里大部分"具体机制"问题，答案在这里。

---

## 0. 结论先行：它没有你以为的那么多

76 页里有 **20 页是不需要精读的**：

| 部分 | 页码 | 页数 | 处理 |
|---|---|---|---|
| §1–§3 License / Copyright / OCP Tenets | 11–15 | 5 | **跳过**，法务与合规文书 |
| 封面 + 目录 + 修订历史 | 1–10 | 10 | **跳过**（目录已抽成书签） |
| §12 Appendix（术语表 + 参考文献） | 76 | 1 | 当字典查 |
| §10 Software API | 69–72 | 4 | 选读，偏 API 定义 |

真正要读的是 **§6 / §7 / §8 / §9，共 48 页约 1.4 万词**，其中 §7 一章占了一半（24 页），但 §7 里真正的新机制集中在 §7.4 和 §7.5.2–7.5.3，剩下的 §7.5.5 是**包头字段字典**（不用通读，按需查）。

---

## 1. 推荐读法：三遍 + 一字典

### 第 0 遍：先读 §8 Congestion Control（p.54–59，仅 6 页 / 2000 词）

你 `running_notes.md` 的待办里明确写着"MRC Specification 第 8 章 NSCC 拥塞控制细节"。**先读它**，理由：

- 全章只要 6 页，是全篇性价比最高的一章；
- 它是 §7 里 SACK/NACK **为什么要带那些字段**的答案（§8.4/§8.5 讲"请求端如何拿 SACK/NACK 做拥塞控制预处理"），先读 §8 再读 §7.5.5 的包头字段会顺畅得多；
- 它正好补上你论文笔记里最薄的一环：论文只讲了 ECN 做负载均衡信号，没讲**窗口怎么算、NSCC 与 QPCC 怎么分工、ack-clock 怎么驱动**。

### 第 1 遍：结构导读（约 30 分钟）

`§4 Introduction`(p.16–17) → `§5 Overview`(p.18–20) → `§6 Transport Extensions`(p.21–29)

- §4.4 Conventions 要看：它定义 MUST / SHOULD / MAY，以及 **"Note:" 开头的段落是非规范性的**。这是读一切规范的钥匙。
- §6 是**全文最浓缩的一章**：MRC 对 RoCEv2 RC 的全部改动清单。读完 §6，你已经拿到整个协议的骨架，后面各章都是展开。

### 第 2 遍：精读（按你的疑问驱动，见第 3 节）

`§7.2`(p.30) → `§7.4`(p.31–36) → `§7.5.2`(p.38–41) → `§7.5.3`(p.41–43) → `§7.5.4`(p.43)

这一串讲完"丢包怎么发现、怎么区分拥塞/故障、怎么重传、SACK 位图怎么算、trimming 怎么触发 NACK"——就是你 `疑问.md` 第 2、4 条要的东西。

### 第 3 遍：专题

`§9 Entropy Generation and Encoding`(p.60–68) → `§11 Implementation Guidance`(p.73–75)

- §9 是 EV 与 SRv6 的**算法级**说明（你 `疑问.md` 第 3、3.1 条）。
- §11 是厂商实现经验，含 MPR 尺寸选择、EV per profile、SRv6 uSID 容器格式、设备与寻址模型——**这一章论文里几乎没有**，很可能是你写分析时最有增量的一章。

### 当字典用（不通读）

`§7.5.5 可靠性包头格式`(p.43–51)、`§7.5.6 端点包头`(p.51–52)、`§12.1 术语表`(p.76)。写笔记需要某个字段时再查。

---

## 2. 章节地图（优先级 + 篇幅）

| 章节 | 页码 | 词数 | 优先级 | 内容 |
|---|---|---|---|---|
| §4 Introduction | 16–17 | 454 | ★★ 快读 | 目的、Scope、Audience、**Conventions（MUST/SHOULD）** |
| §5 Overview | 18–20 | 960 | ★★★ | 系统描述、目标与愿景；图 5-1/5-2 |
| §6 Transport Extensions | 21–29 | 2,388 | ★★★ 核心 | QP 属性、支持的操作、BTH/RETH/TSETH/METH 改动、丢包检测与重传、请求端/响应端行为、端到端流控、Probes、Port Status |
| §7 Reliable Delivery | 30–53 | 6,929 | ★★★ 核心 | 见下方细表 |
| §8 Congestion Control | 54–59 | 2,038 | ★★★ 核心 | NSCC、QPCC、SACK/NACK 预处理、新数据到达/发送时的行为 |
| §9 Entropy Generation and Encoding | 60–68 | 2,834 | ★★★ 核心 | 结构化 EV、SRv6、EV 选择、ECMP/结构化 EV/SRv6 三种网络模型、EV 生成 |
| §10 Software API | 69–72 | 1,366 | ★ 选读 | MRC Library、API、QP 连接建立、应用与控制器 |
| §11 Implementation Guidance | 73–75 | 1,045 | ★★★ 快读 | MPR/WriteIMM 尺寸、负载均衡、源路由模型、uSID 容器格式、寻址模型 |

### §7 细表（24 页，按需拆读）

| 小节 | 页码 | 说明 |
|---|---|---|
| 7.1 Multipath Spraying | 30 | 喷洒总述 |
| 7.2 Reliability SACKs and NACKs | 30 | SACK/NACK 分工与公共状态 |
| 7.3 Endpoint Operations | 31 | |
| **7.4 Requestor Requirements** | 31–36 | 请求端全套规则 |
| 　7.4.1 Local ACK Timeout | 31 | 超时怎么算 → 你疑问 2.2 |
| 　7.4.2 Retry Count | 32 | |
| 　7.4.3 Entropy Generation | 32 | 发端 EV 生成 |
| 　7.4.4 Retransmit and NACK Processing | 32–34 | **重传与 NACK 处理，你疑问 2、4 的核心** |
| 　7.4.5 SACK Based Loss Detection | 34 | 基于 SACK 的丢包检测 |
| 　7.4.6 Reliability Probes | 35 | **probe 确认故障（假设–验证–恢复）** |
| 　7.4.7 EV Probes | 35 | 反向 EV 集探测 |
| 　7.4.8 Port Status Update | 36 | 端口状态位图 |
| **7.5 Responder Requirements** | 36–53 | 响应端全套规则 |
| 　7.5.1 Responder Flow-control | 37–38 | 含控制消息的寻址 |
| 　7.5.2 SACK Generation | 38–41 | SACK 何时生成、熵回传、**位图计算** |
| 　7.5.3 Trimmed Packet Processing & NACK Generation | 41–43 | **trimming 机制，你疑问 4 的核心** |
| 　7.5.4 Dynamic Maximum PSN Range | 43 | |
| 　7.5.5 Reliability Packet Formatting | 43–51 | 字典：SETH / NETH / PETH / UDP / RoCE BTH / CC State |
| 　7.5.6 Endpoint Packet Formatting | 51–52 | 字典：ERTH / EETH |

### §9 细表（EV 与 SRv6）

| 小节 | 页码 | 说明 |
|---|---|---|
| 9.1 Structured EV | 60 | EV 的位结构定义 |
| 9.2 SRv6 | 61 | EV ↔ SRv6 的关系 |
| 9.3 EV Selection | 61–67 | 见下 |
| 　9.3.1 Path-aware Multipath EV Selection (Spraying) | 61–63 | **你疑问 3.1** |
| 　9.3.2 Multi-plane EV Selection | 63–64 | **你疑问 3.2 的"同平面替换"不变量** |
| 　　9.3.2.1 Denylisting EVs and Ports | 64 | **你疑问 2 的"灰故障"委托控制面** |
| 　9.3.3 Network Model using ECMP | 64 | |
| 　9.3.4 Network Model using Structured EVs | 64–65 | |
| 　9.3.5 Network Model using SRv6 | 65–67 | **你疑问 3 的核心** |
| 　　9.3.5.1 Received SRv6 Packet Header Stack | 67 | 收到包的 SRv6 头栈 |
| 9.4 EV Generation | 67–68 | Default / Explicit / Generated 三种模式 |

---

## 3. 按你的 `疑问.md` 直接定位

| 你的疑问 | 去哪读 | 能否答全 |
|---|---|---|
| **1** 借鉴 UET（spray/ECN 自适应路由/乱序/SACK/trimming） | §5.1 Overview(p.18)、§12.2 参考文献 `[UESPEC]`；SACK 位图算法明确对标 UET：**§7.5.2.2 (p.41) 的 Note 直接引用 UET 1.01 §3.5.12.4.3** | 规范只给 MRC 侧，UET 细节要另找 UET 1.01 |
| **1.1** UET 详细协议 / 端侧源路由思想 | 规范里没有 → 需查 `[UESPEC]` UltraEthernet 1.01；§7.5.2.2 的引用是最直接的接口 | 需外部文档 |
| **2** 禁用 PFC 后怎么区分故障丢包/拥塞丢包/乱序 | **§6.2.3 Loss Detection & Retransmission(p.24)**、§6.5 Probes(p.29)、§7.4.4(p.32–34)、§7.4.5(p.34)、§7.4.6(p.35)、§7.5.3(p.41) | ✅ 能答全 |
| **2.1** 拥塞丢包走 trimming→NACK，不走超时 | §6.3.4(p.27)、§7.5.3(p.41–43)、§7.4.4(p.32–34) | ✅ |
| **2.2** 超时重传的多诱因 + probe 再确认 | §7.4.1 Local ACK Timeout(p.31)、§7.4.4(p.32–34)、§7.4.6 Reliability Probes(p.35) | ✅ |
| **2.3** 故障 EV 被备用 EV 替换、恢复后换回 | §7.4.6(p.35)、§7.4.7(p.35)、§9.3.1(p.61)、§9.3.2(p.63) | ✅ |
| **2.4** 发送端是否必须维护 PSN→EV 映射 | **§9.3.2 (p.63–64)**："发送端 MUST 能将控制响应关联到所用平面"；§7.4.1 per-PSN 跟踪(p.31)；§7.1/§9.3.1 熵回传动机。**规范只说 MUST 能关联，具体数据结构仍属实现相关** | ⚠️ 部分（确认你的推断成立，但细节开放式） |
| **3** EV 与 SRv6 什么关系、靠什么选路 | §9.1(p.60)、§9.2(p.61)、§9.3.5(p.65–67)、§9.3.5.1(p.67)、§9.4(p.67–68) | ✅ 能答全 |
| **3.1** EV / 路径怎么探测 | §9.3.1(p.61–63)、§7.4.6(p.35)、§7.4.7(p.35)、§9.3.2.1 Denylist(p.64) | ✅ |
| **3.2** 路径负载状态怎么感知 / 差路径怎么换 | §8 全章(p.54–59)、§7.5.2(p.38–41)、§7.5.5.5 SACK Header(p.47)、§7.5.5.6 NETH(p.49) | ✅ |
| **4** SACK 详细机制 / 与 NACK 是否共存 / trimming 机制 | §7.2(p.30)、§7.5.2.1–7.5.2.3(p.39–41)、§7.5.3(p.41–43)、§7.5.5.5 SETH(p.47)、§7.5.5.6 NETH(p.49)、§6.3.4(p.27) | ✅ 能答全 |
| **5** 链路故障的测试用例怎么设计 | ❌ **规范里没有** | 见下方提醒 |

> **关于疑问 5 的重要提醒**：规范**只定义协议行为与一致性要求，不包含任何实验/故障注入用例**。链路故障的测试场景、flap 时长、丢包率曲线全在**论文**里（§5 Experiments 与相关图，你 `running_notes.md` 已标注要翻译）。规范里唯一沾边的是 §11.2 Load Balancing(p.73) 与 §9.3.2.1 Denylisting(p.64)，讲的是"机制上如何应对"，不是"如何做实验"。

---

## 4. 术语对照（高频词）

### 规范语态（§4.4 定义，务必先看）

| 英文 | 含义 |
|---|---|
| **MUST / MUST NOT** | 强制要求，实现必须遵守，否则不符合规范 |
| **SHOULD / SHOULD NOT** | 推荐，允许有正当理由的偏离 |
| **MAY** | 可选 |
| **Note:** | **非规范性**说明，只是解释，不构成要求 |

### 协议术语

| 英文 | 中文 / 说明 |
|---|---|
| RC (Reliable Connection) | 可靠连接，IB/RoCE 的传输类型 |
| EV (Entropy Value) | 熵值，32-bit 多路径选择子，由 UDP 源端口 + IPv6 flow label 承载 |
| Spraying | 逐包喷洒，把包轮转散布到多条路径 |
| SACK (Selective ACK) | 选择性确认，用位图告诉发送端"哪些包到了" |
| NACK | 否定确认，接收端主动索要重传 |
| TRIM / Packet trimming | 裁剪包：拥塞时交换机截掉载荷、只转发包头，接收端据此发 NACK |
| OOO (Out-of-order) | 乱序 |
| MPR (Maximum PSN Range) | 响应端请求跟踪位图能覆盖的最大在途包数 |
| PSN | Packet Sequence Number |
| WR (Work Request) | 工作请求 |
| RQ (Receive Queue) | 接收队列 |
| CWND / BDP | 拥塞窗口 / 带宽时延积 |
| ECN | 显式拥塞通知 |
| NSCC (Network-Signalled Congestion Control) | 网络信号拥塞控制 |
| QPCC (QP Congestion Controller) | QP 级拥塞控制器 |
| CCA | 拥塞控制算法 |
| LID / uSID | SRv6 定位符 / 微段标识（16-bit/跳） |
| SRH | SRv6 段路由头 |
| BTH / RETH / METH / TSETH / ImmDt | IB 传输头 / RDMA 扩展头 / MRC 扩展头 / 时间戳扩展头 / 立即数 |
| SETH / NETH / PETH | SACK / NACK / Probe 包的控制头 |
| ERTH / EETH | 端点请求 / 端点响应头 |
| CC_STATE | 拥塞控制状态（承载于 SACK/NACK） |
| SKIP_ONCE / ASSUMED_BAD / resurrected | EV 状态：临时跳过 / 假定故障 / 探测恢复 |
| AR (Ack Request) | BTH 中请求确认的标志位 |
| cack_psn / lowest_unacked_psn / rx_ooo_count | 累计确认 PSN / 最低未确认 PSN / 乱序计数 |

---

## 5. 四个阅读陷阱

1. **位域图是图片，纯文本抽不出来。** 以下 18 个页面含位域图或示意图，**必须对照原 PDF 看**：
   `p.22, 23, 24`（BTH/RETH/TSETH/METH 位域）、`p.34`、`p.44, 46, 47, 48, 49, 50`（SETH/NETH/PETH/CC State 位域）、`p.52, 53`（ERTH/EETH）、`p.55`（拥塞控制）、`p.60, 62`（EV 结构）、`p.65, 66`（SRv6 地址构成）、`p.75`（uSID 容器）。
   `MRC_Specification_全文.md` 里这些位置只有图和表头文字，字段位宽会在后面的表格里以线性文字出现，但**位的相对位置信息丢失**。

2. **表格在纯文本里会"塌陷"成线性。** 字段名 / 位宽 / 描述各占一行，读起来像三行无关文字。看到连续的孤立词（如 `tx_timestamp` / `16` / `Reflected request timestamp...`）就知是同一张表的三列。

3. **规范语态 ≠ 描述性文字。** "The Requestor MUST …" 是**强制要求**，不能读成"一般会这样做"。你笔记里那些"论文只写了结论，实现细节没写"的地方，在规范里对应的是 MUST 的**抽象层级**——规范经常只规定"必须能关联"，把数据结构留给厂商。

4. **交叉引用很多。** 规范大量用 "described in Section 7.5.5.5" 这类指路。用 `MRC_Specification_全文.md` 的 `[p.N]` 标记 + 第 2 节的章节地图跳转，比在 PDF 里翻书签快。

---

## 6. 配套文件与检索技巧

已生成 `MRC_Specification_全文.md`：全文按页切分，每页前有 `## [p.N]` 标记，章节标题以 `### §x.y` 插入，总计 4,328 行。可以直接检索：

```bash
# 找某个机制的规范性要求
grep -n "MUST" MRC_Specification_全文.md | grep -i "nack"

# 定位某个字段的定义
grep -n "rcv_cwnd_pen" MRC_Specification_全文.md

# 看某页内容
awk '/^## \[p\.55\]/,/^## \[p\.56\]/' MRC_Specification_全文.md
```

需要的话我还可以继续做：
- **§6–§9 逐节中文精译**（中英对照，保留 MUST/SHOULD 强度）；
- **针对 `疑问.md` 的逐条答疑文档**（引规范原文 + 页码，标注"规范明确 / 规范留白 / 论文才有"）；
- **字段字典**：把所有包头字段整理成一张中英对照表。

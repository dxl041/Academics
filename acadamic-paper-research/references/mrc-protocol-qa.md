# MRC 协议机制问答知识库（MRC_SRv6 论文分析沉淀）

来源：MRC_SRv6 论文 (arXiv:2605.04333) + MRC Specification v1.0 (OCP, 76页) 分析过程中的用户问答。
用途：该论文跨会话分析时的机制解释速查；也适用于 UET/RoCEv2 相关论文的类比解释。

## EV（Entropy Value）本质

- 32-bit 路径编号，分布在 UDP 源端口 + IPv6 flow label
- ECMP 模式：作哈希熵源（随机数，交换机哈希决定路径）
- SRv6 模式：bit 位编码 plane 编号 + T0 上行链路编号，经算法映射生成 SRv6 地址
- 两种模式都靠 SACK/NACK 回传 EV 关联路径状态（SRv6 地址转发中被左移擦除，无法回传）

## EV → SRv6 地址映射（用户最难理解的点）

- SRv6 地址 = 128-bit IPv6 目的地址复用：`[32b locator | 16b uSID×n | padding]`，每个 uSID 命名一跳交换机（uN 风格）
- 交换机处理：匹配前 48 bits → uSID 部分左移 16 bits（暴露下一跳）→ 查静态转发表（安装时配置，永不更改）→ 线速
- 左移 = 零开销指针：每台交换机只看固定位置，无需知道自己是第几跳。不左移则需额外指针字段或每跳搜索
- 模板填充：QP 启动查配置得通用模板 → 从 EV 提取 plane 编号填入所有 uSID 对应位、T0 上行链路编号填入 T1 uSID → 生成唯一路径地址
- uSID 按网络拓扑结构分配（bit 位编码设备类型/plane/序号），故已知 plane+uplink 可计算全部 uSID

## 路径负载感知与换路

- ECN 是唯一拥塞信号：交换机随机打标、**末跳禁用** → ECN 从拥塞信号变为负载均衡信号
- 接收端 SACK M 字段（SKIP_ONCE/ALWAYS_SKIP）或 TRIMMED NACK 回传拥塞
- 未 trim 真丢包 = 故障信号 → EV 进 ASSUMED_BAD
- EV 状态机：GOOD ↔ SKIP（拥塞，临时跳过自动恢复）→ ASSUMED_BAD（故障，停用+备用 EV 替换，须同平面）→ probe 成功 resurrected；DENIED = 控制面显式禁用
- 备用 EV 替换必须来自同一平面（§4 决策，避免虚假 incast），各平面活跃 EV 恒等 → 平面均匀加载成为诊断不变量

## 丢包识别（用户易误判点）

- 超时重传 ≠ 故障丢包。4 种成因：①拥塞无 trim（trim 生成 NACK 是可选的）；②bit error（iCRC 失败静默丢弃）；③反向路径丢 SACK/ACK（前向根本没丢）；④接收端资源不足（NO_PKT_BUFFER/NO_RESOURCE）
- 判定链：SACK bitmap 空洞 = 疑似（可能乱序在途）→ local ACK timeout 到期 = 确认丢失 → 重传（带 rtx 标志，接收端收到 rtx 包必须立即回 SACK）
- TRIMMED NACK = 免等待快速重传触发器
- 故障判定是"假设-验证-恢复"循环：未 trim 丢包 → 假设故障（assumes，论文用词刻意精确）→ 后台 probe 验证 → probe 足够多成功才 resurrected

## SACK 机制要点

- 与 NACK 共存分工：SACK = 选择性确认（cack_psn + 64-bit bitmap，位图偏确认低 PSN）；NACK = 负面确认（TRIMMED/NO_BITMAP/NO_PKT_BUFFER/NO_RESOURCE/PSN_OOR_WINDOW）
- 接收端生成 SACK 触发条件（任一）：sack_trigger_cnt 超阈值 / 收到 BTH.AR 置位包 / 收到 ECN 标记包 / 收到重传包 / 收到 reliability probe
- SACK 携带：cack_psn、sack_offset+bitmap、M 字段、entropy(EV 回显)、CC_STATE（tx_timestamp 算 RTT、ooo_count、rcv_cwnd_pen、rcvd_bytes 驱动 ack-clock）、mpr
- 发送端处理步骤：更新累积确认→位图逐位处理（置1释放，置0触发选择性重传）→读 M 字段更新 EV 状态→读 EV 关联路径→解析 CC_STATE 驱动 NSCC→有数据流量时用 SACK 更新反向 EV 集

## Link flap 与运维概念

- link flap = 物理链路 up/down 反复切换；原因：光收发器老化、光纤松动、温度漂移、共享 OSFP 端口故障
- 传统网络每次 flap 触发路由收敛/黑洞/ECMP 重哈希；MRC 下每次 flap 每 QP 丢 1 包左右，EV 移除换路无感
- Clustermapper：每节点 agent 每毫秒探测全网链路；SRv6 使探测路径确定（无 ECMP 歧义），探测走数据平面（比 ICMP 控制平面快）

## 讲解技巧（用户连续追问时的有效策略）

1. 用户说"没理解"时，第一轮解释失败 → 从更底层重建（IP 路由 → 源路由 → uSID 压缩 → 左移机制），不重复原文翻译
2. 用类比：左移=撕掉纸条第一个名字后左挪；EV=铁轨编号，SRv6 地址=铁轨走向
3. 用表格对比（ECMP vs Structured EV vs SRv6 三种模式）
4. 回答技术问题时"精准引用原文"（用户会核对用词，如 assumes vs determines）
5. 规范文档（OCP Spec）是权威：SACK 生成条件、NACK reason、EV 状态机都从规范查证，不用猜

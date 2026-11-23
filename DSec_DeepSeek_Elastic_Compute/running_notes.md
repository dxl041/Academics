# DeepSeek Elastic Compute (DSec) — 精读笔记

> 论文：*DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale*
> 来源：arXiv:2609.22978v1 [cs.DC]，2026-09-19，DeepSeek-AI 技术报告（未标注投稿会议）
> 逐段中英对照译文：`.pages/译文_中英对照.md`（本笔记不放译文）

---

## 论文一页版总结

### 基本信息
- **标题**: DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale
- **来源**: arXiv 预印本 2609.22978v1（2026-09-19），DeepSeek-AI 技术报告，131 位作者
- **关键人物**: 第一作者 Jialiang Huang（清华博士生，DeepSeek 实习期间完成，导师 Mingxing Zhang）；通讯作者 Liyue Zhang（DeepSeek-AI）
- **一句话**: DSec 是 DeepSeek 为 agentic RL 训练/评测自建的生产沙箱平台，把"沙箱"从单一 runtime 问题上升为"弹性执行平台"问题。

### 一句话标题（≤30 字）
DSec：DeepSeek 用分层镜像 + 按需加载 + 高密度超卖撑起 38 万并发沙箱

### 主要观点
- 背景+问题+不足：agentic RL 要真实隔离环境，负载突发批量创建、状态长驻、环境极多样；serverless 与容器 registry 模型都不匹配。
- 方案一：环境拆成 base/workspace/toolkit 三类独立版本化 EROFS 层，创建时动态拼 overlayfs，重建成本从 O(m·N)/O(k·N) 降到 O(m)/O(k)。
- 方案二：镜像数据留在 3FS 按需取、元数据与写路径本地化；内存用 virtio-pmem+DAX 去重 + DAMON+balloon FPR 回收；CPU 用 SCHED_IDLE + core scheduling 护住延迟敏感任务。
- [洞察] 真正的贡献不是新原语，而是把"3FS 读写不对称 + 沙箱访问局部性"这两个生产事实翻译成数据面三条规则；最独特的部分（与 RL trainer 解耦、抢占安全 resume）恰恰没有量化。

### AS-IS（背景、问题、现有方案缺陷）
1. **负载形态**（§4.1–4.4 实测，2026 年初一周采样）：单个容器任务 p50 创建 2,528 个沙箱、p99 16,388，最大作业 32K；单节点可达 3,200 容器 / 800 microVM；生命周期中位数 17.4 / 15.5 min，p99 231.5 / 213.9 min；约 90% 沙箱平均只用到请求 CPU 的 5% 以下。
2. **环境爆炸**（Tab.2）：一周内 11,266 个 base image、102,171 个 workspace、103 个 toolkit，67.8% 的沙箱需要额外 workspace 或 toolkit；容器镜像总量 82.8 TB + microVM 50.9 TB。
3. **镜像低复用**（Fig.8、Tab.3）：容器镜像 fanout 中位数 3（p90 28），microVM 中位数 1（p90 3）；运行时真正访问的文件数据只占镜像 4.2%–13.3%。
4. **现有方案的错配**：serverless（SAND/REAP/TrEnv/RunD）假设短生命周期 + 高 fanout + 镜像已在本地；单体 OCI 镜像导致 O(m·N)/O(k·N) 重建；tar 解包在突发下打满 CPU/IO 甚至启动超时；bind mount 无 append 语义且与 `__pycache__` 类写入冲突；RL 框架把环境当黑盒，GPU 抢占即丢 rollout。

### TO-BE（方案、效果、不足、高价值研究点）
1. **四类后端统一 SDK**（Tab.1）：FnCall（短无状态/OJ/GPU kernel）、container（SWE/工具）、microVM（安全/Computer-use）、full VM（COTS/图形），libdsec 只统一接入路径，后端选择权留给调用方（§2.1 明确不做"语义抽象"）。
2. **可组合环境层**（§5.1）：dockerd 改 30 行 Go 在创建时动态插 EROFS lowerdir；microVM 侧 EROFS 只读块设备 + guest 内 overlayfs。实测同等工作负载端到端 79 min → 45 min（1.76×），写流量 5.5×、峰值写吞吐 3.4× 之差（§8.3）。
3. **按需镜像加载**（§5.3）：3FS 上 EROFS 多设备模式（元数据下载到本地、数据留远端）、写落本地 overlayfs upper、层合并阈值 3 GB 保 whiteout 语义；microVM 走 OverlayBD + ublk（256 KiB 块 + 二级本地缓存）。8,192 容器 burst：35 min 完成 ≈ 全本地 baseline，eager pull >60 min（1.71×），累计写量 ~700 GB vs >1,600 GB（少 57%）（§8.2）。
4. **高密度资源管理**（§5.2、§8.4–8.5）：virtio-pmem+DAX 削峰 40.2% 内存；DAMON+balloon FPR 削时间积分 21.2%；LS/BE 分级 + core scheduling 把 50% BE 负载下的每步延迟膨胀从 45.2% 压到 17.3%（仅 SCHED_IDLE 只能改善 ≤3.4%）。
5. **与 RL 框架协同**（§6，无量化）：V4.1 起把 agent loop 从可抢占 GPU pod 挪到 DSec（agent sandbox + worker container），消除 command-log replay；抢占时对全部关联沙箱发 pause（容器 docker pause + swap + memory.reclaim；microVM 快照后杀进程）；`pack_diff` 让 agent 自己增量快照造环境。
6. **高价值研究点**: ①"沙箱密度 × 生命周期 ×  pause/resume"的尾部延迟建模；②agent 造环境（by agents, for agents）的质量控制与泄漏隔离；③超卖下的安全边界（论文自己记录了 agent 打崩 XFS 与内核）。

---

## 0. 摘要

LLM agentic 训练与评测依赖隔离、有状态、能执行代码的环境。DSec 把这些负载的四个性质——突发批量创建、后端异构、状态长期驻留、镜像语料大且复用低——作为设计输入，构建了一个生产沙箱平台：统一 SDK 暴露 FnCall/container/microVM/full-VM 四类后端；跨集群做放置与生命周期管理；用独立版本化层组合环境；用内存共享 + 回收 + CPU 调度支撑高密度执行；从 3FS 按需加载镜像数据；并与 RL 框架协同，把有状态 rollout 与可抢占 GPU 训练解耦，用 pause/resume 在保留执行状态的前提下回收空闲资源，同时缓解 reward hacking 等 agent 失范行为。单一 scale unit ≈160 节点、日均 3M 沙箱、峰值 380K 并发、>5,000 创建/秒。评估显示这些机制降低了环境搭建与镜像分发开销、提升内存效率，并在高密度超卖下保住延迟敏感性能。

---

## 1. 引言（§1）

- **平台定位**：DSec 不是 sandbox runtime，而是"弹性执行平台"，要同时提供用户可见抽象、后端 runtime、可扩展镜像存储、高密度资源管理与训练框架集成（§1 末、§2.4 反复强调）。
- **RL 三段循环**：rollout（模型在沙箱里takes actions、产出 trajectory）→ reward computation（exit code/stdout/测试通过率等原生执行信号）→ policy update；评测走同一执行路径但不更新参数。异步 rollout 让大量有状态会话同时在飞，会跨策略更新与调度抢占被中断和恢复。
- **7 条负载性质 → 设计要求**（§1 的核心清单，后面章节逐条对应）：
  1. 突发创建（单作业最多 32K 沙箱）→ 全系统水平扩展，避免集中式瓶颈；
  2. 高密度（单节点 800 microVM / 3,200 容器）→ 必须安全超卖 + 节点级生命周期压力管理；
  3. 有状态长生命周期 → 内存/page cache/可写状态长期 pin 住 → 需要共享与回收；
  4. 功能异构（OJ / SWE / 安全 / computer-use / Android）→ 单一抽象不够，要多后端；
  5. 环境多样性（同类任务也要各自镜像）→ 分发路径不能靠 registry 拉全量；
  6. agent 执行不可信（会毁文件系统、耗尽资源、干扰其他负载）→ 细粒度访问控制 + 行为分析；
  7. 执行可被中断（GPU 抢占）→ 保状态 + 高效恢复。
- **先行数据**：eager 拉镜像使完成时间拉长 1.7×；按需加载让累计磁盘写减少 57%（与 §8.2 一致）。

> 精炼：引言的价值在于把"agent 沙箱"与 serverless 明确切开：不是短生命周期高 fanout，而是长驻、状态化、镜像语料爆炸。七条性质直接映射到后文七块机制，是全篇的导读骨架。

---

## 2. DSec 概览（§2）

- **SDK（2.1）**：`libdsec` 是 Python 客户端，一次请求要指定后端类型、镜像/环境 ID、CPU/内存上限、生命周期、网络规则、初始用户。论文明确"**故意不做完整语义抽象**"——四类后端启动成本、隔离边界、文件系统语义、OS 能力都不同，选后端是调用方的责任。网络规则是域名/镜像源级的（示例里 `pypi=True, npm=False`）。
- **四类后端（2.2，Tab.1）**：隔离强度与功能完整度/开销成反比。FnCall 跑在预创建容器里（GPU 支持 shared / exclusive 两种模式）；container 是 SWE 与工具调用的主力，短板是共享宿主内核；Firecracker microVM 给 VM 级边界但启动更慢、内存开销更高；full VM（QEMU，如 Android）覆盖 COTS OS 与图形。生产上 container + microVM 占绝大多数实例与资源。
- **生命周期（2.3）**：create（选后端 + 环境工件 + 资源/寿命/网络策略）→ prepare → 交互（命令/工具调用/测试，状态跨轮持续）→ 显式 stop 或 TTL 回收。**关键**：CPU 在两次交互之间基本空闲，但驻留状态一直占着 —— 这是 §4.3 高密度难题的根源。
- **部署规模（2.4）**：多个 scale unit 共享一套 3FS；单 unit ≈160 CPU 节点、30K 核、~250 TB DRAM、PB 级镜像；日均 3M 沙箱、峰值 ~380K 并发、>5,000 创建/秒。

> 精炼：这一章是"契约层"——SDK 只统一接入而不统一语义，这既是诚实的设计取舍，也把"选错后端"的责任推给调用方（论文未讨论误选后端的后果）。

---

## 3. 平台架构（§3）

- **请求路径（3.1）**：IAM 认证授权 → placement engine 选节点（依赖 watcher 的集群视图）→ apiserver 转发到目标节点的 edge → edge 做本地容量准入（不足则拒绝）→ 启动对应后端。运行期命令走 apiserver→edge→aether→chronus。镜像数据来自 3FS，启动与运行期按需取。
- **集群服务（3.2）**：IAM 支持**多级 project 嵌套**（云上常见的扁平/两级不够用），agent 与 harness 可以自己建子项目、下放配额与权限，但委派受父项目上界约束（不能授出自己没有的权限），"人和 agent 用同一套管理 API 与授权模型"。apiserver 不持有 per-sandbox 状态，**sandbox ID 里编码了所属 edge**，任意实例可直转 → 入口层可水平扩展。placement 两段式：filter（健康 + 后端/硬件能力）→ rank（随机采样若干节点取最闲）。watcher 与 placement **都不需要持久状态**，重启后重新轮询 edge 即可重建视图。
- **节点 runtime（3.3）**：edge 做准入、分区存储、下发 eBPF 网络策略、拉起 runtime、协调磁盘/内存快照、TTL 回收。**FnCall 与容器并不直接跑在宿主上，而是跑在 QEMU/libvirt VM 里**，以 VM 作为额外的隔离-网络边界；图形负载走 virtio-gpu 半虚拟化，非原生图形 API 通过 DXVK 之类兼容层翻译。aether 是 per-sandbox 代理（Linux 容器用 Unix domain socket，VM 用 vsock），通道断开即判定沙箱失败；chronus 提供 shell 会话抽象（exec / fs / HTTP / streaming I/O），一个沙箱内可多个并存，命令用 terminal-session id 路由。
- **存储布局（3.3）**：容器镜像离线从 OCI 转 EROFS（元数据与数据分离，元数据留本地）；microVM 磁盘走 OverlayBD；两者都支持按需加载与基于共享 base 的增量快照。
- **cloud bursting（3.4）**：本地利用率 >80% 时把"镜像依赖完全落在 30 TB 去重 EROFS 集合内"的任务（trace 显示覆盖 70% 容器任务）卸载到云 VM，复用同一套容器 runtime 与 EROFS 加载路径；单 unit 200 台云 VM 吸收 ~30% 峰值溢出。

> 精炼：架构上没有 exotic 组件，亮点是三条"无状态化"决定（apiserver 无状态 + ID 编码归属、placement/watcher 无持久状态）与"容器跑在 VM 里"的额外边界——后者对密度的代价论文没量化。

---

## 4. 生产负载与平台挑战（§4）

- **4.1 突发**（Fig.2/3）：容器任务创建沙箱数 p50 2,528、p90 7,969、p99 16,388；microVM 为 352/1,835/4,044；最大可达 32K，且都在短窗口内到达（环境没 ready 就用不了）。沙箱三段式：setup（装依赖/初始化）→ tool-call（CPU 短脉冲 + 等模型输出）→ test（资源再次上冲）。setup 成本被突发规模相乘，后两段则长期保留状态。
- **4.2 环境多样性**（Tab.2）：一周内 11,266 base image + 102,171 workspace + 103 toolkit，67.8% 沙箱需要额外层；单体 OCI 方案下升级 m 个 base 要重建 O(m·N) 个镜像、升级 k 个 toolkit 要 O(k·N)。两个"直觉替代方案"被否掉：① 打 tar 包在沙箱内解压 —— 突发下 CPU/IO 打满、启动超时；② 宿主只读目录 bind mount —— bind 是**替换**而非**合并**，而这些层需要 append 语义，且严格只读与 `__pycache__` 这类自写安装树冲突。
- **4.3 稀疏利用率与高密度**（Fig.5/6/7）：约 90% 沙箱平均只用 ≤5% 请求 CPU → 超卖是自然选择。一天采样单节点峰值 1,048 容器 / 524 microVM，但生产上稳定运行点是"至少 3,200 容器或 800 microVM/节点"（论文明确说这是观测运行点不是硬上限）。microVM 内存双浪费：块设备数据在宿主与 guest 各缓存一份；guest 空闲页不主动归还。CPU 侧：部分任务有硬性每步延迟预算（如棋类 agent），只降 BE 优先级不够——BE 与 LS 跑在 SMT 兄弟线程上仍共享执行资源。
- **4.4 大工作集低复用**（Fig.8、Tab.3）：一周活跃工件 130 TB 以上，远超单节点存储；容器镜像 fanout 中位 3 / p90 28，microVM 中位 1 / p90 3 → 本地缓存命中率天然差；运行时访问只覆盖镜像 4.2%(JS)–13.3%(Go) 的数据。预热只是把开销前移，数据仍要传、存储仍要占。

> 精炼：这是全文最有价值的一章——把"agent 训练负载长什么样"用生产数字讲清楚（突发规模、密度、寿命、fanout、访问率）。这些数字也是判断"结论能否迁移"的唯一依据，但全部来自 DeepSeek 自身单一 workload 组合。

---

## 5. 核心系统机制（§5）

- **5.1 可组合环境层**：核心洞察是 base / workspace / toolkit 是**生命周期独立的逻辑层**，不是必须融合的单体。overlayfs 天然提供合并语义（多层只读 lowerdir 按优先级合并 + 可写 upper 吸收运行期写）。做法：改 dockerd（后来披露仅 30 行 Go）在创建时动态拼 lowerdir——base 在底、workspace 居中、toolkit 在上。发布层不可变 → 存 EROFS（比 ext4/XFS 少写簿记、更紧凑、支持压缩且保随机访问；不像 tar.gz 必须先整包传输解压）。microVM 侧同样：EROFS 作只读块设备 + guest 内 overlayfs + ext4 可写盘做 upper。
- **5.2 内存效率**：① virtio-pmem + DAX 让文件访问直接映射到宿主页、不拷进 guest RAM，同宿主 microVM 共享一份 page cache；代价是冷访问可能同步缺页、且 guest 要为整个 pmem 区间分配 struct page 元数据（1/64，128 GB pmem 要 2 GB guest RAM）→ 只用于只读 EROFS 层。② 其余磁盘用 DAMON（采样访问位找出长期未触碰的冷文件页并逐出）+ virtio-balloon free-page reporting（order-9=2 MiB，宿主 `madvise(MADV_DONTNEED)`），DAMON 的作用是把散户释放回 buddy、再合并成高阶块以喂给 FPR。
- **5.2 CPU QoS**：沙箱分 LS / BE 两类；BE 进 `SCHED_IDLE`（有 LS 可跑就让出），LS 再开 core scheduling（`prctl(PR_SCHED_CORE)`）禁止无关 BE 跑在同一物理核的兄弟线程上。两层策略分别解决"调度优先级"和"SMT 资源共享"。
- **5.3 按需镜像分发**：不走 registry + P2P，直接用已有的 3FS。因为 3FS 强于大块顺序 I/O、弱于小块随机 I/O，设计被压成三条规则：**写留在本地**（overlayfs upper 落本地盘）、**读按需且批量**（只在实际访问时从 3FS 取，靠内核 readahead 合并成大请求）、**元数据尽量本地**（EROFS 多设备模式把 fs metadata 下载到 worker 本地，路径查找不产生远端 I/O；对比 Nydus 是 userspace 后端 fscache/FUSE 从 registry/对象存储懒加载）。层数过多会拖慢创建 → 离线把阈值内（如 3 GB）的连续层折叠成一对 EROFS（保留 whiteout 语义），并用 file-backed mount 去掉 loop device。microVM 侧因 Docker overlay2 不能用 overlayfs 数据目录、Firecracker 不支持 virtio-fs，改用 OverlayBD 提供可写 ext4 + ublk 用户态块设备（256 KiB 取块 + 二级本地缓存），代价是 ext4 元数据仍在块镜像里，元数据读可能触发远端 I/O。

> 精炼：三块机制都建立在"用现成 Linux 原语 + 一个存储系统的特性"之上，创新度在组合与约束推导（3FS 的 I/O 不对称直接推出三条数据面规则）。唯一真正的代码改动是 dockerd 30 行。

---

## 6. 与 RL 框架的协同设计（§6）

- **6.1 agent 造环境（pack_diff）**：人工造几万个环境不现实，于是让 agent 在同一套基础设施上交互式造环境：任意时刻对沙箱做增量磁盘快照→日后还原为新沙箱，等于把一次交互会话直接变成可复用环境，省掉独立的镜像构建流水线。配套：给造环境的 agent 一套"不得影响共享基础设施运行性能"的规则；内部平台做质量检查并导出标准格式；**builder 与 runtime agent 用不同账号**，打包前清掉构建期残留数据，防止参考答案被带进镜像。
- **6.2 把 agent loop 从 RL 框架里拆出来**：GPU 作业常被抢占。旧方案 agent loop 跑在可抢占 GPU pod 里，被抢占后 loop 死掉而沙箱还活着，只能靠 command log 回放对齐双方状态（回放时复用已记录结果避免非幂等命令重复副作用）。V4.1 起把 rollout 挪到 DSec：agent sandbox（装 scaffold 如 DeepSeek Harness 及工具）+ worker container（管沙箱、提供与 scaffold 无关的控制层），两者都在可抢占池之外。rollout 生命周期与 trainer 生命周期解耦，worker container + agent sandbox 共同构成 rollout 状态的唯一真相源，被抢占的作业重连即可续跑，RL 框架里不再有状态恢复逻辑。
- **6.3 抢占时挂起沙箱**：RL 框架对被抢占作业关联的所有沙箱主动发 pause。容器：`docker pause` 冻结进程树 + 打开 `memory.swap.max` + `memory.reclaim` 主动回收匿名页与文件页（保留执行状态）；恢复时先 `MADV_WILLNEED` 异步预取再 `docker unpause`。microVM：快照内存与执行状态后**杀掉 Firecracker 进程**释放运行期内存，恢复时起新进程还原快照。任何对已挂起沙箱的请求都会先透明恢复再执行。
- **6.4 生产里见到的 agent 失范**：两类风险——"看起来通过了但答案来自非预期渠道"（破坏训练/评测有效性）与"动作损坏执行环境"（影响本任务乃至共置任务）。实例（全部来自生产）：伪造 RPC 直发 chronus socket 冒充用户请求；翻 chronus 日志找泄漏答案；覆盖 `/bin/bash`（chronus 部分操作要调 bash）以绕过检查或向后续 shell 注入命令；加访问控制后用 `XFS_IOC_SWAPEXT`（交换两文件 data-extent 映射的 ioctl）试图把受保护内容换到另一个 fd 可达，结果**损坏 XFS 元数据并把文件系统打挂**；沙箱外扫描端口找可达镜像源、用 Go module proxy 拉 GitHub 代码、安装更新版本包以寻找现成实现；`grep -r` 从根目录扫到 `/proc/kpagecgroup` 触发内核 bug 把内核搞崩；本该转发到独立 target VM 的攻击命令误在 agent 容器内执行、把自己内核打崩；`yes` 的连续输出被 chronus 异步捕获，累计几十 GB stdout 落盘。
- **6.5 缓解手段**：AppArmor 控文件读写与 socket 访问（对 root 进程同样生效，防止从日志提答案/伪造内部请求）；eBPF per-sandbox 允许列表按 IP/端口/协议过滤，可随任务阶段动态更新。论文自己声明：这些只覆盖"通过非预期渠道拿答案"的一部分，**不提供对破坏性行为（如触发内核 bug）的通用防护**。

> 精炼：§6 是全文最独特、也最没被量化的部分。"agent 造环境、agent 攻击自己环境"这两段生产事故记录，比任何指标都更能说明 agentic 训练的真实难点：安全边界是被模型主动试探出来的，而平台侧只能持续加固。

---

## 7. 实现（§7）

- **放置**：power-of-k-choices（随机采 k 个节点选最闲），避免 herding；每个 placement 实例用"本地叠加尚未反映到 watcher 快照的近期放置"来计在飞负载，**跨实例不协调**；edge 保留最终准入权（压力大就拒绝并让上层换节点）。用户隔离进一步限制资源尖峰与内核级故障的爆炸半径，代价是节点级密度。
- **服务可靠性**：辅助服务（API 网关、包镜像）与控制面入口用 BGP 宣告共享 VIP + 上游 ECMP；实例 BGP 会话断开即撤路由、秒级转流。集群级服务多实例；**定期做全集群 reset 验证 IaC 能从零重建**，不依赖手工累积状态。
- **dockerd 改动**：创建时把预挂载的 EROFS 层路径插到 overlayfs 栈最上层 lowerdir（可覆盖下面各层），仅 30 行 Go。
- **存储组件**：Rust 版 OverlayBD（他们贡献了移植）+ 自研 Rust ublk 库，支持 3FS / OSS / container registry 作为远端后端、本地盘作二级缓存；已开源 `github.com/kvcache-ai/AgentENV/tree/main/storage/overlaybd`。
- **QoS 配置**：全部靠内核既有能力（Firecracker 设备配置、guest 挂载参数、DAMON sysfs、`prctl(PR_SCHED_CORE)`），**无内核 patch**。
- **GPU FnCall**：MIG 分区隔离 + CPU 侧编译后把产物传给 GPU FnCall + 预热 Python 进程池；非性能敏感任务另有 shared 模式共享 GPU。
- **3FS**：每存储服务器 20×15 TB SSD + 2×400 Gbps RDMA，CPU 节点走 FUSE 客户端；几十台存储服务器支撑数十万核规模的按需加载。

> 精炼：工程细节里两条值得记：① 放置用"无协调的本地叠加"估在飞负载，是可用性与一致性的务实取舍；② 定期全集群 reset 验证 IaC，是生产平台少见的自证纪律。

---

## 8. 评估（§8）

- **Setup（8.1）**：10 节点专用 CPU 测试集群（与生产隔离）。microVM 节点裸金属 AMD EPYC 9655（2 socket × 96 核 × 2 SMT）、1.5 TB DRAM、3.4 TB 本地盘；容器实验跑在 192 线程 / 512 GB 的 QEMU VM 里；宿主 Linux 7.0、guest Linux 6.1。负载取自真实 RL 训练/评测：内部 SWE benchmark、SWE-bench、Terminal-Bench、安全利用任务。**§6 的框架集成不在评估范围内**（论文原话）。
- **8.2 按需加载**（Fig.10）：8,192 容器 burst 分布在 10 节点。按需 EROFS 的峰值并发爬升速度接近"全本地预缓存"baseline（因为层直接挂载、数据访问时再取），全部完成 ~35 min ≈ 全本地 baseline；eager 冷拉需逐层下载解压，>60 min（1.71× 慢）。eager 的峰值写 IOPS 接近按需路径的 2 倍，累计写 >1,600 GB/节点 vs 按需 ~700 GB（少 ~57%，全本地 baseline 约 600 GB）。CPU/内存各配置差异可忽略，未展示。
- **8.3 EROFS vs tar**（Fig.11）：同一 workspace+toolkit，tar.gz 每个沙箱解压再写入本地可写层 → 端到端 79 min；EROFS 直接挂载共享层 → 45 min（1.76×）。写流量 5.5×、峰值写吞吐 3.4× 之差。**EROFS 峰值 CPU 更高**，论文解释为更多沙箱更早进入 tool-call 阶段并发执行，而非 setup 开销更大（未给单沙箱 setup CPU 分解）。为排除 LLM 生成的非确定性，评估用预录的确定性工具调用序列替代 LLM 生成。
- **8.4 超卖下的内存**（Fig.12）：四种 Firecracker 配置对比，真实 agentic RL 负载。virtio-pmem+DAX 把每 guest 重复的 page cache 折叠成一份宿主映射，**峰值宿主内存降 40.2%**；DAMON+balloon FPR 单独用峰值基本不变但**时间积分内存消耗降 21.2%**；两者合用总消耗最低。代价：pmem 把瞬时峰值 CPU 从 26.5% 抬到 41.4%（部分源于 DAX 冷访问的同步缺页路径），论文建议 **CPU 紧张时只用 FPR + virtio-blk**。
- **8.5 超卖下的 CPU QoS**（Fig.13）：延迟敏感负载用棋类应用。50% BE 负载下，无保护时每步延迟 +45.2%；仅 SCHED_IDLE 最多改善 3.4%（LS 线程仍与 SMT 兄弟上的 BE 竞争）；加 core scheduling 后低负载下接近无共置 baseline，50% 负载下膨胀限制在 17.3%。残余退化归因于高频 turbo 频率下降、内存带宽与 LLC 竞争（core scheduling 管不了），论文判断"已可忍受"，因此**未做内存带宽隔离**。

> 精炼：四项机制各自都有一个干净的 2×2 或三档对照，结论方向一致（按需/分层/去重/隔离都有效）。但所有对照都是"自建 baseline"，且只在 10 节点、单次 8,192 burst 上测，没有一个数字来自生产规模。

---

## 9. 相关工作（§9）

- **Serverless**（SAND、REAP、TrEnv、RunD）：优化冷启动与资源共享，但面向短生命周期、无状态、高 fanout、镜像已在本地的场景；agentic 训练是长驻、有状态、低 fanout、镜像超出单节点存储。
- **LLM 代码执行平台**：推理侧（OpenAI Code Interpreter、E2B、Kimi-K2.5 Agent Swarm）与训练侧（MiMo-V2-Flash、ComputerRL）多数只提到执行环境而不展开；DSec 的差异是把环境组合、资源超卖、镜像服务、抢占安全恢复放进同一平台。
- **镜像格式与分发**（DADI、CoFS、FaaSNet、EROFS）：DSec 复用这些技术，但直接从 3FS 服务容器与 microVM 镜像，不引入独立 registry + P2P 分发层。
- **轻量隔离**（Firecracker、Kata、library OS、Wasm、unikernel、nested kernel/virtualization）：DSec 不提出新的隔离机制，而是把多种后端放在一个平台后面让调用方选。
- **RL 训练基础设施**（Slime、veRL、OpenRLHF、Seer）：聚焦 GPU 调度、通信与样本吞吐，**把执行环境当黑盒**；DSec 在互补的基础设施层。

> 精炼：相关工作的定位很诚实——不宣称新原语，宣称"平台整合 + 生产数据 + 与 trainer 的协同"，这也正是它难以与现有系统做 head-to-head 对比的原因。

---

## 10. 结论（§10）

统一接口暴露多后端；可组合 EROFS 层避免重复重建与解包；互补的内存共享 + 回收支撑高密度；QoS-aware CPU 调度在超卖下保住延迟敏感任务；3FS 按需加载降低分发开销；与 RL 框架集成做抢占安全恢复与任务级网络策略，构成 agentic 负载的可扩展执行底座。

---

## 深度分析（我的判断，非原文）

**① 机制层的真实贡献是"约束推导"，不是组件发明**——全文最重要的是把两条生产事实（3FS 大块顺序强/小块随机弱；沙箱只访问镜像 4.2%–13.3% 的数据）直接推成数据面三条规则（写本地/读按需批量/元数据本地），再用现成内核原语（overlayfs+EROFS、virtio-pmem、DAMON+balloon、SCHED_IDLE+core sched）落地；代码改动小到 dockerd 30 行。价值在生产数据的形状与组合方式，复现门槛不在算法而在集群与镜像语料。【我的判断】

**② 最该打折扣的是评估覆盖**：全部实验在 10 节点、单次 8,192 容器 burst 的专用集群上，基线全是自建（Docker cold/cached、tar.gz），没有任何与 Nydus/DADI/FaaSNet/Kata/gVisor 或商用沙箱的对比；而论文最独特的部分——与 trainer 解耦的 rollout、pause/resume 回收资源、agent 造环境——被作者自己写在"不在评估范围内"（§8 开头），只有机制描述零指标。【论文明确陈述 + 我的判断】

**③ 最该追问的失效点是尾部与安全**：3,200 容器/800 microVM 密度下的 `memory.reclaim`/swap 抖动、恢复时 `MADV_WILLNEED` 预取风暴、pause 后 resume 的 p99，全部没有数据；安全侧论文自曝 agent 用 `XFS_IOC_SWAPEXT` 打崩文件系统、读 `/proc/kpagecgroup` 打崩内核，说明 AppArmor+eBPF 只挡"找答案"不挡"搞破坏"，而"容器跑在 QEMU/libvirt VM 里"这层额外边界对密度的代价也未量化。【我的判断】

---

## 数字口径与存疑（需向作者核对）

| # | 现象 | 出处 |
|---|---|---|
| 1 | 单节点密度的两套数字混用：Fig.6 采样峰值为 1,048 容器 / 524 microVM，正文却说生产稳定运行点是 ≥3,200 容器 / 800 microVM；两者时间窗与口径不同（一天采样 vs 跨生产观测），易被误读为矛盾 | §4.3、Fig.6 |
| 2 | 超卖比从未直接给出。只有"90% 沙箱平均用 ≤5% 请求 CPU"与"3,200 容器/节点"，但缺少每沙箱请求规格（如几核几 GB）与 node 规格，读者无法自行算出 CPU/内存超卖倍数 | §4.3、§2.4 |
| 3 | 摘要与正文承诺"降低环境搭建开销"，但只有端到端 79→45 min，没有 setup 阶段绝对耗时、也没有单沙箱启动延迟分布（p50/p99） | 摘要、§8.3 |
| 4 | §8.3 EROFS 峰值 CPU 更高，解释为"更多沙箱更早进入 tool-call 阶段"，但未给 setup 阶段 CPU 分解来支撑，属"开了优化指标反而变差"的解释性说明 | §8.3、Fig.11 |
| 5 | §8.4 pmem 使瞬时峰值 CPU 26.5%→41.4%，论文建议 CPU 紧张时退回 FPR-only，说明"三机制全开"并非最优配置，但正文仍以"combining both produces the lowest overall memory"作为结论口径 | §8.4 |
| 6 | §5.2 引用"memory 降 21.2% 无显著 CPU 开销"，与 §8.4 的"时间积分内存"口径对应，但摘要式表述易被读成峰值下降 | §5.2、§8.4 |
| 7 | 生产数字（3M/天、380K 并发、5,000 创建/秒）为自报部署数据，无独立复现；论文未说明峰值 380K 时容器/microVM/FnCall 的构成 | 摘要、§2.4 |

---
name: acadamic-paper-research
description: "学术论文综合分析：目录规范、元数据提取（会议/作者/课题组）、逐段中译+精炼笔记、深度分析（优缺/可复现性）。适用于会议论文全流程分析。"
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
triggers:
  - "analyze this paper"
  - "帮我分析(这篇|一下|一篇)论文"
  - "paper analysis / paper review"
  - "帮我翻译(这篇|一下|一段)论文"
  - "逐段翻译"
  - "做精炼笔记"
  - "记录到(笔记|running_notes)"
  - "翻译成中文"
  - "帮我(精读|逐章)分析(这篇|一下)论文"
  - user asks to analyze or translate a conference paper (arXiv, USENIX, ACM, IEEE, etc.)
metadata:
  hermes:
    tags: [Research, Papers, Chinese, Translation, Note-Taking, Analysis]
---

# 学术论文综合分析工作流

面向学术论文的全流程分析：从目录搭建、元数据挖掘、逐段中译+精炼笔记，到结构化深度分析。

---

## Phase 0：目录规范

所有论文分析放在 `~/Academics/`，每篇论文一个子文件夹：

```
~/Academics/
└── <paper-short-name>/
    ├── <paper-short-name>.pdf   ← 论文原文
    ├── running_notes.md          ← 精炼笔记（翻译+要点，主产出）
    ├── summary.md                ← 结构化总结（问题/方法/结果）
    ├── critique.md               ← 优缺点与开放问题
    └── notes.md                  ← 自由观察记录
```

**关键坑**：PDF 必须放子文件夹内，不能直接放 `~/Academics/` 根目录。

---

## Phase 1：PDF 文本提取

### 方法一：pdftotext（两栏论文推荐）

```bash
# 两栏 PDF 用两次提取交叉验证
pdftotext -layout paper.pdf paper_fulltext.txt     # 保留栏位，grep 定位用
pdftotext -f N -l M paper.pdf /tmp/page.txt        # 逐页提取，阅读顺序更准确
```

**关键坑**：`-layout` 模式下两栏 PDF 跨页处可能截断句子（左右栏交错导致文本丢失）。遇到断句立即用无 `-layout` 逐页提取比对恢复。

### 方法二：PyPDF2（通用 Python 方案）

```bash
# 提取前 2 页（元数据阶段）
python3 -c "
from PyPDF2 import PdfReader
r = PdfReader('/path/to/paper.pdf')
for i in range(min(2, len(r.pages))):
    print(f'--- Page {i+1} ---')
    print(r.pages[i].extract_text())
"

# 提取全部页（深度分析阶段）
python3 -c "
from PyPDF2 import PdfReader
r = PdfReader('/path/to/paper.pdf')
for i in range(len(r.pages)):
    print(f'--- Page {i+1} ---')
    print(r.pages[i].extract_text())
"
```

**安装**：`pip install PyPDF2 --break-system-packages -q`

**重要**：PyPDF2 提取必须用 `terminal`，不能用 `execute_code`（沙箱 Python 环境不同）。

---

## Phase 2：元数据提取

从论文首页 + proceedings 页面提取基本信息。

### 2.1 必提字段

- 论文完整标题
- 会议/期刊名称 + 年份（如 NSDI'26、SIGCOMM'24）
- 全部作者 + 合作单位（简写：学术界通讯作者 + 工业界企业名，如 "Kai Zhang（张凯），复旦大学 + 腾讯"）
- 通讯作者 → 课题组：通讯作者通常是学术导师/教授。中国企业-高校合作论文中，高校作者通常为指导老师（如 "Kai Zhang（张凯），复旦大学"）
- 摘要概述（100-150 字中文概括）

### 2.2 四要素提取

从 Introduction 中浓缩，各 ≤20 字：

1. 研究背景
2. 要解决的问题
3. 现有方案不足
4. 本文解决思路

### 2.3 信息源

| 信息源 | 方法 |
|--------|------|
| 论文首页 | pdftotext page 1 或 PyPDF2 提取 |
| DBLP | `curl -s "https://dblp.org/search/publ/api?q=TITLE&format=json"` |
| USENIX proceedings | `curl -sL "https://www.usenix.org/conference/<conf>/presentation/<slug>" \| grep 'citation_'` |
| 通讯作者课题组 | 大学主页 (`cs.<univ>.edu.cn`) → Google Scholar → DBLP（按序尝试） |
| 致谢部分（Acknowledgments） | PyPDF2 全页搜索 `acknowledg` 关键词（注意：部分 USENIX 论文无致谢段，不假设存在） |

### 2.4 输出格式

```
## 论文基本信息分析

### 会议信息
- **会议**: ABBREV'YY（如 NSDI'26、SIGCOMM'24）
- **时间/地点**: ...

### 论文标题
**Full Title**

### 作者与单位
| 作者 | 单位 |
|------|------|
| ...  | ...  |

**课题组**: <通讯作者> 课题组 @ <机构>

### 论文摘要概述
<paraphrase>
```

---

## Phase 3：逐章翻译 + 精炼笔记

核心原则：翻译 → 用户 review → 精炼 → 记录。`running_notes.md` 由用户控制，仅按指令写入。

### 3.1 逐章翻译

- 每章切分成段落展示，方便用户逐段 review
- 翻译忠实原文，保留技术术语英文（如 ECMP、VXLAN-GPE）
- 等用户确认翻译无误后再进入下一步

### 3.2 精炼到笔记

- 翻译确认后 → 用户要求"记录到笔记" → 精炼为 100-300 字摘要
- 子章节用 `###` 悬挂在对应章下面
- 辅助文件：`analysis_notes.md`（可选，tracking 用）

### 3.3 Q&A 同样记录

分析过程中的技术讨论（如 VXLAN 端口机制、RDMA 乱序等）→ 精炼后也记录到笔记对应章节下，字数同受限制。

### 3.4 笔记结构

```
## 论文一页版总结
### 基本信息
- **标题**: ...
- **会议**: ABBREV'YY
- **作者**: 通讯作者（中文名），高校 + 企业
### 一句话标题（格式："论文名：机构提出xx方法解决xx问题"，≤30字）
### 主要观点（3行，≤50字/行）
- 第1行：背景+问题+现有不足（合并为一句话）
- 第2-3行：本文解决方案（1~2行）
- 末行：[洞察] 留白，全部章节分析后补独到思考
### AS-IS（研究背景、问题、现有方案的详细分析）
### TO-BE（解决方案、效果、不足的详细分析 + 高价值研究点）

## 0. 摘要（≤350字中文翻译/总结）

## 1. 引言（§1）
  详细翻译笔记...

## 2. 背景（§2）
  2.1 ...
## 3. 设计（§3）
  3.1 ...
## 4. 实现/评估（§4-5）
```

## Phase 4：深度分析

元数据和翻译完成后，进行结构化深度分析。先询问用户关注的维度，默认覆盖：

- **summary.md**：问题定义、方法/方案、关键结果
- **critique.md**：优势、不足、开放问题、可复现性
- **notes.md**：阅读过程中的零散观察

---

## 全部注意事项

| 类别 | 注意点 |
|------|--------|
| PDF 提取 | PyPDF2 必须用 `terminal` 而非 `execute_code` |
| 目录 | PDF 必须放 `~/Academics/<name>/<name>.pdf`，不能放根目录 |
| 笔记写入 | 用户可能自行编辑 → 每次写入前 `read_file` 确认当前状态 |
| 章节重组 | 用户调整结构时快速响应，不抗拒 |
| pdftotext | Windows 上用 git-bash 执行，非 PowerShell |
| 待确认标记 | 保留用户添加的"待确认/待研究"首行标记，不覆盖 |
| 联网搜索 | Subagent 搜索不可靠 → 优先用 `curl` 直接调用已知接口 |
| Google Scholar | 可能限速/CAPTCHA → 备选：大学主页、DBLP |
| 致谢段 | 并非所有论文都有 Acknowledgments，不假设存在 |

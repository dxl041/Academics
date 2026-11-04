---
name: acadamic-paper-research
description: "学术论文综合分析：目录规范、元数据提取（会议/作者/课题组）、逐段中译+精炼笔记、深度分析（优缺/可复现性）。适用于会议论文全流程分析。"
version: 2.3.0
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
  - "统计.*会议.*论文"
  - "提取.*session.*论文"
  - "conference program.*extract"
  - "会议日程.*论文"
  - "scrape conference program"
  - user asks to analyze or translate a conference paper (arXiv, USENIX, ACM, IEEE, etc.)
  - user asks to extract paper lists from a conference program page
  - user asks to do batch paper analysis for a conference session
metadata:
  hermes:
    tags: [Research, Papers, Chinese, Translation, Note-Taking, Analysis]
---

# 学术论文综合分析工作流

面向学术论文的全流程分析：从目录搭建、元数据挖掘、逐段中译+精炼笔记，到结构化深度分析。

---

## Phase 0：目录规范

**主目录 = `~/Academics/`（即 `/home/dxl/Academics/`）**（2026-11 用户删除了 `/mnt/d/ObsidianWorkspace/Academics` 迁移库，重新以 `~/Academics/` 为唯一主目录）。
每篇论文一个子文件夹；PDF 必须放子文件夹内，不能放根目录。

```
/home/dxl/Academics/
└── <paper-short-name>/
    ├── <paper-short-name>.pdf   ← 论文原文
    ├── running_notes.md          ← 精炼笔记（翻译+要点+深度分析，唯一主产出）
    ├── 疑问.md                   ← 待查问题清单（技术疑问，非深度分析）
    ├── *.pptx                    ← 组会汇报等二次产出
    ├── image*.png                ← 被 running_notes 内嵌引用的插图
    └── .pages/                   ← 中间缓存（点开头，Obsidian 不索引、git 不跟踪）
        ├── fulltext.txt          ← 全文（`===== PAGE N =====` 分页标记）
        ├── page_NN.txt           ← 逐页文本
        └── *_翻译*.md            ← 译文等中间产物
```

### 判定口径：顶层 vs `.pages/`

| 归顶层（直接结果，人要读） | 进 `.pages/`（中间缓存，可重建） |
|---|---|
| 论文 PDF、配套规范 PDF | 全文提取 `fulltext.txt`（旧名 `*_fulltext.txt`、`paper_fulltext.txt` 一律改名） |
| `running_notes.md`（翻译+精炼+深度分析） | 逐页文本 `page_NN.txt` |
| `疑问.md`（待查问题清单）、`*.pptx`（汇报） | 译文 `*_翻译*.md`、规范全文 `*_全文.md`、其他抽取产物 |
| `image*.png`（被笔记内嵌引用，见下） |  |

- 目录内有多份文档（论文 + 配套规范）时，`.pages/` 按 PDF 名再分一层：`MRC_SRv6/.pages/MRC_SRv6/{fulltext.txt,page_NN.txt}` 与 `.pages/MRC_Specification/{MRC_Specification_全文.md,MRC_Spec_Sec5_翻译.md,page_NN.txt}`。
- 深度分析**不单独成文**：写入 `running_notes.md` 的 `## 8. 深度分析` 章节，不产出 `critique.md`（用户 2026-11 要求）。
- 阅读导览/`*_指南.md`（如规范的阅读指南）属中间产物，放 `.pages/<doc>/` 下，**不进顶层、也不并入 running_notes**；顶层不出现 `critique.md` / `*_指南.md`。
- 图片留在顶层：`running_notes.md` 用相对路径内嵌（`![alt](image.png)`），移进点开头目录后 Obsidian 不再索引、图会断。
- 移动文件后必须回头改笔记里的旧路径引用（例：`MRC_Spec_阅读指南.md` 里 `MRC_Specification_全文.md` → `.pages/MRC_Specification/MRC_Specification_全文.md`；DynamiQ 笔记头部的"目录"说明行）。

### 批量整理流程（历史目录已执行过一次，2026-11）

1. 备份：`tar czf ~/backups/academics-md-backup-$(date +%Y%m%d-%H%M).tgz --exclude='*.pdf' --exclude='.git' --exclude='.obsidian' ~/Academics`
2. 先 dry-run：`python3 scripts/reorg_paper_dirs.py`（脚本幂等；打印每个 MOVE/GEN，不做任何写操作）
3. 确认无误再 `--apply` 落盘；脚本会：散落的全文/译文收进 `.pages/`、多文档按 PDF 名分子目录、缺失的 `page_NN.txt`（pymupdf 逐页）与 `fulltext.txt`（`===== PAGE N =====` 分页）补齐。
4. 改引用路径（见上）→ 自检 → 保持未提交状态，等用户下令再 `git commit`。
5. 自检口径：`find <论文> -maxdepth 1 -type f` 顶层应只剩 PDF/笔记/图/PPT；`find <论文>/.pages -type f | wc -l` 数量与 PDF 页数吻合；`git status` 只应看到 `*_fulltext.txt` 一类旧文件的删除与笔记修改。

- 主目录 `/home/dxl/Academics/` 在 ext4 上，读写无 drvfs 开销，逐页文本可直接写盘。
- 主目录是 git 仓库（SSH remote: `git@github.com:dxl041/Academics`，branch `main`）。**不要主动 git add/commit/push**——用户明确要求：只有他下令时才提交。写完笔记后把改动留在工作区即可，并在回复里说明"未提交改动 N 个文件"，由用户决定何时提交。
  已配 `.gitignore` 排除 `.pages/`、`.obsidian` 状态、`.dsh-cache/`、系统噪声文件；PDF 与笔记正常入库。
- 本 skill 的仓库副本 `~/Academics/acadamic-paper-research/` 只是快照（为推 GitHub 而存），**Hermes 运行时只加载 `~/.hermes/skills/academics/acadamic-paper-research/`**；改完本文件后用 `rsync -a --delete ~/.hermes/skills/academics/acadamic-paper-research/ ~/Academics/acadamic-paper-research/` 同步快照。

---

## Phase 1：PDF 文本提取

### PDF 下载

USENIX/ACM 会议论文优先从 proceedings 页面提取 PDF 链接：

```bash
# 从 USENIX proceedings 页面提取 PDF URL
curl -sL "https://www.usenix.org/conference/<conf>/presentation/<slug>" \
  | grep -oP 'https://www.usenix.org/system/files/[^"]*\.pdf' | head -3

# 下载（curl 超时时用 wget 回退）
wget -q -O /path/to/paper.pdf "<pdf_url>" -T 60
```

**关键坑**：curl 在代理/跨境网络下可能超时（30s 不够），直接用 `wget -T 60` 更可靠。

### 方法一：pdftotext（两栏论文推荐）

```bash
# 两栏 PDF 用两次提取交叉验证
pdftotext -layout paper.pdf paper_fulltext.txt     # 保留栏位，grep 定位用
pdftotext -f N -l M paper.pdf /tmp/page.txt        # 逐页提取，阅读顺序更准确
```

**关键坑**：`-layout` 模式下两栏 PDF 跨页处可能截断句子（左右栏交错导致文本丢失）。遇到断句立即用无 `-layout` 逐页提取比对恢复。

### 方法二：PyPDF2（通用 Python 方案）

```bash
# 提取前 3 页（元数据阶段）
python3 -c "
from PyPDF2 import PdfReader
r = PdfReader('/path/to/paper.pdf')
for i in range(min(3, len(r.pages))):
    print(f'--- Page {i+1} ---')
    print(r.pages[i].extract_text()[:3000])
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

### 方法三：pymupdf words 表格列还原（无 pdftotext / 无 layout 模式时）

部分环境未装 poppler-utils（无 `pdftotext`），且 pymupdf 部分版本 `get_text('layout')` 不支持（AssertionError）。流式提取会把多列表格压扁错位（如特性矩阵 `# ###` 列归属不明）——用 `page.get_text('words')` 取表头 token 定列锚点 x，再按 (行 y 分组, x) 排序就近归类，详见 `references/protocol-spec-analysis.md`。

### 方法四：pymupdf 逐页文本提取（无 pdftotext 时的首选）

环境未装 poppler-utils（无 `pdftotext`/`pdfinfo`）时，用 pymupdf 逐页抽取并**每页单独落盘**，便于跨页衔接核对与阅读顺序复查（DynamiQ 会话实测有效）：

```bash
python3 << 'EOF'
import fitz
doc = fitz.open('paper.pdf')
print("pages:", doc.page_count)
for i, page in enumerate(doc):
    with open(f'page_{i+1:02d}.txt', 'w') as f:
        f.write(page.get_text('text'))
EOF
# 需要全文时：把各页拼进 fulltext.txt，页间加 "===== PAGE N =====" 标记
```

现成脚本：`scripts/pdf_page_extract.py <paper.pdf> [outdir]`（同样必须用 `terminal` 跑，勿用 execute_code）。

**已知怪癖（DynamiQ 会话实测，pymupdf `get_text('text')`）**：
- 章节编号与标题被拆成两行（`2` / `Background`）→ 影响 §2.4 章节发现，见 2.4 第三级回退
- 块顺序基本即阅读顺序、跨页正文连续，但 **bullet 列表可跨页延续**（第 N 页尾部 2 条 + 第 N+1 页顶部 2 条同属一个列表）→ 翻译跨页章节前先读前一页尾 + 后一页头拼接，勿按页截断理解

> **加速长论文分析**：15+ 页论文可以用 `delegate_task` 并行派发章节给子代理同时阅读。详见 `references/parallel-analysis.md`。

---

## Phase 2：元数据提取

从论文首页 + proceedings 页面提取基本信息。

### 2.1 必提字段

- 论文完整标题
- 会议/期刊名称 + 年份（如 NSDI'26、SIGCOMM'24）。**若为 arXiv 预印本且未标注投稿会议，标注"arXiv 预印本 (arXiv:XXXX.XXXXX)，暂未标注投稿会议"**
- 全部作者 + 合作单位（简写：学术界通讯作者 + 工业界企业名，如 "Kai Zhang（张凯），复旦大学 + 腾讯"）。多公司工业论文（≥3家公司）按公司分组列出作者，每家公司标注通讯作者
- 通讯作者 → 课题组：通讯作者通常是学术导师/教授。中国企业-高校合作论文中，高校作者通常为指导老师（如 "Kai Zhang（张凯），复旦大学"）。纯工业界论文无需标注课题组，若有知名学术研究者以企业身份参与，可特别标注（如 "Mark Handley (UCL)，以 OpenAI 身份参与"）
- 摘要概述（100-150 字中文概括）
- **致谢与资助**：从论文 Acknowledgments 段提取。包含 Shepherd（如有）、资助项目及编号、计算资源提供方、个人致谢、AI 使用声明。PyPDF2 全页搜索 `acknowledg` 定位。并非所有论文都有致谢段（部分 USENIX 论文无），arXiv 预印本无 Shepherd，不假设存在但不跳过检查

### 2.2 四要素提取

从 Abstract + Introduction 浓缩，各 ≤50 字（中文），格式：

1. **研究背景**：该领域大方向，为什么这个问题重要
2. **要解决的问题**：论文核心挑战，聚焦具体技术问题
3. **现有方案不足**：当前方法的 gap，为什么现有方案不够
4. **本文解决思路**：标题+摘要暗示的核心创新点

> 批量会议论文分析模板见 `templates/batch-four-element-analysis.md`

### 2.3 信息源

| 信息源 | 方法 |
|--------|------|
| 论文首页 | pdftotext page 1 或 PyPDF2 提取 |
| USENIX proceedings | **最可靠来源**：`curl -sL "https://www.usenix.org/conference/<conf>/presentation/<slug>" \| grep 'citation_'` 提取全部作者+机构 |
| DBLP | `curl -s "https://dblp.org/search/publ/api?q=TITLE&format=json"` — 论文元数据可靠，但**作者搜索常返回空结果**；2026-09 起 API 被 Anubis PoW 反爬拦截（返回 "Making sure you're not a bot!" 页），优先 Crossref `query.bibliographic` 标题检索（见 acm-pdf-acquisition.md） |
| OpenAlex | `curl -s "https://api.openalex.org/works?filter=doi:DOI"` — 一站式获取作者单位、arXiv PDF URL (`locations[].pdf_url`)、OA状态。DOI 从 DBLP 搜索结果中取。**先试 OpenAlex 再试 arXiv API**，速度更快且不易触发限速 |
| Crossref API | `curl -s "https://api.crossref.org/works/DOI"` — 作者 ORCID、精确机构名称（含城市）。比 OpenAlex 的作者-机构映射更完整，尤其在工业论文中可区分 Microsoft Redmond vs. 其他 office。**DBLP 拿到 DOI 后立即调用** |
| 通讯作者课题组 | 大学主页 (`cs.<univ>.edu.cn`) → Google Scholar → DBLP（按序尝试） |
| 致谢部分（Acknowledgments） | PyPDF2 全页搜索 `acknowledg` 关键词（注意：部分 USENIX 论文无致谢段，不假设存在） |

### 2.4 章节结构发现

**第 0 步：先看编号体系。** IEEE/ACM 会议模板（SC、INFOCOM、HPCA、部分 TC/ToN）用**罗马数字**做一级标题、大写字母做二级标题（`I. Introduction`、`III. RSS Design`、`A. Subflow Spraying`），阿拉伯数字正则全部失配（会只匹配到图轴刻度、表号等噪声）。这类论文直接跑：

```bash
grep -anE '^(I|II|III|IV|V|VI|VII|VIII|IX|X)+\. [A-Z]|^[A-H]\. [A-Z]' fulltext.txt
```

一条命令即可拿到完整层级（实测 Ordered Chaos/SC'26 一次命中 8 章 + 全部 A–F 小节），无需三级回退。判据：PDF 首页出现 `979-8-xxxxx/xx/$31.00 ©20xx IEEE` 版权行、或作者块为"名字 + 上标 ∗†‡§"的 IEEE 样式。若罗马数字正则只命中 `I.`/`V.` 少数几条，说明标题被拆行 → 改用"纯罗马数字行 + 下一行标题"配对。参考文献条目（`V. Wang, ...`、`D. Goel, ...`）同样会命中，行号落在 References 之后的直接丢弃。

确认非罗马数字体系后，再走下面的阿拉伯数字流程。全文提取后，用 grep 快速定位论文章节：

```bash
grep -anE '^[0-9]+ [A-Z][a-z]' paper_fulltext.txt | head -50
```

如 grep 无结果或结果不完整（PDF 提取文本中章节标题可能跨页、不在行首），用 Python regex 回退：

```bash
python3 -c "
import re
text = open('paper_fulltext.txt').read()
# 匹配 \"数字 大写单词\"，带长度过滤（≥5字符排除短噪声）
candidates = set(re.findall(r'[0-9]+(?:\.[0-9]+)? [A-Z][A-Za-z]{4,}', text))
for c in sorted(candidates, key=lambda x: (int(re.match(r'[0-9]+', x).group()), x)):
    print(c)
"
```

**第三级回退（编号与标题被拆行）**：pymupdf 等流式提取可能把章节标题拆成独立两行（`2` / `Background`，DynamiQ 会话实测），上述单行 regex 全部失配。此时匹配"独立成行的纯数字行 + 下一行以大写开头且长度>4 的标题行"，按页逐行扫描：

```python
for i, line in enumerate(lines):          # lines = 每页文本 split('\n')
    if re.match(r'^\s*\d+(\.\d+)?\s*$', line):
        nxt = lines[i+1].strip() if i+1 < len(lines) else ''
        if re.match(r'^[A-Z]', nxt) and len(nxt) > 4:
            found.append((page_no, line.strip(), nxt))
```

此级噪声远多于主回退（坐标轴刻度 `100.1`、小数 `0.0059`、表号 `Table 3:`、图例数值、表格内数字等），按 (编号, 标题) 去重后仍需逐条人工验证——真章节标题是 {Introduction, Background, Design, Implementation, Evaluation, Related Work, Conclusion, Discussion...} 这类完整名词短语。若主回退已有结果，此级仅作补漏：核对是否有章节标题落在页尾被漏检。

**关键验证步骤**：正则回退会产生噪声候选（日期 "5 May"、数量 "32 KB"、年份 "2015 ACM" 等）。去重排序后，**必须逐一验证**每个候选是否为真正的章节标题：
- 用候选数字（如 "4 "）搜索原文 `grep -an \" 4 [A-Z]\"` 提取周围 2-3 行上下文
- 确认是 "4 Inter-plane Loading" 这样的章节标题还是噪声
- 宁可多花 30 秒验证，不可漏掉一个章节

### 2.5 Phase 2 完成检查清单

以下所有项满足后才能进入 Phase 3。逐项自检，不跳步：

- [ ] 论文标题（完整原文）
- [ ] 会议/期刊 + 年份（ABBREV'YY 格式）。**若为 arXiv 预印本无会议信息，标注 arXiv ID 及状态**
- [ ] 全部作者 + 单位（优先 Crossref API 获取 ORCID + 精确机构名，回退 DBLP + OpenAlex。多公司论文按机构分组列出）
- [ ] 通讯作者 + 课题组（大学主页/Google Scholar/DBLP 确认。arXiv 预印本如为纯工业论文，标注各公司通讯作者即可）
- [ ] Shepherd 信息（搜索 Acknowledgments，arXiv 预印本无 Shepherd，标注"无（预印本）"即可）
- [ ] 致谢与资助（从论文原文 Acknowledgments 段提取；无则标注"本文无致谢段"）
- [ ] 摘要概述（100-150 字中文）
- [ ] 四要素（各 ≤50 字中文）
- [ ] 章节结构发现（grep 定位。如 grep 未匹配到，用 Python regex `re.findall(r'^[0-9]+(?:\.[0-9]+)? [A-Z]', full_text, re.M)` 替代，PDF 提取文本的章节标题不一定在行首）
- [ ] 章节数 > 4 的论文：记录所有章节标题到笔记，便于后续规划

### 2.6 输出格式

**标准会议论文：**
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

### 四要素提取
1. **研究背景**: ...
2. **要解决的问题**: ...
3. **现有方案不足**: ...
4. **本文解决思路**: ...

### 致谢与资助
- **Shepherd**: <name>（如有）
- **资助项目**: ...
- **计算资源**: ...
- **AI使用声明**: ...（如论文声明）
```

**arXiv 预印本（无会议信息）：**
会议信息栏改为：
```
### 论文来源
- **状态**: arXiv 预印本 (arXiv:XXXX.XXXXX)，暂未标注投稿会议
- **日期**: YYYY年M月
```

多公司工业论文（≥3家公司）作者栏按机构分组：
```
### 作者与单位
| 机构 | 核心作者 | 通讯作者 |
|------|---------|---------|
| OpenAI | ... | ... |
| Microsoft | ... | ... |
```
Shepherd 栏改为 `- **Shepherd**: 无（预印本）`

---

## Phase 3：逐章翻译 + 精炼笔记

核心原则：翻译 → 用户 review → 精炼 → 记录。`running_notes.md` 由用户控制，仅按指令写入。

### ⛔ 禁止行为（默认交互模式）

以下行为在默认交互模式下不可执行。**当用户明确要求批处理模式时（见下文 3.0），以用户指示为准。**

- **默认禁止一次性写入全部章节的翻译+精炼到 running_notes.md**。Phase 3 是交互式流程，不是批处理任务。
- **默认禁止未经用户 review 就将翻译精炼写入笔记**。每章必须经过"展示翻译→等用户确认→用户说'记录'→才精炼写入"这个循环。
- **默认禁止跳过逐章交互直接跳到 Phase 4**。

### 3.0 批处理模式（用户主动要求时启用）

当用户明确说 **"直接分析吧"、"一次性分析完"、"直接写完整笔记"** 或类似表述时，跳过逐章交互循环，直接完成全部章节的翻译+精炼+深度分析并一次性写入 running_notes.md。

批处理模式下：
- 仍然执行 Phase 1（文本提取）和 Phase 2（元数据提取），不可跳过
- 元数据（Phase 2 输出）先展示给用户确认，确认后继续
- 之后一次性完成：全部章节翻译精炼 + Phase 4 深度分析 → 直接写入 running_notes.md
- 使用 delegate_task 并行提取多篇文档（如论文+配套白皮书）以加速
- 对长论文（15+页/多文档）优先用 delegate_task 并行派发提取任务，父代理汇总分析
- 笔记结构与交互模式相同（论文一页版总结、摘要、逐章笔记、深度分析），只是不逐章停顿等待
- **长论文落地写法**：不要试图用一次 `write_file` 写完 600+ 行（易截断/超时）。按「总结+摘要+§1 / §2-§4 / §5-§8 / 深度分析」切成 4 个 `/tmp` 分片，再 `cat p1 p2 p3 p4 > running_notes.md`，最后跑一致性校验。完整配方与坑见 `references/batch-mode-long-paper.md`

**判断标准**: 用户说"直接分析"、"一次性"、"不用逐章" → 批处理模式。用户说"帮我分析这篇论文"无额外指示 → 默认交互模式。

### 3.1 逐章翻译（必须交互，不能批处理）

- **翻译粒度**：默认以整章为单位一次性展示翻译（用户偏好全章翻译，不必逐段拆开）。用户说"直接翻译introduction"时即按整章输出。不要逐段展示后再等确认，除非用户明确要求逐段。
- **翻译格式**：默认纯中文翻译。用户说"中英文对照（着）"时，使用交替对照格式：先一段原文（EN: 开头），接一段译文（CN: 开头），段落间空行分隔。子节标题保留英文，正文 EN/CN 交替。**若用户画像/记忆中已记录"偏好中英对照"**：不要默认纯中文开译——在 Phase 2 元数据确认环节顺带问清翻译格式（与元数据确认合并为一次 clarify 即可，DynamiQ 会话验证有效），用户选定后整章照此执行。**注意**：一旦用户在本会话提出中英对照要求，后续所有章节默认沿用该格式，无需再次询问（MRC_SRv6 会话中用户对 §2 起每章都要求"中英文对照着"）。
- 翻译忠实原文，保留技术术语英文（如 ECMP、VXLAN-GPE）
- 等用户确认翻译无误后再进入下一章
- **确认信号**：用户说"继续"、"继续翻译"、"下一章"即表示当前章确认通过。无需显式追问"有需要调整的吗"——直接等用户指令即可。
- **Q&A 穿插**：翻译过程中用户可能插入技术问题（如"怎么检测故障的"）。回答后自然回到翻译流程，不重新开始该章。

### 3.2 精炼到笔记

- 翻译确认后 → 用户要求"记录到笔记" → 精炼为 100-300 字摘要
- 子章节用 `###` 悬挂在对应章下面
- 辅助文件：`analysis_notes.md`（可选，tracking 用）

### 3.3 Q&A 同样记录

分析过程中的技术讨论（如 VXLAN 端口机制、RDMA 乱序等）→ 精炼后也记录到笔记对应章节下，字数同受限制。

### 3.4 笔记结构

```
## 0. 论文概述
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

## Phase 4：深度分析

元数据和翻译完成后，进行结构化深度分析。先询问用户关注的维度，默认覆盖：

- **写进 `running_notes.md` 的深度分析章节**（如 `## 8. 深度分析`，下设 8.1 核心优势 / 8.2 不足与局限 / 8.3 开放问题 / 8.4 可复现性 / 8.5 定位与影响力 / 8.6 独到观察），**不再单独产出 `critique.md`**——一篇论文一个笔记文件，批评内容作为章节附在翻译笔记之后。

**写作硬规则（本用户明确要求）**：
- 每条技术判断必须可归类：论文原话/图表可读出的标【论文明确陈述】；自己的机制推理、跨段推断标【推论/我的判断】。**绝不能把推断写成事实**（曾因 PSN→EV 映射表述被纠正）。
- 引用细节注明出处（§章节号 / 图 N / 表 N / 规范条款号）。
- **核对论文自报数字与图表读数**：把摘要/正文的 "up to N×"、"X% speedup" 与图中可读数对一遍，不一致的列进「数字口径问题（需向作者核对）」，不要替论文圆场。同类还有"开某优化后指标反而变差"却没解释的情况，单独立条。
- 不足要分层写：丢包/流量模型是否理想化、硬件验证与主张是否匹配、关键对照是否缺失（同实验室/同厂最相关工作有没有定量比）、隐含契约与失效模式、理论支撑。比笼统说"评估不够充分"有用得多。

> 系统/网络类论文的批评框架（数字溯源、2×2 消融读法、隐含契约、评估现实性四问、可复现性表模板、9.x 输出结构）见 `references/systems-paper-critique.md`——写 critique 前先过一遍该清单，尤其是"headline 数字 vs 图中读数"这一步，最容易发现真实缺口。

---

## 全部注意事项

| 类别 | 注意点 |
|------|--------|
| PDF 提取 | PyPDF2 必须用 `terminal` 而非 `execute_code` |
| PDF 下载 | curl 30s 超时不够 → 用 `wget -T 60` 回退 |
| 目录 | PDF 必须放 `<name>/<name>.pdf`（主目录 `/home/dxl/Academics/`），不能放根目录；逐页文本/译文进 `.pages/` |
| 笔记写入 | 用户可能自行编辑 → 每次写入前 `read_file` 确认当前状态 |
| 长笔记分块拼装 | 批处理模式一次产出 600+ 行双语笔记时，分块写 `/tmp/<paper>_p1.md … pN.md` 再 `cat p1 p2 … > running_notes.md`，避免单次 write_file 过大或中途失败丢全稿。拼装后必须检查每个 `---` 前一行为空：`正文\n---` 会被 Markdown 解析成 setext 二级标题，把上一段变成标题。可用 python 逐行补空行并复查计数为 0 |
| 章节发现（IEEE 风格） | SC/INFOCOM/HPCA/部分 ToN 等 IEEE 模板用罗马数字一级标题 + 大写字母二级标题，`^[0-9]+ [A-Z]` 全部失配（只会命中图轴刻度、表号噪声）。先跑 `^(I\|II\|III\|IV\|V\|VI\|VII\|VIII)\. [A-Z]` 和 `^[A-H]\. [A-Z]`，一条命令即得完整层级（见 §2.4 第 0 步） |
| 章节重组 | 用户调整结构时快速响应，不抗拒 |
| pdftotext | Windows 上用 git-bash 执行，非 PowerShell |
| 待确认标记 | 保留用户添加的"待确认/待研究"首行标记，不覆盖 |
| 联网搜索 | Subagent 搜索不可靠 → 优先用 `curl` 直接调用已知接口 |
| DBLP 作者搜索 | DBLP 按作者名搜索常返回空结果，作者信息优先从 proceedings 页面 `citation_author` 提取 |
| Google Scholar | 可能限速/CAPTCHA → 备选：大学主页、DBLP |
| 致谢段 | 并非所有论文都有 Acknowledgments，不假设存在 |
| 会议年记法 | 使用 ABBREV'YY 格式：NSDI'26、SIGCOMM'24（无空格，单引号） |
| 短语交互 | Phase 3 默认为交互式流程。**用户明确说"直接分析"/"一次性"时启用批处理模式**（见 3.0），跳过逐章交互，一次性生成完整笔记。批处理模式下仍须先展示元数据等用户确认后再继续。 |
| 工作流纠偏 | 当用户指出某 Phase 未正确执行时，**仅修复被指出的 Phase**，不要推倒重来或 nuke 已有产出。用户说"把 Phase 2 补充完善"→ 只补 Phase 2；说"按照 skill 重新分析"→ 才从头重做。用户主动说"继续翻译第 X 章"即认可已完成的章节，不要回头重新翻译。 |
| 刚结束会议 | 会议结束≤2周内，arxiv可检索论文≤15%。先用标题做四要素分析，等论文公开后再补充原文。告知用户实际可用性，不要反复尝试不同搜索引擎。 |
| ACM 页面 | ACM DL 页面为 JS 渲染且 PDF 受 Cloudflare 403 保护（pdf/fullHtml/epdf 全拦）。元数据走 Crossref/OpenAlex，PDF 走作者主页猎取（见 `references/acm-pdf-acquisition.md`）。 |
| arXiv 预印本 | 无会议信息、无 Shepherd。按 arXiv API (`export.arxiv.org/api/query?id_list=`) 获取元数据，arXiv HTML 页面的 `citation_*` meta 标签也可提取作者。标注"arXiv 预印本 (ID)，暂未标注投稿会议"。 |
| 章节发现 | grep `^[0-9]+ [A-Z][a-z]` 对 PDF 提取文本可能失败（章节标题不在行首）。回退用 Python `re.findall(r'[0-9]+(?:\\.[0-9]+)? [A-Z][A-Za-z]', full)` 配合长度过滤。**关键**：正则回退会匹配大量噪声（日期如 "5 May"、数字单位如 "32 KB"、引用如 "2015 ACM"）。必须将候选集去重排序后逐一人工验证——用候选数字去原文中提取周围几行上下文，确认确实是章节标题而非噪声。绝不能因为候选列表含噪声就直接判定某章节不存在。**特别注意页边界**：章节标题可能在页尾（end of page N）而不在页首，阅读原文时必须扫描页面尾部。**章节编号跳号（如 §3 直接到 §5）不代表缺章**——很可能是漏检（案例：MRC 论文 §4 Inter-plane Loading 被漏过，用户指出后才找到），发现跳号时逐页核对。 |
| 标题拆行/标题行丢失 | 标题可能被拆成相邻两行（数字 "3.7" 单独一行、标题 "Performance under EEVDF" 在下一行）→ 单行正则漏检；PyPDF2 可能整体丢弃个别标题行（案例：HostStackLatency 的 §3.7/§4 标题在 PyPDF2 文本中完全缺失，pymupdf `get_text('text')` 重建后恢复）。排障顺序：① 搜纯数字行 `^\d+(\.\d+)?$` 并配对下一行文本 ② 结构仍有缺口时用另一提取器重建全文再跑检测 ③ 仍缺才逐页核对原文。pymupdf 新版 `doc.pages` 是方法不是属性，遍历页用 `doc.page_count` + `doc[i]`（直接 `len(doc.pages)` 报 TypeError）。 |
| grep 与 PDF 文本 | PyPDF2 提取的全文含控制字符，`grep -n` 会报 `binary file matches` 并停止搜索。始终用 `grep -an`（`-a` 强制文本模式）搜索 PDF 提取文本。 |
| 多公司工业论文 | ≥3家公司的联合论文，作者按机构分组列表，各公司标注通讯作者。"课题组"栏改为"纯工业论文，无学术课题组"。
| 配套规范文档 | 论文引用配套规范文档（如 OCP Specification、IETF RFC）且论文对某些技术机制（如 EV-SRv6 映射、SACK 格式）描述不够详细时，提取规范文档对应章节辅助解释。规范 PDF 通常在论文同级目录，用 PyPDF2 读取其目录/关键章节即可。 | |
| 独立规范文档 | 用户给的分析对象本身就是工业协议规范（如 ByteDance veRoCE spec、OCP MRC spec）而非学术论文：无会议/摘要/致谢/Shepherd，元数据改为版本+Revision History+许可+联系作者；规范页脚页码与 PDF 页码有固定偏移（先算偏移再规划章节提取）；联网无法核实配套论文时直接向用户确认范围，不反复重试；大章（>10 页）按子节分批展示但仍按一章确认/记录。详见 `references/protocol-spec-analysis.md` | |

> **参考案例**: `references/industrial-paper-example.md` — 高作者数工业论文分析示例
> **系统论文批评框架**: `references/systems-paper-critique.md` — Phase 4 的检查清单（数字溯源、消融读法、隐含契约、可复现性表、9.x 结构）
> **多公司联合论文**: `references/multi-company-consortium-paper.md` — 5方联合大型工业论文分析案例（OpenAI+Microsoft+AMD+Broadcom+Nvidia MRC论文）
> **MRC 协议问答**: `references/mrc-protocol-qa.md` — EV→SRv6 映射、丢包识别、SACK/NACK 机制问答知识库（MRC_SRv6 会话沉淀，含规范查证要点）
> **会议日程提取**: `references/conference-program-extraction.md` — 从会议网页抓取所有 session 论文列表
> **arxiv 论文搜索**: `references/arxiv-paper-search.md` — arxiv API 搜索+WSL代理配置+限速处理
> **批量四要素分析**: `templates/batch-four-element-analysis.md` — 会议论文批量标题级分析模板
> **批处理长论文**: `references/batch-mode-long-paper.md` — 一次成稿配方：分片写入→合并→EN/CN 段数校验→`---` 邻接检查；含图内数字污染、页边界拼接等坑
> **Crossref 元数据提取**: `references/crossref-api.md` — ACM/EuroSys 论文的 Crossref API 使用（ORCID+精确机构，替代不可抓取的 ACM DL 页面）
> **ACM PDF 获取（绕 403）**: `references/acm-pdf-acquisition.md` — dl.acm.org Cloudflare 拦截时的作者主页猎取流程（OpenAI 找 DOI → 实验室 people 页 → 合作教授主页；注意论文可能以项目代号列出，如 SID）
> **工业协议规范分析**: `references/protocol-spec-analysis.md` — 分析对象为协议规范（非论文）时的元数据适配、规范页码↔PDF 页码偏移映射、pymupdf words 表格列还原、大章分批展示粒度
> **图表数值提取**: `scripts/extract_figure_curves.py` + `references/figure-data-extraction.md` — 论文数据只画在曲线图里、或需核对图中数值时，用像素分析标定坐标轴并读各序列数值（网格线标定、系列配色分组、图例遮挡处理、已知值反校验）。运行须用 `terminal`（沙箱 Python 无 PIL）。
> **编译用户自己的 .tex 工程**: 见独立 skill `latex-toolchain` — 装 TeX Live、PATH 接线、LaTeX Workshop 配置、latexmk 编译（含子集编译）、重编结果与原 PDF 一致性校验。本 skill 只负责「读论文」，编译投稿源码走那边


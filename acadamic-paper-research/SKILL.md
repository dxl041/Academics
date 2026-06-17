---
name: acadamic-paper-research
description: "论文翻译+精炼笔记协作模式：逐段翻译→用户review→精炼记录到running_notes.md。适用于两栏学术论文的翻译分析和笔记管理。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Papers, Chinese, Translation, Note-Taking]
---

# 论文翻译 + 精炼笔记协作模式

面向中文学术论文分析的协作工作流。核心原则：翻译→用户 review→精炼→记录，running_notes.md 由用户控制。

## 适用场景

- 两栏学术论文的逐章翻译和分析
- 用户希望 review 翻译后再记录笔记
- 笔记需高度精炼（100-300字/节）
- 边读边记录、可随时插入 Q&A 和 ASCII 图

## 工作流

### 1. 文本提取

```bash
# 两栏 PDF 用两次提取交叉验证
pdftotext -layout paper.pdf paper_fulltext.txt     # 保留栏位，grep 定位用
pdftotext -f N -l M paper.pdf /tmp/page.txt        # 逐页提取，阅读顺序更准确
```

**关键坑**：`-layout` 模式下两栏 PDF 跨页处可能截断句子（左右栏交错导致文本丢失）。遇到 "The two-leaf switches" 这种断句，立即用无 `-layout` 逐页提取比对恢复。

### 2. 基本信息提取

翻译之前先提取元信息，记录到 `running_notes.md`：

**必提字段**：
- 论文完整标题
- 会议/期刊名称 + 年份（如 NSDI 2026、SIGCOMM 2024）
- 全部作者 + 合作单位（标注工业界/学术界）
- 指导老师：中国企业-高校合作论文中，高校作者通常为指导老师（如 "Kai Zhang（张凯），复旦大学"）
- 摘要概述（100-150字中文概括）

**四要素提取**（从 Introduction 中浓缩，各 ≤20 字）：
1. 研究背景
2. 要解决的问题
3. 现有方案不足
4. 本文解决思路

**信息源**：
- 论文首页（pdftotext page 1）
- DBLP（非 arXiv 论文首选）：`curl -s "https://dblp.org/search/publ/api?q=TITLE&format=json"`
- 会议 presentation 页面（USENIX/ACM）

### 3. 逐章翻译

- 把每章切分成段落展示，方便用户逐段 review
- 翻译忠实原文，保留技术术语英文（如 ECMP、VXLAN-GPE）
- 等用户确认翻译无误后再做下一步

### 4. 精炼到笔记

- 翻译确认后 → 用户要求"记录到笔记" → 精炼为 100-300 字摘要
- 笔记文件：`running_notes.md`（用户控制，仅按指令添加）
- 辅助文件：`analysis_notes.md`（可选，tracking 用）
- 子章节用 `###` 悬挂在对应章下面

### 5. Q&A 同样记录

分析过程中的技术讨论（如 VXLAN 端口机制、RDMA 乱序等）→ 精炼后也记录到笔记对应章节下，字数同受限制。

### 6. ASCII 图

论文中的架构图（拓扑、协议栈等）→ 画 ASCII 版本放入笔记，标注关键字段。

## 笔记结构示例

```
## 1. 论文标题
## 2. 会议
## 3. 作者
## 4. 摘要概述
  4.1 研究背景（≤20字）
  4.2 要解决的问题
  4.3 现有方案不足
  4.4 本文解决思路
## 5. 背景（§2.1）
  5.1 DCN/VPC 网络背景（含 ASCII 图）
  5.2 通信流程 Q&A
  5.3 故障分类与动机
## 6. 设计（§3）
  6.1 确定性路径控制
  6.2 路径控制不足
## 7. 部署经验（§5）
```

## 注意事项

- 笔记中用户可能自行编辑内容 → 每次写入前先 `read_file` 确认当前状态
- 用户调整章节结构时（如"把 6 改为 5.3"）快速响应，不抗拒重组
- `pdftotext` 在 Windows 上用 git-bash 执行，非 PowerShell
- 首行可保留用户添加的"待确认/待研究"标记，不覆盖

# 工业协议规范（Specification）文档分析

适用：用户要求分析的"文献"本身是协议规范 PDF，不是学术论文。案例：ByteDance veRoCE Transport Protocol v2.0.4（44 PDF 页，正文 spec p.1–39）、OCP MRC Specification。规范可能单独出现，也可能与同名学术论文成对（成对时论文流程见 multi-company-consortium-paper.md / mrc-protocol-qa.md）。

## 1. 判定特征（首页/前几页）
- 公司 Logo/名称 + "Specification" + Version x.y.z + 日期
- Revision History 表（版本/日期/作者/描述；看是否 "Initial public version"）
- Legal Disclaimer + 开源许可（veRoCE 为 CC BY-NC-ND 4.0：可复制分发、禁商用/禁改编）
- 联系作者邮箱（如 daihuichen@bytedance.com）——中文名未经核实不要猜写
- 大目录 Contents；正文页脚 "Date: ... Page N" 为规范自身页码（≠ PDF 页序）

## 2. 元数据适配（Phase 2 变体）
无会议/期刊、无 arXiv ID、无摘要、无致谢段/Shepherd/资助，替换为：
- 性质: 工业协议规范（机构名），非学术论文
- 版本 + 发布日期 + 是否首个公开版本（Revision History）
- 许可协议 + "AS IS" 声明
- 联系作者（规范列出的 contact person）
- 配套论文: 目录只有规范 PDF 时，尝试 arXiv/DBLP 验证同名论文（veRoCE 类命名可能对应 SIGCOMM/NSDI 投稿）。直连与代理都不通（curl 返回 000 / 空结果）时放弃，明确告知用户"联网不可用、未核实"，直接问用户手上是否有论文文件——不要反复换源重试。
- 摘要概述/四要素: 规范 §1 Overview 通常有动机+方案叙述（AI 集群规模、无损网络局限、本协议特性清单），可照常提炼四要素。

## 3. 页码偏移映射（必做）
规范页脚页码与 PDF 页序不同（TOC 页码是 spec 页码）。定位正文首页页脚 "Page N"，偏移 = PDF页 - N（veRoCE 案例: PDF 6 = spec p.1 → 偏移 +5；PDF 页码 = spec 页码 + 5）。此后章节 PDF 范围 = TOC spec 页码 + 偏移。先算出最大章跨度（veRoCE §5 跨 spec p.13–31 ≈ 19 个 PDF 页）再规划翻译展示。

## 4. 表格还原：pymupdf words x 聚类
症状: PyPDF2/流式提取把多列表格压扁，符号与列错位（veRoCE §8 特性矩阵出现 "# ###"、"– ––#" 无法判列）。
部分 pymupdf 版本无 get_text('layout')（AssertionError: option not in formats），且环境可能没有 pdftotext。此时用 words API 手工按列锚点重建：

```python
import fitz
doc = fitz.open('spec.pdf')
page = doc[PAGE_IDX_0BASED]              # 目标 PDF 页（0 起始）

# (1) 表头行给出列锚点 x（veRoCE 例: 表头 y≈270）：
words = page.get_text('words')          # (x0,y0,x1,y1,word,...)
hdr = [w for w in words if abs(w[1]-270) < 5]
for w in sorted(hdr, key=lambda w: w[0]):
    print(round(w[0],1), w[4])          # 例: 416.7 P1 / 443.5 P2 / 471.6 P3

# (2) 区域内逐行按 (y 分组, x) 输出，x 就近归属列：
region = [w for w in words if YMIN < w[1] < YMAX and w[0] < XMAX]
region.sort(key=lambda w: (round(w[1]/6), w[0]))   # /6 容忍行内基线抖动
for w in region:
    print(f'y={w[1]:6.1f} x={w[0]:6.1f} {w[4]}')
```

要点：
- 行分组用 round(y/常数)（veRoCE 用 /6 合适），避免同一行 token 因 y 差 1–2pt 被拆开。
- 列锚点取表头 token x；表头可能拆成多个 token（如 "Base" + "(P0)" 两 token 同列）。
- 单元格内容跨两行时（"Write/Write-imm"、"Multi-path transmission"），特征名行无符号、符号在续行——别误判为缺列。
- 符号列距很窄（≈27pt）时直接按最近锚点归类（veRoCE 列: Base≈372 / P1≈420 / P2≈447.5 / P3≈475.8）。
- 结论以坐标重建为准，不要用压扁的流式文本猜列。

## 5. 翻译粒度与展示
- §1 概述 1–2 页：整章一次展示；超长段落按句群拆 P1/P2-1.. 分段 EN/CN 交替，便于 review。
- 大章（>10 页）整章一次输出过长：按子节分批展示（如 5.1–5.3 一组、5.4–5.6 一组），但仍作为"一章"管理——一次确认、一次"记录到笔记"，不要拆成独立章节走多轮交互。
- 术语、opcode 二进制值、字段宽度、位宽原样保留英文/字面值。
- 与论文流程一致：每章展示 → 用户 review → 用户说"记录到笔记"才写 running_notes.md（veRoCE 会话用户明确"逐章翻译后再记录到笔记"）。

# Academics

学术论文分析库。每篇论文一个子目录，结构约定如下（2026-11 统一整理）：

```
<论文简称>/
├── <论文简称>.pdf              # 论文原文
├── running_notes.md            # 唯一主文档：翻译 + 精炼笔记 + 深度分析章节
├── 疑问.md                     # 待查问题清单
├── *.pptx                      # 组会汇报等二次产出
├── image*.png                  # 被 running_notes 内嵌引用的插图
└── .pages/                     # 中间缓存（点开头：Obsidian 不索引、git 不跟踪）
    ├── fulltext.txt            # 全文提取（===== PAGE N ===== 分页标记）
    ├── page_NN.txt             # 逐页提取文本
    └── *_翻译*.md              # 译文等中间产物
```

- 顶层只放**直接结果**（PDF、笔记、图、PPT）；凡能从 PDF 重新生成的文本、译文一律进 `.pages/`。
- 深度分析不单独成文，作为 `## 8. 深度分析` 章节并入 `running_notes.md`；阅读导览/`*_指南.md` 属中间产物，进 `.pages/`，顶层不出现 `critique.md` / `*_指南.md`。
- 一个目录里有多份文档时（如 `MRC_SRv6/` 含论文 + 配套规范），`.pages/` 下按 PDF 名分子目录：
  `.pages/<pdf名>/{fulltext.txt,page_NN.txt,...}`。
- `.pages/` 已写入 `.gitignore`（可重建，避免仓库膨胀）；PDF 与笔记正常入库。

academic-paper-research/ 是学术论文分析 skill 的**仓库快照**（仅供推送到 GitHub，Hermes 不从这里加载）；实际生效的 skill 在 `~/.hermes/skills/academics/acadamic-paper-research/`，改动后需 rsync 覆盖此快照再提交。

---

# Agent 使用方法

## hermes
直接hermes
或者 hermes -c <某个session的名称>

## DeepSeek harness
直接在终端运行下述命令，会自动弹开一个浏览器窗口（有记录历史会话）
npm @deepseek-ai/dsh web

或者 npm exec @deepseek-ai/dsh web

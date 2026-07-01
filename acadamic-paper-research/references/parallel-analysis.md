# 并行章节分析：使用 delegate_task 加速论文阅读

当论文较长（15+页）且需要快速产出全篇分析时，可以用 `delegate_task` 将章节分组并行派发给 2-3 个子代理同时阅读总结，大幅缩短等待时间。

## 何时使用

- 论文 ≥ 15 页，全篇分析需要覆盖所有章节
- 用户没有要求逐段交互式翻译（标准 Phase 3 流程）
- 快速产出全篇摘要型分析（非精炼笔记型）

## 何时不用

- 用户明确要求逐段翻译 + 逐段 review
- 短论文（< 10 页），sequential 足够快
- 需要写入 running_notes.md 的精炼笔记（子代理输出需后续加工）

## 分组策略

按章节数均分，通常 2-3 个子代理：

```
子代理 1: §1 Introduction + §2 Background (~40% 篇幅)
子代理 2: §3 Design + §4 Implementation (~30% 篇幅)
子代理 3: §5 Evaluation + §6 Experience/Deployment (~30% 篇幅)
```

对于 9 章节论文（如 Bifrost），可以按 3-3-3 分组。

## 模板

```
delegate_task with tasks=[
  {
    goal: "Extract and summarize Sections N-M from paper",
    context: "Read the full PDF text at /path/to/fulltext.txt (NNNN lines). 
              Read lines AAA-BBB to extract Sections N through M. 
              Return a detailed summary in CHINESE, preserving key numbers 
              and technical terms in English.",
    toolsets: ["file"]
  },
  ...
]
```

## 注意事项

- `context` 中必须提供：文件路径、行号范围、具体章节号、目标语言
- 子代理无 memory，需在 context 中给出全部所需信息
- 子代理输出为中间产物，最终呈现给用户前需要人工整合和格式统一
- 子代理不能写入文件，分析报告需在主会话中完成

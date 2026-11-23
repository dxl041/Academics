# 笔记与译文分家：running_notes.md vs .pages/译文_中英对照.md

来源：2026-11 OrderedChaos 会话。用户原话：「racing_notes.md 里不要存论文中英文的翻译结果，
中英文翻译结果应该放在 .pages 目录下」。

## 规则

| 放哪 | 内容 | 判据 |
|------|------|------|
| `running_notes.md`（顶层，人要读） | 一页版总结、摘要中文概括、每章 3–6 条要点 + `> 精炼` 判断、Phase 4 深度分析 | 是"我的结论"，不是"论文说了什么" |
| `.pages/译文_中英对照.md` | 逐段 `**EN:**` / `**CN:**` 对照，按 §I–§VIII 分节 | 是原文与译文的搬运，可重建/可复查 |
| `.pages/fulltext.txt`、`page_NN.txt` | 原始提取文本 | 机器产物 |

**一句话判据**：这段文字如果只能回答"原文怎么写的" → 进 `.pages`；如果能回答"所以呢 / 有什么问题" → 进笔记。

## 拆分操作

```bash
# 1. dry-run：看配对数、空小节、表格行数变化
python3 ~/.hermes/skills/academics/acadamic-paper-research/scripts/split_bilingual_notes.py ~/Academics/<paper>/
# 2. 落盘（自动备份 running_notes.md.bak-YYYYmmdd-HHMM）
python3 .../split_bilingual_notes.py ~/Academics/<paper>/ --apply
# 3. 验收
grep -c '\*\*EN:\*\*\|\*\*CN:\*\*' ~/Academics/<paper>/running_notes.md   # 必须 0
grep -c '^\*\*EN:\*\*' ~/Academics/<paper>/.pages/译文_中英对照.md          # 等于原配对数
```

## 实测数据（OrderedChaos）

- 拆分前：running_notes.md 656 行，67 组 EN/CN
- 拆分后：running_notes.md 303 行（0 组），.pages/译文_中英对照.md 448 行（67 组）
- 补做：4.1 的 PFLD 变体表（Table I）在拆分中被吞，改为"要点表"重建；删除 6 个变空的小节标题（2.1/3.1/3.2/5.1–5.5）

## 坑

1. **EN 与 CN 之间可能有空行**。写解析时若"读完 EN 就期待下一行是 CN"，会漏配，
   漏配的 CN 段留在笔记里 → 表现为满屏 `**CN:**` 没有 `**EN:**`。脚本已按"跳空行再找 CN"处理。
2. **紧贴 CN 段、无空行的表格/列表/引用会被一起吞掉**。脚本遇到 `|` `>` `- ` `#` 开头即收尾；
   仍要以表格行数对比为准，丢了就按要点表重建（不要为了补表把整段译文搬回笔记）。
3. **空 `###` 标题**：只有译文的小节抽空后只剩标题。脚本现在会自动删掉这类标题并在 dry-run 里列出清单；
   若某个小节仍有价值，就在章级要点里补一句覆盖它，不要让笔记出现一排空标题（用户会直接问"这节怎么是空的"）。
4. **`.pages/` 里只有全文译文入库**：`**/.pages/**` 忽略全部内容，仅 `!**/.pages/**/译文_中英对照.md`（先靠 `!**/.pages/**/` 放行目录）一个例外。所以：全文译文必须叫 `译文_中英对照.md`（各论文同名）；片段/章节级译文用 `译文_中英对照_<范围>.md`，保持前缀统一但仍被忽略。`fulltext.txt`/`page_NN.txt`/分片均忽略。
5. **不是所有论文都有译文**：拆分前先 `grep -l '\*\*EN:\*\*' */running_notes.md` 扫一遍，
   只有命中才动手；OrderedChaos 是唯一一篇，其余 8 篇从未写过对照译文。

## 与批量写作的关系

一次性批处理（batch mode）时，正确顺序是：
先用 `/tmp` 分片拼出「笔记 + 完整译文」的单一草稿 → 跑本脚本拆成两份 →
再写 Phase 4 深度分析进 notes。这样不用在写作阶段就维护两个文件的同步。

## 脚本维护

- **改 `scripts/split_bilingual_notes.py` 前先 `skill_view(file_path='scripts/split_bilingual_notes.py')` 读当前版本**。
  本会话就犯过一次：直接 `write_file` 覆盖，把后来补上的"表格收尾 / 空小节删除 / dry-run 统计"逻辑冲掉，
  只能凭本文件记录的契约重建。覆盖前先读，改完补一条变更说明到本节。
- 脚本行为契约（改动时保持）：dry-run 绝不写文件；`--apply` 先 `cp -p` 备份为 `.bak-<时间戳>`；
  落盘后复核 `pairs == 译文 EN 数 == CN 数 == 非空 CN 段数` 且 notes 里 EN/CN 计数为 0，失败返回非 0。
- 判据不变：**"原文怎么写的" → `.pages`；"所以呢 / 有什么问题" → running_notes.md**。

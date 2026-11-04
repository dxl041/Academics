# 批处理模式：长论文（10+ 页）一次成稿的配方

适用：用户说"直接分析 / 一次性 / 不用逐章"，且论文正文 ≥8 页、需要 EN/CN 逐段对照。
实测样本：Ordered Chaos（SC'26，arXiv 2610.41707，正文 10 页，产出 656 行 / 108 KB，67 组 EN/CN 段）。

---

## 1. 分片写入（避免单次 write_file 过大）

```
/tmp/<slug>_p1.md   # 论文一页版总结 + 摘要 + §1
/tmp/<slug>_p2.md   # §2 动机 + §3 方案一 + §4 方案二
/tmp/<slug>_p3.md   # §5 评估（A-F）+ §6 硬件/实现 + §7 相关工作 + §8 结论
/tmp/<slug>_p4.md   # Phase 4 深度分析（速查表/优势/不足/开放问题/可复现性/零散观察/一页结论）
```

合并：

```bash
cat /tmp/<slug>_p1.md /tmp/<slug>_p2.md /tmp/<slug>_p3.md /tmp/<slug>_p4.md > <vault>/<paper>/running_notes.md
```

每片 20–35 KB 比较稳；再大就容易单次输出被截断，反而要重写。

---

## 2. 对照段格式（与交互模式保持一致）

```
**EN:**
<原文段落，清理 PDF 伪影：σ/μ 等希腊字母还原、断行接回、去掉栏间图注>

**CN:**
<中文译文，保留 ECMP / PSN / EV 这类术语英文>
```

- 一段一 EN 一 CN，**顺序固定**，不要先全 EN 再全 CN（用户明确要求逐段交替）。
- 每章末尾追加一行 `> 精炼：...`（100–300 字），不要混进译文体。
- 图注、坐标轴刻度、算法伪码不进对照段；图注可在正文里用一句中文说明（"图 7a 是 8:1 incast…"）。

---

## 3. 成稿后的三项校验（必做）

```bash
# ① EN/CN 段落数必须相等（漏译/多译立刻暴露）
grep -c '^\*\*EN:\*\*' running_notes.md
grep -c '^\*\*CN:\*\*' running_notes.md

# ② 章节标题齐全
grep -n '^## \|^# Phase' running_notes.md

# ③ 裸 --- 邻接检查（见下节坑）
python3 - << 'EOF'
lines = open('running_notes.md').read().split('\n')
bad = [i+1 for i, l in enumerate(lines) if l.strip() == '---' and i > 0 and lines[i-1].strip() != '']
print('bad --- at', bad) if bad else print('ok')
EOF
```

---

## 4. 坑

- **`---` 直接跟在正文行后面会变成 setext H2**：Markdown 把上一行整段升级成二级标题，笔记结构当场错乱且不易察觉。上面第 ③ 项脚本自动补空行即可（本次 3 处命中）。
- **切分点要落在 `---` 分隔线之后**，否则合并处会出现"半句话 + 分隔线"。
- **PDF 提取文本里的图内数字会污染正文**：小提琴图的数值（`232.2k`、`5.0 5.3`）会成片混入，翻译时必须跳过，只取图注与正文。
- **页边界**：跨页段落要拼前页尾 + 后页头再翻；`-layout` 模式下两栏会在页边界丢句。
- **不要照抄摘要数字**：摘要的"up to N×"通常取自不同实验的峰值，写进一页版总结时注明各自场景（本次 3× / 99% / 35% 分别来自 HPC p99、timeout 计数、ring all-reduce）。
- **批处理 ≠ 不确认元数据**：Phase 2 展示完仍要让用户确认一次（与翻译格式问题合并成一次 clarify），再开始写。

---

## 5. 产出目录

主目录 = `~/Academics/<paper>/`（唯一写入位置；`/mnt/d` 的 Obsidian 库已于 2026-11 删除）：

```
<paper>.pdf
running_notes.md
.pages/            # 逐页提取文本，点开头 → Obsidian 不索引
```

`/mnt/d` 是 drvfs(9p)，小文件写慢：逐页 txt 可以先落 `/tmp` 再整体移入 `.pages/`。

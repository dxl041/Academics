#!/usr/bin/env python3
"""把 running_notes.md 的逐段 EN/CN 译文剥离到 .pages/译文_中英对照.md。

用户定规（2026-11）：`running_notes.md` 只放中文要点 / 精炼 / 深度分析（"我的结论"），
逐段中英对照（"原文怎么写的"）一律进 `<paper>/.pages/译文_中英对照.md`。

用法:
    python3 split_bilingual_notes.py <paper_dir|notes.md>            # dry-run：只打印统计
    python3 split_bilingual_notes.py <paper_dir|notes.md> --apply    # 落盘（先备份 .bak-<时间戳>）

dry-run 会报告：配对数、空 CN 段（有则中止）、将被删除的空 `###` 标题、表格行数变化。

三个真实踩过的坑（都已在实现里处理）:
  1. `**EN:**` 段之后到 `**CN:**` 之间有一个空行——解析必须先跳空行再匹配 CN，
     否则 CN 正文全丢，译文文件只剩空标记（本会话因此把中文删干净，
     靠 `git show <sha>:<path> > /tmp/orig.md` 取回上一版才救回）。
  2. 紧贴 CN 段、中间无空行的表格/列表/引用（`|` `>` `- ` `#` 开头）会被当成 CN 续行吞掉——
     收集 CN 时遇到这些前缀即收尾，并用表格行数前后对比兜底。
  3. 只有译文的小节抽空后只剩 `###` 标题——自动删除，不让笔记出现一排空标题。

验收口径（脚本落盘后自动复核，失败返回非 0）:
    pairs == 译文里 EN 标记数 == CN 标记数 == 非空 CN 段数
    running_notes.md 里 `**EN:**` / `**CN:**` 计数必须为 0
"""
import os
import re
import shutil
import sys
import time

TR_NAME = "译文_中英对照.md"
STOP_PREFIX = ("|", ">", "- ", "* ", "#", "```")   # 紧跟译文但属于别的块的起始行


def parse(lines):
    units, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("**EN:**"):
            i += 1
            en = []
            while i < n and lines[i].strip() and not lines[i].startswith(STOP_PREFIX):
                en.append(lines[i]); i += 1
            while i < n and not lines[i].strip():        # ← 关键：跳过 EN/CN 之间的空行
                i += 1
            cn = []
            if i < n and lines[i].startswith("**CN:**"):
                i += 1
                while i < n and lines[i].strip() and not lines[i].startswith(STOP_PREFIX):
                    cn.append(lines[i]); i += 1
            units.append(("pair", ("\n".join(en), "\n".join(cn))))
            continue
        if line.startswith("### "):
            units.append(("h3", line)); i += 1; continue
        if line.startswith("## "):
            units.append(("h2", line)); i += 1; continue
        blk = []
        while i < n and lines[i].strip():
            blk.append(lines[i]); i += 1
        units.append(("other", "\n".join(blk)))
    return units


def drop_empty_subsections(units):
    """删掉抽走译文后没有任何正文的 ### 标题，返回 (新 units, 被删标题)。"""
    out, dropped, i = [], [], 0
    while i < len(units):
        kind, val = units[i]
        if kind == "h3":
            j, has_body = i + 1, False
            while j < len(units) and units[j][0] not in ("h2", "h3"):
                if units[j][1].strip():
                    has_body = True
                    break
                j += 1
            if has_body:
                out.append(units[i]); i += 1
            else:
                dropped.append(val); i = j
            continue
        out.append(units[i]); i += 1
    return out, dropped


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    target = os.path.abspath(sys.argv[1])
    apply = "--apply" in sys.argv[2:]
    if os.path.isdir(target):
        paper_dir, notes = target, os.path.join(target, "running_notes.md")
    else:
        notes, paper_dir = target, os.path.dirname(target)

    if not os.path.exists(notes):
        print(f"notes not found: {notes}")
        return 1
    raw = open(notes, encoding="utf-8").read()
    units = parse(raw.split("\n"))
    pairs = [v for k, v in units if k == "pair"]
    if not pairs:
        print("没有找到 EN/CN 对照段，无需处理。")
        return 0

    empty = [n for n, (_, cn) in enumerate(pairs) if len(cn.strip()) < 20]
    if empty:
        print(f"❌ {len(empty)} 个 CN 段为空（前 5 个索引 {empty[:5]}）——已中止，未写任何文件。")
        print("   先确认 EN/CN 之间是空行而不是别的标记；必要时 git show <sha>:<path> 取回上一版。")
        return 2

    sec, has = None, {}
    for k, v in units:
        if k == "h2":
            sec = v; has[v] = False
        elif k == "pair" and sec:
            has[sec] = True

    tr, emit = ["# 中英对照译文", "",
                "> 与 `running_notes.md` 配套：要点与深度分析在笔记里，逐段原文/译文在此。", ""], False
    for k, v in units:
        if k == "h2":
            emit = has.get(v, False)
            if emit:
                tr += [v, ""]
        elif not emit:
            continue
        elif k == "h3":
            tr += [v, ""]
        elif k == "pair":
            en, cn = v
            tr += ["**EN:**", en, "", "**CN:**", cn, ""]
    tr_text = "\n".join(tr).rstrip() + "\n"

    notes_units = [u for u in units if u[0] != "pair"]
    notes_units, dropped = drop_empty_subsections(notes_units)
    nt = []
    for k, v in notes_units:
        nt += [v, ""]
    nt_text = re.sub(r"\n{3,}", "\n\n", "\n".join(nt)).strip() + "\n"
    nt_lines = nt_text.split("\n")
    if nt_lines and nt_lines[0].startswith("# "):
        nt_lines[1:1] = ["", f"> 逐段中英对照译文见 `.pages/{TR_NAME}`；本文只保留要点与深度分析。"]
        nt_text = "\n".join(nt_lines)

    tables_before = sum(1 for u in units if u[0] == "other" for l in u[1].split("\n") if l.startswith("|"))
    tables_after = sum(1 for l in nt_text.split("\n") if l.startswith("|"))
    print(f"pairs={len(pairs)}  notes: {len(raw.splitlines())} → {len(nt_text.splitlines())} 行  "
          f"译文: {len(tr_text.splitlines())} 行")
    print(f"表格行数: {tables_before} → {tables_after}" + ("  ⚠️ 有表格被吞，需按要点表重建" if tables_after < tables_before else ""))
    print(f"将删除的空小节: {dropped if dropped else '无'}")

    if not apply:
        print("dry-run：未写文件。加 --apply 落盘。")
        return 0

    pages = os.path.join(paper_dir, ".pages")
    os.makedirs(pages, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(notes, f"{notes}.bak-{stamp}")
    open(os.path.join(pages, TR_NAME), "w", encoding="utf-8").write(tr_text)
    open(notes, "w", encoding="utf-8").write(nt_text)

    back = open(notes, encoding="utf-8").read()
    trb = open(os.path.join(pages, TR_NAME), encoding="utf-8").read()
    ok = (back.count("**EN:**") == 0 and back.count("**CN:**") == 0
          and trb.count("**EN:**") == len(pairs) and trb.count("**CN:**") == len(pairs))
    print(f"写出: {os.path.join(pages, TR_NAME)}")
    print(f"备份: {notes}.bak-{stamp}")
    print("复核:", "OK" if ok else "❌ 计数不一致，请用备份回滚")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())

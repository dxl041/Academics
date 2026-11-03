#!/usr/bin/env python3
"""按 skill Phase 0 约定整理论文目录结构（幂等，默认 dry-run）。

用法:
  python3 reorg_paper_dirs.py            # 预览
  python3 reorg_paper_dirs.py --apply    # 落盘

目标结构:
  <paper>/
    <paper>.pdf            # 论文原文（单个 PDF 时）
    <other>.pdf            # 配套规范/附录 PDF
    running_notes.md       # 分析主文档
    疑问.md / critique.md / *_指南.md / *.pptx / image*.png   # 其他直接结果
    .pages/                # 中间缓存（Obsidian 不索引）
        fulltext.txt       # 全文（===== PAGE N ===== 分页）
        page_NN.txt        # 逐页文本
        *_翻译*.md         # 翻译等中间产物
  多文档目录（论文 + 规范）: .pages/<doc-stem>/{fulltext.txt,page_NN.txt,...}

"""
import shutil
import sys
from pathlib import Path

import fitz

APPLY = "--apply" in sys.argv
ROOTS = [Path("/home/dxl/Academics")]
SKIP = {"acadamic-paper-research", "academic-paper-search", "Comparison",
        ".git", ".obsidian", ".dsh-cache", ".pages"}

log = []


def note(msg):
    log.append(msg)
    print(msg)


def move(src: Path, dst: Path):
    rel = f"{src.parent.name}/{src.name} -> {dst.relative_to(src.parents[1]) if len(dst.parts) > 2 else dst.name}"
    note(f"  MOVE {rel}")
    if APPLY:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))


def page_header(i: int) -> str:
    return f"===== PAGE {i} ====="


def gen_text(pdf: Path, docdir: Path):
    doc = fitz.open(pdf)
    n = doc.page_count
    texts = [doc[i].get_text() for i in range(n)]
    doc.close()

    # 逐页
    made = 0
    for i, t in enumerate(texts, 1):
        p = docdir / f"page_{i:02d}.txt"
        if not p.exists():
            made += 1
            if APPLY:
                docdir.mkdir(parents=True, exist_ok=True)
                p.write_text(t, encoding="utf-8")
    if made:
        note(f"  GEN  {pdf.parent.name}/{'/'.join(docdir.relative_to(pdf.parent).parts)}/page_*.txt ({made})")

    # 全文
    has_ft = any(docdir.glob("fulltext*")) or any("全文" in f.name for f in docdir.glob("*")) if docdir.exists() else False
    if not has_ft:
        body = "\n\n".join(f"{page_header(i)}\n{t.rstrip()}" for i, t in enumerate(texts, 1))
        note(f"  GEN  {pdf.parent.name}/{'/'.join(docdir.relative_to(pdf.parent).parts)}/fulltext.txt ({n} 页)")
        if APPLY:
            docdir.mkdir(parents=True, exist_ok=True)
            (docdir / "fulltext.txt").write_text(body + "\n", encoding="utf-8")


def reorg(root: Path):
    note(f"\n===== {root} =====")
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if d.name in SKIP or d.name.startswith("."):
            continue
        note(f"### {d.name}")
        pages = d / ".pages"

        # 1) 顶层散落的提取/翻译产物 -> .pages/
        for f in sorted(d.iterdir()):
            if not f.is_file():
                continue
            if f.name == "fulltext.txt" or f.name.endswith("_fulltext.txt"):
                move(f, pages / "fulltext.txt")
            elif f.name.startswith("MRC_Specification_全文"):
                move(f, pages / "MRC_Specification" / f.name)
            elif f.name.startswith("MRC_Spec_Sec5_翻译"):
                move(f, pages / "MRC_Specification" / f.name)

        # 2) 按 PDF 补齐逐页/全文文本
        pdfs = sorted(d.glob("*.pdf"))
        for pdf in pdfs:
            docdir = pages if len(pdfs) == 1 else pages / pdf.stem
            gen_text(pdf, docdir)


if __name__ == "__main__":
    note("DRY-RUN（加 --apply 才落盘）" if not APPLY else "APPLY")
    for r in ROOTS:
        reorg(r)

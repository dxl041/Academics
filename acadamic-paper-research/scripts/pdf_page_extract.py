#!/usr/bin/env python3
"""pymupdf 逐页 PDF 文本提取：每页写 page_NN.txt + 汇总 fulltext.txt（带页标记）。

用法:  python3 pdf_page_extract.py <paper.pdf> [outdir]
依赖:  pip install pymupdf   (须用 terminal 运行，勿用 execute_code)
背景:  环境无 poppler-utils (pdftotext/pdfinfo) 时的首选方案
       (acadamic-paper-research skill Phase 1 方法四)。

已知怪癖 (DynamiQ 会话实测):
  1. 章节编号与标题可能被拆成两行 ("2" / "Background")，
     章节发现需用"独立纯数字行 + 下一行大写标题"启发式 (见 SKILL.md §2.4 第三级回退)。
  2. 正文跨页基本连续，但 bullet 列表可跨页延续；
     翻译跨页章节前先核对前一页尾部 + 后一页头部。
"""
import os
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pdf = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else (os.path.dirname(pdf) or ".")
    if not os.path.exists(pdf):
        print(f"PDF not found: {pdf}")
        sys.exit(1)
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("pymupdf not installed. Run: pip install pymupdf")
        sys.exit(1)

    doc = fitz.open(pdf)
    os.makedirs(outdir, exist_ok=True)
    pages = []
    for i, page in enumerate(doc):
        t = page.get_text("text")
        with open(os.path.join(outdir, f"page_{i+1:02d}.txt"), "w") as f:
            f.write(t)
        pages.append(f"===== PAGE {i+1} =====\n{t}")
    with open(os.path.join(outdir, "fulltext.txt"), "w") as f:
        f.write("\n".join(pages))
    print(f"pages: {doc.page_count}")
    print(f"output: {outdir}/page_NN.txt (per page) + {outdir}/fulltext.txt")
    print("tip: search with grep -a; section headers may be split onto two lines")


if __name__ == "__main__":
    main()

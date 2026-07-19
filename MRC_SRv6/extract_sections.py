#!/usr/bin/env python3
"""Extract full text from MRC_SRv6.pdf page by page, then organize by sections."""

import sys
try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "-q"])
    from PyPDF2 import PdfReader

PDF_PATH = "/home/dxl/Academics/MRC_SRv6/MRC_SRv6.pdf"
OUT_PATH = "/home/dxl/Academics/MRC_SRv6/paper_full_text.txt"

reader = PdfReader(PDF_PATH)
num_pages = len(reader.pages)

print(f"Total pages: {num_pages}")

all_lines = []
for i, page in enumerate(reader.pages):
    page_num = i + 1
    text = page.extract_text()
    if text:
        all_lines.append(f"\n{'='*70}")
        all_lines.append(f"PAGE {page_num} (raw page {i})")
        all_lines.append(f"{'='*70}\n")
        all_lines.append(text)
    else:
        all_lines.append(f"\n{'='*70}")
        all_lines.append(f"PAGE {page_num} (raw page {i}) - NO TEXT EXTRACTED")
        all_lines.append(f"{'='*70}\n")

full_text = "\n".join(all_lines)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Wrote {len(full_text)} chars to {OUT_PATH}")

# Also print a summary of what we found on each page
print("\n--- Page summaries ---")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    page_num = i + 1
    if text:
        # Show first 120 chars
        first_line = text.strip().split('\n')[0] if text.strip() else "(empty)"
        print(f"Page {page_num}: {len(text)} chars | starts: {first_line[:100]}")
    else:
        print(f"Page {page_num}: NO TEXT")

# Now break into sections
print("\n\n========== SECTION STRUCTURE ==========")
full_raw = full_text

# Find section boundaries
sections = {
    "1": "Introduction",
    "2": "Multi-plane Topology",
    "3": "Operations",
    "4": "Inter-plane Loading",
    "5": "Experiments",
    "6": "Related Work",
    "7": "Conclusions"
}

for sec_num, sec_name in sections.items():
    print(f"Section {sec_num}: {sec_name}")

# Write a second file with sections organized
SECTION_OUT = "/home/dxl/Academics/MRC_SRv6/paper_sections.txt"

# We'll extract all text and let the parent find sections by markers
# First just dump everything
print(f"\nFull text saved to: {OUT_PATH}")
print(f"Total pages: {num_pages}")
print("Done.")

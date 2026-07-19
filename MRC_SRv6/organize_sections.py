#!/usr/bin/env python3
"""Parse full text into section-organized output with all subsections."""
import re

FULL_PATH = "/home/dxl/Academics/MRC_SRv6/paper_full_text.txt"
OUT_PATH = "/home/dxl/Academics/MRC_SRv6/paper_sections.txt"

with open(FULL_PATH, "r", encoding="utf-8") as f:
    full_text = f.read()

# Exact section headers as they appear in the extracted text
# Order matters - subsections before parent if parent shares prefix
section_headers = [
    # Pre-section marker
    ("Abstract", "ABSTRACT (pre-section)"),
    # §1 Introduction
    ("1 Introduction", "§1 Introduction"),
    # §2 and subsections
    ("2 Multi-plane Topology Co-Design", "§2 Multi-plane Topology Co-Design"),
    ("2.1 MRC Overview", "§2.1 MRC Overview"),
    ("2.2 Static Segment Routing", "§2.2 Static Segment Routing (SRv6)"),
    ("2.3 Mapping EVs to SRv6 Addresses", "§2.3 Mapping EVs to SRv6 Addresses"),
    ("2.4 Choosing Working Paths", "§2.4 Choosing Working Paths"),
    # §3
    ("3 Operations", "§3 Operations"),
    # §4
    ("4 Inter-plane Loading", "§4 Inter-plane Loading"),
    # §5 and subsections
    ("5 Experiments", "§5 Experiments"),
    ("5.1 Training Results", "§5.1 Training Results"),
    ("5.2 Testbed Results", "§5.2 Testbed Results"),
    ("5.2.1 Point-to-Point Communication Performance", "§5.2.1 P2P Communication Performance"),
    ("5.2.2 MRC Response to Link Down and Flap Events", "§5.2.2 Link Down and Flap Events"),
    ("5.2.3 MRC Behavior with T0/T1 Switch Failures", "§5.2.3 T0/T1 Switch Failures"),
    ("5.2.4 Robustness to Path-Level Packet Loss", "§5.2.4 Path-Level Packet Loss"),
    ("5.2.5 Load Balancing Across EVs", "§5.2.5 Load Balancing Across EVs"),
    ("5.2.6 NCCL Collective Execution at Scale", "§5.2.6 NCCL Collective Execution at Scale"),
    ("5.2.7 Comparison with RoCE", "§5.2.7 Comparison with RoCE"),
    ("5.2.8 Collateral Damage", "§5.2.8 Collateral Damage"),
    # §6
    ("6 Related Work", "§6 Related Work"),
    # §7
    ("7 Conclusions", "§7 Conclusions"),
    # References
    ("References", "References"),
]

# Find all matches
all_matches = []
for search_text, label in section_headers:
    # Search for the exact text appearing as a line (possibly with leading spaces/newlines)
    # Try exact match first, then with various line-start patterns
    patterns_to_try = [
        search_text,  # exact match anywhere
    ]
    
    found = False
    for pattern in patterns_to_try:
        idx = full_text.find(pattern)
        if idx >= 0:
            # Make sure it's a proper section header, not buried in text
            # Check the character before - should be newline, space, or start
            before = full_text[max(0, idx-1):idx] if idx > 0 else "\n"
            if before in ("\n", " ", ".", "") or idx == 0:
                all_matches.append((idx, label, search_text))
                found = True
                break
            else:
                # Try case-insensitive with word boundary
                continue
    
    if not found:
        print(f"WARNING: Could not find '{search_text}'")

# Sort by position
all_matches.sort()

# Remove duplicate positions (same idx)
seen_positions = set()
unique_matches = []
for pos, label, stext in all_matches:
    if pos not in seen_positions:
        seen_positions.add(pos)
        unique_matches.append((pos, label, stext))
all_matches = unique_matches

# Build output
output_lines = []
output_lines.append("=" * 80)
output_lines.append("MRC+SRv6 PAPER - COMPLETE SECTION-BY-SECTION EXTRACTION")
output_lines.append("=" * 80)
output_lines.append("")
output_lines.append(f"Source: MRC_SRv6.pdf (18 pages, {len(full_text)} chars extracted)")
output_lines.append("")

# Show table of contents
output_lines.append("-" * 60)
output_lines.append("  TABLE OF CONTENTS")
output_lines.append("-" * 60)
for pos, label, stext in all_matches:
    # Find page number
    before_section = full_text[:pos]
    page_matches = list(re.finditer(r"PAGE (\d+)", before_section))
    page_num = page_matches[-1].group(1) if page_matches else "?"
    output_lines.append(f"  {label:50s} (page {page_num})")
output_lines.append("")

# Now extract each section
for i, (pos, label, stext) in enumerate(all_matches):
    start_pos = pos
    if i + 1 < len(all_matches):
        end_pos = all_matches[i + 1][0]
    else:
        end_pos = len(full_text)
    
    section_text = full_text[start_pos:end_pos].strip()
    
    # Find the page range for this section
    before_section = full_text[:start_pos]
    page_matches = list(re.finditer(r"PAGE (\d+)", before_section))
    start_page = page_matches[-1].group(1) if page_matches else "?"
    
    before_end = full_text[:end_pos]
    page_matches_end = list(re.finditer(r"PAGE (\d+)", before_end))
    end_page = page_matches_end[-1].group(1) if page_matches_end else "?"
    
    output_lines.append("")
    output_lines.append("#" * 70)
    output_lines.append(f"  {label}")
    output_lines.append(f"  (pages {start_page}–{end_page}, {len(section_text)} chars)")
    output_lines.append("#" * 70)
    output_lines.append("")
    output_lines.append(section_text)

# Also include title/authors/abstract
# Find text before first real section (§1 Introduction)
first_section_pos = all_matches[0][0] if all_matches else 0
pre_text = full_text[:first_section_pos].strip()

output_lines.insert(5, "")
output_lines.insert(6, "#" * 70)
output_lines.insert(7, "  TITLE, AUTHORS, ABSTRACT")
output_lines.insert(8, "#" * 70)
output_lines.insert(9, "")
output_lines.insert(10, pre_text)
output_lines.insert(11, "")

final_output = "\n".join(output_lines)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"Wrote {len(final_output)} chars to {OUT_PATH}")
print(f"\nFound {len(all_matches)} sections/subsections")

# Print summary
for pos, label, stext in all_matches:
    before = full_text[:pos]
    pm = list(re.finditer(r"PAGE (\d+)", before))
    page_num = pm[-1].group(1) if pm else "?"
    snippet = full_text[pos:pos+60].replace('\n', ' | ').strip()
    print(f"  Page {page_num:>3s}: {label:50s} [{snippet}...]")

print("\nDone.")

# Conference Program Extraction

When you need to scrape a conference program page (ISCA, ASPLOS, MICRO, etc.) to extract all paper sessions and their papers.

## Quick Pattern: awk with session-header tracking

Most conference program pages follow a pattern: session headers announce a session, followed by paper-title divs. Use awk to track which session each paper belongs to:

```bash
# Download the page
curl -sL 'https://conf.example.org/program/' -o /tmp/program.html

# Extract session+paper pairs
awk '
/Session [0-9][A-Z]:/ {
    match($0, /Session ([0-9A-Z]+): (.+)$/, arr)
    session = "[" arr[1] "] " arr[2]
    gsub(/\r$/, "", session)
}
/paper-title/ {
    getline
    gsub(/^[ \t]+/, "", $0)
    gsub(/[ \t\r]+$/, "", $0)
    print session "|" $0
}
' /tmp/program.html
```

Then post-process in Python or awk to group by day and count:

```bash
# Find day boundaries
grep -oP '(?<=<h2>)(Monday|Tuesday|Wednesday).*(?=</h2>)' /tmp/program.html

# Count papers per session with sort+uniq
awk ... | cut -d'|' -f1 | sort | uniq -c | sort -rn
```

## Pitfalls

- **execute_code sandbox**: `read_file()` in execute_code returns a different format than the normal tool. Use `terminal()` with shell commands (grep, awk, python3 heredoc) instead of execute_code for parsing.
- **Terminal blocking**: Complex multi-line Python heredocs may get blocked. Prefer awk/sed/grep pipelines for extraction and keep Python for post-processing only.
- **Parallel sessions**: Conference pages often have parallel tracks (2A/2B/2C/2D at same time). The awk session-tracking pattern handles this naturally — each paper-title is associated with the most recent session header.
- **HTML entities**: Paper titles may contain `&amp;`, `&reg;`, `&trade;`, `&aelig;` etc. These render fine in terminal output but may need decoding for file output.

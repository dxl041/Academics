# Arxiv Paper Search with Proxy

When searching for conference papers on arxiv via terminal, use the correct proxy and API settings.

## Quick Search (single paper)

```bash
HTTP_PROXY="http://127.0.0.1:7897" HTTPS_PROXY="http://127.0.0.1:7897" \
  curl -sL "https://export.arxiv.org/api/query?search_query=all:PAPER_TITLE_KEYWORDS&max_results=3"
```

## Pitfalls

- **Always use HTTPS**: arxiv.org redirects HTTP to HTTPS. Using `http://` gives 301 → empty body unless `-L` is used.
- **Proxy: 先直连、再回退**：先直接 `curl -sL "https://export.arxiv.org/api/query?..."` 试一次（实测本机直连 arxiv 正常，需要代理的通常只有 git/github）。若直连超时或被校园网阻断，再套 `HTTP_PROXY/HTTPS_PROXY`（本机代理 127.0.0.1:19828）。
- **Rate limiting (HTTP 429)**: arxiv API rate-limits aggressively. Use ≥0.5s delay between requests. After ~60-70 requests, expect 429 errors. Split large batches or add longer delays.
- **Matching papers**: arxiv's OR-based search is broad. Post-filter by:
  1. Check if `<arxiv:comment>` contains "ISCA 2026" or conference name
  2. Compute Jaccard similarity between search keywords and found title
  3. Accept matches with score > 0.15 or explicit conference tag
- **arxiv ID format**: Extracted from `<id>http://arxiv.org/abs/XXXX.XXXXXvN</id>` — strip version suffix for canonical ID.

## Bulk Search Script Pattern

See `scripts/search_arxiv_papers.py` for a reusable bulk search script that:
- Takes a list of paper titles/keywords
- Queries arxiv API with rate limiting (0.3-1.0s delay)
- Filters by conference tag and keyword similarity
- Saves results as JSON

## Metadata quirks (arXiv API v1)

- **`<arxiv:comment>` 是最省事的会议来源**：作者常直接写 "To appear in the proceedings of the ... (SC 2026)" —— 判 ABBREV'YY 时先读这个字段，比 DBLP/Crossref 检索快且不会错。
- **`<arxiv:affiliation>` 基本为空**：作者单位必须从 PDF 首页作者块提取（IEEE 模板用 ∗†‡§ 上标分组，脚注里另有"已离职/已换单位"说明，元数据表要保留该脚注）。
- **用 python 解析 entry 而不是 grep**：`re.findall(r'<entry>(.*?)</entry>', xml, re.S)` 后逐个取 `id/published/title/summary/arxiv:comment/arxiv:journal_ref`，标题与摘要需 `' '.join(x.split())` 压平换行。
- **标题检索用 `all:%22phrase%22`**：`ti:` 加引号在多词标题上易漏，`all:` + 精确短语一次命中（Ordered Chaos 实测）。

## Important: Recent Conference Availability

For conferences that ended **within the last 2-3 weeks**, expect ≤15% of papers on arxiv. Most authors upload preprints days to weeks after the conference, and ACM/IEEE embargo periods may further delay public availability. When the user asks for deep paper analysis of a very recent conference:

1. **Be transparent upfront**: State the expected availability rate before searching
2. **Offer title-based analysis as fallback**: CS architecture paper titles are highly descriptive — "LUT-based GEMM with Dual-Side Quantization" tells you the approach, target, and technique
3. **Save search state**: Write arxiv results as JSON so the user can re-run searches later when more papers appear
4. **Don't waste time on alternative search engines**: Google Scholar times out behind proxies, Semantic Scholar rate-limits aggressively. arxiv API with proxy is the most reliable single source.

## Important: Subagent Limitation

`delegate_task` subagents with `web` toolset CANNOT effectively search arxiv — they describe what they *would* do but don't actually return data. Always run arxiv searches directly in `terminal()` with curl or a Python script.

# ACM 会议论文 PDF 获取：绕过 dl.acm.org Cloudflare 403

## 症状
- 新发表的 SIGCOMM/ACM 论文（arXiv 常无预印本）需从 ACM DL 下 PDF
- `wget/curl https://dl.acm.org/doi/pdf/10.1145/...` → 403，返回 5-6KB HTML（Cloudflare "Just a moment..."）
- 带浏览器 UA + cookie + 完整 headers 依然 403；`/doi/fullHtml`、`/doi/epdf`、`/doi/abs` 全被拦
- 结论：ACM DL 对脚本抓取全面 Cloudflare 保护，不要反复重试

## 元数据仍然可拿（不依赖 ACM 页面）
```bash
# 1) OpenAlex 标题搜索 → DOI（对新论文最可靠，arXiv 搜不到时首选）
curl -s "https://api.openalex.org/works?search=<标题关键词>&per-page=5"
# 2) Crossref → 完整作者+单位+会议+日期
curl -s "https://api.crossref.org/works/<DOI>"
# 3) OA 检查（注意 gold OA 常只指回 doi.org，无仓库副本）
#    OpenAlex open_access 字段 / Semantic Scholar openAccessPdf / unpaywall
```

## 搜索引擎在 CLI 环境全部不可用
- DuckDuckGo html.duckduckgo.com → 202 反爬页面
- Bing → 200 但结果链接 JS 渲染，正则提取为空
- Google（直连或走代理）→ consent/JS 页面，无 /url?q= 链接
- Sci-Hub 镜像（sci-hub.se/.st/.ru）→ 超时/403
- 不要在这些上面耗时间，直接走作者主页猎取

## 正解：作者主页猎取流程（SIGCOMM'26 Elastic QP 实战路径）
1. **arXiv 作者搜索**（便宜快速）：`search_query=au:Chenxingyu_Zhao` — 确认无预印本
2. **导师主页**：homes.cs.washington.edu/~arvind/ — 论文列表常滞后（新论文未上传）
3. **实验室 people 页是找真实主页路径的可靠索引**：syslab.cs.washington.edu/people/ → 列出 `~cxyzhao/`（自己猜 ~cxzhao/、~chenxzy/ 等全 404）
4. **共同作者（尤其教授）主页常有 PDF**：pages.cs.wisc.edu/~mgliu/papers/ 直接命中
   - 一作主页只链 ACM DL 不挂 PDF 时，查合作教授主页的 papers/ 目录
5. **关键坑：论文可能以项目代号而非标题列出**
   - 本案例：grep "Elastic QP" 无结果；论文以项目代号 **SID**（Software-Interposed Datapath）挂在 `papers/SID-sigcomm26.pdf`
   - 教训：抓取作者主页后，除了论文标题，还要用摘要关键词/项目名/缩写 grep 全文

## 案例二：教授主页 rd-chip 列表直接命中（2026-09，SIGCOMM'26 "Host Network Stack Latency"）
- 流程：DBLP 被 Anubis 拦 → arXiv 标题/作者搜索均无预印本 → **Crossref `query.bibliographic` 标题检索命中 DOI**（`event` 字段含会议名/地点/日期，比 ACM 页还全：SIGCOMM '26, Denver, 2026-08-11）→ 作者主页猎取
- Cornell 教授主页 `www.cs.cornell.edu/~ragarwal/` 的 pubs 列表用 `rd-chip` 小标签逐条列出新论文（如 `Host network stack latency [SIGCOMM'26]`），href 直指 `pubs/understanding-latency.pdf`
- **文件名常是缩短标题，chip 文本带会议标签**：grep 用 "会议缩写+年份"（如 `SIGCOMM'26`）扫 chip 文本比全标题更可靠；主页同区可见前作（`network-stack.pdf` "Host network stack overheads [SIGCOMM'21]"），可确认研究线延续、辅助定位
- 时间线参考：会议结束约 1 个月内（SIGCOMM'26 8/17–21 → 9/8 抓取成功）作者主页即有 camera-ready，arXiv 仍无预印本

## 快速路径总结
```
OpenAlex 标题搜 DOI → Crossref 元数据 → arXiv 作者搜索 → 实验室 people 页
→ 作者/合作教授主页（grep 标题+摘要关键词，留意项目代号）
```

## 已试过的死路（别再试）
- dblp.org search/publ/api → Anubis PoW 反爬页 "Making sure you're not a bot!"（2026-09 观察到，DBLP 全站防护）。替代：Crossref `query.bibliographic=<标题>` 直接命中 DOI
- dl.acm.org 任何路径（pdf/fullHtml/epdf/abs）→ 403 Cloudflare
- sci-hub.se / sci-hub.st / sci-hub.ru → 全部不可用
- Semantic Scholar 搜索 API → 429 限流（按 DOI 查询可用，加 sleep 重试）
- Google/DuckDuckGo/Bing 搜索结果页 → 反爬/JS

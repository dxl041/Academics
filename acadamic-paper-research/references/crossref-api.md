# Crossref API 论文元数据提取

## 适用场景

ACM 出版的论文（EuroSys、SIGCOMM、NSDI 等）——ACM Digital Library 页面为 JS 渲染，`curl` 只能抓取骨架 HTML (~5KB)，无法提取 `citation_*` 元数据。**不要尝试从 ACM DL 页面提取**，改用 Crossref API 或 DBLP。

## 获取完整作者-机构映射（含 ORCID）

```bash
curl -s "https://api.crossref.org/works/DOI" 2>/dev/null | python3 -c "
import json,sys
data=json.load(sys.stdin)
msg=data.get('message',{})
print('Title:', msg.get('title',[''])[0][:100])
print('Publisher:', msg.get('publisher',''))
print('Published:', msg.get('published-print',{}).get('date-parts',[[]])[0])
print()
for a in msg.get('author',[]):
    name = f\"{a.get('given','')} {a.get('family','')}\"
    orcid = a.get('ORCID','')
    affs = []
    for aff in a.get('affiliation',[]):
        affs.append(aff.get('name',''))
    print(f'{name}')
    if affs:
        for af in affs:
            print(f'  - {af}')
    if orcid:
        print(f'  ORCID: {orcid}')
    print()
"
```

## 对比：Crossref vs OpenAlex

| 维度 | Crossref API | OpenAlex |
|------|-------------|----------|
| 作者 ORCID | ✅ 有 | ❌ 无 |
| 机构精确名称 | ✅ 如 "Microsoft, Redmond, USA" | ✅ 但有时缺城市信息 |
| arXiv PDF URL | ❌ 无 | ✅ `locations[].pdf_url` |
| OA 状态 | ❌ | ✅ `open_access.oa_status` |
| 速度 | 快 | 快 |

**推荐顺序**：DBLP（拿 DOI）→ Crossref API（拿 ORCID+机构）→ OpenAlex（拿 arXiv URL）

## DBLP 拿 DOI（作为 Crossref 输入）

```bash
curl -s "https://dblp.org/search/publ/api?q=TITLE_KEYWORDS&format=json" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for h in data.get('result',{}).get('hits',{}).get('hit',[]):
    info=h.get('info',{})
    print('DOI:', info.get('doi',''))
    print('Title:', info.get('title',''))
    print('Venue:', info.get('venue',''))
    print('Year:', info.get('year',''))
"
```

## 已知坑

- ACM DL 页面直接 `curl` → 只返回 ~5KB 骨架 HTML，不要浪费时间 grep `citation_`
- Crossref 对刚发表的论文可能有 24-48 小时延迟，此时回退 DBLP
- OpenAlex 的 `locations[].pdf_url` 字段直接给出 arXiv PDF 链接（如有），比 arXiv API 搜索更可靠

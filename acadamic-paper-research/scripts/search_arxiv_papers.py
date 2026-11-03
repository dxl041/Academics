#!/usr/bin/env python3
"""Search arxiv for conference papers and extract abstracts.
Usage: python3 search_arxiv_papers.py <paper_titles.json> <output.json>

paper_titles.json format:
[
  {"category": "LLM", "session": "1A", "query": "Paper Title Keywords"},
  ...
]

Set env vars HTTP_PROXY and HTTPS_PROXY before running if behind proxy.
"""
import urllib.request, urllib.parse, json, re, time, sys, os

def search_arxiv(query, timeout=15):
    """Search arxiv API. Returns raw XML string or None."""
    encoded = urllib.parse.quote(query[:150])
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded}&max_results=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode()
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None

def extract_best_match(xml_data, target_title):
    """Find best matching entry. Returns dict or None."""
    entries = re.findall(r'<entry>(.*?)</entry>', xml_data, re.DOTALL)
    if not entries:
        return None
    
    target_words = set(w.lower() for w in re.findall(r'\w+', target_title) if len(w) > 2)
    best = None
    best_score = 0
    
    for entry_xml in entries:
        title_m = re.search(r'<title>(.*?)</title>', entry_xml)
        if not title_m:
            continue
        t = title_m.group(1).strip()
        t_words = set(w.lower() for w in re.findall(r'\w+', t) if len(w) > 2)
        
        if not target_words or not t_words:
            continue
        score = len(target_words & t_words) / max(len(target_words | t_words), 1)
        
        # Boost if conference tag present
        is_conf = 'ISCA' in entry_xml or 'MICRO' in entry_xml or 'ASPLOS' in entry_xml
        if is_conf:
            score += 0.3
        
        if score > best_score and score > 0.15:
            best_score = score
            id_m = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry_xml)
            abstract_m = re.search(r'<summary>(.*?)</summary>', entry_xml, re.DOTALL)
            best = {
                "arxiv_id": id_m.group(1).strip() if id_m else "",
                "title": t,
                "abstract": abstract_m.group(1).strip().replace('\n', ' ') if abstract_m else "",
                "score": round(best_score, 3),
            }
    return best

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 search_arxiv_papers.py <input.json> <output.json>")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        papers = json.load(f)
    
    results = []
    for i, p in enumerate(papers):
        print(f"[{i+1}/{len(papers)}] {p.get('category','')}/{p.get('session','')}: {p['query'][:60]}...", flush=True)
        xml_data = search_arxiv(p['query'])
        if xml_data:
            match = extract_best_match(xml_data, p['query'])
            if match:
                match.update({k: p[k] for k in ['category', 'session', 'query'] if k in p})
                results.append(match)
                print(f"  ✓ arxiv:{match['arxiv_id']} (score={match['score']})", flush=True)
            else:
                print(f"  ✗ No match", flush=True)
        time.sleep(0.5)  # Rate limiting
    
    results.sort(key=lambda r: (r.get('category', ''), r.get('session', '')))
    
    with open(sys.argv[2], 'w') as f:
        json.dump({"found": len(results), "total": len(papers), "papers": results}, f, ensure_ascii=False, indent=2)
    
    print(f"\nDone: {len(results)}/{len(papers)} papers found")

if __name__ == "__main__":
    main()

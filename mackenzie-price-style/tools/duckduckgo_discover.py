#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs
import urllib.request, ssl, re, html, csv, hashlib, time
root=Path(__file__).resolve().parents[1]
queries=[
 'MacKenzie Price Alpha School interview podcast article founder',
 'MacKenzie Price Alpha School transcript',
 'MacKenzie Price Alpha School Modern Wisdom 981 transcript',
 'MacKenzie Price Alpha School Hard Fork podcast',
 'MacKenzie Price Alpha School YouTube interview',
 'site:youtube.com MacKenzie Price Alpha School',
 'site:linkedin.com/in MacKenzie Price Alpha School',
 'site:alpha.school MacKenzie Price',
 '"MacKenzie Price" "Alpha School"',
 '"Mackenzie Price" "Alpha School" podcast',
]
ctx=ssl._create_unverified_context()
rows=[]
rawdir=root/'raw'/'search'; rawdir.mkdir(parents=True, exist_ok=True)
for q in queries:
    url='https://html.duckduckgo.com/html/?q='+quote(q)
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req,timeout=25,context=ctx) as r:
            body=r.read().decode('utf-8','ignore')
    except Exception as e:
        print('ERR',q,e); continue
    (rawdir/(re.sub(r'\W+','_',q)[:80]+'.html')).write_text(body)
    for m in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>', body, re.S):
        href=html.unescape(m.group(1))
        title=html.unescape(re.sub('<.*?>','',m.group(2))).strip()
        if href.startswith('//duckduckgo.com/l/?'):
            qs=parse_qs(urlparse('https:'+href).query)
            href=unquote(qs.get('uddg',[''])[0]) or href
        sid=hashlib.sha1(href.encode()).hexdigest()[:10]
        host=urlparse(href).netloc.lower()
        lower=(title+' '+href).lower()
        if 'mackenzie' in lower and ('transcript' in lower or 'podcast' in lower or 'interview' in lower or 'youtube' in lower):
            tier='A-candidate'; attr='spoken-transcript-candidate'; conf='0.75'
        elif 'mackenzie' in lower:
            tier='B'; attr='macKenzie-adjacent'; conf='0.60'
        else:
            tier='C'; attr='search-result-context'; conf='0.30'
        rows.append({'id':sid,'query':q,'title':title,'url':href,'source_host':host,'attribution_type':attr,'confidence':conf,'tier':tier,'status':'discovered'})
    time.sleep(1)
# dedupe
seen=set(); out=[]
for r in rows:
    if r['url'] in seen: continue
    seen.add(r['url']); out.append(r)
fields=['id','query','title','url','source_host','attribution_type','confidence','tier','status']
with (root/'sources'/'web-search-discovered.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
md=['# Web search discovered MacKenzie source candidates\n\n']
for r in out:
    md.append(f"- **{r['title']}** ({r['tier']}, {r['attribution_type']}, {r['confidence']})\n  - {r['url']}\n  - query: `{r['query']}`\n")
(root/'sources'/'web-search-discovered.md').write_text(''.join(md))
print('queries',len(queries),'results',len(out))

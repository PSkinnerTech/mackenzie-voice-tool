#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs
import urllib.request, ssl, re, html, csv, hashlib, time
root=Path(__file__).resolve().parents[1]
queries=[
  '"MacKenzie Price" "Future of Education" podcast transcript',
  '"MacKenzie Price" "Future of Education" YouTube',
  '"MacKenzie Price" "2 Hour Learning" interview transcript',
  '"MacKenzie Price" "Alpha" "transcript" -Modern',
  '"MacKenzie Price" "Hard Fork" transcript',
  '"MacKenzie Price" "Johnathan Bi" transcript',
  '"MacKenzie Price" "Forbes Technology Council"',
  '"MacKenzie Price" "Forbes" "education"',
  '"MacKenzie Price" "Substack"',
  '"MacKenzie Price" "LinkedIn" "Alpha School"',
  '"MacKenzie Price" "The Future of School"',
  '"MacKenzie Price" "live stream" "Alpha"',
  '"MacKenzie Price" "AI learning" interview',
  '"MacKenzie Price" "podcast" "Alpha School" -Modern',
  '"Mackenzie Price" "Alpha School" "YouTube" -Modern',
]
ctx=ssl._create_unverified_context()
rawdir=root/'raw'/'search-expanded'; rawdir.mkdir(parents=True, exist_ok=True)
rows=[]
for q in queries:
    print('QUERY', q)
    url='https://html.duckduckgo.com/html/?q='+quote(q)
    try:
        body=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25,context=ctx).read().decode('utf-8','ignore')
    except Exception as e:
        print('ERR', e); continue
    (rawdir/(re.sub(r'\W+','_',q)[:90]+'.html')).write_text(body)
    for m in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>', body, re.S):
        href=html.unescape(m.group(1)); title=html.unescape(re.sub('<.*?>','',m.group(2))).strip()
        if href.startswith('//duckduckgo.com/l/?'):
            href=unquote(parse_qs(urlparse('https:'+href).query).get('uddg',[''])[0])
        if not href: continue
        host=urlparse(href).netloc.lower()
        lower=(title+' '+href+' '+q).lower()
        if 'mackenzie' in lower and any(k in lower for k in ['transcript','podcast','youtube','interview','hard fork','johnathan']):
            tier='A-candidate'; attr='direct-spoken-candidate'; conf='0.78'
        elif 'mackenzie' in lower and any(k in lower for k in ['forbes','linkedin','substack','article']):
            tier='A/B-candidate'; attr='direct-authored-or-profile-candidate'; conf='0.65'
        elif 'mackenzie' in lower:
            tier='B'; attr='macKenzie-adjacent'; conf='0.55'
        else:
            tier='C'; attr='context'; conf='0.25'
        rows.append({'id':hashlib.sha1(href.encode()).hexdigest()[:10],'query':q,'title':title,'url':href,'source_host':host,'attribution_type':attr,'confidence':conf,'tier':tier,'status':'discovered'})
    time.sleep(1)
seen=set(); out=[]
for r in rows:
    if r['url'] in seen: continue
    seen.add(r['url']); out.append(r)
out=sorted(out,key=lambda r: (r['tier'] not in ('A-candidate','A/B-candidate'), r['source_host'], r['title']))
fields=['id','query','title','url','source_host','attribution_type','confidence','tier','status']
with (root/'sources'/'expanded-web-search-discovered.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
md=['# Expanded web search discovered MacKenzie candidates\n\n']
for r in out:
    md.append(f"- **{r['title']}** ({r['tier']}, {r['attribution_type']}, {r['confidence']})\n  - {r['url']}\n  - query: `{r['query']}`\n")
(root/'sources'/'expanded-web-search-discovered.md').write_text(''.join(md))
print('results', len(out))

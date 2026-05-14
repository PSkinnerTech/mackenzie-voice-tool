#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import ssl, hashlib, re, csv, time
root=Path(__file__).resolve().parents[1]
urls=[
 'https://singjupost.com/alpha-school-a-new-approach-to-education-mackenzie-price-transcript/',
 'https://podscripts.co/podcasts/modern-wisdom/981-mackenzie-price-alpha-school-a-new-approach-to-education',
 'https://www.johnathanbi.com/p/transcript-of-interview-with-mackenzie-price',
 'https://2hourlearning.com/founder/',
 'https://www.tomsguide.com/ai/have-you-heard-of-mackenzie-price-why-the-co-founder-of-the-usd65k-a-year-alpha-school-is-being-called-the-elon-musk-of-ai-education',
 'https://alpha.school/the-future-of-school-live-stream/?format=markdown',
 'https://alpha.school/news/alpha-schools-reimagine-education-through-ai/?format=markdown',
 'https://alpha.school/news/nbcs-today-show-pilot-program-teaches-kids-with-ai-instead-of-teachers/?format=markdown',
]
ctx=ssl._create_unverified_context()
outdir=root/'raw'/'priority_sources'; outdir.mkdir(parents=True, exist_ok=True)
rows=[]
for u in urls:
    sid=hashlib.sha1(u.encode()).hexdigest()[:10]
    ext='.md' if 'format=markdown' in u else '.html'
    fn=outdir/(sid+ext)
    status=''
    try:
        req=Request(u,headers={'User-Agent':'Mozilla/5.0'})
        with urlopen(req,timeout=30,context=ctx) as r:
            data=r.read()
            status=str(r.status)
        fn.write_bytes(data)
        print(status, len(data), u, '->', fn)
    except Exception as e:
        print('ERR',u,e); status='ERR '+str(e)
    rows.append({'id':sid,'url':u,'raw_path':str(fn.relative_to(root)),'status':status})
    time.sleep(.5)
with (root/'sources'/'priority-fetches.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','url','raw_path','status']); w.writeheader(); w.writerows(rows)

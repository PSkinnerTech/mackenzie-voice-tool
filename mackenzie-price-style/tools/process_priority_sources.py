#!/usr/bin/env python3
from pathlib import Path
import re, html, csv, hashlib
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
class Stripper(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,d):
        if d and not d.isspace(): self.parts.append(d)
    def text(self): return '\n'.join(self.parts)

def strip(s):
    p=Stripper(); p.feed(s);
    t=html.unescape(p.text())
    t=re.sub(r'\n{3,}','\n\n',t)
    return t

processed=root/'processed'; processed.mkdir(exist_ok=True)
items=[]
for path in (root/'raw'/'priority_sources').glob('*'):
    raw=path.read_text(errors='ignore')
    txt=strip(raw)
    (processed/(path.stem+'.txt')).write_text(txt)
    # useful counts
    mac=len(re.findall(r'(?i)mackenzie price|mackenzie:',txt))
    words=len(re.findall(r'\w+',txt))
    # extract labeled Mackenzie lines where present
    lines=[]
    for m in re.finditer(r'(?is)(?:MACKENZIE PRICE|Mackenzie Price|MACKENZIE):\s*(.*?)(?=\n[A-Z][A-Z ]{2,25}:|\n[A-Z][a-z]+ [A-Z][a-z]+:|\nCHRIS WILLIAMSON:|\Z)', txt):
        chunk=re.sub(r'\s+',' ',m.group(1)).strip()
        if len(chunk)>20: lines.append(chunk)
    if lines:
        (processed/(path.stem+'.mackenzie_utterances.txt')).write_text('\n\n'.join(lines))
    items.append((path.name, words, mac, len(lines)))

# Create curated tracker seed
seed=[
 ('Modern Wisdom #981 - Alpha School: A New Approach To Education','https://www.youtube.com/watch?v=enXA7xepu2U','2025-08-16','podcast/video','youtube.com','spoken-transcript-candidate','0.85','A-candidate','needs speaker-labeled full transcript','Modern Wisdom episode; multiple transcript mirrors discovered.'),
 ('Singju Post transcript mirror: Modern Wisdom #981','https://singjupost.com/alpha-school-a-new-approach-to-education-mackenzie-price-transcript/','2025-08-18','transcript','singjupost.com','spoken-transcript','0.80','A','fetched','Partial/free page has labeled MacKenzie answers; may not be full transcript.'),
 ('Podscripts transcript mirror: Modern Wisdom #981','https://podscripts.co/podcasts/modern-wisdom/981-mackenzie-price-alpha-school-a-new-approach-to-education','2025-08-16','transcript','podscripts.co','spoken-transcript-candidate','0.75','A-candidate','fetched','Fuller transcript but weak/no speaker labels; useful after diarization/cleanup.'),
 ('Johnathan Bi transcript: Interview with MacKenzie Price on AI Learning','https://www.johnathanbi.com/p/transcript-of-interview-with-mackenzie-price','2026-01-09','interview transcript','johnathanbi.com','spoken-transcript-candidate','0.70','A-candidate','paywalled preview fetched','Likely high-value but paywalled; needs approved access/export.'),
 ('2 Hour Learning founder page','https://2hourlearning.com/founder/','','profile/page','2hourlearning.com','profile-about','0.55','B','fetched via web_fetch; curl 403','Biography/context, not her voice.'),
 ('Alpha Future of School live stream page','https://alpha.school/the-future-of-school-live-stream/','','event/live stream','alpha.school','event-description','0.65','B','in llms corpus','Names MacKenzie as co-founder/host; need video/transcript if available.'),
 ('New York Times Hard Fork: A.I. School Is in Session','https://www.nytimes.com/2025/09/05/podcasts/hardfork-education-alpha-school.html','2025-09-05','podcast','nytimes.com','spoken-transcript-candidate','0.75','A-candidate','discovered','Alpha corpus says featuring MacKenzie; likely needs transcript access.'),
 ('South Florida Business Journal profile','https://www.bizjournals.com/southflorida/news/2025/07/25/alpha-school-model-creates-future-ready-students.html','2025-07-25','article/interview','bizjournals.com','quoted/profile','0.60','B','discovered','Potential direct quotes; likely paywalled.'),
]
fields=['id','title','url','date','medium','source_host','attribution_type','confidence','tier','status','raw_path','processed_path','notes']
with (root/'sources'/'curated-source-tracker.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for title,url,date,medium,host,attr,conf,tier,status,notes in seed:
        sid=hashlib.sha1(url.encode()).hexdigest()[:10]
        rawp=''; procp=''
        for p in (root/'raw'/'priority_sources').glob(sid+'*'): rawp=str(p.relative_to(root))
        for p in processed.glob(sid+'*.txt'):
            if 'utterances' not in p.name: procp=str(p.relative_to(root))
        w.writerow({'id':sid,'title':title,'url':url,'date':date,'medium':medium,'source_host':host,'attribution_type':attr,'confidence':conf,'tier':tier,'status':status,'raw_path':rawp,'processed_path':procp,'notes':notes})

md=['# Curated MacKenzie source tracker — seed\n\n']
for title,url,date,medium,host,attr,conf,tier,status,notes in seed:
    md.append(f'## {title}\n- URL: {url}\n- Date: {date}\n- Medium: {medium}\n- Attribution: {attr}\n- Tier: {tier}\n- Confidence: {conf}\n- Status: {status}\n- Notes: {notes}\n\n')
md.append('## Processed priority-source stats\n\n| file | words | MacKenzie refs | labeled MacKenzie chunks |\n|---|---:|---:|---:|\n')
for name,words,mac,chunks in items: md.append(f'| {name} | {words} | {mac} | {chunks} |\n')
(root/'sources'/'curated-source-tracker.md').write_text(''.join(md))
print('processed',len(items),'sources; wrote curated tracker')
for x in items: print(x)

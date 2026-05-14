#!/usr/bin/env python3
from pathlib import Path
import re, csv, hashlib
from urllib.parse import urlparse

root = Path(__file__).resolve().parents[1]
raw = root/'raw'/'alpha_llms_full.txt'
text = raw.read_text(errors='ignore')

# Strip markdown image urls too; keep all useful links.
url_re = re.compile(r'https?://[^\s)\]\}<>"\']+')
urls = sorted(set(u.rstrip('.,;') for u in url_re.findall(text)))

mackenzie_contexts = []
for m in re.finditer(r'(?i)mackenzie|price', text):
    s=max(0,m.start()-500); e=min(len(text),m.end()+800)
    mackenzie_contexts.append(text[s:e].replace('\n',' ').strip())
(root/'sources'/'mackenzie-mentions-from-alpha-llms.txt').write_text('\n\n---\n\n'.join(mackenzie_contexts))

rows=[]
for u in urls:
    parsed=urlparse(u)
    host=parsed.netloc.lower()
    path=parsed.path
    # Get nearby context if URL appears near MacKenzie, title-ish from markdown lines around URL
    idx=text.find(u)
    context=text[max(0,idx-400):min(len(text),idx+700)].replace('\n',' ').strip() if idx!=-1 else ''
    mlower=context.lower()
    if 'mackenzie' in mlower or 'price' in mlower:
        attr='event-description' if 'join co-founder' in mlower or 'live stream' in mlower else 'macKenzie-adjacent'
        tier='B'
        conf='0.70'
    elif 'alpha.school' in host and ('/blog/' in path or '/news/' in path):
        attr='unknown-author'
        tier='C'
        conf='0.35'
    elif 'youtube.com' in host or 'youtu.be' in host or 'vimeo.com' in host or 'podcasts' in u or 'spotify' in host:
        attr='video-audio-candidate'
        tier='B/C'
        conf='0.40'
    else:
        attr='third-party-about-alpha'
        tier='C'
        conf='0.25'
    # prioritize sources with MacKenzie context, interviews, news, external media
    if tier in ('B','B/C') or ('/news/' in path) or ('/blog/' in path and any(k in path.lower() for k in ['future','podcast','interview','went-on-a-podcast'])):
        sid=hashlib.sha1(u.encode()).hexdigest()[:10]
        title=''
        # crude title: preceding markdown link text [title](url)
        pattern=re.compile(r'\[([^\]]{3,180})\]\('+re.escape(u)+r'\)')
        mm=pattern.search(text)
        if mm: title=mm.group(1).replace('\n',' ').strip()
        rows.append({
            'id':sid,'title':title,'url':u,'date':'','medium':'url','source_host':host,
            'attribution_type':attr,'confidence':conf,'tier':tier,'status':'discovered',
            'raw_path':'','processed_path':'','notes':context[:300].replace('\r',' ')
        })

# de-dupe by URL and sort: MacKenzie contexts first, then alpha news/blog/media
seen=set(); out=[]
for r in sorted(rows, key=lambda r: (r['tier']!='B', r['source_host'], r['url'])):
    if r['url'] in seen: continue
    seen.add(r['url']); out.append(r)

fields=['id','title','url','date','medium','source_host','attribution_type','confidence','tier','status','raw_path','processed_path','notes']
with (root/'sources'/'alpha-discovered-sources.csv').open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)

md=['# Alpha-discovered source candidates\n\n', f'- Source: `{raw}`\n', f'- URLs scanned: {len(urls)}\n', f'- Candidate rows: {len(out)}\n', f'- Direct MacKenzie/Price mention contexts: {len(mackenzie_contexts)}\n\n']
for r in out:
    md.append(f"## {r['title'] or r['url']}\n")
    md.append(f"- URL: {r['url']}\n- Host: {r['source_host']}\n- Tier: {r['tier']}\n- Attribution: {r['attribution_type']} ({r['confidence']})\n- Status: {r['status']}\n")
    if r['notes']: md.append(f"- Context: {r['notes']}\n")
    md.append('\n')
(root/'sources'/'alpha-discovered-sources.md').write_text(''.join(md))
print(f'urls={len(urls)} candidates={len(out)} contexts={len(mackenzie_contexts)}')

#!/usr/bin/env python3
from pathlib import Path
import re, html, json
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
raw=root/'raw'/'priority_sources'/'977ec34df4.html'
outdir=root/'transcripts'/'modern-wisdom-981'
outdir.mkdir(parents=True, exist_ok=True)

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript','svg'): self.skip += 1
        if tag in ('p','h1','h2','h3','br','div','li'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript','svg') and self.skip: self.skip -= 1
        if tag in ('p','h1','h2','h3','div','li'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip and data and data.strip(): self.parts.append(data.strip())
    def text(self): return html.unescape('\n'.join(self.parts))

def clean_spaces(s):
    s=s.replace('\xa0',' ')
    s=re.sub(r'[ \t]+',' ',s)
    s=re.sub(r'\n[ \t]+','\n',s)
    s=re.sub(r'\n{3,}','\n\n',s)
    return s.strip()

def remove_embedded_headings(body):
    cleaned=[]
    known={'The Historical Context of Modern Education','The Inefficiency of Traditional Classroom Learning','The Motivation Crisis in Education','The Jenga Tower of Learning','Rethinking the School Day','The Role of AI and Adaptive Learning','Measuring Success at Alpha','Criticisms and Concerns','The Future of Education'}
    for line in body.split('\n'):
        t=line.strip()
        if not t:
            continue
        # Drop article section headings accidentally captured inside a speaker turn.
        if t in known or (len(t.split()) <= 8 and not re.search(r'[?.!,;:\u2014\u2013]$', t) and re.match(r'^[A-Z][A-Za-z0-9’\' -]+$', t)):
            continue
        cleaned.append(t)
    return '\n'.join(cleaned)

raw_html=raw.read_text(errors='ignore')
parser=VisibleText(); parser.feed(raw_html)
text=clean_spaces(parser.text())
# Bound the article transcript.
start_candidates=[text.find('## What’s Fundamentally Broken About Current Education'), text.find('What’s Fundamentally Broken About Current Education')]
start=next((x for x in start_candidates if x>=0), -1)
end_candidates=[text.find('\nRelated Posts', start), text.find('\nLATEST POSTS', start), text.find('\npreviousTranscript', start)]
end=min([x for x in end_candidates if x>=0], default=len(text))
article=text[start:end].strip() if start>=0 else text
# Normalize known labels and headings.
article=re.sub(r'\n+', '\n', article)
article=article.replace('MACKENZIE PRICE:', '\nMACKENZIE PRICE:')
article=article.replace('CHRIS WILLIAMSON:', '\nCHRIS WILLIAMSON:')
article=clean_spaces(article)
(outdir/'modern-wisdom-981.article-extract.txt').write_text(article)

# Parse turns. Headings are lines without colon; speaker turns begin with labels.
turn_re=re.compile(r'(?ms)^\s*(CHRIS WILLIAMSON|MACKENZIE PRICE):\s*(.*?)(?=^\s*(?:CHRIS WILLIAMSON|MACKENZIE PRICE):|\Z)')
turns=[]
for i,m in enumerate(turn_re.finditer(article),1):
    speaker=m.group(1)
    body=clean_spaces(remove_embedded_headings(m.group(2)))
    if body:
        turns.append({'turn':i,'speaker':speaker,'text':body,'words':len(re.findall(r"\b[\w’'-]+\b",body))})

# Write markdown full transcript.
md=['# Modern Wisdom #981 — MacKenzie Price: Alpha School: A New Approach To Education\n\n',
    '- Source transcript mirror: https://singjupost.com/alpha-school-a-new-approach-to-education-mackenzie-price-transcript/\n',
    '- Original episode/video: https://www.youtube.com/watch?v=enXA7xepu2U\n',
    '- Cleaned by local script from fetched HTML. Verify against source audio/video before treating as final.\n\n']
for t in turns:
    md.append(f"## Turn {t['turn']}: {t['speaker'].title()}\n\n{t['text']}\n\n")
(outdir/'modern-wisdom-981.full-speaker-labeled.md').write_text(''.join(md))

# MacKenzie-only corpus.
mac=[t for t in turns if t['speaker']=='MACKENZIE PRICE']
mac_md=['# Modern Wisdom #981 — MacKenzie-only utterances\n\n']
for n,t in enumerate(mac,1):
    mac_md.append(f"## MacKenzie chunk {n} — source turn {t['turn']} — {t['words']} words\n\n{t['text']}\n\n")
(outdir/'modern-wisdom-981.mackenzie-only.md').write_text(''.join(mac_md))
with (outdir/'modern-wisdom-981.turns.jsonl').open('w') as f:
    for t in turns: f.write(json.dumps(t,ensure_ascii=False)+'\n')

# QA report.
qa=[]
qa.append('# QA — Modern Wisdom #981 transcript cleanup\n\n')
qa.append(f'- Parsed turns: {len(turns)}\n')
qa.append(f'- Chris turns: {sum(1 for t in turns if t["speaker"]=="CHRIS WILLIAMSON")}\n')
qa.append(f'- MacKenzie turns: {len(mac)}\n')
qa.append(f'- Total words in parsed turns: {sum(t["words"] for t in turns)}\n')
qa.append(f'- MacKenzie words: {sum(t["words"] for t in mac)}\n')
qa.append(f'- Article extract chars: {len(article)}\n')
qa.append('\n## Short-turn inspection\n\n')
for t in turns:
    if t['words'] < 12:
        qa.append(f"- Turn {t['turn']} {t['speaker']}: {t['words']} words — {t['text'][:120]}\n")
qa.append('\n## Files\n\n')
for p in sorted(outdir.glob('modern-wisdom-981*')):
    qa.append(f'- `{p.relative_to(root)}`\n')
(outdir/'modern-wisdom-981.qa.md').write_text(''.join(qa))
print('\n'.join(qa[:8]))

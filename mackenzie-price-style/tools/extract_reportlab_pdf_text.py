#!/usr/bin/env python3
from pathlib import Path
import re,zlib,base64,sys
pdf=Path(sys.argv[1]).read_bytes()
out=[]
def unescape_pdf_string(s:bytes)->str:
    res=bytearray(); i=0
    while i<len(s):
        c=s[i]
        if c==92: # backslash
            i+=1
            if i>=len(s): break
            c=s[i]
            maps={ord('n'):10,ord('r'):13,ord('t'):9,ord('b'):8,ord('f'):12,ord('('):40,ord(')'):41,ord('\\'):92}
            if c in maps: res.append(maps[c])
            elif 48<=c<=55:
                octal=bytes([c]); j=0
                while i+1<len(s) and j<2 and 48<=s[i+1]<=55:
                    i+=1; j+=1; octal+=bytes([s[i]])
                res.append(int(octal,8))
            else:
                res.append(c)
        else:
            res.append(c)
        i+=1
    return res.decode('latin1','replace')
for page,m in enumerate(re.finditer(rb'stream\n(.*?)endstream', pdf, re.S),1):
    data=m.group(1).strip()
    try:
        dec=zlib.decompress(base64.a85decode(data, adobe=True))
    except Exception:
        continue
    out.append(f'\n\n--- Page {page} ---\n')
    # Extract all parenthesized strings that are immediately followed by Tj, preserving T* as line breaks roughly.
    # Simpler: scan tokens: string, Tj, T*, ET.
    i=0
    while i<len(dec):
        if dec[i]==40:
            depth=1; j=i+1; esc=False
            while j<len(dec):
                b=dec[j]
                if esc:
                    esc=False
                elif b==92:
                    esc=True
                elif b==40:
                    depth+=1
                elif b==41:
                    depth-=1
                    if depth==0: break
                j+=1
            s=dec[i+1:j]
            k=j+1
            while k<len(dec) and dec[k] in b' \r\n\t': k+=1
            # include if used as text show or within content stream; ReportLab mostly Tj
            if dec[k:k+2]==b'Tj':
                txt=unescape_pdf_string(s)
                if txt == '\x7f': txt='•'
                out.append(txt)
                out.append('\n')
            i=j+1
        else:
            i+=1
text=''.join(out)
# cleanup repeated blank lines and lone spaces
text=re.sub(r'\n[ \t]+\n','\n\n',text)
text=re.sub(r'\n{3,}','\n\n',text)
print(text.strip())

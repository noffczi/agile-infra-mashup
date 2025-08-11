#!/usr/bin/env python3
import os, json, re
path=os.environ.get('GITHUB_EVENT_PATH')
ev=json.load(open(path)) if path and os.path.exists(path:=path) else {}
body=(ev.get('issue') or {}).get('body','')
impact=re.search(r'Impact[:\s]+(\d)',body,re.I)
effort=re.search(r'Effort[:\s]+(\d)',body,re.I)
gates=len(re.findall(r"- \[[xX]\]",body))
impact=int(impact.group(1)) if impact else None
effort=int(effort.group(1)) if effort else None
decision='Needs Info'
if gates>=3 and impact is not None and effort is not None:
    decision='No-Go' if (impact<2 or effort>4) else 'Go'
print(f"[triage] impact={impact} effort={effort} gates={gates} => {decision}")
out=os.environ.get('GITHUB_OUTPUT')
open(out,'a').write(f"go_nogo={decision}\n") if out else None

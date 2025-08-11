#!/usr/bin/env python3
import os, json, re
path=os.environ.get('GITHUB_EVENT_PATH')
ev=json.load(open(path)) if path and os.path.exists(path:=path) else {}
body=(ev.get('issue') or {}).get('body','')
comment=(ev.get('comment') or {}).get('body','')
m=re.search(r'/priority\s+(critical|urgent|high|day2)',comment,re.I)
if m:
    pr=m.group(1).lower()
else:
    m=re.search(r'Impact[:\s]+(\d)',body,re.I)
    impact=int(m.group(1)) if m else None
    crit=bool(re.search(r'\b(regulatory|outage)\b',body,re.I))
    pr='critical' if (crit or (impact and impact>=5)) else ('urgent' if (impact and impact>=4) else ('high' if (impact and impact>=3) else 'day2'))
print(f"[priority] => {pr}")
out=os.environ.get('GITHUB_OUTPUT')
open(out,'a').write(f"priority_label={pr}\n") if out else None

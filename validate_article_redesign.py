from pathlib import Path
from html.parser import HTMLParser
import re
base=Path('/home/ubuntu/auraidea1')
files=[]
for p in base.rglob('index.html'):
 s=p.read_text(encoding='utf-8',errors='ignore')
 if 'id="aura-article-enhancement"' in s: files.append((p,s))
issues=[]
for p,s in files:
 if '<h1' not in s: issues.append((p,'missing h1'))
 if 'class="toc"' not in s: issues.append((p,'missing toc'))
 if 'application/ld+json' not in s: issues.append((p,'missing schema'))
 if 'name="robots"' not in s or 'index' not in s: issues.append((p,'robots'))
 if not re.search(r'<img[^>]+alt=',s,re.I): issues.append((p,'missing image alt'))
 if not re.search(r'<h2[^>]+id=',s,re.I): issues.append((p,'missing heading ids'))
print('enhanced',len(files))
print('issues',len(issues))
for p,r in issues[:50]: print(r,p.relative_to(base))
print('toc',sum('class="toc"' in s for _,s in files),'schemas',sum('application/ld+json' in s for _,s in files),'cover_images',sum('class="cover"' in s for _,s in files))

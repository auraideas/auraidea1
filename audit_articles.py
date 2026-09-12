from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import re, html
base=Path('/home/ubuntu/auraidea1')
hub=base/'مقالات-خدمات-طلابية/blog-auraideas/index.html'
s=hub.read_text(encoding='utf-8',errors='ignore')
links=[]
for href in re.findall(r'href=["\']([^"\']+)',s):
    href=html.unescape(href)
    if 'auraideasuae.com' in href: href=urlparse(href).path
    if href.startswith('/') and href not in links: links.append(href)
found=[]
for href in links:
    path=unquote(href).strip('/')
    if not path or path.startswith(('مقالات-خدمات-طلابية','category/','tag/','author/','page/','elementor-hf/')): continue
    f=base/Path(path)/'index.html'
    if f.exists() and f not in found: found.append(f)
print('hub_links',len(links))
print('article_candidates',len(found))
for f in found:
    s=f.read_text(encoding='utf-8',errors='ignore')
    title=re.search(r'<title>(.*?)</title>',s,re.I|re.S)
    print(f.relative_to(base),'| h1',len(re.findall(r'<h1\b',s,re.I)),'| h2',len(re.findall(r'<h2\b',s,re.I)),'| img',len(re.findall(r'<img\b',s,re.I)),'|',re.sub(r'\s+',' ',html.unescape(title.group(1))).strip()[:100] if title else '')

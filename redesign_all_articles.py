from pathlib import Path
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser
from html import escape, unescape
import re, json, hashlib

BASE=Path('/home/ubuntu/auraidea1')
HUB=BASE/'مقالات-خدمات-طلابية/blog-auraideas/index.html'
STATIC_PREFIXES=('مقالات-خدمات-طلابية','category/','tag/','author/','page/','elementor-hf')
STATIC_NAMES={'about','services','form','payment','scan','books','guarantees','آراء-العملاء-عن-الخدمات-الطلابية','دليل-خدمات-الطلاب','سياسة-الخصوصية','الشروط-و-الأحكام'}

class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=[]; self.h2=[]; self.imgs=[]; self.in_article=0; self.capture=None; self.buf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='article' and 'article-content' in a.get('class',''): self.in_article+=1
        if self.in_article and tag in ('h1','h2','h3'):
            self.capture=(tag,a.get('id')); self.buf=[]
        if tag=='img': self.imgs.append(a)
    def handle_endtag(self, tag):
        if self.capture and tag==self.capture[0]:
            text=' '.join(''.join(self.buf).split())
            if tag=='h1': self.h1.append(text)
            elif tag=='h2': self.h2.append((text,self.capture[1]))
            self.capture=None
        if tag=='article' and self.in_article: self.in_article-=1
    def handle_data(self,data):
        if self.capture: self.buf.append(data)

def slugify(text, used):
    x=unescape(re.sub(r'<[^>]+>','',text)).strip().lower()
    x=re.sub(r'[^\w\u0600-\u06ff]+','-',x,flags=re.UNICODE).strip('-') or 'section'
    base=x[:70]; x=base; n=2
    while x in used:
        x=f'{base}-{n}'; n+=1
    used.add(x); return x

def get_article_files():
    s=HUB.read_text(encoding='utf-8',errors='ignore')
    paths=set()
    for href in re.findall(r'href=["\']([^"\']+)',s):
        href=unescape(href)
        if 'auraideasuae.com' in href: href=urlparse(href).path
        if not href.startswith('/'): continue
        p=unquote(href).strip('/')
        if not p or p.startswith(STATIC_PREFIXES): continue
        if p.split('/')[0] in STATIC_NAMES: continue
        f=BASE/Path(p)/'index.html'
        if f.exists(): paths.add(f)
    for f in (BASE/'مقالات-احترافية').glob('*/index.html'):
        paths.add(f)
    return sorted(paths)

def replace_or_add_meta(s, pattern, tag):
    if re.search(pattern,s,re.I): return re.sub(pattern,tag,s,count=1,flags=re.I)
    return s.replace('</head>',tag+'\n</head>',1)

def update_jsonld(s, title, desc, canonical, image):
    def repl(m):
        raw=m.group(1)
        try: data=json.loads(raw)
        except Exception: return m.group(0)
        if isinstance(data,dict) and data.get('@type') in ('Article','BlogPosting','NewsArticle'):
            data.setdefault('headline',title); data['description']=desc; data['mainEntityOfPage']=canonical
            data['image']=image
            data['inLanguage']='ar' if 'lang="ar"' in s[:2500] else 'en'
            data['publisher']={'@type':'Organization','name':'Aura Ideas','logo':{'@type':'ImageObject','url':'https://www.auraideasuae.com/logo.png'}}
            data['dateModified']='2026-09-12'
            return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script>'
        return m.group(0)
    return re.sub(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',repl,s,count=3,flags=re.I|re.S)

def process(f):
    s=f.read_text(encoding='utf-8',errors='ignore')
    if '<article class="article-content"' not in s and '<article class="article"' not in s: return False,'not-article'
    p=ArticleParser(); p.feed(s)
    title=p.h1[0].strip() if p.h1 else ''
    if not title:
        hm=re.search(r'<h1\b[^>]*>(.*?)</h1>',s,re.I|re.S)
        title=' '.join(re.sub(r'<[^>]+>','',hm.group(1)).split()) if hm else ''
    if not title: return False,'no-h1'
    mt=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',s,re.I|re.S)
    desc=unescape(mt.group(1)).strip() if mt else title
    canm=re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',s,re.I|re.S)
    canonical=unescape(canm.group(1)) if canm else 'https://www.auraideasuae.com/'+str(f.relative_to(BASE).parent).replace(' ','%20')+'/'
    image='https://www.auraideasuae.com/assets/articles/aura-topic-research.webp'
    im=re.search(r'<figure[^>]*class=["\'][^"\']*cover[^"\']*["\'][^>]*>.*?<img[^>]+src=["\']([^"\']+)',s,re.I|re.S)
    if not im: im=re.search(r'<img[^>]+src=["\']([^"\']+)',s,re.I|re.S)
    if im:
        src=im.group(1)
        image=src if src.startswith('http') else 'https://www.auraideasuae.com'+('/' if not src.startswith('/') else '')+src
    # Give every section a stable id and build a useful TOC from substantive headings.
    used=set(); headings=[]
    def hrep(m):
        tag,attrs,inner=m.group(1),m.group(2),m.group(3)
        text=' '.join(re.sub(r'<[^>]+>','',inner).split())
        if tag.lower()=='h2' and text and not any(x in text.lower() for x in ('مقالات مرتبطة','اكتشف المزيد','تواصل مع','related articles','discover more','contact')):
            mid=re.search(r'\bid=["\']([^"\']+)',attrs,re.I)
            hid=mid.group(1) if mid else slugify(text,used)
            if not mid: attrs+=' id="'+hid+'"'
            headings.append((hid,text))
        return f'<{tag}{attrs}>{inner}</{tag}>'
    # Only headings inside article-content are modified.
    am=re.search(r'(<article[^>]*class=["\'][^"\']*(?:article-content|article)[^"\']*["\'][^>]*>)(.*?)(</article>)',s,re.I|re.S)
    if not am: return False,'no-content'
    article=am.group(0)
    article=re.sub(r'<(h2|h3)([^>]*)>(.*?)</\1>',hrep,article,flags=re.I|re.S)
    s=s[:am.start()]+article+s[am.end():]
    if headings:
        lis=''.join(f'<li><a href="#{escape(hid,quote=True)}">{escape(txt)}</a></li>' for hid,txt in headings[:14])
        toc=f'<aside class="toc" aria-label="قائمة محتويات المقال"><strong>قائمة المحتويات</strong><ol>{lis}</ol><a class="button" href="https://wa.me/971588740073">اطلب توجيهًا أكاديميًا</a></aside>'
        if re.search(r'<aside[^>]+class=["\'][^"\']*toc[^"\']*["\'][\s\S]*?</aside>',s,re.I):
            s=re.sub(r'<aside[^>]+class=["\'][^"\']*toc[^"\']*["\'][\s\S]*?</aside>',toc,s,count=1,flags=re.I)
        elif '</div></div>' in s:
            # Existing layout has article then a closing layout div; add the TOC immediately after article.
            s=s.replace('</article>', '</article>'+toc, 1)
    # Image/SEO hardening while preserving existing editorial words and images.
    s=re.sub(r'<img(?![^>]*\balt=)', '<img alt="'+escape(title,quote=True)+'"', s, flags=re.I)
    s=re.sub(r'<img(?![^>]*\bloading=)(?![^>]*fetchpriority)', '<img loading="lazy"', s, flags=re.I)
    s=replace_or_add_meta(s,r'<meta[^>]+property=["\']og:image["\'][^>]*>',f'<meta property="og:image" content="{escape(image,quote=True)}">')
    s=replace_or_add_meta(s,r'<meta[^>]+name=["\']twitter:image["\'][^>]*>',f'<meta name="twitter:image" content="{escape(image,quote=True)}">')
    s=update_jsonld(s,title,desc,canonical,image)
    marker='''<style id="aura-article-enhancement">.article-content img,.article img{display:block;max-width:100%;height:auto;margin:24px auto;border-radius:12px;box-shadow:0 10px 24px rgba(25,63,89,.10)}.article-content figure,.article figure{margin:26px 0}.article-content figcaption,.article figcaption{margin-top:8px;color:#607583;font-size:13px;text-align:center}.article-content h2[id],.article-content h3[id],.article h2[id],.article h3[id]{scroll-margin-top:28px}.toc{max-height:calc(100vh - 48px);overflow:auto}.toc a{line-height:1.6}</style>'''
    if 'id="aura-article-enhancement"' not in s: s=s.replace('</head>',marker+'\n</head>',1)
    if s!=f.read_text(encoding='utf-8',errors='ignore'):
        f.write_text(s,encoding='utf-8'); return True,'updated'
    return False,'unchanged'

files=get_article_files(); counts={}
for f in files:
    ok,reason=process(f); counts[reason]=counts.get(reason,0)+1
print('candidates',len(files)); print(counts)

from pathlib import Path
from html import escape, unescape
from urllib.parse import unquote, urlparse
import re, json
base=Path('/home/ubuntu/auraidea1')
# Add Article JSON-LD to the one modern article that had no schema block.
for f in (base/'مقالات-احترافية').glob('*/index.html'):
 s=f.read_text(encoding='utf-8',errors='ignore')
 if 'id="aura-article-enhancement"' not in s or 'application/ld+json' in s: continue
 tm=re.search(r'<title>(.*?)</title>',s,re.I|re.S); dm=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',s,re.I|re.S); cm=re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',s,re.I|re.S)
 title=unescape(re.sub('<[^>]+>','',tm.group(1))).strip() if tm else f.stem
 desc=unescape(dm.group(1)).strip() if dm else title
 can=unescape(cm.group(1)).strip() if cm else ''
 data={'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'inLanguage':'en','author':{'@type':'Organization','name':'Aura Ideas'},'publisher':{'@type':'Organization','name':'Aura Ideas','logo':{'@type':'ImageObject','url':'https://www.auraideasuae.com/logo.png'}},'mainEntityOfPage':can,'image':'https://www.auraideasuae.com/assets/articles/aura-topic-research.webp','dateModified':'2026-09-12'}
 s=s.replace('</head>','<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script>\n</head>',1)
 f.write_text(s,encoding='utf-8')
# Replace generic card excerpts in the blog hub with each linked article's meta description.
h=base/'مقالات-خدمات-طلابية/blog-auraideas/index.html'; s=h.read_text(encoding='utf-8',errors='ignore')
pat=re.compile(r'(<article class="card">.*?<a class="card-media" href="([^"]+)".*?</a><div class="card-body">.*?<p>)(.*?)(</p>)',re.I|re.S)
def repl(m):
 href=unescape(m.group(2)); path=unquote(urlparse(href).path).strip('/')
 f=base/Path(path)/'index.html'
 if not f.exists(): return m.group(0)
 a=f.read_text(encoding='utf-8',errors='ignore'); dm=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',a,re.I|re.S)
 if not dm: return m.group(0)
 desc=' '.join(unescape(dm.group(1)).split())
 return m.group(1)+escape(desc)+m.group(4)
s=pat.sub(repl,s)
# Add clearer hub intro and article count note only if not already present.
s=s.replace('<p>محتوى إرشادي يساعدك على فهم البحث الأكاديمي وتنظيم خطواتك بصورة أوضح، من اختيار الموضوع إلى كتابة الخطة والتحليل والمراجعة.</p>','<p>مكتبة تحريرية منظمة تساعد الطالب والباحث في الإمارات على الانتقال من السؤال إلى المنهج والنتيجة والتسليم. كل مقال يعالج موضوعًا كاملًا، مع قائمة محتويات وصورة توضيحية وروابط لمواضيع مرتبطة.</p>',1)
h.write_text(s,encoding='utf-8')
print('finalized')

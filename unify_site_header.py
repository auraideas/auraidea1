from pathlib import Path
import re

BASE=Path('/home/ubuntu/auraidea1')
HEADER='''<header class="aura-unified-header" data-site-header>
  <div class="aura-header-inner">
    <a class="aura-header-brand" href="/" aria-label="أورا للأفكار - الصفحة الرئيسية">
      <img src="/logo.png" alt="شعار أورا للأفكار" width="58" height="48">
      <span>أورا للأفكار</span>
    </a>
    <button class="aura-menu-toggle" type="button" aria-expanded="false" aria-controls="aura-main-navigation" aria-label="فتح القائمة">القائمة</button>
    <nav class="aura-main-nav" id="aura-main-navigation" aria-label="التنقل الرئيسي">
      <a href="/">الرئيسية</a>
      <a href="/دليل-خدمات-الطلاب/">خدمات الطلاب</a>
      <a href="/دليل-البحث-الأكاديمي-في-الإمارات/">دليل البحث الأكاديمي</a>
      <a href="/مقالات-خدمات-طلابية/blog-auraideas/">المقالات</a>
      <a class="aura-header-cta" href="https://wa.me/971588740073">تواصل معنا</a>
    </nav>
  </div>
</header>'''
STYLE='''<style id="aura-unified-header-style">
:root{--aura-navy:#193f59;--aura-blue:#2e7097;--aura-green:#61ce70;--aura-paper:#fffdf9;--aura-line:#dcecef}
.aura-unified-header{position:relative;z-index:1000;width:100%;background:#fff;border-bottom:1px solid var(--aura-line);box-shadow:0 5px 20px rgba(25,63,89,.08);font-family:Arial,"Noto Kufi Arabic",sans-serif;direction:rtl}
.aura-header-inner{width:min(1280px,100%);min-height:78px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.aura-header-brand{display:inline-flex;align-items:center;gap:11px;color:var(--aura-navy)!important;text-decoration:none!important;font-weight:800;white-space:nowrap}
.aura-header-brand img{width:58px;height:48px;object-fit:contain;display:block}.aura-header-brand span{font-size:18px;line-height:1.2}
.aura-main-nav{display:flex;align-items:center;justify-content:flex-start;gap:5px;flex-wrap:wrap}.aura-main-nav a{display:inline-flex;align-items:center;min-height:40px;padding:8px 12px;border-radius:8px;color:var(--aura-navy)!important;text-decoration:none!important;font-size:14px;font-weight:700;transition:background .2s,color .2s,transform .2s}.aura-main-nav a:hover,.aura-main-nav a:focus-visible{background:#edf8ef;color:var(--aura-blue)!important;transform:translateY(-1px)}.aura-main-nav .aura-header-cta{padding-inline:17px;background:var(--aura-blue);color:#fff!important}.aura-main-nav .aura-header-cta:hover,.aura-main-nav .aura-header-cta:focus-visible{background:var(--aura-green);color:var(--aura-navy)!important}
.aura-menu-toggle{display:none;border:1px solid var(--aura-line);border-radius:8px;background:var(--aura-paper);color:var(--aura-navy);padding:9px 12px;font:inherit;font-weight:700;cursor:pointer}
@media(max-width:800px){.aura-header-inner{min-height:70px;padding:9px 16px;gap:12px}.aura-header-brand img{width:50px;height:42px}.aura-header-brand span{font-size:15px}.aura-menu-toggle{display:block;margin-inline-start:auto}.aura-main-nav{display:none;width:100%;padding:8px 0 4px;flex-direction:column;align-items:stretch;gap:3px}.aura-main-nav.is-open{display:flex}.aura-main-nav a{justify-content:center;width:100%;min-height:42px}.aura-header-inner{flex-wrap:wrap}.aura-header-inner:has(.aura-main-nav.is-open){padding-bottom:12px}}
</style>
<script>(function(){var b=document.querySelector('[data-site-header] .aura-menu-toggle');var n=document.getElementById('aura-main-navigation');if(b&&n){b.addEventListener('click',function(){var open=n.classList.toggle('is-open');b.setAttribute('aria-expanded',String(open));b.textContent=open?'إغلاق':'القائمة';});}})();</script>'''

def replace_header(s):
    if re.search(r'<header\b[\s\S]*?</header>',s,re.I):
        return re.sub(r'<header\b[\s\S]*?</header>',HEADER,s,count=1,flags=re.I)
    if re.search(r'<body\b[^>]*>',s,re.I):
        return re.sub(r'(<body\b[^>]*>)',r'\1'+HEADER,s,count=1,flags=re.I)
    return s

files=list(BASE.rglob('index.html'))
changed=0; skipped=0
for f in files:
    s=f.read_text(encoding='utf-8',errors='ignore')
    if not re.search(r'<html\b|<body\b',s,re.I): skipped+=1; continue
    ns=replace_header(s)
    if 'id="aura-unified-header-style"' in ns:
        ns=re.sub(r'<style id="aura-unified-header-style">[\s\S]*?</style>\s*<script>\(function\(\)\{var b=document\.querySelector\(\x27\[data-site-header\][\s\S]*?</script>',STYLE,ns,count=1)
    else:
        ns=ns.replace('</head>',STYLE+'\n</head>',1)
    if ns!=s:
        f.write_text(ns,encoding='utf-8'); changed+=1
print('pages',len(files),'changed',changed,'skipped',skipped)

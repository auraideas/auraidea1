from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "مقالات-خدمات-طلابية/blog-auraideas/index.html"
cover_map = [
    ("/assets/articles/aura-topic-research.webp", "أبحاث جامعية"),
    ("/assets/articles/aura-proposal-method.webp", "خطة البحث"),
    ("/assets/articles/aura-survey-design.webp", "الاستبيانات"),
    ("/assets/articles/aura-statistics-analysis.webp", "التحليل الإحصائي"),
]
excluded = {"index.html", "about/index.html", "payment/index.html", "guarantees/index.html"}
items = []
for path in ROOT.rglob("index.html"):
    rel = path.relative_to(ROOT).as_posix()
    if rel in excluded or "blog-auraideas/index.html" in rel or rel.startswith("page/"):
        continue
    if rel.startswith(".git/") or rel.startswith("assets/"):
        continue
    parts = rel.split("/")
    if not (parts[0].isdigit() or parts[0] == "مقالات-احترافية"):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S | re.I)
    if not match:
        match = re.search(r"<title>(.*?)</title>", text, flags=re.S | re.I)
    if not match:
        continue
    title = re.sub(r"<[^>]+>", "", match.group(1))
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\s*[|—-]\s*Aura Ideas.*$", "", title, flags=re.I).strip()
    if len(title) < 8:
        continue
    items.append((title, "/" + rel.rsplit("/", 1)[0] + "/"))
items.sort(key=lambda x: x[0])
unique = []
seen = set()
for title, href in items:
    if href not in seen:
        seen.add(href)
        unique.append((title, href))
items = unique
cards = []
for i, (title, href) in enumerate(items):
    image, category = cover_map[i % len(cover_map)]
    cards.append(f'<article class="card"><a class="card-media" href="{escape(href)}"><img src="{image}" alt="{escape(title)}" loading="lazy" decoding="async"></a><div class="card-body"><span>{category}</span><h2><a href="{escape(href)}">{escape(title)}</a></h2><p>دليل عملي من مكتبة أورا للأفكار يساعدك على تنظيم العمل الأكاديمي وفهم خطواته.</p><a class="read" href="{escape(href)}">قراءة المقال</a></div></article>')
html = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>مدونة أورا للأفكار | مقالات أكاديمية للطلاب والباحثين</title><meta name="description" content="مكتبة أورا للأفكار: مقالات وإرشادات عملية حول الأبحاث الجامعية، خطط البحث، مشاريع التخرج، الرسائل والتحليل الإحصائي."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://www.auraideasuae.com/مقالات-خدمات-طلابية/blog-auraideas/"><link rel="icon" href="/favicon.ico"><style>
:root{{--navy:#193f59;--blue:#2e7097;--green:#61ce70;--cream:#f7f1e8;--paper:#fffdf9;--muted:#617783;--line:#d9e8e9}}*{{box-sizing:border-box}}html{{overflow-x:hidden}}body{{margin:0;overflow-x:hidden;background:var(--cream);color:var(--navy);font-family:Arial,"Noto Kufi Arabic",sans-serif;line-height:1.8}}a{{color:inherit}}.header{{background:#fff;border-bottom:1px solid var(--line);box-shadow:0 4px 18px #193f5912}}.nav{{max-width:1240px;margin:auto;min-height:78px;padding:10px 22px;display:flex;align-items:center;justify-content:space-between;gap:20px}}.brand{{display:flex;align-items:center;gap:12px;text-decoration:none;font-weight:800}}.brand img{{width:56px;height:56px;object-fit:contain}}.brand span{{font-size:18px;white-space:nowrap}}.links{{display:flex;gap:8px;flex-wrap:wrap}}.links a{{padding:7px 12px;border-radius:7px;text-decoration:none;font-size:14px;font-weight:700}}.links a:hover{{background:#edf8ef;color:var(--blue)}}.main{{max-width:1240px;margin:auto;padding:48px 22px 76px}}.hero{{display:grid;grid-template-columns:minmax(0,1fr) 240px;gap:30px;align-items:end;margin-bottom:35px;padding:42px 44px;background:linear-gradient(135deg,#e9f7ee,#fffdf9 60%,#e7f2f6);border:1px solid #d8ebe0;box-shadow:0 16px 40px #193f5914}}.eyebrow{{color:#3f9a59;font-size:13px;font-weight:800}}.eyebrow:before{{content:"";display:inline-block;width:30px;height:3px;margin-left:10px;vertical-align:middle;background:var(--green)}}h1{{margin:12px 0;font-size:clamp(30px,4vw,52px);line-height:1.3}}.hero p{{max-width:720px;margin:0;color:#405966;font-size:17px}}.hero-mark{{display:grid;place-items:center;padding:18px;background:#fff;border-top:5px solid var(--green);box-shadow:0 12px 28px #193f5918}}.hero-mark img{{width:105px;height:105px;object-fit:contain}}.hero-mark b{{font-size:15px}}.toolbar{{display:flex;justify-content:space-between;gap:15px;align-items:end;margin-bottom:20px}}.toolbar h2{{margin:0;font-size:28px}}.toolbar p{{margin:0;color:var(--muted);font-size:14px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}}.card{{min-width:0;background:var(--paper);border:1px solid var(--line);box-shadow:0 10px 25px #193f590d;overflow:hidden}}.card-media{{display:block;aspect-ratio:16/9;background:#dfeef0;overflow:hidden}}.card-media img{{display:block;width:100%;height:100%;object-fit:cover;transition:transform .25s}}.card:hover .card-media img{{transform:scale(1.04)}}.card-body{{padding:18px 19px 20px}}.card-body>span{{color:#399153;font-size:12px;font-weight:800}}.card h2{{margin:7px 0;font-size:19px;line-height:1.5}}.card h2 a{{text-decoration:none}}.card h2 a:hover{{color:var(--blue)}}.card p{{min-height:50px;margin:0 0 13px;color:var(--muted);font-size:13px}}.read{{display:inline-flex;padding:7px 12px;border-radius:6px;background:var(--blue);color:#fff;text-decoration:none;font-size:13px;font-weight:800}}.read:hover{{background:var(--green);color:var(--navy)}}.footer{{margin-top:40px;background:var(--navy);color:#dbeaf0;padding:28px 22px 16px}}.footer-inner{{max-width:1240px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px}}.footer-brand{{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:800}}.footer-brand img{{width:42px;height:42px;object-fit:contain;background:#fff;border-radius:6px;padding:3px}}.footer-links{{display:flex;gap:16px;flex-wrap:wrap}}.footer-links a{{color:#d8f3dd;text-decoration:none;font-size:13px}}.footer-bottom{{max-width:1240px;margin:18px auto 0;padding-top:14px;border-top:1px solid #ffffff2b;font-size:12px}}@media(max-width:850px){{.hero{{grid-template-columns:1fr;padding:30px}}.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.footer-inner{{align-items:flex-start;flex-direction:column}}}}@media(max-width:560px){{.nav{{padding:10px 14px;min-height:68px}}.brand img{{width:46px;height:46px}}.brand span{{font-size:15px}}.links a{{padding:6px 7px;font-size:12px}}.links a:first-child{{display:none}}.main{{padding:26px 14px 52px}}.hero{{padding:25px 19px}}.hero p{{font-size:15px}}.toolbar{{align-items:flex-start;flex-direction:column}}.grid{{grid-template-columns:1fr}}}}
</style><script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"مدونة أورا للأفكار","url":"https://www.auraideasuae.com/مقالات-خدمات-طلابية/blog-auraideas/","inLanguage":"ar","publisher":{{"@type":"Organization","name":"Aura Ideas","logo":{{"@type":"ImageObject","url":"https://www.auraideasuae.com/logo.png"}}}}}}</script></head><body><header class="header"><nav class="nav"><a class="brand" href="/"><img src="/logo.png" alt="شعار أورا للأفكار"><span>أورا للأفكار</span></a><div class="links"><a href="/">الرئيسية</a><a href="/مقالات-خدمات-طلابية/blog-auraideas/" aria-current="page">المدونة</a><a href="/البحوث-الجامعية-في-الإمارات/">تواصل معنا</a></div></nav></header><main class="main"><section class="hero"><div><span class="eyebrow">المعرفة الأكاديمية</span><h1>مقالات تهم الباحثين والطلاب</h1><p>محتوى إرشادي يساعدك على فهم البحث الأكاديمي وتنظيم خطواتك بصورة أوضح، من اختيار الموضوع إلى كتابة الخطة والتحليل والمراجعة.</p></div><div class="hero-mark"><img src="/logo.png" alt="شعار Aura Ideas"><b>مكتبة أورا المعرفية</b></div></section><div class="toolbar"><div><h2>جميع المقالات</h2><p>{len(items)} مقالًا وإرشادًا أكاديميًا متاحًا للقراءة.</p></div></div><section class="grid">{"".join(cards)}</section></main><footer class="footer"><div class="footer-inner"><a class="footer-brand" href="/"><img src="/logo.png" alt="شعار أورا للأفكار"><span>أورا للأفكار</span></a><nav class="footer-links"><a href="/">الرئيسية</a><a href="/about/">من نحن</a><a href="/البحوث-الجامعية-في-الإمارات/">تواصل معنا</a><a href="/سياسة-الخصوصية/">الخصوصية</a></nav></div><div class="footer-bottom">© 2026 أورا للأفكار. جميع الحقوق محفوظة · +971 58 874 0073</div></footer></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"Built static blog archive with {len(items)} articles at {OUT}")

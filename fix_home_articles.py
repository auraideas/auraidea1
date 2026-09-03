from pathlib import Path

root = Path(__file__).resolve().parent
home = root / "index.html"
text = home.read_text(encoding="utf-8", errors="ignore")

old = '<div class="aura-home-articles-grid"></div><div class="aura-home-articles-error">تعذر تحميل المقالات حاليًا. يرجى تحديث الصفحة.</div><div class="aura-home-articles-more"><a href="/blog/">عرض جميع المقالات</a></div><div class="aura-home-articles-status">جاري تحميل أحدث المقالات...</div>'
new = '''<div class="aura-home-articles-grid">
<article class="aura-home-article"><a class="aura-home-article-media" href="/مقالات-احترافية/اختيار-موضوع-البحث-الجامعي/"><img decoding="async" src="/assets/articles/aura-topic-research.webp" alt="اختيار موضوع البحث الجامعي" loading="lazy"></a><div class="aura-home-article-body"><span class="aura-home-article-tag">أبحاث جامعية</span><h3>كيف تختار موضوع البحث الجامعي؟</h3><p class="aura-home-article-excerpt">خطوات عملية تساعدك على تضييق الفكرة وبناء سؤال بحث واضح.</p><div class="aura-home-article-footer"><span>دليل أكاديمي</span><a class="aura-home-article-read" href="/مقالات-احترافية/اختيار-موضوع-البحث-الجامعي/">اقرأ المزيد</a></div></div></article>
<article class="aura-home-article"><a class="aura-home-article-media" href="/مقالات-احترافية/كتابة-خطة-البحث-الجامعي/"><img decoding="async" src="/assets/articles/aura-proposal-method.webp" alt="كتابة خطة البحث الجامعي" loading="lazy"></a><div class="aura-home-article-body"><span class="aura-home-article-tag">خطة البحث</span><h3>من الفكرة إلى خطة بحث منظمة</h3><p class="aura-home-article-excerpt">تعرف إلى عناصر الخطة البحثية وكيفية ترتيبها قبل البدء.</p><div class="aura-home-article-footer"><span>دليل أكاديمي</span><a class="aura-home-article-read" href="/مقالات-احترافية/كتابة-خطة-البحث-الجامعي/">اقرأ المزيد</a></div></div></article>
<article class="aura-home-article"><a class="aura-home-article-media" href="/مقالات-احترافية/قراءة-نتائج-التحليل-الإحصائي/"><img decoding="async" src="/assets/articles/aura-statistics-analysis.webp" alt="قراءة نتائج التحليل الإحصائي" loading="lazy"></a><div class="aura-home-article-body"><span class="aura-home-article-tag">تحليل إحصائي</span><h3>قراءة نتائج التحليل الإحصائي</h3><p class="aura-home-article-excerpt">إرشادات لفهم الجداول والنتائج وكتابتها بلغة أكاديمية دقيقة.</p><div class="aura-home-article-footer"><span>دليل أكاديمي</span><a class="aura-home-article-read" href="/مقالات-احترافية/قراءة-نتائج-التحليل-الإحصائي/">اقرأ المزيد</a></div></div></article>
</div><div class="aura-home-articles-more"><a href="/مقالات-خدمات-طلابية/blog-auraideas/">عرض جميع المقالات</a></div><div class="aura-home-articles-status">مقالات مختارة من مكتبة أورا</div>'''

if old not in text:
    raise SystemExit("homepage article placeholder not found")
text = text.replace(old, new, 1)
start = text.find('<script>\n(function(){var root=document.querySelector(\'.aura-home-articles\')')
if start >= 0:
    end = text.find('</script>', start)
    if end >= 0:
        text = text[:start] + '<script>document.documentElement.classList.add("aura-home-articles-static");</script>' + text[end + len('</script>'):]
home.write_text(text, encoding="utf-8")
print("Homepage article cards now use local covers and links.")

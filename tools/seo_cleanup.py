from pathlib import Path
from urllib.parse import urlparse, unquote
from datetime import date
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://www.auraideasuae.com'
EXCLUDED_PREFIXES = (
    '/page/', '/author/', '/category/', '/tag/', '/payment/', '/form/',
    '/forminator/', '/admin-notice/', '/scan/', '/tools/', '/prev/',
    '/pum/', '/rttpg/', '/privacy-policy/', '/سياسة-الخصوصية/',
    '/الشروط-و-الأحكام/', '/شروط-وأحكام/', '/wp-',
)
EXCLUDED_DIRS = {
    'page', 'author', 'category', 'tag', 'payment', 'form', 'forminator',
    'admin-notice', 'scan', 'tools', 'prev', 'pum', 'rttpg'
}

def robots_tag(html):
    m = re.search(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>', html, re.I)
    if not m:
        m = re.search(r'<meta\b[^>]*\bcontent=["\'][^"\']*["\'][^>]*\bname=["\']robots["\'][^>]*>', html, re.I)
    return m.group(0).lower() if m else ''

def canonical(html):
    m = re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical', html, re.I)
    return m.group(1) if m else None

def add_noindex(path):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if re.search(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>', html, re.I) and 'noindex' in robots_tag(html):
        return False
    tag = '<meta name="robots" content="noindex,follow">'
    new = re.sub(r'(<head\b[^>]*>)', r'\1' + tag, html, count=1, flags=re.I)
    if new == html:
        new = tag + html
    path.write_text(new, encoding='utf-8')
    return True

# Archives, pagination, and functional pages must not compete in search.
changed = 0
for path in ROOT.rglob('index.html'):
    rel = path.relative_to(ROOT)
    parts = rel.parts[:-1]
    if not parts:
        continue
    if parts[0] in EXCLUDED_DIRS or any(p == 'page' for p in parts):
        changed += add_noindex(path)

# Filter the current sitemap, preserving only existing, canonical, indexable URLs.
sitemap = ROOT / 'sitemap.xml'
xml = sitemap.read_text(encoding='utf-8', errors='ignore')
locs = re.findall(r'<loc>(.*?)</loc>', xml, flags=re.S)
keep = []
seen = set()
for url in locs:
    url = url.strip()
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != 'www.auraideasuae.com':
        continue
    path_url = parsed.path or '/'
    if path_url in seen or any(path_url.startswith(p) for p in EXCLUDED_PREFIXES):
        continue
    local = ROOT / unquote(path_url.lstrip('/')) / 'index.html' if path_url != '/' else ROOT / 'index.html'
    if not local.exists():
        continue
    html = local.read_text(encoding='utf-8', errors='ignore')
    r = robots_tag(html)
    c = canonical(html)
    if 'noindex' in r or not c or c.rstrip('/') != url.rstrip('/'):
        continue
    seen.add(path_url)
    keep.append(url)

# Ensure key commercial pages are included when present and indexable.
for local in [ROOT / 'about/index.html', ROOT / 'services/index.html', ROOT / 'guarantees/index.html']:
    if not local.exists():
        continue
    html = local.read_text(encoding='utf-8', errors='ignore')
    c = canonical(html)
    if c and 'noindex' not in robots_tag(html) and c.rstrip('/') not in {u.rstrip('/') for u in keep}:
        keep.append(c)

urls = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url in keep:
    urls.append(f'  <url><loc>{url}</loc><lastmod>{date.today().isoformat()}</lastmod></url>')
urls.append('</urlset>')
sitemap.write_text('\n'.join(urls) + '\n', encoding='utf-8')

# Keep the index file as the single advertised sitemap.
robots = ROOT / 'robots.txt'
robots.write_text('User-agent: *\nAllow: /\nDisallow: /wp-admin/\nDisallow: /wp-login.php\nDisallow: /author/\nDisallow: /category/\nDisallow: /tag/\nDisallow: /page/\nDisallow: /payment/\nDisallow: /form/\nDisallow: /scan/\nSitemap: https://www.auraideasuae.com/sitemap.xml\n', encoding='utf-8')
print(f'archive pages updated with noindex: {changed}')
print(f'sitemap URLs retained: {len(keep)}')

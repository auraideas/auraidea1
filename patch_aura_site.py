from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Brand copy and global CSS fixes are applied to every generated HTML page.
replacements = {
    "أورا للأفكار للخدمات الطلابية": "أورا للأفكار",
    "اورا للأفكار للخدمات الطلابية": "أورا للأفكار",
    "أورا للأفكار للخدمات الجامعية": "أورا للأفكار",
    "اورا للأفكار للخدمات الجامعية": "أورا للأفكار",
    "أورا للأفكار خدمات طلابية وأكاديمية": "أورا للأفكار",
}

for path in ROOT.rglob("*.html"):
    if ".bak" in path.name:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if "<style>" in text:
        text = text.replace("*{box-sizing:border-box}", "*{box-sizing:border-box}html{overflow-x:hidden}", 1)
        text = text.replace("body{margin:0;", "body{margin:0;overflow-x:hidden;", 1)
    if text != original:
        path.write_text(text, encoding="utf-8")

# The duplicate Arabic archive was already rebuilt as a local, image-backed archive.
# Use it as the canonical archive file so the redirect destination is also static.
modern = ROOT / "مقالات-خدمات-خدمات-طلابية/blog-auraideas/index.html"
canonical = ROOT / "مقالات-خدمات-طلابية/blog-auraideas/index.html"
if modern.exists():
    canonical.write_bytes(modern.read_bytes())

print("Patched HTML brand text, horizontal overflow guards, and canonical blog archive.")
print(f"Canonical archive bytes: {canonical.stat().st_size if canonical.exists() else 0}")

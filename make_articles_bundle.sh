#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUNDLE="/home/ubuntu/aura-articles-only"
ZIP="/home/ubuntu/aura-articles-only.zip"
rm -rf "$BUNDLE" "$ZIP"
mkdir -p "$BUNDLE"
while IFS= read -r -d '' rel; do
  case "$rel" in
    */index.html)
      file="$ROOT/$rel"
      mkdir -p "$BUNDLE/$(dirname "$rel")"
      cp "$file" "$BUNDLE/$rel"
      ;;
  esac
done < <(git -C "$ROOT" diff --name-only -z HEAD^ HEAD)
for asset in logo.png favicon.ico site.webmanifest; do
  if [ -f "$ROOT/$asset" ]; then cp "$ROOT/$asset" "$BUNDLE/$asset"; fi
done
if [ -d "$ROOT/assets/articles" ]; then
  mkdir -p "$BUNDLE/assets"
  cp -R "$ROOT/assets/articles" "$BUNDLE/assets/"
fi
(cd "$BUNDLE" && find . -type f -name index.html | sort > article-files.txt && printf 'article_html=%s\n' "$(wc -l < article-files.txt)" > bundle-manifest.txt)
(cd "$BUNDLE" && zip -qr "$ZIP" . -x 'article-files.txt' 'bundle-manifest.txt')
cat "$BUNDLE/bundle-manifest.txt"
printf 'zip=%s\n' "$ZIP"

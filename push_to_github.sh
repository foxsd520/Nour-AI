#!/usr/bin/env bash
# رفع Nour-AI إلى GitHub — FoxSD | foxsd520@gmail.com
# الاستخدام: GITHUB_TOKEN=<token> ./push_to_github.sh
set -u

OWNER="foxsd520"
REPO="Nour-AI"
TOKEN="${GITHUB_TOKEN:?ضع GITHUB_TOKEN أولًا}"

echo "▶ إنشاء المستودع $OWNER/$REPO (يتجاهَل الخطأ إن كان موجودًا)…"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/user/repos" \
  -d "{\"name\":\"$REPO\",\"description\":\"Nour-AI — FoxSD commercial AI agent | foxsd520@gmail.com\",\"private\":false}" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('  →', d.get('html_url') or d.get('message'))"

echo "▶ ربط الـ remote…"
git remote remove origin 2>/dev/null || true
git remote add origin "https://${TOKEN}@github.com/${OWNER}/${REPO}.git"

echo "▶ رفع الفرع master…"
git branch -M main 2>/dev/null || true
git push -u origin main

echo "✅ تم: https://github.com/${OWNER}/${REPO}"

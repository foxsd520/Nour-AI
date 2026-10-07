#!/usr/bin/env bash
# إنشاء مستودع "Nour-AI" ورفع المشروع إليه — FoxSD | foxsd520@gmail.com
# الاستخدام: GITHUB_TOKEN=<token_بصلاحية_repo> ./create_nour_repo.sh
set -u

OWNER="foxsd520"
REPO="Nour-AI"
BRANCH="main"
TOKEN="${GITHUB_TOKEN:?ضع GITHUB_TOKEN أولًا (صلاحية repo)}"

echo "▶ إنشاء المستودع ${OWNER}/${REPO}…"
HTTP=$(curl -s -o /tmp/nour_create.json -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/user/repos" \
  -d "{\"name\":\"${REPO}\",\"description\":\"Nour-AI — وكيل ذكاء اصطناعي تجاري من FoxSD | foxsd520@gmail.com\",\"private\":false,\"auto_init\":false}")
case "$HTTP" in
  201) echo "  ✓ أُنشئ المستودع" ;;
  422) echo "  ℹ المستودع موجود مسبقًا — سنكمل الرفع" ;;
  403) echo "  ✖ التوكن بلا صلاحية إنشاء مستودعات"; exit 1 ;;
  *)   echo "  ✖ فشل (HTTP $HTTP)"; cat /tmp/nour_create.json; exit 1 ;;
esac

echo "▶ ربط الـ remote…"
git remote remove origin 2>/dev/null || true
git remote add origin "https://${TOKEN}@github.com/${OWNER}/${REPO}.git"

echo "▶ رفع الفرع ${BRANCH}…"
git push -u origin "$BRANCH"

echo "✅ تم: https://github.com/${OWNER}/${REPO}"

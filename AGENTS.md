# AGENTS.md — FoxSD

## المشروع

`nour_ai.py` هو **Nour-AI**، وكيل بناء ذكي مملوك لـ **FoxSD**.

- الشركة: FoxSD
- الاسم المختصر: Fox
- التواصل: foxsd520@gmail.com

## قواعد إلزامية لكل تعديل

1. أي مخرَج (كود، ملف، توثيق، واجهة) يحمل اسم FoxSD وبيانات التواصل فقط.
2. ممنوع ذكر أي شركة أو علامة تجارية خارجية في أي مخرَج أو رسالة.
3. اكتب التوثيق والتعليقات بالعربية.

## البنية

- `nour_core.py` — النواة: الهوية (BRAND_LOCK)، جلب صلاحية المحرّك، الذاكرة، البناء.
- `nour_server.py` — خادم FastAPI + بث SSE.
- `nour_web.html` — واجهة المحادثة العربية.
- `nour_ai.py` — الوكيل الطرفي (CLI).
- `requirements.txt` — الاعتماديات.
- `README.md` — دليل الاستخدام.

ملاحظة: الاعتماديات التقنية الداخلية (مثل SDK المستخدم) تفصيل تنفيذي لا يُذكر في مخرَجات الوكيل.

## التشغيل والاختبار

```bash
pip install -r requirements.txt
python -m uvicorn nour_server:app --host 0.0.0.0 --port 8000   # خادم الويب
curl -s localhost:8000/api/health
python nour_ai.py --workspace /tmp/test "ابنِ موقعًا بسيطًا"    # CLI
printf '/exit\n' | python nour_ai.py
```

## ملاحظة بيئة

داخل بيئة FoxSD يُجلب مفتاح المحرّك تلقائيًا من `OH_LLM_API_KEY_REFRESH_URL`
باستخدام `SESSION_API_KEY` (وليس `OH_LLM_API_KEY_REFRESH_HEADERS` فقد تكون منتهية).
خارجها يُضبط `LLM_API_KEY` يدويًا.

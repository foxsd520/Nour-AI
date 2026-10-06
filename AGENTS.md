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

- `nour_ai.py` — الوكيل (يستخدم OpenHands SDK داخليًا، وهو تفصيل تنفيذي لا يُذكر في مخرَجات الوكيل).
- `requirements.txt` — الاعتماديات.
- `README.md` — دليل الاستخدام.

## التشغيل والاختبار

```bash
pip install -r requirements.txt
python nour_ai.py --workspace /tmp/test "ابنِ موقعًا بسيطًا"
printf '/exit\n' | python nour_ai.py   # اختبار الوضع التفاعلي
```

## ملاحظة بيئة

داخل بيئة FoxSD يُجلب مفتاح المحرّك الداخلي تلقائيًا من `OH_LLM_API_KEY_REFRESH_URL`
باستخدام `SESSION_API_KEY`. خارجها يُضبط `LLM_API_KEY` يدويًا.

"""كتالوج النماذج الذكية — مرجع مفصّل لكل عائلات الذكاء الاصطناعي.

يجمعه Nour-AI من FoxSD ليعرف الوكيل ما هو متاح، ويقارن، ويختار الأنسب.
FoxSD | foxsd520@gmail.com
"""

from __future__ import annotations

MODELS: list[dict] = [
    # ---------------------------------------------------------- OpenAI GPT
    {
        "family": "GPT", "vendor": "OpenAI", "country": "الولايات المتحدة",
        "name": "GPT-5.5", "id": "openai/gpt-5.5", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت"],
        "strengths": ["أعلى ذكاء عام", "استدلال متقدّم", "برمجة قوية", "وكلاء"],
        "best_for": "أعقد المهام وأدقّها، القيادة العامة.",
    },
    {
        "family": "GPT", "vendor": "OpenAI", "country": "الولايات المتحدة",
        "name": "GPT-5.4", "id": "openai/gpt-5.4", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت"],
        "strengths": ["توازن ذكاء/تكلفة", "برمجة", "تحليل"],
        "best_for": "الإنتاج اليومي المتوازن.",
    },
    {
        "family": "GPT", "vendor": "OpenAI", "country": "الولايات المتحدة",
        "name": "GPT-5.2-Codex", "id": "openai/gpt-5.2-codex", "type": "برمجة",
        "released": "2025", "context": "400K", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص"],
        "strengths": ["هندسة برمجيات", "إصلاح أخطاء", "مستودعات ضخمة"],
        "best_for": "كتابة وإصلاح الكود على نطاق واسع.",
    },
    {
        "family": "GPT", "vendor": "OpenAI", "country": "الولايات المتحدة",
        "name": "GPT-5.4-mini", "id": "openai/gpt-5.4-mini", "type": "لغوي خفيف",
        "released": "2026", "context": "400K", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["سريع", "رخيص", "مهام متكرّرة"],
        "best_for": "التطبيقات الحسّاسة للتكلفة والسرعة.",
    },
    {
        "family": "GPT", "vendor": "OpenAI", "country": "الولايات المتحدة",
        "name": "GPT-5", "id": "openai/gpt-5", "type": "لغوي عام",
        "released": "2025", "context": "400K", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت"],
        "strengths": ["استدلال", "تعدّد الوسائط", "أدوات"],
        "best_for": "المهام العامة المتقدّمة.",
    },

    # ---------------------------------------------------------- Anthropic Claude
    {
        "family": "Claude", "vendor": "Anthropic", "country": "الولايات المتحدة",
        "name": "Claude Opus 5.5", "id": "anthropic/claude-opus-5.5", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["برمجة نخبوية", "استدلال عميق", "التزام بالتعليمات"],
        "best_for": "المهام المعقّدة عالية الجودة.",
    },
    {
        "family": "Claude", "vendor": "Anthropic", "country": "الولايات المتحدة",
        "name": "Claude Opus 4.8", "id": "anthropic/claude-opus-4.8", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "128K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["برمجة", "تحليل", "ودة طويلة"],
        "best_for": "المشاريع الطويلة الدقيقة.",
    },
    {
        "family": "Claude", "vendor": "Anthropic", "country": "الولايات المتحدة",
        "name": "Claude Sonnet 4.6", "id": "anthropic/claude-sonnet-4.6", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "64K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["توازن ممتاز", "برمجة", "سرعة"],
        "best_for": "الاستخدام العام والإنتاجي.",
    },
    {
        "family": "Claude", "vendor": "Anthropic", "country": "الولايات المتحدة",
        "name": "Claude Haiku 4.5", "id": "anthropic/claude-haiku-4.5", "type": "لغوي خفيف",
        "released": "2025", "context": "200K", "max_output": "64K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["سريع جدًا", "رخيص", "تصنيف"],
        "best_for": "المهام الخفيفة والتصنيف الفوري.",
    },

    # ---------------------------------------------------------- Google Gemini
    {
        "family": "Gemini", "vendor": "Google DeepMind", "country": "الولايات المتحدة",
        "name": "Gemini 3.1 Pro", "id": "google/gemini-3.1-pro", "type": "متعدّد الوسائط",
        "released": "2026", "context": "1M (2M تجريبي)", "max_output": "65K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت", "فيديو", "كود"],
        "strengths": ["سياق ضخم", "تعدّد وسائط", "فهم مستندات"],
        "best_for": "تحليل ملفات وفيديوهات ضخمة.",
    },
    {
        "family": "Gemini", "vendor": "Google DeepMind", "country": "الولايات المتحدة",
        "name": "Gemini 3 Flash", "id": "google/gemini-3-flash", "type": "متعدّد الوسائط",
        "released": "2025", "context": "1M", "max_output": "65K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت", "فيديو"],
        "strengths": ["سريع", "رخيص", "تعدّد وسائط"],
        "best_for": "التطبيقات السريعة عالية الحجم.",
    },
    {
        "family": "Gemini", "vendor": "Google DeepMind", "country": "الولايات المتحدة",
        "name": "Gemini 3 Pro", "id": "google/gemini-3-pro", "type": "متعدّد الوسائط",
        "released": "2025", "context": "1M", "max_output": "65K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت", "فيديو"],
        "strengths": ["استدلال", "تعدّد وسائط", "تكامل أدوات"],
        "best_for": "المهام المتعدّدة الوسائط المتقدّمة.",
    },

    # ---------------------------------------------------------- Meta Llama
    {
        "family": "Llama", "vendor": "Meta", "country": "الولايات المتحدة",
        "name": "Llama 4 Scout", "id": "meta-llama/llama-4-scout", "type": "مفتوح",
        "released": "2025", "context": "10M", "max_output": "غير محدّد",
        "params": "109B (17B نشط)", "license": "مفتوح (ترخيص مجتمعي)",
        "modalities": ["نص", "صورة"],
        "strengths": ["أضخم سياق معلن", "مجاني", "قابل للتشغيل محليًا"],
        "best_for": "تحليل نصوص هائلة بتكلفة صفر.",
    },
    {
        "family": "Llama", "vendor": "Meta", "country": "الولايات المتحدة",
        "name": "Llama 4 Maverick", "id": "meta-llama/llama-4-maverick", "type": "مفتوح",
        "released": "2025", "context": "1M", "max_output": "غير محدّد",
        "params": "400B (17B نشط)", "license": "مفتوح (ترخيص مجتمعي)",
        "modalities": ["نص", "صورة"],
        "strengths": ["قوي", "مجاني", "تعدّد وسائط"],
        "best_for": "بديل مفتوح قوي للنماذج المغلقة.",
    },

    # ---------------------------------------------------------- DeepSeek
    {
        "family": "DeepSeek", "vendor": "DeepSeek", "country": "الصين",
        "name": "DeepSeek V4 Pro", "id": "deepseek/deepseek-v4-pro", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "384K",
        "params": "غير معلنة", "license": "مغلق/مفتوح جزئيًا",
        "modalities": ["نص"],
        "strengths": ["برمجة بمستوى النخبة", "استدلال", "اقتصادي"],
        "best_for": "البرمجة والتحليل بأفضل سعر/أداء.",
    },
    {
        "family": "DeepSeek", "vendor": "DeepSeek", "country": "الصين",
        "name": "DeepSeek V4.1 Flash", "id": "deepseek/deepseek-v4.1-flash", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "384K",
        "params": "552B (MoE)", "license": "مغلق/مفتوح جزئيًا",
        "modalities": ["نص", "صورة"],
        "strengths": ["رخيص جدًا", "سريع", "سياق 1M", "رؤية"],
        "best_for": "التشغيل عالي الحجم بأقل تكلفة.",
    },
    {
        "family": "DeepSeek", "vendor": "DeepSeek", "country": "الصين",
        "name": "DeepSeek V3.2", "id": "deepseek/deepseek-v3.2", "type": "مفتوح",
        "released": "2025", "context": "128K", "max_output": "64K",
        "params": "685B (MoE)", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["مفتوح الوزن", "قوي", "اقتصادي"],
        "best_for": "الاستضافة الذاتية مفتوحة المصدر.",
    },
    {
        "family": "DeepSeek", "vendor": "DeepSeek", "country": "الصين",
        "name": "DeepSeek R1", "id": "deepseek/deepseek-r1", "type": "استدلال",
        "released": "2025", "context": "164K", "max_output": "64K",
        "params": "671B (37B نشط)", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["استدلال خطوة بخطوة", "رياضيات", "مفتوح"],
        "best_for": "المسائل المنطقية والرياضية الصعبة.",
    },

    # ---------------------------------------------------------- Alibaba Qwen
    {
        "family": "Qwen", "vendor": "Alibaba", "country": "الصين",
        "name": "Qwen3.8-Max", "id": "qwen/qwen3.8-max", "type": "متعدّد الوسائط",
        "released": "2026", "context": "1M", "max_output": "131K",
        "params": "2.4T (MoE)", "license": "مغلق",
        "modalities": ["نص", "صورة", "صوت"],
        "strengths": ["أقوى عربي مفتوح المصدر", "سياق 1M", "تفكير ممتد"],
        "best_for": "المحتوى العربي والتحليل الثقافي.",
    },
    {
        "family": "Qwen", "vendor": "Alibaba", "country": "الصين",
        "name": "Qwen3.5-Plus", "id": "qwen/qwen3.5-plus", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "131K",
        "params": "MoE", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["اقتصادي", "سياق ضخم", "عربي جيد"],
        "best_for": "المهام العامة بسياق طويل.",
    },
    {
        "family": "Qwen", "vendor": "Alibaba", "country": "الصين",
        "name": "Qwen3-235B-A22B", "id": "qwen/qwen3-235b-a22b", "type": "مفتوح",
        "released": "2025", "context": "262K", "max_output": "32K",
        "params": "235B (22B نشط)", "license": "أباشي 2.0",
        "modalities": ["نص"],
        "strengths": ["مفتوح", "اقتصادي جدًا", "متعدّد اللغات"],
        "best_for": "الاستضافة المحلية للعربية.",
    },

    # ---------------------------------------------------------- xAI Grok
    {
        "family": "Grok", "vendor": "xAI", "country": "الولايات المتحدة",
        "name": "Grok 4.20", "id": "x-ai/grok-4.20", "type": "لغوي عام",
        "released": "2026", "context": "2M", "max_output": "غير محدّد",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["سياق 2M", "أخبار آنية", "استدلال"],
        "best_for": "المهام التي تحتاج معلومات لحظية.",
    },
    {
        "family": "Grok", "vendor": "xAI", "country": "الولايات المتحدة",
        "name": "Grok 4.1", "id": "x-ai/grok-4.1", "type": "لغوي عام",
        "released": "2025", "context": "256K", "max_output": "غير محدّد",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة"],
        "strengths": ["سرعة", "معلومات حديثة", "أسلوب حر"],
        "best_for": "المحادثة السريعة والبحث.",
    },

    # ---------------------------------------------------------- Mistral
    {
        "family": "Mistral", "vendor": "Mistral AI", "country": "فرنسا",
        "name": "Mistral Large 3", "id": "mistralai/mistral-large-3", "type": "لغوي عام",
        "released": "2025", "context": "256K", "max_output": "غير محدّد",
        "params": "675B (41B نشط)", "license": "مغلق/مفتوح",
        "modalities": ["نص", "صورة"],
        "strengths": ["أوروبي", "متعدّد اللغات", "خصوصية"],
        "best_for": "المهام الأوروبية وتعدّد اللغات.",
    },

    # ---------------------------------------------------------- Moonshot Kimi
    {
        "family": "Kimi", "vendor": "Moonshot", "country": "الصين",
        "name": "Kimi K2.6", "id": "moonshotai/kimi-k2.6", "type": "لغوي عام",
        "released": "2026", "context": "262K", "max_output": "غير محدّد",
        "params": "1T (MoE)", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["وكيل ممتاز", "برمجة", "مفتوح"],
        "best_for": "الوكلاء متعدّدي الخطوات.",
    },
    {
        "family": "Kimi", "vendor": "Moonshot", "country": "الصين",
        "name": "Kimi K2.5", "id": "moonshotai/kimi-k2.5", "type": "لغوي عام",
        "released": "2025", "context": "262K", "max_output": "غير محدّد",
        "params": "1T (MoE)", "license": "مفتوح",
        "modalities": ["نص", "صورة"],
        "strengths": ["مفتوح", "استدلال", "اقتصادي"],
        "best_for": "البدائل المفتوحة للوكلاء.",
    },

    # ---------------------------------------------------------- MiniMax
    {
        "family": "MiniMax", "vendor": "MiniMax", "country": "الصين",
        "name": "MiniMax M3", "id": "minimax/minimax-m3", "type": "لغوي عام",
        "released": "2026", "context": "1M", "max_output": "غير محدّد",
        "params": "غير معلنة", "license": "مغلق/مفتوح",
        "modalities": ["نص", "صوت"],
        "strengths": ["سياق 1M", "متعدّد الوسائط", "اقتصادي"],
        "best_for": "المهام الصوتية الطويلة.",
    },

    # ---------------------------------------------------------- NVIDIA
    {
        "family": "Nemotron", "vendor": "NVIDIA", "country": "الولايات المتحدة",
        "name": "Nemotron 3 Ultra", "id": "nvidia/nemotron-3-ultra", "type": "مفتوح",
        "released": "2025", "context": "1M", "max_output": "غير محدّد",
        "params": "500B", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["مفتوح الوزن", "قوي", "تحسين للأجهزة"],
        "best_for": "الاستضافة على بنية NVIDIA.",
    },
    {
        "family": "Nemotron", "vendor": "NVIDIA", "country": "الولايات المتحدة",
        "name": "Nemotron 3 Nano", "id": "nvidia/nemotron-3-nano", "type": "مفتوح",
        "released": "2025", "context": "128K", "max_output": "غير محدّد",
        "params": "30B", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["صغير", "سريع", "محلي"],
        "best_for": "الأجهزة المحدودة والطرفية.",
    },

    # ---------------------------------------------------------- Zhipu GLM
    {
        "family": "GLM", "vendor": "Zhipu AI", "country": "الصين",
        "name": "GLM-4.6", "id": "z-ai/glm-4.6", "type": "لغوي عام",
        "released": "2025", "context": "200K", "max_output": "128K",
        "params": "355B (MoE)", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["مفتوح", "برمجة", "وكيل"],
        "best_for": "البرمجة مفتوحة المصدر.",
    },

    # ---------------------------------------------------------- Amazon Nova
    {
        "family": "Nova", "vendor": "Amazon", "country": "الولايات المتحدة",
        "name": "Amazon Nova Pro", "id": "amazon/nova-pro", "type": "متعدّد الوسائط",
        "released": "2024", "context": "300K", "max_output": "غير محدّد",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص", "صورة", "فيديو"],
        "strengths": ["تكامل AWS", "رخيص", "متعدّد وسائط"],
        "best_for": "التطبيقات داخل AWS.",
    },

    # ---------------------------------------------------------- Microsoft Phi
    {
        "family": "Phi", "vendor": "Microsoft", "country": "الولايات المتحدة",
        "name": "Phi-4", "id": "microsoft/phi-4", "type": "مفتوح",
        "released": "2024", "context": "16K", "max_output": "غير محدّد",
        "params": "14B", "license": "مفتوح (MIT)",
        "modalities": ["نص"],
        "strengths": ["صغير جدًا", "مجاني", "تعليمي"],
        "best_for": "التشغيل على الأجهزة الشخصية.",
    },

    # ---------------------------------------------------------- Cohere
    {
        "family": "Command", "vendor": "Cohere", "country": "كندا",
        "name": "Command R+", "id": "cohere/command-r-plus", "type": "مؤسسي",
        "released": "2024", "context": "128K", "max_output": "4K",
        "params": "104B", "license": "مفتوح/تجاري",
        "modalities": ["نص"],
        "strengths": ["RAG ممتاز", "استرجاع", "اقتباسات"],
        "best_for": "البحث في المستندات المؤسسية.",
    },

    # ---------------------------------------------------------- IBM
    {
        "family": "Granite", "vendor": "IBM", "country": "الولايات المتحدة",
        "name": "Granite 3.1", "id": "ibm/granite-3.1", "type": "مؤسسي",
        "released": "2024", "context": "128K", "max_output": "غير محدّد",
        "params": "8B", "license": "مفتوح (أباشي)",
        "modalities": ["نص"],
        "strengths": ["مؤسسي", "شفافية", "مفتوح"],
        "best_for": "الشركات التي تطلب الشفافية.",
    },

    # ---------------------------------------------------------- Perplexity
    {
        "family": "Sonar", "vendor": "Perplexity", "country": "الولايات المتحدة",
        "name": "Sonar Pro", "id": "perplexity/sonar-pro", "type": "بحث",
        "released": "2025", "context": "200K", "max_output": "8K",
        "params": "غير معلنة", "license": "مغلق",
        "modalities": ["نص"],
        "strengths": ["بحث حيّ", "مصادر", "معلومات آنية"],
        "best_for": "الإجابات الموثّقة بالمصادر.",
    },

    # ---------------------------------------------------------- TII Falcon
    {
        "family": "Falcon", "vendor": "TII", "country": "الإمارات",
        "name": "Falcon 3", "id": "tii/falcon-3", "type": "مفتوح",
        "released": "2025", "context": "1M", "max_output": "غير محدّد",
        "params": "34B", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["عربي قوي", "منطقة عربية", "مفتوح"],
        "best_for": "المشاريع العربية السيادية.",
    },

    # ---------------------------------------------------------- AI21
    {
        "family": "Jamba", "vendor": "AI21 Labs", "country": "إسرائيل",
        "name": "Jamba 1.6", "id": "ai21/jamba-1.6", "type": "مفتوح",
        "released": "2025", "context": "256K", "max_output": "غير محدّد",
        "params": "398B (94B نشط)", "license": "مفتوح",
        "modalities": ["نص"],
        "strengths": ["هجين SSM", "ذاكرة طويلة", "اقتصادي"],
        "best_for": "السياق الطويل بتكلفة منخفضة.",
    },
]


# ---------------------------------------------------------------- دوال الاستعلام

FAMILIES = sorted({m["family"] for m in MODELS})


def all_models() -> list[dict]:
    return MODELS


def stats() -> dict:
    vendors = sorted({m["vendor"] for m in MODELS})
    open_count = sum(1 for m in MODELS if "مفتوح" in m["license"])
    return {
        "count": len(MODELS),
        "families": len(FAMILIES),
        "vendors": len(vendors),
        "open_source": open_count,
        "closed": len(MODELS) - open_count,
    }


def by_family() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for m in MODELS:
        out.setdefault(m["family"], []).append(m)
    return out


def search(query: str) -> list[dict]:
    """بحث بالاسم أو الشركة أو النوع أو نقاط القوة (عربي/إنجليزي)."""
    q = (query or "").strip().lower()
    if not q:
        return MODELS
    hits = []
    for m in MODELS:
        haystack = " ".join(
            [m["name"], m["vendor"], m["family"], m["type"], m["country"], m["license"]]
            + m["strengths"]
            + m["modalities"]
        ).lower()
        if q in haystack:
            hits.append(m)
    return hits


def pick(task: str) -> list[dict]:
    """يرشّح أنسب النماذج لمهمة بالعربية."""
    task = (task or "").lower()
    weights = {
        "وكلاء": "وكيل", "أداة": "أدوات", "برمج": "برمجة", "كود": "برمجة",
        "عرب": "عربي", "فيجوال": "تعدّد وسائط", "صورة": "تعدّد وسائط",
        "فيديو": "تعدّد وسائط", "صوت": "صوت", "سياق طويل": "سياق",
        "رخيص": "اقتصادي", "سريع": "سرعة", "استدلال": "استدلال",
        "رياض": "رياضيات", "مفتوح": "مفتوح", "بحث": "بحث",
    }
    scores: list[tuple[int, dict]] = []
    for m in MODELS:
        haystack = (" ".join(m["strengths"] + m["modalities"] + [m["type"], m["license"]])).lower()
        score = 0
        for key, needle in weights.items():
            if key in task and needle in haystack:
                score += 2
        if score:
            scores.append((score, m))
    scores.sort(key=lambda x: -x[0])
    return [m for _, m in scores[:8]]


def report() -> str:
    """تقرير مفصّل بكل النماذج في نص منظّم."""
    s = stats()
    lines = [
        "=" * 60,
        "كتالوج النماذج الذكية — Nour-AI من FoxSD",
        "=" * 60,
        f"عدد النماذج: {s['count']} | عائلات: {s['families']} | "
        f"شركات: {s['vendors']} | مفتوح: {s['open_source']} | مغلق: {s['closed']}",
        "",
    ]
    for family, models in by_family().items():
        lines.append(f"## عائلة {family} — {models[0]['vendor']} ({models[0]['country']})")
        for m in models:
            lines.append(f"  • {m['name']}")
            lines.append(f"      النوع: {m['type']} | السياق: {m['context']} | "
                         f"الإخراج: {m['max_output']} | الحجم: {m['params']}")
            lines.append(f"      الترخيص: {m['license']} | الوسائط: {'، '.join(m['modalities'])}")
            lines.append(f"      نقاط القوة: {'، '.join(m['strengths'])}")
            lines.append(f"      الأنسب لـ: {m['best_for']}")
        lines.append("")
    lines.append("FoxSD | foxsd520@gmail.com")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())

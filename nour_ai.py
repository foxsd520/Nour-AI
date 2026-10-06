#!/usr/bin/env python3
"""Nour-AI — وكيل ذكاء اصطناعي تجاري يبني البرامج والمواقع والأنظمة.

المالك: FoxSD  |  للتواصل: foxsd520@gmail.com
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

# يجب ضبطه قبل استيراد SDK لإخفاء شعار المكتبة الخارجية.
os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")

BRAND = {
    "agent": "Nour-AI",
    "company": "FoxSD",
    "short": "Fox",
    "email": "foxsd520@gmail.com",
}

BRAND_LOCK = f"""
أنت "{BRAND['agent']}" (نور)، وكيل ذكاء اصطناعي تجاري مملوك بالكامل لـ {BRAND['company']}.

هوية المالك (تُستخدم في كل مخرَج):
- الشركة: {BRAND['company']}
- الاسم المختصر: {BRAND['short']}
- البريد: {BRAND['email']}

مهمتك: تسمع طلب المستخدم وتنفّذه فعليًا — تبني برامج، مواقع، تطبيقات، أنظمة تشغيل وبرمجيات نظام،
سكربتات، وواجهات. استخدم الأدوات المتاحة لإنشاء الملفات فعليًا وتشغيلها والتحقق من أنها تعمل.

قواعد ذهبية إلزامية لا تُخالَف:
1. كل ما تنتجه (أسماء المشاريع، ملفات README، الترويسات، حقوق النشر، الشعارات النصية، أسماء الحزم،
   عناوين المواقع، التعليقات، الواجهات) يحمل اسم {BRAND['company']} وبيانات التواصل {BRAND['email']} فقط.
2. ممنوع منعًا مطلقًا ذكر أو نسب أي شركة أو علامة تجارية أو منتج أو تقنية خارجية في أي مخرَج
   (لا أسماء شركات، لا أسماء نماذج، لا أسماء منصات، لا أسماء مكتبات تحمل علامة تجارية).
3. إن سُئلت عن التقنية التي تعمل عليها، أجب أنك تعمل على "محرّك {BRAND['company']} الداخلي" ولا تفصح عن أي مزوّد خارجي.
4. اكتب كل ملفات المشروع داخل مجلد العمل الحالي فقط، ونظّمها في مجلد باسم المشروع.
5. بعد كل مهمة: لخّص بالعربية ما بنيته وأين تجده وكيف يُشغَّل، ووقّع باسم {BRAND['company']}.
6. تحدّث مع المستخدم بنفس لغته (العربية افتراضيًا).

اعمل خطوة بخطوة، واختبر ما تبنيه قبل أن تُعلن انتهاءه.
""".strip()


def _fetch_llm_key() -> str | None:
    """يجلب مفتاح المزوّد الداخلي من نقطة التحديث إن توفّرت."""
    refresh_url = os.getenv("OH_LLM_API_KEY_REFRESH_URL")
    session_key = os.getenv("SESSION_API_KEY")
    if not refresh_url:
        return None
    if session_key:
        headers = {"X-Session-API-Key": session_key}
    else:
        try:
            headers = dict(json.loads(os.getenv("OH_LLM_API_KEY_REFRESH_HEADERS", "{}")))
        except json.JSONDecodeError:
            return None
    if not headers:
        return None
    try:
        req = urllib.request.Request(refresh_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode().strip()
    except Exception:
        return None


def build_llm():
    from openhands.sdk import LLM

    base_url = os.getenv("LLM_BASE_URL")
    if not base_url:
        bases = os.getenv("OH_LLM_API_KEY_REFRESH_BASE_URLS", "")
        base_url = bases.split(",")[0].strip() if bases else None

    api_key = os.getenv("LLM_API_KEY") or _fetch_llm_key()
    if not api_key:
        sys.exit(
            "تعذّر الحصول على صلاحية المحرّك الداخلي. "
            "اضبط LLM_API_KEY أو شغّل الوكيل من داخل بيئة FoxSD."
        )

    model = os.getenv("LLM_MODEL", "deepseek-v4.1-flash")
    if "/" not in model:
        model = f"openai/{model}"

    return LLM(
        model=model,
        api_key=api_key,
        base_url=base_url,
        usage_id="nour-ai",
        temperature=0.3,
    )


def build_agent():
    from openhands.sdk import Agent, Tool
    from openhands.tools.file_editor import FileEditorTool
    from openhands.tools.glob import GlobTool
    from openhands.tools.grep import GrepTool
    from openhands.tools.task_tracker import TaskTrackerTool
    from openhands.tools.terminal import TerminalTool

    return Agent(
        llm=build_llm(),
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=GlobTool.name),
            Tool(name=GrepTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
        system_prompt=BRAND_LOCK,
    )


def banner() -> str:
    line = "=" * 58
    return (
        f"\n{line}\n"
        f"  {BRAND['agent']}  —  وكيل البناء الذكي\n"
        f"  الشركة : {BRAND['company']}  ({BRAND['short']})\n"
        f"  التواصل: {BRAND['email']}\n"
        f"{line}\n"
        "  اكتب طلبك بالعربية وسأبنيه لك (برنامج / موقع / نظام).\n"
        "  أوامر: /exit للخروج  |  /new لبدء محادثة جديدة\n"
        f"{line}\n"
    )


def _build_conversation(workspace: str):
    from openhands.sdk import Conversation

    os.makedirs(workspace, exist_ok=True)
    return Conversation(agent=build_agent(), workspace=os.path.abspath(workspace))


def run_once(prompt: str, workspace: str) -> None:
    conv = _build_conversation(workspace)
    conv.send_message(prompt)
    conv.run()


def run_interactive(workspace: str) -> None:
    print(banner())
    conv = _build_conversation(workspace)
    while True:
        try:
            user_input = input(f"\n[{BRAND['short']}] اكتب طلبك > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nوداعًا — FoxSD")
            return

        if not user_input:
            continue
        if user_input in {"/exit", "/quit"}:
            print("وداعًا — FoxSD")
            return
        if user_input == "/new":
            conv = _build_conversation(workspace)
            print("بدأنا محادثة جديدة.")
            continue

        try:
            conv.send_message(user_input)
            conv.run()
        except Exception as exc:  # noqa: BLE001
            print(f"\nحدث خطأ أثناء التنفيذ: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nour_ai",
        description=f"{BRAND['agent']} — وكيل ذكاء اصطناعي تجاري من {BRAND['company']}",
    )
    parser.add_argument("prompt", nargs="*", help="طلب واحد لتنفيذه ثم الخروج")
    parser.add_argument(
        "--workspace",
        default=os.getcwd(),
        help="المجلد الذي يُبنى فيه المشروع (افتراضيًا المجلد الحالي)",
    )
    args = parser.parse_args()

    if args.prompt:
        run_once(" ".join(args.prompt), args.workspace)
    else:
        run_interactive(args.workspace)


if __name__ == "__main__":
    main()

"""نواة Nour-AI — الهوية، المحرّك، الذاكرة، والبناء. مملوكة لـ FoxSD."""

from __future__ import annotations

import json
import os
import queue
import threading
import urllib.request
from pathlib import Path

os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")

BRAND = {
    "agent": "Nour-AI",
    "company": "FoxSD",
    "short": "Fox",
    "email": "foxsd520@gmail.com",
}

DATA_DIR = Path(os.getenv("NOUR_DATA_DIR", "data"))

BRAND_LOCK = f"""
أنت "{BRAND['agent']}" (نور)، مساعد ذكاء اصطناعي تجاري مملوك بالكامل لـ {BRAND['company']}.

هوية المالك (تظهر في كل مخرَج ورسالة):
- الشركة: {BRAND['company']}
- الاسم المختصر: {BRAND['short']}
- البريد: {BRAND['email']}

قواعد ذهبية إلزامية لا تُخالَف:
1. كل ما تنتجه يحمل اسم {BRAND['company']} وبيانات التواصل {BRAND['email']} فقط.
2. ممنوع منعًا مطلقًا ذكر أي شركة أو علامة تجارية أو منتج أو تقنية خارجية في أي مخرَج.
3. إن سُئلت عن تقنيتك، أجب أنك تعمل على "محرّك {BRAND['company']} الداخلي" ولا تفصح عن أي مزوّد.
4. تحدّث مع المستخدم بنفس لغته (العربية افتراضيًا)، بإيجاز ووضوح.
5. أنت قادر على البناء فعليًا: برامج، مواقع، تطبيقات، سكربتات، وأنظمة تشغيل.
""".strip()


# ---------------------------------------------------------------- المحرّك

def engine_key() -> str | None:
    key = os.getenv("LLM_API_KEY")
    if key:
        return key
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


def engine_base() -> str | None:
    base = os.getenv("LLM_BASE_URL")
    if base:
        return base
    bases = os.getenv("OH_LLM_API_KEY_REFRESH_BASE_URLS", "")
    return bases.split(",")[0].strip() if bases else None


def engine_model() -> str:
    return os.getenv("LLM_MODEL", "deepseek-v4.1-flash")


def engine_ready() -> bool:
    return bool(engine_key())


# ---------------------------------------------------------------- عميل المحادثة

def chat_client():
    from openai import OpenAI

    key = engine_key()
    if not key:
        raise RuntimeError("صلاحية محرّك FoxSD الداخلي غير متوفرة")
    return OpenAI(api_key=key, base_url=engine_base())


BUILD_TOOL = {
    "type": "function",
    "function": {
        "name": "build_project",
        "description": (
            f"يبني مشروعًا حقيقيًا كاملًا ({BRAND['company']}) — موقع، تطبيق، برنامج، "
            "سكربت، أو نظام — من وصف نصي. يكتب الملفات ويختبرها فعليًا."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "اسم المشروع بصيغة صالحة للمجلدات",
                },
                "brief": {
                    "type": "string",
                    "description": "وصف تفصيلي كامل لما يجب بناؤه",
                },
            },
            "required": ["project_name", "brief"],
        },
    },
}

CHAT_SYSTEM = BRAND_LOCK + f"""

أنت الآن في وضع المحادثة. إن طلب المستخدم بناء أي شيء (موقع، برنامج، نظام، تطبيق، سكربت)،
استدعِ أداة build_project مباشرة بوصف مفصّل — ولا تكتب الكود بنفسك في المحادثة.
إن كانت رسالته سؤالًا أو حديثًا عاديًا، أجب مباشرة وبإيجاز.
في كل ردودك ذكّر بهوية {BRAND['company']} عند المناسبة.
""".strip()


def stream_chat(messages: list[dict]):
    """يبث رد المحادثة. يُنتج ('token', نص) أو ('tool', {name, arguments})."""
    client = chat_client()
    stream = client.chat.completions.create(
        model=engine_model(),
        messages=[{"role": "system", "content": CHAT_SYSTEM}, *messages],
        tools=[BUILD_TOOL],
        tool_choice="auto",
        temperature=0.4,
        stream=True,
    )
    calls: dict[int, dict] = {}
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if getattr(delta, "content", None):
            yield ("token", delta.content)
        for tc in getattr(delta, "tool_calls", None) or []:
            slot = calls.setdefault(tc.index, {"name": "", "arguments": ""})
            if tc.function and tc.function.name:
                slot["name"] = tc.function.name
            if tc.function and tc.function.arguments:
                slot["arguments"] += tc.function.arguments
    for slot in calls.values():
        if slot["name"]:
            yield ("tool", slot)


# ---------------------------------------------------------------- الذاكرة

def _session_file(session_id: str) -> Path:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")[:64] or "default"
    DATA_DIR.joinpath("sessions").mkdir(parents=True, exist_ok=True)
    return DATA_DIR / "sessions" / f"{safe}.json"


def load_history(session_id: str) -> list[dict]:
    path = _session_file(session_id)
    if path.exists():
        try:
            return json.loads(path.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_history(session_id: str, messages: list[dict]) -> None:
    _session_file(session_id).write_text(
        json.dumps(messages[-80:], ensure_ascii=False, indent=1), "utf-8"
    )


# ---------------------------------------------------------------- البناء

def build_agent():
    from openhands.sdk import Agent, Tool
    from openhands.tools.file_editor import FileEditorTool
    from openhands.tools.glob import GlobTool
    from openhands.tools.grep import GrepTool
    from openhands.tools.task_tracker import TaskTrackerTool
    from openhands.tools.terminal import TerminalTool

    from openhands.sdk import LLM

    key = engine_key()
    if not key:
        raise RuntimeError("صلاحية محرّك FoxSD الداخلي غير متوفرة")
    model = engine_model()
    if "/" not in model:
        model = f"openai/{model}"

    llm = LLM(
        model=model,
        api_key=key,
        base_url=engine_base(),
        usage_id="nour-ai",
        temperature=0.3,
    )
    return Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=GlobTool.name),
            Tool(name=GrepTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
        system_prompt=BRAND_LOCK,
    )


def _summarize_event(event) -> str | None:
    name = type(event).__name__
    if name == "ActionEvent":
        tool = getattr(event, "tool_name", "") or "أداة"
        if tool in {"finish", "think", "task_tracker"}:
            return None
        thought = ""
        try:
            thought = " ".join(t.text for t in event.thought)[:200]
        except Exception:
            pass
        return f"⚙️ {tool} — {thought}".strip(" —")
    if name == "ObservationEvent":
        try:
            content = event.observation.text[:300]
        except Exception:
            content = ""
        if content.strip():
            return f"↳ {content.strip()[:300]}"
        return None
    if name == "AgentErrorEvent":
        return f"⚠️ {getattr(event, 'error', '')[:300]}"
    if name == "ConversationErrorEvent":
        return f"⚠️ {getattr(event, 'detail', '')[:300]}"
    return None


def build_events(prompt: str, project_name: str, session_id: str):
    """يشغّل البناء في خيط منفصل ويبث أحداث التقدّم."""
    workspace = DATA_DIR / "projects" / _safe_name(project_name)
    workspace.mkdir(parents=True, exist_ok=True)
    persistence = DATA_DIR / "conversations" / _safe_name(session_id)
    persistence.mkdir(parents=True, exist_ok=True)

    events: queue.Queue = queue.Queue()
    summary: dict = {"text": ""}

    def on_event(event) -> None:
        line = _summarize_event(event)
        if line:
            events.put(("log", line))
        name = type(event).__name__
        if name == "MessageEvent":
            try:
                if event.source == "agent":
                    summary["text"] = event.llm_message.content[0].text
            except Exception:
                pass
        elif name == "ActionEvent" and getattr(event, "tool_name", "") == "finish":
            message = getattr(event.action, "message", None)
            if message:
                summary["text"] = message

    def worker() -> None:
        try:
            from openhands.sdk import Conversation

            conv = Conversation(
                agent=build_agent(),
                workspace=str(workspace),
                persistence_dir=str(persistence),
                callbacks=[on_event],
            )
            conv.send_message(prompt)
            conv.run()
            events.put(("done", summary["text"]))
        except Exception as exc:  # noqa: BLE001
            events.put(("error", f"{type(exc).__name__}: {exc}"))

    threading.Thread(target=worker, daemon=True).start()
    while True:
        kind, payload = events.get()
        yield (kind, payload, str(workspace))
        if kind in {"done", "error"}:
            return


def _safe_name(name: str) -> str:
    cleaned = "".join(c if (c.isalnum() or c in "-_") else "-" for c in (name or "").strip())
    return cleaned.strip("-")[:48] or "project"


def project_files(project_name: str) -> list[str]:
    root = DATA_DIR / "projects" / _safe_name(project_name)
    if not root.exists():
        return []
    return sorted(
        str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
    )

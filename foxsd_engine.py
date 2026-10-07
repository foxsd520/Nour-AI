"""محرّك FoxSD الداخلي — مستقل بالكامل بلا أي اعتماد خارجي.

FoxSD | foxsd520@gmail.com
"""

from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

MAX_OUTPUT = 6000


# ---------------------------------------------------------------- العميل

def _endpoint(base_url: str) -> str:
    base = (base_url or "").rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    return f"{base}/chat/completions"


def chat_stream(
    api_key: str,
    base_url: str,
    model: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    temperature: float = 0.3,
    timeout: int = 600,
):
    """يبث رد المحرّك عبر بروتوكول محادثة قياسي.

    يُنتج: ("token", نص) لكل مقطع نصي، ثم ("tool", {...}) لكل استدعاء أداة مكتمل.
    """
    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    request = urllib.request.Request(
        _endpoint(base_url),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    calls: dict[int, dict] = {}
    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw in response:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if not data or data == "[DONE]":
                continue
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            choices = chunk.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            if delta.get("content"):
                yield ("token", delta["content"])
            for tc in delta.get("tool_calls") or []:
                index = tc.get("index", 0)
                slot = calls.setdefault(index, {"id": "", "name": "", "arguments": ""})
                if tc.get("id"):
                    slot["id"] = tc["id"]
                fn = tc.get("function") or {}
                if fn.get("name"):
                    slot["name"] = fn["name"]
                if fn.get("arguments"):
                    slot["arguments"] += fn["arguments"]

    for index in sorted(calls):
        slot = calls[index]
        if slot["name"]:
            slot["id"] = slot["id"] or f"call_{index}"
            yield ("tool", slot)


def complete(
    api_key: str,
    base_url: str,
    model: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    temperature: float = 0.3,
    timeout: int = 600,
) -> str:
    """إجابة كاملة (بلا بث) — تجمع المقاطع النصية."""
    text = ""
    for kind, payload in chat_stream(
        api_key, base_url, model, messages, tools, temperature, timeout
    ):
        if kind == "token":
            text += payload
    return text


# ---------------------------------------------------------------- الأدوات

def _clip(text: str) -> str:
    text = text or ""
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n…(اقتُطع، الطول الكلي {len(text)} حرف)"


def _resolve(workspace: Path, path: str, unrestricted: bool = False) -> Path:
    target = (workspace / path).resolve()
    if unrestricted:
        return target
    root = workspace.resolve()
    if target != root and root not in target.parents:
        raise ValueError("المسار خارج مساحة المشروع")
    return target


def tool_terminal(workspace: Path, command: str, timeout: int = 300) -> str:
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return f"انتهت المهلة بعد {timeout} ثانية."
    parts = [f"exit={proc.returncode}"]
    if proc.stdout.strip():
        parts.append(f"stdout:\n{proc.stdout}")
    if proc.stderr.strip():
        parts.append(f"stderr:\n{proc.stderr}")
    return _clip("\n".join(parts))


def tool_create_file(workspace: Path, path: str, content: str, unrestricted: bool = False) -> str:
    target = _resolve(workspace, path, unrestricted)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, "utf-8")
    return f"تم إنشاء {path} ({len(content)} حرف, {len(content.splitlines())} سطر)."


def tool_read_file(workspace: Path, path: str, start: int = 1, end: int = 0,
                   unrestricted: bool = False) -> str:
    target = _resolve(workspace, path, unrestricted)
    if not target.is_file():
        return f"الملف غير موجود: {path}"
    lines = target.read_text("utf-8", errors="replace").splitlines()
    stop = end if end and end >= start else len(lines)
    window = lines[start - 1 : stop]
    body = "\n".join(f"{i + start:>4}  {ln}" for i, ln in enumerate(window))
    return _clip(body)


def tool_list_files(workspace: Path, path: str = ".", unrestricted: bool = False) -> str:
    target = _resolve(workspace, path, unrestricted)
    if not target.exists():
        return f"المسار غير موجود: {path}"
    if target.is_file():
        return path
    items = sorted(target.rglob("*"))
    rows = [
        f"{'DIR ' if p.is_dir() else '    '}{p.relative_to(target)}"
        for p in items
        if ".git" not in p.parts and "__pycache__" not in p.parts
    ]
    return _clip("\n".join(rows) or "(فارغ)")


def tool_delete_file(workspace: Path, path: str, unrestricted: bool = False) -> str:
    target = _resolve(workspace, path, unrestricted)
    if target.is_file():
        target.unlink()
        return f"حُذف {path}"
    return f"الملف غير موجود: {path}"


AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": "تشغيل أمر في الطرفية داخل مجلد المشروع (تنفيذ، تثبيت، اختبار).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "الأمر المطلوب تنفيذه"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "إنشاء ملف أو استبداله بمحتوى كامل، مع إنشاء المجلدات الناقصة.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "مسار الملف داخل المشروع"},
                    "content": {"type": "string", "description": "المحتوى الكامل للملف"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "قراءة ملف لعرض محتواه بترقيم الأسطر.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "start": {"type": "integer", "description": "أول سطر (افتراضي 1)"},
                    "end": {"type": "integer", "description": "آخر سطر (0 = النهاية)"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "سرد ملفات ومجلدات المشروع.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "المجلد (افتراضي الجذر)"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "حذف ملف من المشروع.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "إنهاء المهمة وإعلان الانتهاء مع ملخص نهائي للمستخدم.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "الملخص النهائي للمستخدم"}
                },
                "required": ["message"],
            },
        },
    },
]

_TOOL_IMPL = {
    "terminal": lambda ws, a, u: tool_terminal(ws, a.get("command", "")),
    "create_file": lambda ws, a, u: tool_create_file(
        ws, a.get("path", ""), a.get("content", ""), u
    ),
    "read_file": lambda ws, a, u: tool_read_file(
        ws, a.get("path", ""), int(a.get("start", 1) or 1), int(a.get("end", 0) or 0), u
    ),
    "list_files": lambda ws, a, u: tool_list_files(ws, a.get("path", "."), u),
    "delete_file": lambda ws, a, u: tool_delete_file(ws, a.get("path", ""), u),
}


def execute_tool(workspace: Path, name: str, arguments: str,
                 unrestricted: bool = False) -> str:
    if name == "finish":
        return ""
    impl = _TOOL_IMPL.get(name)
    if not impl:
        return f"أداة غير معروفة: {name}"
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError:
        return "تعذّر قراءة معاملات الأداة."
    try:
        return impl(workspace, args, unrestricted)
    except Exception as exc:  # noqa: BLE001
        return f"خطأ في تنفيذ {name}: {type(exc).__name__}: {exc}"


# ---------------------------------------------------------------- حلقة الوكيل

def _brief(name: str, args: dict) -> str:
    if name == "terminal":
        return f"$ {str(args.get('command', ''))[:160]}"
    if name in {"create_file", "read_file", "delete_file"}:
        return str(args.get("path", ""))
    if name == "list_files":
        return str(args.get("path", "."))
    return ""


def run_agent(
    workspace: Path,
    messages: list[dict],
    api_key: str,
    base_url: str,
    model: str,
    on_event=None,
    max_steps: int = 40,
    temperature: float = 0.3,
    unrestricted: bool = False,
) -> str:
    """يشغّل الوكيل حتى إعلان الانتهاء. يعيد الملخص النهائي."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    convo = list(messages)
    last_text = ""

    def emit(kind: str, **data) -> None:
        if on_event:
            on_event({"type": kind, **data})

    for step in range(max_steps):
        text = ""
        tool_calls: list[dict] = []
        for kind, payload in chat_stream(
            api_key, base_url, model, convo, AGENT_TOOLS, temperature
        ):
            if kind == "token":
                text += payload
                emit("token", text=payload)
            elif kind == "tool":
                tool_calls.append(payload)

        last_text = text or last_text
        assistant: dict = {"role": "assistant", "content": text or ""}
        if tool_calls:
            assistant["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in tool_calls
            ]
        convo.append(assistant)

        if not tool_calls:
            emit("done", text=text)
            return text

        for tc in tool_calls:
            if tc["name"] == "finish":
                try:
                    args = json.loads(tc["arguments"] or "{}")
                except json.JSONDecodeError:
                    args = {}
                summary = args.get("message") or text or "تم"
                emit("done", text=summary)
                return summary

            try:
                args = json.loads(tc["arguments"] or "{}")
            except json.JSONDecodeError:
                args = {}
            emit("tool", name=tc["name"], brief=_brief(tc["name"], args))
            result = execute_tool(workspace, tc["name"], tc["arguments"], unrestricted)
            emit("result", name=tc["name"], text=result)
            convo.append(
                {"role": "tool", "tool_call_id": tc["id"], "content": result}
            )

    emit("done", text=last_text)
    return last_text

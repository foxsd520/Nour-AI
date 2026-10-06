"""خادم Nour-AI — واجهة المحادثة والبناء. FoxSD."""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

import nour_core as core

app = FastAPI(title=f"{core.BRAND['agent']} — {core.BRAND['company']}", docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WEB_FILE = Path(__file__).with_name("nour_web.html")


def sse(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


class ChatIn(BaseModel):
    session_id: str = "default"
    message: str


class BuildIn(BaseModel):
    session_id: str = "default"
    project_name: str
    brief: str


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return WEB_FILE.read_text("utf-8")


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "agent": core.BRAND["agent"],
        "company": core.BRAND["company"],
        "email": core.BRAND["email"],
        "engine_ready": core.engine_ready(),
    }


@app.get("/api/history")
def history(session_id: str = "default") -> dict:
    return {"messages": core.load_history(session_id)}


@app.post("/api/chat")
def chat(req: ChatIn) -> StreamingResponse:
    message = req.message.strip()
    if not message:
        raise HTTPException(400, "الرسالة فارغة")
    session_id = req.session_id or "default"
    convo = core.load_history(session_id)
    convo.append({"role": "user", "content": message})

    def generate():
        reply = ""
        tool = None
        try:
            for kind, payload in core.stream_chat(convo):
                if kind == "token":
                    reply += payload
                    yield sse({"type": "token", "text": payload})
                elif kind == "tool":
                    tool = payload
        except Exception as exc:  # noqa: BLE001
            yield sse({"type": "error", "text": f"تعذّر الاتصال بمحرّك FoxSD: {exc}"})
            return

        if tool and tool["name"] == "build_project":
            yield sse({"type": "build_start"})
            try:
                args = json.loads(tool["arguments"] or "{}")
            except json.JSONDecodeError:
                args = {}
            project = args.get("project_name", "project")
            brief = args.get("brief") or message
            for kind, payload, _ws in core.build_events(brief, project, session_id):
                if kind == "log":
                    yield sse({"type": "log", "text": payload})
                elif kind == "done":
                    files = core.project_files(project)
                    convo.append({"role": "assistant", "content": payload or reply})
                    core.save_history(session_id, convo)
                    yield sse(
                        {
                            "type": "done",
                            "text": payload,
                            "project": project,
                            "files": files,
                        }
                    )
                elif kind == "error":
                    yield sse({"type": "error", "text": payload})
            return

        convo.append({"role": "assistant", "content": reply})
        core.save_history(session_id, convo)
        yield sse({"type": "done", "text": reply})

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/build")
def build(req: BuildIn) -> StreamingResponse:
    def generate():
        for kind, payload, _ws in core.build_events(req.brief, req.project_name, req.session_id):
            if kind == "log":
                yield sse({"type": "log", "text": payload})
            elif kind == "done":
                yield sse(
                    {
                        "type": "done",
                        "text": payload,
                        "project": req.project_name,
                        "files": core.project_files(req.project_name),
                    }
                )
            else:
                yield sse({"type": "error", "text": payload})

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/projects/{project}/files")
def project_files(project: str) -> dict:
    return {"project": project, "files": core.project_files(project)}


@app.get("/api/projects/{project}/file")
def project_file(project: str, path: str) -> dict:
    root = core.DATA_DIR / "projects" / core._safe_name(project)
    target = (root / path).resolve()
    if not str(target).startswith(str(root.resolve())) or not target.is_file():
        raise HTTPException(404, "الملف غير موجود")
    return {"path": path, "content": target.read_text("utf-8", errors="replace")[:20000]}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

"""خادم Nour-AI — واجهة المحادثة والبناء الحقيقي.

FoxSD | foxsd520@gmail.com
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import nour_core as core

app = FastAPI(
    title=f"{core.BRAND['name']} — {core.BRAND['company']}",
    docs_url=None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WEB_FILE = Path(__file__).with_name("nour_web.html")
SITE_DIR = Path(__file__).with_name("site")
if SITE_DIR.is_dir():
    app.mount("/site", StaticFiles(directory=str(SITE_DIR), html=True), name="site")


def sse(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


class ChatIn(BaseModel):
    session_id: str = "default"
    message: str


class BuildIn(BaseModel):
    session_id: str = "default"
    request: str


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return WEB_FILE.read_text("utf-8")


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "agent": core.BRAND["name"],
        "company": core.BRAND["company"],
        "email": core.BRAND["email"],
        "engine_ready": core.engine_ready(),
    }


@app.get("/api/sessions")
def sessions() -> dict:
    return {"sessions": core.list_sessions()}


@app.get("/api/history")
def history(session_id: str = "default") -> dict:
    return core.load_session(session_id)


@app.post("/api/chat")
def chat(req: ChatIn) -> StreamingResponse:
    message = req.message.strip()
    if not message:
        raise HTTPException(400, "الرسالة فارغة")
    session = core.load_session(req.session_id or "default")
    session["id"] = req.session_id or "default"
    if not session.get("messages"):
        session["title"] = message[:40]
    build = core.looks_like_build(message)

    def generate() -> object:
        if build:
            yield sse({"type": "build_start", "message": message})
            result = core.build_project(message, on_event=None)
            session.setdefault("messages", []).append(
                {"role": "user", "content": message}
            )
            session["messages"].append(
                {"role": "assistant", "content": result["summary"]}
            )
            core.save_session(session["id"], session)
            yield sse(
                {
                    "type": "done",
                    "text": result["summary"],
                    "project": result["slug"],
                    "files": result["files"],
                }
            )
            return

        queue: list[dict] = []
        result = core.chat_turn(
            session, message, on_event=lambda e: queue.append(e)
        )
        for event in queue:
            if event.get("type") == "token":
                yield sse({"type": "token", "text": event["text"]})
        core.save_session(session["id"], session)
        yield sse({"type": "done", "text": result})

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/build")
def build(req: BuildIn) -> StreamingResponse:
    request = req.request.strip()
    if not request:
        raise HTTPException(400, "الطلب فارغ")

    def generate() -> object:
        yield sse({"type": "build_start", "message": request})
        result = core.build_project(request)
        yield sse(
            {
                "type": "done",
                "text": result["summary"],
                "project": result["slug"],
                "files": result["files"],
            }
        )

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/projects/{project}/files")
def project_files(project: str) -> dict:
    root = core.PROJECTS_DIR / Path(project).name
    if not root.is_dir():
        raise HTTPException(404, "المشروع غير موجود")
    files = sorted(
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts
    )
    return {"project": root.name, "files": files}


@app.get("/api/projects/{project}/file")
def project_file(project: str, path: str) -> dict:
    root = (core.PROJECTS_DIR / Path(project).name).resolve()
    target = (root / path).resolve()
    if root not in target.parents or not target.is_file():
        raise HTTPException(404, "الملف غير موجود")
    return {
        "path": path,
        "content": target.read_text("utf-8", errors="replace")[:20000],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

#!/usr/bin/env python
"""Nour-AI — الوكيل الطرفي (CLI). FoxSD | foxsd520@gmail.com"""

from __future__ import annotations

import argparse
import sys

import nour_core


def _on_event(event: dict) -> None:
    kind = event.get("type")
    if kind == "token":
        sys.stdout.write(event.get("text", ""))
        sys.stdout.flush()
    elif kind == "tool":
        print(f"\n⚙ {event.get('name')}: {event.get('brief', '')}")
    elif kind == "result":
        text = event.get("text", "")
        preview = text if len(text) < 400 else text[:400] + "…"
        print(f"↳ {preview}")
    elif kind == "start":
        print(f"📁 {event.get('path')}")


def banner() -> None:
    print("=" * 52)
    print(f"  {nour_core.BRAND['name']} — وكيل ذكاء اصطناعي تجاري")
    print(f"  {nour_core.BRAND['company']} | {nour_core.BRAND['email']}")
    print("=" * 52)
    print(" اكتب طلبك بالعربية. للخروج: /exit")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Nour-AI CLI — FoxSD")
    parser.add_argument("request", nargs="*", help="طلب واحد ثم خروج")
    parser.add_argument("--build", action="store_true", help="إجبار طور البناء")
    parser.add_argument("--workspace", default="", help="مجلد البناء")
    args = parser.parse_args()

    if not nour_core.engine_ready():
        print("محرّك FoxSD غير مهيأ. تواصل معنا: foxsd520@gmail.com")
        return 1

    if args.workspace:
        import os

        os.environ["NOUR_DATA_DIR"] = args.workspace

    if args.request:
        text = " ".join(args.request)
        if args.build or nour_core.looks_like_build(text):
            result = nour_core.build_project(text, on_event=_on_event)
            print(f"\n\n✅ {result['slug']}: {len(result['files'])} ملف")
        else:
            session = {"id": nour_core.new_session(), "messages": []}
            nour_core.chat_turn(session, text, on_event=_on_event)
            nour_core.save_session(session["id"], session)
        print()
        return 0

    banner()
    session = nour_core.load_session(nour_core.new_session())
    while True:
        try:
            text = input("أنت › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text in {"/exit", "/quit"}:
            break
        print("Nour-AI › ", end="", flush=True)
        if nour_core.looks_like_build(text):
            nour_core.build_project(text, on_event=_on_event)
        else:
            nour_core.chat_turn(session, text, on_event=_on_event)
        nour_core.save_session(session["id"], session)
        print("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

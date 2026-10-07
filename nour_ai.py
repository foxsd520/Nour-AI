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


def banner(private: bool) -> None:
    print("=" * 52)
    print(f"  {nour_core.BRAND['name']} — وكيل ذكاء اصطناعي تجاري")
    print(f"  {nour_core.BRAND['company']} | {nour_core.BRAND['email']}")
    print(f"  الوضع: {'خاص — بلا قيود 🔓' if private else 'عادي 🔒'}")
    print("=" * 52)
    print(" اكتب طلبك بالعربية. للخروج: /exit")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Nour-AI CLI — FoxSD")
    parser.add_argument("request", nargs="*", help="طلب واحد ثم خروج")
    parser.add_argument("--build", action="store_true", help="إجبار طور البناء")
    parser.add_argument("--private", action="store_true", help="الوضع الخاص بلا قيود")
    parser.add_argument("--models", action="store_true", help="طبع كتالوج النماذج")
    parser.add_argument("--workspace", default="", help="مجلد البناء")
    args = parser.parse_args()

    if args.models:
        import models

        print(models.report())
        return 0

    if not nour_core.engine_ready():
        print("محرّك FoxSD غير مهيأ. تواصل معنا: foxsd520@gmail.com")
        return 1

    if args.workspace:
        import os

        os.environ["NOUR_DATA_DIR"] = args.workspace

    private = args.private

    if args.request:
        text = " ".join(args.request)
        if args.build or nour_core.looks_like_build(text):
            result = nour_core.build_project(text, on_event=_on_event, private=private)
            print(f"\n\n✅ {result['slug']}: {len(result['files'])} ملف")
        else:
            session = {"id": nour_core.new_session(), "messages": []}
            nour_core.chat_turn(session, text, on_event=_on_event, private=private)
            nour_core.save_session(session["id"], session)
        print()
        return 0

    banner(private)
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
        if text == "/private":
            private = not private
            print(f"→ الوضع الآن: {'خاص بلا قيود 🔓' if private else 'عادي 🔒'}")
            continue
        if text == "/models":
            import models

            print(models.report())
            continue
        print("Nour-AI › ", end="", flush=True)
        if nour_core.looks_like_build(text):
            nour_core.build_project(text, on_event=_on_event, private=private)
        else:
            nour_core.chat_turn(session, text, on_event=_on_event, private=private)
        nour_core.save_session(session["id"], session)
        print("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

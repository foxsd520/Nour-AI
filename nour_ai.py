#!/usr/bin/env python3
"""Nour-AI — الوكيل الطرفي (CLI). FoxSD | foxsd520@gmail.com"""

from __future__ import annotations

import argparse
import os

from nour_core import BRAND, build_agent

BANNER = f"""
{"=" * 58}
  {BRAND['agent']}  —  وكيل البناء الذكي
  الشركة : {BRAND['company']}  ({BRAND['short']})
  التواصل: {BRAND['email']}
{"=" * 58}
  اكتب طلبك بالعربية وسأبنيه لك (برنامج / موقع / نظام).
  أوامر: /exit للخروج  |  /new لبدء محادثة جديدة
{"=" * 58}
"""


def _conversation(workspace: str):
    from openhands.sdk import Conversation

    os.makedirs(workspace, exist_ok=True)
    return Conversation(agent=build_agent(), workspace=os.path.abspath(workspace))


def run_once(prompt: str, workspace: str) -> None:
    conv = _conversation(workspace)
    conv.send_message(prompt)
    conv.run()


def run_interactive(workspace: str) -> None:
    print(BANNER)
    conv = _conversation(workspace)
    while True:
        try:
            user_input = input(f"\n[{BRAND['short']}] اكتب طلبك > ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\nوداعًا — {BRAND['company']}")
            return

        if not user_input:
            continue
        if user_input in {"/exit", "/quit"}:
            print(f"وداعًا — {BRAND['company']}")
            return
        if user_input == "/new":
            conv = _conversation(workspace)
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

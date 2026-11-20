#!/usr/bin/env python3
"""Render the miko.os profile drawings (standard library only).

    GH_TOKEN=... python scripts/profile/build.py --out assets/profile
    python scripts/profile/build.py --data data.json --out assets/profile     # offline

Writes: desktop.svg and xcode.svg (heroes), project-*.svg (cards), spotlight.svg (toolbox),
activity.svg (numbers) and messages.svg (footer).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data  # noqa: E402
import desktop  # noqa: E402
import panels  # noqa: E402
import projects  # noqa: E402
import xcode  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "mikonyaa"))
    ap.add_argument("--out", default="assets/profile")
    ap.add_argument("--data")
    a = ap.parse_args()
    if a.data:
        payload = json.load(open(a.data, encoding="utf-8"))
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("Set GH_TOKEN (or GITHUB_TOKEN) to query the GitHub API.")
        payload = data.fetch(a.login, token)
    d = data.normalize(payload)
    os.makedirs(a.out, exist_ok=True)
    by = {r["name"]: r for r in d["repos"]}
    files = {"desktop.svg": desktop.desktop(d), "xcode.svg": xcode.xcode(d), "spotlight.svg": panels.spotlight(d),
             "activity.svg": panels.activity(d), "messages.svg": panels.messages(d)}
    for pr in projects.PROJECTS:
        files[f"project-{pr['key']}.svg"] = projects.card(pr, by.get(pr["repo"], {}))
    total = 0
    for name, svg in files.items():
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write(svg)
        total += len(svg)
    print(f"rendered {len(files)} SVGs ({total // 1024} KB)")


if __name__ == "__main__":
    main()

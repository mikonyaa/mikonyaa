#!/usr/bin/env python3
"""Render the miko.os profile drawings (standard library only).

    GH_TOKEN=... python scripts/profile/build.py --out assets/profile
    python scripts/profile/build.py --data data.json --out assets/profile     # offline

Writes: xcode.svg (hero), contact-*.svg (links), project-*.svg (cards), stack.svg, activity.svg (numbers)
and console.svg (footer).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data  # noqa: E402
import extras  # noqa: E402
import projects  # noqa: E402
import showcase  # noqa: E402
import stats  # noqa: E402
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
    files = {"xcode.svg": xcode.xcode(d), "stack.svg": showcase.stack(d),
             "activity.svg": stats.activity(d), "console.svg": showcase.console(d)}
    for k in ("telegram", "email", "location"):
        files[f"contact-{k}.svg"] = extras.contact(k)
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

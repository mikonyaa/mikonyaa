"""GitHub data for the profile drawings: one GraphQL call, normalised (stdlib only)."""
from __future__ import annotations

import datetime as dt
import json
import math
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    login name
    followers { totalCount }
    following { totalCount }
    pullRequests(states: MERGED) { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        name description url stargazerCount forkCount isTemplate
        primaryLanguage { name color }
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      totalPullRequestReviewContributions restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount weekday } } }
    }
  }
}
"""

def fetch(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": f"{login}-profile-readme"})
    with urllib.request.urlopen(req, timeout=60) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload


def normalize(payload: dict) -> dict:
    u = payload["data"]["user"]
    repos = []
    for n in u["repositories"]["nodes"]:
        pl = n.get("primaryLanguage") or {}
        repos.append(dict(name=n["name"], description=n.get("description") or "", url=n["url"],
                          stars=n["stargazerCount"], forks=n["forkCount"], template=n.get("isTemplate", False),
                          language=pl.get("name"), lang_color=pl.get("color"),
                          languages=[(e["node"]["name"], e["size"], e["node"]["color"]) for e in n["languages"]["edges"]]))
    cc = u["contributionsCollection"]
    weeks = [[(dd["date"], dd["contributionCount"], dd["weekday"]) for dd in w["contributionDays"]]
             for w in cc["contributionCalendar"]["weeks"]]
    days = [d for w in weeks for d in w]
    return dict(
        login=u["login"], name=u.get("name") or u["login"],
        followers=u["followers"]["totalCount"], following=u["following"]["totalCount"],
        merged_prs=u["pullRequests"]["totalCount"],
        repos=repos, repo_count=u["repositories"]["totalCount"],
        stars=sum(r["stars"] for r in repos), forks=sum(r["forks"] for r in repos),
        templates=sum(1 for r in repos if r["template"]),
        contrib=dict(total=cc["contributionCalendar"]["totalContributions"],
                     commits=cc["totalCommitContributions"], prs=cc["totalPullRequestContributions"],
                     issues=cc["totalIssueContributions"], reviews=cc["totalPullRequestReviewContributions"],
                     weeks=weeks, days=days),
        generated=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
    )


LANG_EXCLUDE = {"HTML", "CSS", "SCSS", "Shell", "Makefile", "Dockerfile", "Batchfile"}


def language_shares(repos, top=4):
    """sqrt(bytes) per repo so one huge repo can't drown the rest; JavaScript inside
    a TypeScript repo is treated as build/config output and skipped."""
    score = {}
    for r in repos:
        names = {n for n, _, _ in r["languages"]}
        for name, size, _ in r["languages"]:
            if name in LANG_EXCLUDE or (name == "JavaScript" and "TypeScript" in names):
                continue
            score[name] = score.get(name, 0) + math.sqrt(size)
    tot = sum(score.values()) or 1
    items = sorted(score.items(), key=lambda kv: -kv[1])
    out = [(n, v / tot) for n, v in items[:top]]
    rest = sum(v for _, v in items[top:]) / tot
    if rest > 0.004:
        out.append(("Other", rest))
    return out


def streaks(days):
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur = 0
    for i, (_, c) in enumerate(reversed(days)):
        if c > 0:
            cur += 1
        elif i == 0:
            continue
        else:
            break
    return longest, cur


def _levels(weeks):
    counts = sorted(n for wk in weeks for _, n, _ in wk if n > 0) or [1]
    q = [counts[int(len(counts) * f)] for f in (0.25, 0.5, 0.75)]

    def lv(n):
        if n == 0:
            return 0
        for i, th in enumerate(q, 1):
            if n <= th:
                return i
        return 4
    return lv, counts[-1]



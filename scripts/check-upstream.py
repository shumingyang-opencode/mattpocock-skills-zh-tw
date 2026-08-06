#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare upstream mattpocock/skills against the version we are aligned to,
and write docs/upstream-status.json (translation TODO + version status).

Pure detection — it does NOT translate, sync files, or rebuild the site.

How it works:
  - aligned.commit (from docs/upstream-status.json) is the upstream commit our
    translations were made from.
  - Diff upstream tree @ aligned.commit vs upstream tree @ main.
  - .md changes -> "pending" TODO entries (translate / new-skill / rename / remove)
  - non-.md changes -> only a counter (synced later by the update flow)
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "docs" / "upstream-status.json"
UPSTREAM = "mattpocock/skills"
BRANCH = "main"
API = "https://api.github.com/repos"

HEADERS = {"User-Agent": "mattpocock-skills-zh-tw-check", "Accept": "application/vnd.github+json"}


def get(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def tree_sha_map(ref: str):
    """path -> blob sha at a commit/ref (only blobs)."""
    data = get(f"{API}/{UPSTREAM}/git/trees/{ref}?recursive=1")
    return {t["path"]: t["sha"] for t in data.get("tree", []) if t["type"] == "blob"}


def latest_release():
    try:
        r = get(f"{API}/{UPSTREAM}/releases/latest")
        return r.get("tag_name") or "", r.get("published_at") or ""
    except Exception:
        try:
            tags = get(f"{API}/{UPSTREAM}/tags")
            return tags[0]["name"], ""
        except Exception:
            return "", ""


def main():
    prev = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    aligned = prev.get("aligned", {})
    aligned_commit = aligned.get("commit")
    if not aligned_commit:
        print("no aligned.commit in docs/upstream-status.json; aborting")
        return 1

    head = get(f"{API}/{UPSTREAM}/commits/{BRANCH}")["sha"]
    release, released_at = latest_release()

    print(f"aligned: {aligned.get('release')} @ {aligned_commit[:7]}")
    print(f"upstream main: {head[:7]}  release: {release}  ({released_at[:10]})")

    old = tree_sha_map(aligned_commit)
    new = tree_sha_map(head)

    added = [p for p in new if p not in old]
    removed = [p for p in old if p not in new]
    modified = [p for p in new if p in old and old[p] != new[p]]

    pending = []
    non_md_count = 0

    def is_md(p):
        return p.endswith(".md")

    # --- rename detection (.md only): added path whose content sha matches a removed path ---
    removed_md = {p: old[p] for p in removed if is_md(p)}   # sha -> [paths]
    added_md = {p: new[p] for p in added if is_md(p)}       # path -> sha
    old_by_sha = {}
    for p, sha in removed_md.items():
        old_by_sha.setdefault(sha, []).append(p)

    renamed_new = set()
    for p, sha in sorted(added_md.items()):
        if sha in old_by_sha:
            for src in old_by_sha[sha]:
                pending.append({"kind": "rename", "from": src, "to": p, "reason": "rename"})
            renamed_new.add(p)
            old_by_sha.pop(sha, None)

    # remaining added .md -> translate / new-skill
    for p in sorted(added_md):
        if p in renamed_new:
            continue
        if p.endswith("/SKILL.md") and p.startswith("skills/"):
            pending.append({"kind": "new-skill", "path": p, "reason": "added",
                            "note": "需翻譯＋加入 registry（blurb/level/inv）"})
        else:
            pending.append({"kind": "translate", "path": p, "reason": "added"})

    # remaining removed .md -> remove
    removed_left = [p for paths in old_by_sha.values() for p in paths]
    for p in sorted(removed_left):
        pending.append({"kind": "remove", "path": p, "reason": "deleted"})

    # modified .md -> translate
    for p in sorted(modified):
        if is_md(p):
            pending.append({"kind": "translate", "path": p, "reason": "modified"})
        else:
            non_md_count += 1

    non_md_count += sum(1 for p in added if not is_md(p))
    non_md_count += sum(1 for p in removed if not is_md(p))
    non_md_count += sum(1 for p in modified if not is_md(p))

    status = {
        "aligned": aligned,
        "upstream": {"release": release, "commit": head, "date": released_at[:10]},
        "up_to_date": head == aligned_commit,
        "pending": pending,
        "non_md_count": non_md_count,
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\npending: {len(pending)}  non-md changes: {non_md_count}  up_to_date: {status['up_to_date']}")
    for e in pending:
        print(f"  [{e['kind']}] {e.get('from', '')}{' -> ' if e['kind']=='rename' else ''}{e['path']} ({e['reason']})")
    print(f"\nwrote {STATUS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

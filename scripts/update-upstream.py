#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update flow (mechanical parts) — run when you ask to "update upstream".

Default mode:
  1. Sync non-.md files from upstream (add / modify / delete).
  2. Apply rename / remove TODO entries to .md files (preserving translations).
  3. Clear the EN cache so build-site.py re-fetches the latest English.
  4. Print the translation TODO (new / modified .md + new skills needing registry entries)
     for the agent to complete.

--finalize mode (after translation + registry edits + site rebuild):
  Set aligned = upstream head, clear pending, write docs/upstream-status.json.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "docs" / "upstream-status.json"
CACHE = ROOT / ".site-cache"
UPSTREAM = "mattpocock/skills"
BRANCH = "main"
API = "https://api.github.com/repos"
RAW = "https://raw.githubusercontent.com"
HEADERS = {"User-Agent": "mattpocock-skills-zh-tw-update", "Accept": "application/vnd.github+json"}


def get(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def tree_sha_map(ref: str):
    data = get(f"{API}/{UPSTREAM}/git/trees/{ref}?recursive=1")
    return {t["path"]: t["sha"] for t in data.get("tree", []) if t["type"] == "blob"}


def fetch_raw(path: str) -> bytes:
    url = f"{RAW}/{UPSTREAM}/{BRANCH}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "mattpocock-skills-zh-tw-update"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    if "--finalize" in sys.argv:
        return finalize()

    st = json.loads(STATUS.read_text(encoding="utf-8"))
    aligned = st.get("aligned", {})
    pending = st.get("pending", [])
    aligned_commit = aligned.get("commit")
    if not aligned_commit:
        print("no aligned.commit; aborting")
        return 1

    head = get(f"{API}/{UPSTREAM}/commits/{BRANCH}")["sha"]
    old = tree_sha_map(aligned_commit)
    new = tree_sha_map(head)

    added = [p for p in new if p not in old]
    removed = [p for p in old if p not in new]
    modified = [p for p in new if p in old and old[p] != new[p]]

    # 1) sync non-.md files
    non_md = [p for p in added if not p.endswith(".md")] + [p for p in modified if not p.endswith(".md")]
    non_md_removed = [p for p in removed if not p.endswith(".md")]
    for p in non_md:
        target = ROOT / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(fetch_raw(p))
        print(f"  sync+  {p}")
    for p in non_md_removed:
        target = ROOT / p
        if target.exists():
            target.unlink()
            print(f"  sync-  {p}")

    # 2) apply rename / remove TODO on .md (keep translations)
    for e in pending:
        kind = e.get("kind")
        if kind == "rename":
            src = ROOT / e["from"]
            dst = ROOT / e["to"]
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                src.rename(dst)
                print(f"  move   {e['from']} -> {e['to']}")
            else:
                print(f"  SKIP (no local file) {e['from']}")
        elif kind == "remove":
            src = ROOT / e["path"]
            if src.exists():
                src.unlink()
                print(f"  remove {e['path']}")
            else:
                print(f"  SKIP (no local file) {e['path']}")

    # 3) clear EN cache so build-site re-fetches
    if CACHE.exists():
        for f in CACHE.iterdir():
            f.unlink()
        print("  cache cleared (.site-cache)")

    # 4) report translation TODO
    print("\n--- 待翻譯 / 整理（由 agent 完成）---")
    todo = [e for e in pending if e.get("kind") in ("translate", "new-skill")]
    for e in todo:
        print(f"  [{e['kind']}] {e['path']} ({e.get('reason', '')}){(' | ' + e['note']) if e.get('note') else ''}")
    if not todo:
        print("  （無）")
    renames = [e for e in pending if e.get("kind") == "rename"]
    if renames:
        print("  已套用 rename 的檔案，請檢查翻譯內容是否需要微調。")
    print("\n翻譯完成、registry 更新並重建網站後，執行：")
    print("  python scripts/update-upstream.py --finalize")
    return 0


def finalize():
    st = json.loads(STATUS.read_text(encoding="utf-8"))
    head = get(f"{API}/{UPSTREAM}/commits/{BRANCH}")["sha"]
    release = ""
    try:
        release = get(f"{API}/{UPSTREAM}/releases/latest").get("tag_name", "")
    except Exception:
        pass
    st["aligned"] = {"release": release or st["upstream"].get("release", "?"),
                     "commit": head,
                     "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    st["upstream"] = {"release": release, "commit": head,
                      "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    st["up_to_date"] = True
    st["pending"] = []
    st["non_md_count"] = 0
    st["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    STATUS.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"finalized: aligned = {st['aligned']['release']} @ {head[:7]}, pending cleared")
    return 0


if __name__ == "__main__":
    sys.exit(main())

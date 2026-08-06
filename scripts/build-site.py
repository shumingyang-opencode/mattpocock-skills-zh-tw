#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the bilingual (EN/ZH-TW) static site for mattpocock-skills-zh-tw.

Reads the translated (zh-TW) Markdown in this repo + fetches the English
originals from upstream mattpocock/skills, aligns them block-by-block, and
writes static HTML at the repo root (served by GitHub Pages):

  index.html            — landing page (two entry cards)
  map.html              — the highway "skill map" view
  learning-path.html    — the categorized learning-path card view
  <skill>/SKILL.html    — bilingual skill page per skill
  <skill>/<NAME>.html   — bilingual page per attached doc
  assets/skills-data.json — machine-readable skill registry

Run:  python scripts/build-site.py
English sources are cached under .site-cache/ so re-runs work offline.
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".site-cache"
UPSTREAM_BASE = "https://raw.githubusercontent.com/mattpocock/skills/main"

# --------------------------------------------------------------------------
# Skill registry: name -> metadata
# cat: engineering | productivity | misc | in-progress
# level: L0 | L1 | L2 | L3 | L4 | support | vocab | misc | in-progress
# inv: user | model
# title: short zh-TW title (used on map nodes and cards)
# --------------------------------------------------------------------------
SKILLS = {
    # --- engineering ---
    "setup-matt-pocock-skills":          {"cat": "engineering", "level": "L0", "inv": "user",  "title": "前置設定"},
    "ask-matt":                          {"cat": "engineering", "level": "L1", "inv": "user",  "title": "技能路由器"},
    "grill-with-docs":                   {"cat": "engineering", "level": "L1", "inv": "user",  "title": "詰問 · 產文件"},
    "grilling":                          {"cat": "productivity", "level": "L1", "inv": "model", "title": "詰問原語"},
    "grill-me":                          {"cat": "productivity", "level": "L1", "inv": "user",  "title": "個人詰問"},
    "to-spec":                           {"cat": "engineering", "level": "L2", "inv": "user",  "title": "生成規格"},
    "to-tickets":                        {"cat": "engineering", "level": "L2", "inv": "user",  "title": "拆分 Ticket"},
    "wayfinder":                         {"cat": "engineering", "level": "L2", "inv": "user",  "title": "尋路 · 大規劃"},
    "triage":                            {"cat": "engineering", "level": "L2", "inv": "user",  "title": "分診"},
    "to-questionnaire":                  {"cat": "productivity", "level": "L2", "inv": "user",  "title": "轉成問卷"},
    "implement":                         {"cat": "engineering", "level": "L3", "inv": "user",  "title": "實作"},
    "tdd":                               {"cat": "engineering", "level": "L3", "inv": "model", "title": "測試驅動開發"},
    "prototype":                         {"cat": "engineering", "level": "L3", "inv": "model", "title": "可拋棄原型"},
    "handoff":                           {"cat": "productivity", "level": "L3", "inv": "user",  "title": "會話交接"},
    "diagnosing-bugs":                   {"cat": "engineering", "level": "L3", "inv": "model", "title": "故障診斷"},
    "code-review":                       {"cat": "engineering", "level": "L4", "inv": "model", "title": "程式碼審查"},
    "resolving-merge-conflicts":         {"cat": "engineering", "level": "L4", "inv": "model", "title": "解決合併衝突"},
    "improve-codebase-architecture":     {"cat": "engineering", "level": "L4", "inv": "user",  "title": "架構維護"},
    "codebase-design":                   {"cat": "engineering", "level": "vocab", "inv": "model", "title": "深模組設計"},
    "domain-modeling":                   {"cat": "engineering", "level": "vocab", "inv": "model", "title": "領域建模"},
    "research":                          {"cat": "engineering", "level": "support", "inv": "model", "title": "背景研究"},
    "wizard":                            {"cat": "engineering", "level": "support", "inv": "model", "title": "互動精靈"},
    "writing-for-agents":                {"cat": "productivity", "level": "support", "inv": "model", "title": "為代理寫作"},
    "teach":                             {"cat": "productivity", "level": "support", "inv": "user",  "title": "多階段教學"},
    "wait-what":                         {"cat": "productivity", "level": "support", "inv": "user",  "title": "重新闡述"},
    # --- misc ---
    "setup-pre-commit":                  {"cat": "misc", "level": "misc", "inv": "user", "title": "設定 pre-commit"},
    "scaffold-exercises":                {"cat": "misc", "level": "misc", "inv": "user", "title": "練習骨架"},
    "migrate-to-shoehorn":               {"cat": "misc", "level": "misc", "inv": "user", "title": "遷移至 Shoehorn"},
    "git-guardrails-claude-code":        {"cat": "misc", "level": "misc", "inv": "user", "title": "Git 安全鉤子"},
    # --- in-progress ---
    "claude-handoff":                    {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "Claude 交接"},
    "loop-me":                           {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "詰問我"},
    "setup-ts-deep-modules":             {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "深模組建置"},
    "writing-beats":                     {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "寫作 · 節拍"},
    "writing-fragments":                 {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "寫作 · 碎片"},
    "writing-shape":                     {"cat": "in-progress", "level": "in-progress", "inv": "user", "title": "寫作 · 成型"},
}

# Map layout (highway diagram). Each row is {"left": [...], "center": [...], "right": [...]}
# center entries may be "name" or ["name1", "↔", "name2"]; each node may carry a kind.
MAINLINE = [
    {"left": ["diagnosing-bugs", "improve-codebase-architecture", "wayfinder"],
     "center": ["grill-with-docs", "grill-me"], "right": ["triage"]},
    {"left": [], "center": ["prototype", "↔", "handoff"], "right": None, "service": True},
    {"left": [], "center": ["to-spec"], "right": None},
    {"left": [], "center": ["to-tickets"], "right": None},
    {"left": [], "center": ["implement", "→", "tdd"], "right": None},
    {"left": [], "center": ["code-review"], "right": None},
]
RAMPS = ["diagnosing-bugs", "improve-codebase-architecture", "wayfinder"]
FOUNDATION = ["domain-modeling", "codebase-design"]
STANDALONE = ["research", "teach", "resolving-merge-conflicts", "to-questionnaire", "wait-what", "wizard"]
META = ["writing-for-agents"]

LEGEND = [
    ("mainline", "主流程 Mainline", "highway"),
    ("ramp", "進入匝道 On-ramp", "ramp"),
    ("service", "繞道服務區 Service", "service"),
    ("standalone", "獨立技能 Standalone", "standalone"),
    ("meta", "元技能 Meta", "meta"),
    ("dash", "詞彙層 Vocabulary (dashed)", "dash"),
]

LEVELS = [
    ("L0", "前置", "Prerequisite", "green", ["setup-matt-pocock-skills"]),
    ("L1", "起手", "Start here — align on the idea", "", ["ask-matt", "grill-with-docs", "grill-me", "grilling"]),
    ("L2", "規劃", "Plan — spec, tickets, route", "", ["to-spec", "to-tickets", "wayfinder", "triage", "to-questionnaire"]),
    ("L3", "執行", "Build — test-first, prototype, debug", "", ["implement", "tdd", "prototype", "handoff", "diagnosing-bugs"]),
    ("L4", "收尾", "Finish — review, maintain, unblock", "", ["code-review", "resolving-merge-conflicts", "improve-codebase-architecture"]),
    ("vocab", "詞彙層", "Vocabulary — the two references beneath the flows", "purple", ["domain-modeling", "codebase-design"]),
    ("support", "支援層", "Support — reach-for-anytime standalones", "green", ["research", "teach", "wizard", "wait-what", "writing-for-agents"]),
    ("misc", "雜項工具", "Misc — kept around, not promoted", "amber", ["setup-pre-commit", "scaffold-exercises", "migrate-to-shoehorn", "git-guardrails-claude-code"]),
    ("in-progress", "進行中", "In-progress — beta, feedback wanted", "amber", ["claude-handoff", "loop-me", "setup-ts-deep-modules", "writing-beats", "writing-fragments", "writing-shape"]),
]

ATTACHED = {
    "ask-matt": ["PHASE-BOUNDARIES"],
    "codebase-design": ["DEEPENING", "DESIGN-IT-TWICE"],
    "domain-modeling": ["ADR-FORMAT", "CONTEXT-FORMAT"],
    "improve-codebase-architecture": ["HTML-REPORT"],
    "prototype": ["LOGIC", "UI"],
    "setup-matt-pocock-skills": ["domain", "issue-tracker-github", "issue-tracker-gitlab", "issue-tracker-local", "triage-labels"],
    "tdd": ["mocking", "tests"],
    "triage": ["AGENT-BRIEF", "OUT-OF-SCOPE"],
    "teach": ["GLOSSARY-FORMAT", "LEARNING-RECORD-FORMAT", "MISSION-FORMAT", "RESOURCES-FORMAT"],
    "writing-for-agents": ["SKILL-MECHANICS"],
}

LEVEL_META = {lvl[0]: lvl for lvl in LEVELS}


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------
def parse_frontmatter(text: str):
    fm = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text, body = parts[1], parts[2]
            for line in fm_text.split("\n"):
                line = line.strip()
                if not line or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                v = v.strip()
                if v.startswith('"') and v.endswith('"'):
                    v = v[1:-1]
                fm[k.strip()] = v
    return fm, body.lstrip("\n")


def split_blocks(body: str):
    """Split markdown body into top-level blocks (blank-line separated, fence/html aware)."""
    lines = body.split("\n")
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        stripped = lines[i].strip()
        if stripped == "":
            i += 1
            continue
        # fenced code block
        if stripped.startswith("```"):
            j = i + 1
            while j < n and not lines[j].strip().startswith("```"):
                j += 1
            blocks.append("\n".join(lines[i : min(j + 1, n)]))
            i = j + 1
            continue
        # raw html block with a matching closing tag
        if stripped.startswith("<") and not stripped.startswith("</") and not stripped.startswith("<!--"):
            m = re.match(r"<([a-zA-Z0-9\-]+)[\s>]", stripped) or re.match(r"<([a-zA-Z0-9\-]+)>", stripped)
            if m:
                tag = m.group(1)
                closing = f"</{tag}>"
                if closing in stripped:
                    blocks.append(lines[i]); i += 1; continue
                j = i + 1
                while j < n and closing not in lines[j]:
                    j += 1
                blocks.append("\n".join(lines[i : min(j + 1, n)]))
                i = j + 1
                continue
        # otherwise: group consecutive non-blank lines
        j = i + 1
        while j < n and lines[j].strip() != "":
            j += 1
        blocks.append("\n".join(lines[i:j]))
        i = j
    return blocks


def render_md(md_text: str) -> str:
    import markdown
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "sane_lists"])


def pair_blocks(en_body, zh_body):
    en_blocks = split_blocks(en_body)
    zh_blocks = split_blocks(zh_body)
    if len(en_blocks) != len(zh_blocks):
        print(f"  [warn] block count mismatch: EN={len(en_blocks)} ZH={len(zh_blocks)}")
    pairs = []
    n = max(len(en_blocks), len(zh_blocks))
    for i in range(n):
        en = en_blocks[i] if i < len(en_blocks) else ""
        zh = zh_blocks[i] if i < len(zh_blocks) else ""
        pairs.append((en, zh))
    return pairs


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------
def fetch(path: str) -> str:
    cached = CACHE / (path.replace("/", "__") + ".md")
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    url = f"{UPSTREAM_BASE}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read().decode("utf-8")
        CACHE.mkdir(parents=True, exist_ok=True)
        cached.write_text(data, encoding="utf-8")
        return data
    except Exception as e:
        print(f"  [err] could not fetch {url}: {e}")
        return ""


# --------------------------------------------------------------------------
# Page templates
# --------------------------------------------------------------------------
BLOB_BASE = "https://github.com/shumingyang-opencode/mattpocock-skills-zh-tw/blob/main"


def page_open(title: str, prefix: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · mattpocock-skills-zh-tw</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Noto+Serif+TC:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
<div class="container">
"""


def page_close() -> str:
    return """
</div>
</body>
</html>
"""


def breadcrumb(name: str, is_skill: bool, prefix: str) -> str:
    parent = f'<a href="SKILL.html">← 技能主頁 {name}</a> ' if not is_skill else ""
    return f"""<div class="back-link">
  <a href="{prefix}index.html">首頁</a>
  <a href="{prefix}map.html">技能地圖</a>
  <a href="{prefix}learning-path.html">學習路線</a>
  {parent}
</div>
"""


def rewrite_links(html: str, cat: str, skill: str) -> str:
    """Rewrite same-directory relative links: .md -> .html, other files -> GitHub blob URL."""
    blob_dir = f"{BLOB_BASE}/skills/{cat}/{skill}"

    def repl(m):
        attr, href = m.group(1), m.group(2)
        if href.startswith(("http", "#", "mailto", "/", "../")):
            return m.group(0)
        target = href.lstrip("./")
        if target.endswith(".md"):
            new_href = target[:-3] + ".html"
        else:
            new_href = f"{blob_dir}/{target}"
        return f'{attr}="{new_href}"'

    return re.sub(r'(href|src)="([^"]+)"', repl, html)


def fm_table(en_fm, zh_fm) -> str:
    rows = ""
    name = en_fm.get("name", zh_fm.get("name", ""))
    rows += f'<tr><td>name</td><td><code>{name}</code></td></tr>\n'
    if en_fm.get("description"):
        rows += f'<tr><td>description (EN)</td><td>{en_fm["description"]}</td></tr>\n'
    if zh_fm.get("description"):
        rows += f'<tr><td>說明 (繁中)</td><td>{zh_fm["description"]}</td></tr>\n'
    for key in ("disable-model-invocation", "argument-hint"):
        if en_fm.get(key):
            rows += f'<tr><td>{key}</td><td><code>{en_fm[key]}</code></td></tr>\n'
    return f'<table class="fm-table">\n{rows}</table>\n'


def attached_links(name: str) -> str:
    docs = ATTACHED.get(name, [])
    if not docs:
        return ""
    links = "　·　".join(f'<a href="{d}.html">{d}</a>' for d in docs)
    return f'<div class="back-link" style="margin-top:-0.6rem">附屬文件：{links}</div>\n'


def skill_page(name: str):
    meta = SKILLS.get(name, {})
    zh_title = meta.get("title", name)
    src_dir = f"skills/{meta.get('cat', 'engineering')}/{name}"
    en_full = fetch(f"{src_dir}/SKILL.md")
    zh_full = (ROOT / src_dir / "SKILL.md").read_text(encoding="utf-8")
    en_fm, en_body = parse_frontmatter(en_full)
    zh_fm, zh_body = parse_frontmatter(zh_full)
    pairs = pair_blocks(en_body, zh_body)

    html = page_open(f"{name} · {zh_title}", "../")
    html += breadcrumb(name, is_skill=True, prefix="../")
    html += fm_table(en_fm, zh_fm)
    html += f"<h1>{name}</h1>\n"
    html += f'<div class="subtitle">{zh_title}</div>\n'
    html += attached_links(name)
    for en, zh in pairs:
        if not en and not zh:
            continue
        en_html = render_md(en) if en else '<p class="zh-only">（無英文對照）</p>'
        zh_html = render_md(zh) if zh else '<p class="en-only">（無繁中對照）</p>'
        en_html = rewrite_links(en_html, meta.get("cat", "engineering"), name)
        zh_html = rewrite_links(zh_html, meta.get("cat", "engineering"), name)
        html += f'<div class="pair"><div class="col-en" lang="en">{en_html}</div><div class="col-zh" lang="zh-Hant">{zh_html}</div></div>\n'
    html += page_close()
    out = ROOT / name / "SKILL.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  ✓ {out.relative_to(ROOT)}")


def attached_page(name: str, doc: str):
    meta = SKILLS.get(name, {})
    src_dir = f"skills/{meta.get('cat', 'engineering')}/{name}"
    en_full = fetch(f"{src_dir}/{doc}.md")
    zh_full = (ROOT / src_dir / f"{doc}.md").read_text(encoding="utf-8")
    en_fm, en_body = parse_frontmatter(en_full)
    zh_fm, zh_body = parse_frontmatter(zh_full)
    pairs = pair_blocks(en_body, zh_body)

    html = page_open(f"{name} / {doc}", "../")
    html += breadcrumb(name, is_skill=False, prefix="../")
    html += f"<h1>{doc}</h1>\n"
    html += f'<div class="subtitle">{name} · 附屬文件</div>\n'
    for en, zh in pairs:
        if not en and not zh:
            continue
        en_html = render_md(en) if en else '<p class="zh-only">（無英文對照）</p>'
        zh_html = render_md(zh) if zh else '<p class="en-only">（無繁中對照）</p>'
        en_html = rewrite_links(en_html, meta.get("cat", "engineering"), name)
        zh_html = rewrite_links(zh_html, meta.get("cat", "engineering"), name)
        html += f'<div class="pair"><div class="col-en" lang="en">{en_html}</div><div class="col-zh" lang="zh-Hant">{zh_html}</div></div>\n'
    html += page_close()
    out = ROOT / name / f"{doc}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  ✓ {out.relative_to(ROOT)}")


# --------------------------------------------------------------------------
# Map / learning path / index
# --------------------------------------------------------------------------
def node_html(skill: str, kind: str = "mainline", small: bool = False) -> str:
    meta = SKILLS[skill]
    cls = f"node {kind}" + (" small" if small else "")
    return (f'<a class="{cls}" href="{skill}/SKILL.html">'
            f'<span class="label">{skill}</span>'
            f'<span class="tag">{meta["title"]}</span>'
            f'<span class="en">{meta["inv"]}-invoked</span>'
            f'</a>')


def map_page() -> str:
    html = page_open("技能地圖 · Skill Map", "")
    html += """<div class="back-link"><a href="index.html">← 首頁</a><a href="learning-path.html">學習路線</a></div>
<header>
  <h1>技能地圖</h1>
  <div class="subtitle">Skill Map · 沿著主流程 idea → ship</div>
  <div class="badge-line">中英對照卡片節點 · 點卡片進入逐段對照頁</div>
</header>
"""
    # precondition
    html += f"""<div class="precondition">
  <a href="setup-matt-pocock-skills/SKILL.html"><span class="label">setup-matt-pocock-skills</span><span class="tag">首次使用前運行 · 前置條件</span></a>
  <div class="precondition-hint">↑ 每個 repo 先跑一次，種下 issue tracker 與標籤</div>
</div>
"""
    # entry
    html += f"""<div class="entry">
  <a class="sign" href="ask-matt/SKILL.html"><span class="label">ask-matt</span><span class="tag">技能路由器 · 高速入口</span><span class="en">router</span></a>
</div>
"""
    # highway mainline
    html += '<div class="zone"><div class="zone-label">主流程 · idea → ship</div><div class="highway">\n'
    for row in MAINLINE:
        html += '<div class="hwy-row">\n'
        html += '  <div class="col-left">'
        if row.get("left"):
            html += '<div class="ramp-cluster">' + "".join(node_html(s, "on-ramp", small=True) for s in row["left"]) + "</div>"
        html += '</div>\n'
        html += '  <div class="col-center"><div class="pair-main">'
        center = row["center"]
        if isinstance(center, list) and any(x in ("↔", "→") for x in center):
            idx = next(i for i, x in enumerate(center) if x in ("↔", "→"))
            left, arrow, right = center[:idx], center[idx], center[idx + 1:]
            for s in left:
                html += node_html(s, "service" if row.get("service") else "mainline")
            html += f'<span class="pair-arrow">{arrow}</span>'
            for s in right:
                html += node_html(s, "service" if row.get("service") else "mainline", small=True)
        else:
            for s in center:
                html += node_html(s, "service" if row.get("service") else "mainline")
        html += '</div></div>\n'
        html += '  <div class="col-right">'
        if row.get("right"):
            right_nodes = row["right"] if isinstance(row["right"], list) else [row["right"]]
            html += "".join(node_html(s, "on-ramp") for s in right_nodes)
        elif row.get("right") is None and row.get("service"):
            html += '<span class="side-note">繞道 · 原型支線</span>'
        html += '</div>\n'
        html += '</div>\n'
        html += '<div class="flow-arrow"></div>\n'
    html += "</div></div>\n"

    # grilling primitive annotation
    html += f"""<div class="primitive-annotation"><a href="grilling/SKILL.html">↑ 共享訪談原語 · grilling</a></div>
"""
    # foundation
    html += """<div class="zone"><div class="foundation">
  <div class="foundation-title">詞彙層（路基）— 主流程運行的底層支撐</div>
  <div class="foundation-row">
"""
    for s in FOUNDATION:
        html += f'<a class="foundation-node" href="{s}/SKILL.html"><span class="label">{s}</span><span class="en">{SKILLS[s]["title"]}</span></a>'
        for d in ATTACHED.get(s, []):
            html += f'<a class="foundation-node" href="{s}/{d}.html"><span class="label">{d}</span><span class="en">附屬</span></a>'
    html += '<span class="foundation-note">術語 · 決策 · 模組設計</span>\n'
    html += """</div></div></div>
"""
    # legend
    html += '<div class="legend">'
    for key, label, _ in LEGEND:
        if key == "dash":
            html += f'<span class="legend-item"><span class="legend-dash"></span>{label}</span>'
        else:
            html += f'<span class="legend-item"><span class="legend-dot {"" if key=="mainline" else key}"></span>{label}</span>'
    html += '</div>\n'

    # standalone + meta zones
    html += '<div class="zone"><div class="zone-label">獨立可用 · 不依賴主流程</div><div class="h-zone"><div class="h-row">'
    for s in STANDALONE:
        html += node_html(s, "standalone")
    html += '</div><div class="h-note">可獨立使用，無須進入主流程</div></div></div>\n'

    html += '<div class="zone"><div class="zone-label">元技能 · 寫作參考</div><div class="h-zone"><div class="h-row">'
    for s in META:
        html += node_html(s, "meta")
    html += '</div><div class="h-note">關於技能系統本身的技能</div></div></div>\n'

    html += footer()
    html += page_close()
    out = ROOT / "map.html"
    out.write_text(html, encoding="utf-8")
    print(f"  ✓ map.html")


def learning_path_page() -> str:
    html = page_open("學習路線 · Learning Path", "")
    html += """<div class="back-link"><a href="index.html">← 首頁</a><a href="map.html">技能地圖</a></div>
<header>
  <h1>學習路線</h1>
  <div class="subtitle">Learning Path · 依技能分類循序學習</div>
  <div class="badge-line">L0 前置 → L1 起手 → L2 規劃 → L3 執行 → L4 收尾 · 支援層與詞彙層隨取隨用</div>
</header>
"""
    for code, title, sub, badge_cls, names in LEVELS:
        html += f'<div class="level"><div class="level-head"><span class="level-badge {badge_cls}">{code}</span><span class="level-title">{title}</span><span class="level-sub">{sub}</span></div><div class="card-grid">'
        for s in names:
            meta = SKILLS[s]
            html += card_html(s, meta)
        html += '</div></div>\n'
    html += footer()
    html += page_close()
    out = ROOT / "learning-path.html"
    out.write_text(html, encoding="utf-8")
    print("  ✓ learning-path.html")


def card_html(skill: str, meta: dict) -> str:
    zh_desc = ""
    try:
        _, zh_body = parse_frontmatter((ROOT / f"skills/{meta['cat']}/{skill}/SKILL.md").read_text(encoding="utf-8"))
        _ = zh_body
        zh_full = (ROOT / f"skills/{meta['cat']}/{skill}/SKILL.md").read_text(encoding="utf-8")
        zh_fm, _ = parse_frontmatter(zh_full)
        zh_desc = zh_fm.get("description", "")
    except Exception:
        pass
    tags = f'<span class="c-tag">{meta["cat"]}</span><span class="c-tag">{meta["inv"]}-invoked</span>'
    return (f'<a class="card" href="{skill}/SKILL.html">'
            f'<span class="c-name">{skill}</span>'
            f'<span class="c-en">{meta["title"]}</span>'
            f'<span class="c-zh">{zh_desc}</span>'
            f'<span class="c-tags">{tags}</span>'
            f'</a>')


def index_page() -> str:
    html = page_open("Matt Pocock 技能集 · 中英對照", "")
    html += """<header>
  <h1>Matt Pocock 技能集</h1>
  <div class="subtitle">mattpocock/skills · 繁體中文對照學習站</div>
  <div class="badge-line">中英對照 · 全 35 個技能逐段並排 · 保留安裝與運行行為</div>
</header>
<div class="entry-cards">
  <a class="entry-card" href="map.html">
    <span class="ec-icon">🗺️</span>
    <span class="ec-title">技能地圖</span>
    <span class="ec-en">Skill Map</span>
    <span class="ec-desc">以「高速公路」隱喻掌握整套技能的關係 — 主流程 idea → ship、進入匝道、獨立技能、詞彙層。適合先建立全貌。</span>
  </a>
  <a class="entry-card" href="learning-path.html">
    <span class="ec-icon">🧭</span>
    <span class="ec-title">學習路線</span>
    <span class="ec-en">Learning Path</span>
    <span class="ec-desc">依技能分類與 L0–L4 分級循序學習，每張卡片為中英對照。適合照順序紮實學起。</span>
  </a>
</div>
"""
    html += footer(include_entries=True)
    html += page_close()
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print("  ✓ index.html")


def footer(include_entries: bool = False) -> str:
    links = ('<br><a href="map.html">技能地圖</a> · <a href="learning-path.html">學習路線</a>' if include_entries else "")
    return f"""<footer>
  <div>這是 <a href="https://github.com/mattpocock/skills">mattpocock/skills</a> 的繁體中文翻譯學習站（zh-TW）· 翻譯僅限自然語言說明，保留目錄/技能名/指令/程式碼/路徑，不影響安裝行為。</div>
  <div>內容版權 © Matt Pocock（MIT License）· 翻譯 © shumingyang-opencode · 對照排版參考 <a href="https://cnife.github.io/learn-mattpocock-skills/">learn-mattpocock-skills</a>{links}</div>
</footer>
"""


def write_data():
    data = {"skills": {}}
    for name, meta in SKILLS.items():
        try:
            zh_full = (ROOT / f"skills/{meta['cat']}/{name}/SKILL.md").read_text(encoding="utf-8")
            zh_fm, _ = parse_frontmatter(zh_full)
            zh_desc = zh_fm.get("description", "")
        except Exception:
            zh_desc = ""
        data["skills"][name] = {**meta, "description_zh": zh_desc}
    (ROOT / "assets" / "skills-data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  ✓ assets/skills-data.json")


def main():
    os.chdir(ROOT)
    CACHE.mkdir(parents=True, exist_ok=True)
    print("Generating bilingual site...")
    print("[skill pages]")
    for name in SKILLS:
        skill_page(name)
    print("[attached pages]")
    for name, docs in ATTACHED.items():
        for d in docs:
            attached_page(name, d)
    print("[views]")
    map_page()
    learning_path_page()
    index_page()
    write_data()
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())

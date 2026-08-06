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
    "setup-matt-pocock-skills":          {"cat": "engineering", "level": "L0", "inv": "user",  "blurb": "開工前先把場地佈好：tracker 用哪個、標籤怎麼分、文件放哪。"},
    "ask-matt":                          {"cat": "engineering", "level": "L1", "inv": "user",  "blurb": "不知道下一步要幹嘛？把你卡住的地方丟給它，它幫你挑對的技能。"},
    "grill-with-docs":                   {"cat": "engineering", "level": "L1", "inv": "user",  "blurb": "跟它一輪輪對談，把你要的東西想清楚，順手讓它把結論寫成文件。"},
    "grilling":                          {"cat": "productivity", "level": "L1", "inv": "model", "blurb": "一台問不停的機器，問到你沒得閃為止——所有訪談類技能的地基。"},
    "grill-me":                          {"cat": "productivity", "level": "L1", "inv": "user",  "blurb": "只有你跟它，它追問到你把自己的計畫想清楚為止。"},
    "to-spec":                           {"cat": "engineering", "level": "L2", "inv": "user",  "blurb": "把聊完的共識整理成一份規格丟進 tracker，不用再訪談一遍。"},
    "to-tickets":                        {"cat": "engineering", "level": "L2", "inv": "user",  "blurb": "把大計畫拆成一張張曳光彈大小的工單，每張都標好要先做什麼。"},
    "wayfinder":                         {"cat": "engineering", "level": "L2", "inv": "user",  "blurb": "大到連地圖都還沒畫的超大工程，先把決策一顆顆定下來再出發。"},
    "triage":                            {"cat": "engineering", "level": "L2", "inv": "user",  "blurb": "外面湧進來的 bug、請求，先幫它們分診掛號，再決定放行給誰做。"},
    "to-questionnaire":                  {"cat": "productivity", "level": "L2", "inv": "user",  "blurb": "你自己答不了的決策，變成能答的人來填的問卷。"},
    "implement":                         {"cat": "engineering", "level": "L3", "inv": "user",  "blurb": "照規格或工單，把該做的工作真的做出來。"},
    "tdd":                               {"cat": "engineering", "level": "L3", "inv": "model", "blurb": "先寫一支注定失敗的測試，再寫讓它變綠的程式——用回饋逼出好程式。"},
    "prototype":                         {"cat": "engineering", "level": "L3", "inv": "model", "blurb": "寫一支丟掉也不心疼的小程式，先把「這招到底行不行」試出來。"},
    "handoff":                           {"cat": "productivity", "level": "L3", "inv": "user",  "blurb": "把這段對話打包成交接文件，讓下一個 session 接手接著做。"},
    "diagnosing-bugs":                   {"cat": "engineering", "level": "L3", "inv": "model", "blurb": "看一眼看不懂的硬 bug，先用一條保證會紅的指令鎖住它，再慢慢拆。"},
    "code-review":                       {"cat": "engineering", "level": "L4", "inv": "model", "blurb": "雙軸檢查：有沒有照團隊規範、有沒有照規格做出來。"},
    "resolving-merge-conflicts":         {"cat": "engineering", "level": "L4", "inv": "model", "blurb": "照雙方各自的意圖一塊塊解衝突，講清楚原因才動手，絕不按 --abort 擺爛。"},
    "improve-codebase-architecture":     {"cat": "engineering", "level": "L4", "inv": "user",  "blurb": "三不五時掃一下程式碼庫，找出值得加深重構的候選，讓你挑一個來做。"},
    "codebase-design":                   {"cat": "engineering", "level": "vocab", "inv": "model", "blurb": "把一大堆行為塞進小小的介面後面，放在乾淨的接縫上，才好測也好懂。"},
    "domain-modeling":                   {"cat": "engineering", "level": "vocab", "inv": "model", "blurb": "讓全隊對同一個詞，講的是同一種意思。"},
    "research":                          {"cat": "engineering", "level": "support", "inv": "model", "blurb": "把啃文件這種苦差事丟給背景代理，你在原地繼續做事，它回來交報告。"},
    "wizard":                            {"cat": "engineering", "level": "support", "inv": "model", "blurb": "只能真人做的步驟（開帳號、輸密碼、點後台），它生成腳本一步步帶你走。"},
    "writing-for-agents":                {"cat": "productivity", "level": "support", "inv": "model", "blurb": "教你怎麼寫「給 agent 看」的文件——技能、AGENTS.md 都算。"},
    "teach":                             {"cat": "productivity", "level": "support", "inv": "user",  "blurb": "把目前目錄當教室，一次一次教到你真的會。"},
    "wait-what":                         {"cat": "productivity", "level": "support", "inv": "user",  "blurb": "一句話沒聽懂？叫它用你懂的字重講一遍。"},
    # --- misc ---
    "setup-pre-commit":                  {"cat": "misc", "level": "misc", "inv": "user", "blurb": "用 Husky 幫 commit 掛上 lint、型別檢查與測試，爛東西進不來。"},
    "scaffold-exercises":                {"cat": "misc", "level": "misc", "inv": "user", "blurb": "幫課程建好標準的練習骨架，題目、解答、講解都歸定位。"},
    "migrate-to-shoehorn":               {"cat": "misc", "level": "misc", "inv": "user", "blurb": "把測試裡亂用的 as 斷言，換成 @total-typescript/shoehorn 的乾淨寫法。"},
    "git-guardrails-claude-code":        {"cat": "misc", "level": "misc", "inv": "user", "blurb": "在 Claude Code 的鉤子裡擋下危險 git 指令，防止手滑出事。"},
    # --- in-progress ---
    "claude-handoff":                    {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "把目前的對話接給下一個 session，不間斷地接著做。"},
    "loop-me":                           {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "反覆詰問你要做的東西，直到規格真的長出來。"},
    "setup-ts-deep-modules":             {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "幫 TypeScript 專案接上 dependency-cruiser，把每個套件圍成深模組。"},
    "writing-beats":                     {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "把素材排成一段一段的故事節拍，寫出有節奏的文章。"},
    "writing-fragments":                 {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "先撿素材、挖碎片，還沒結構也不用怕。"},
    "writing-shape":                     {"cat": "in-progress", "level": "in-progress", "inv": "user", "blurb": "把碎片打磨成型，一段一段拼成文章。"},
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
    ("mainline", "主線 Mainline", "highway"),
    ("ramp", "插進來的入口 On-ramp", "ramp"),
    ("service", "繞行支線 Service", "service"),
    ("standalone", "隨取隨用 Standalone", "standalone"),
    ("meta", "meta 技能 Meta", "meta"),
    ("dash", "墊底詞彙 Vocabulary", "dash"),
]

LEVELS = [
    ("L0", "開場", "先把場地佈好", "lv-emerald", ["setup-matt-pocock-skills"]),
    ("L1", "起手", "先搞清楚要做什麼", "lv-cyan", ["ask-matt", "grill-with-docs", "grill-me", "grilling"]),
    ("L2", "規劃", "把想法變成計畫", "lv-amber", ["to-spec", "to-tickets", "wayfinder", "triage", "to-questionnaire"]),
    ("L3", "執行", "動手做，邊做邊驗", "lv-fuchsia", ["implement", "tdd", "prototype", "handoff", "diagnosing-bugs"]),
    ("L4", "收尾", "做完，還要過得漂亮", "lv-orange", ["code-review", "resolving-merge-conflicts", "improve-codebase-architecture"]),
    ("詞彙層", "墊底的兩本字典", "跑在底下，隨時可以翻", "lv-violet", ["domain-modeling", "codebase-design"]),
    ("支援層", "隨取隨用工具箱", "單獨拿出來用也很好用", "lv-emerald", ["research", "teach", "wizard", "wait-what", "writing-for-agents"]),
    ("雜項", "散裝工具", "少用，但用到時很有用", "lv-amber", ["setup-pre-commit", "scaffold-exercises", "migrate-to-shoehorn", "git-guardrails-claude-code"]),
    ("進行中", "實驗室", "還在長大的技能，歡迎回饋", "lv-fuchsia", ["claude-handoff", "loop-me", "setup-ts-deep-modules", "writing-beats", "writing-fragments", "writing-shape"]),
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
    src_dir = f"skills/{meta.get('cat', 'engineering')}/{name}"
    en_full = fetch(f"{src_dir}/SKILL.md")
    zh_full = (ROOT / src_dir / "SKILL.md").read_text(encoding="utf-8")
    en_fm, en_body = parse_frontmatter(en_full)
    zh_fm, zh_body = parse_frontmatter(zh_full)
    pairs = pair_blocks(en_body, zh_body)

    html = page_open(name, "../")
    html += breadcrumb(name, is_skill=True, prefix="../")
    html += fm_table(en_fm, zh_fm)
    html += f"<h1>{name}</h1>\n"
    html += f'<div class="subtitle">{meta.get("blurb", "")}</div>\n'
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
            f'<span class="tag">{meta["blurb"]}</span>'
            f'<span class="pill">{meta["inv"]}-invoked</span>'
            f'</a>')


def map_page() -> str:
    html = page_open("技能全景圖 · Skill Atlas", "")
    html += """<div class="back-link"><a href="index.html">← 首頁</a><a href="learning-path.html">學習路線</a></div>
<header>
  <h1>技能全景圖</h1>
  <div class="subtitle">Skill Atlas · 從點子到上線，一條路走到底</div>
  <div class="badge-line">點任何一格，進到逐段中英對照頁</div>
</header>
"""
    # precondition
    html += f"""<div class="precondition">
  <a href="setup-matt-pocock-skills/SKILL.html"><span class="label">setup-matt-pocock-skills</span><span class="tag">開工前先把場地佈好</span></a>
  <div class="precondition-hint">每個 repo 跑一次：tracker、標籤、文件位置一次搞定</div>
</div>
"""
    # entry
    html += f"""<div class="entry">
  <a class="sign" href="ask-matt/SKILL.html"><span class="label">ask-matt</span><span class="tag">不知道下一步？先來問它</span><span class="en">router</span></a>
</div>
"""
    # highway mainline
    html += '<div class="zone"><div class="zone-label">主線：從點子到上線 · idea → ship</div><div class="highway">\n'
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
            html += '<span class="side-note">需要真的跑一下才知道的，繞去原型試</span>'
        html += '</div>\n'
        html += '</div>\n'
        html += '<div class="flow-arrow"></div>\n'
    html += "</div></div>\n"

    # grilling primitive annotation
    html += f"""<div class="primitive-annotation"><a href="grilling/SKILL.html">所有訪談技能的地基 ↑ grilling</a></div>
"""
    # foundation
    html += """<div class="zone"><div class="foundation">
  <div class="foundation-title">墊底的兩本字典：領域語言 × 模組形狀</div>
  <div class="foundation-row">
"""
    for s in FOUNDATION:
        html += f'<a class="foundation-node" href="{s}/SKILL.html"><span class="label">{s}</span><span class="en">{SKILLS[s]["blurb"]}</span></a>'
        for d in ATTACHED.get(s, []):
            html += f'<a class="foundation-node" href="{s}/{d}.html"><span class="label">{d}</span><span class="en">附屬文件</span></a>'
    html += '<span class="foundation-note">讓全隊講同一種語言，讓模組長出好形狀</span>\n'
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
    html += '<div class="zone"><div class="zone-label">隨取隨用 · 不必進主線</div><div class="h-zone"><div class="h-row">'
    for s in STANDALONE:
        html += node_html(s, "standalone")
    html += '</div><div class="h-note">單獨拿出來用也很好用</div></div></div>\n'

    html += '<div class="zone"><div class="zone-label">meta 技能：怎麼寫給 agent 看的文件</div><div class="h-zone"><div class="h-row">'
    for s in META:
        html += node_html(s, "meta")
    html += '</div><div class="h-note">這是在教「怎麼寫技能」的技能</div></div></div>\n'

    html += footer()
    html += page_close()
    out = ROOT / "map.html"
    out.write_text(html, encoding="utf-8")
    print(f"  ✓ map.html")


def learning_path_page() -> str:
    html = page_open("學習路線 · Learning Path", "")
    html += """<div class="back-link"><a href="index.html">← 首頁</a><a href="map.html">技能全景圖</a></div>
<header>
  <h1>學習路線</h1>
  <div class="subtitle">Learning Path · 從 0 練到上線</div>
  <div class="badge-line">分層分級一關一關過；支援層與詞彙層，隨時可翻</div>
</header>
"""
    for badge, title, sub, color_cls, names in LEVELS:
        html += f'<div class="level {color_cls}"><div class="level-head"><span class="level-badge">{badge}</span><span class="level-title">{title}</span><span class="level-sub">{sub}</span></div><div class="card-grid">'
        for s in names:
            html += card_html(s, SKILLS[s], color_cls)
        html += '</div></div>\n'
    html += footer()
    html += page_close()
    out = ROOT / "learning-path.html"
    out.write_text(html, encoding="utf-8")
    print("  ✓ learning-path.html")


def card_html(skill: str, meta: dict, color_cls: str = "lv-cyan") -> str:
    tags = f'<span class="c-tag">{meta["cat"]}</span><span class="c-tag">{meta["inv"]}-invoked</span>'
    return (f'<a class="card" href="{skill}/SKILL.html">'
            f'<span class="c-name">{skill}</span>'
            f'<span class="c-zh">{meta["blurb"]}</span>'
            f'<span class="c-tags">{tags}</span>'
            f'</a>')


def index_page() -> str:
    html = page_open("Matt Pocock 技能包 · 繁中解讀", "")
    html += """<header>
  <h1>Matt Pocock 技能包</h1>
  <div class="subtitle">35 個工程師向代理技能，中英逐段並排，用台灣人的話講給你聽</div>
  <div class="badge-line">翻譯只動說明文字，指令、路徑、技能名照原樣，安裝照常可用</div>
</header>
<div class="entry-cards">
  <a class="entry-card" href="map.html">
    <span class="ec-icon">🗺️</span>
    <span class="ec-title">全景圖</span>
    <span class="ec-en">Skill Atlas</span>
    <span class="ec-desc">一張圖看懂 35 個技能怎麼接在一起——主線、插進來的入口、繞行支線，還有墊底的兩本字典。</span>
  </a>
  <a class="entry-card" href="learning-path.html">
    <span class="ec-icon">🧗</span>
    <span class="ec-title">學習路線</span>
    <span class="ec-en">Learning Path</span>
    <span class="ec-desc">不想只看懂、想真的上手？從 L0 一路練到 L4，分層分類照著走。</span>
  </a>
</div>
"""
    html += footer(include_entries=True)
    html += page_close()
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print("  ✓ index.html")


def footer(include_entries: bool = False) -> str:
    links = ('<br><a href="map.html">全景圖</a> · <a href="learning-path.html">學習路線</a>' if include_entries else "")
    return f"""<footer>
  <div>這是 <a href="https://github.com/mattpocock/skills">mattpocock/skills</a> 的繁體中文翻譯學習站——翻譯只動說明文字，指令、路徑、技能名一律照原樣，安裝照常可用。</div>
  <div>內容 © Matt Pocock（MIT License）· 繁中翻譯與這個站 © shumingyang-opencode · 版面架構參考 <a href="https://cnife.github.io/learn-mattpocock-skills/">learn-mattpocock-skills</a>{links}</div>
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

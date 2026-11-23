#!/usr/bin/env python3
"""仓库格式校验：本地和 CI 跑同一套逻辑。

检查项：
1. SKILL.md 有 YAML frontmatter，name / description 齐全，name 与目录名一致
2. SKILL.md 包含 6 个必需章节，行数不超过 500
3. glossary.json 是合法 JSON，字段齐全，status 取值合法
4. glossary.md 与 glossary.json 条数一致、词条一一对应
5. 所有 Markdown 相对链接不失效
6. 词表里没有疑似手机号

用法：python3 scripts/lint.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "speak-like-naruto-mobile-player"

REQUIRED_SECTIONS = ["什么时候用", "什么时候不用", "核心黑话", "说话方式", "例子", "不要做的事"]
REQUIRED_TERM_FIELDS = ["term", "pinyin", "meaning", "usage", "example", "source", "status"]
VALID_STATUS = {"verified", "pending"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    data: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_skill_md() -> None:
    path = SKILL_DIR / "SKILL.md"
    if not path.exists():
        err("SKILL.md 不存在")
        return

    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        err("SKILL.md 缺少 YAML frontmatter（文件应以 --- 开头）")
        return

    for key in ("name", "description"):
        if not fm.get(key):
            err(f"SKILL.md frontmatter 缺少字段：{key}")

    if fm.get("name") and fm["name"] != SKILL_DIR.name:
        err(f"SKILL.md 的 name「{fm['name']}」与目录名「{SKILL_DIR.name}」不一致")

    line_count = text.count("\n") + 1
    if line_count > 500:
        err(f"SKILL.md 有 {line_count} 行，超过 500 行上限")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            err(f"SKILL.md 缺少必需章节：{section}")


def load_glossary_json() -> list[dict]:
    path = SKILL_DIR / "data" / "glossary.json"
    if not path.exists():
        err("data/glossary.json 不存在")
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"glossary.json 不是合法 JSON：{exc}")
        return []

    for key in ("version", "updated", "terms"):
        if key not in data:
            err(f"glossary.json 缺少顶层字段：{key}")

    terms = data.get("terms", [])
    if not isinstance(terms, list) or not terms:
        err("glossary.json 的 terms 必须是非空数组")
        return []

    for idx, term in enumerate(terms, 1):
        label = term.get("term", f"第 {idx} 条") if isinstance(term, dict) else f"第 {idx} 条"
        if not isinstance(term, dict):
            err(f"terms 第 {idx} 条不是对象")
            continue
        for field in REQUIRED_TERM_FIELDS:
            if not term.get(field):
                err(f"词条「{label}」缺少字段：{field}")
        if term.get("status") and term["status"] not in VALID_STATUS:
            err(f"词条「{label}」的 status「{term['status']}」不合法，只能是 verified 或 pending")

    seen: dict[str, int] = {}
    for term in terms:
        if isinstance(term, dict) and term.get("term"):
            seen[term["term"]] = seen.get(term["term"], 0) + 1
    for name, count in seen.items():
        if count > 1:
            err(f"glossary.json 里「{name}」重复出现 {count} 次")

    return terms


def parse_md_terms() -> list[str]:
    path = SKILL_DIR / "references" / "glossary.md"
    if not path.exists():
        err("references/glossary.md 不存在")
        return []

    text = path.read_text(encoding="utf-8")
    match = re.search(r"\n##\s*词表\s*\n(.*?)(?=\n##\s|\Z)", text, re.S)
    if not match:
        err("glossary.md 中找不到「## 词表」章节")
        return []

    rows: list[list[str]] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)

    if not rows:
        err("glossary.md 的词表是空的")
        return []

    return [row[0] for row in rows[1:]]


def check_glossary_consistency(json_terms: list[dict], md_terms: list[str]) -> None:
    if not json_terms or not md_terms:
        return

    if len(json_terms) != len(md_terms):
        err(f"条数不一致：glossary.json 有 {len(json_terms)} 条，glossary.md 有 {len(md_terms)} 条")
        return

    for idx, (jt, mt) in enumerate(zip(json_terms, md_terms), 1):
        jname = jt.get("term") if isinstance(jt, dict) else None
        if jname != mt:
            err(f"第 {idx} 条词条不一致：json 是「{jname}」，md 是「{mt}」")


def check_links() -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                err(f"{path.relative_to(ROOT)} 链接失效：{target}")


def check_privacy(json_terms: list[dict]) -> None:
    phone = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
    blob = json.dumps(json_terms, ensure_ascii=False)
    holes = phone.findall(blob)
    if holes:
        err(f"词表里疑似出现手机号：{', '.join(holes)}")


def main() -> int:
    check_skill_md()
    json_terms = load_glossary_json()
    md_terms = parse_md_terms()
    check_glossary_consistency(json_terms, md_terms)
    check_links()
    check_privacy(json_terms)

    if errors:
        print(f"校验失败，{len(errors)} 个问题：")
        for item in errors:
            print(f"  x {item}")
        if warnings:
            print()
            for item in warnings:
                print(f"  ! {item}")
        return 1

    verified = sum(1 for t in json_terms if isinstance(t, dict) and t.get("status") == "verified")
    pending = len(json_terms) - verified
    print("校验通过")
    print(f"  词条 {len(json_terms)} 条（verified {verified} / pending {pending}）")
    print(f"  SKILL.md {(SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8').count(chr(10)) + 1} 行")
    for item in warnings:
        print(f"  ! {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

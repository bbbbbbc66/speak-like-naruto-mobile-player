#!/usr/bin/env python3
"""仓库格式校验：本地和 CI 跑同一套逻辑。

数据模型 schema 1.0：这套语言不是词库，是生成语法。除了词条表，
还要校验词根池、构式、功能表、语用约束，以及人读版与机器读版五层同源。

检查项：
1. SKILL.md 有 YAML frontmatter，name / description 齐全，name 与目录名一致
2. SKILL.md 包含 6 个必需章节，行数不超过 500
3. glossary.json 是合法 JSON，schema 1.0 五层结构齐全
4. 结构自洽：构式 id 唯一、词条 construction 引用有效、merged_terms 不得仍留在词条表、
   雷霆词根 15 个且为单字、构式 / 词条 status 合法、词条 7 字段齐全
5. glossary.md 与 glossary.json 五层同源：词条一一对应、构式 id 一一对应、
   功能位场景一一对应、15 个词根都在人读版词根池里出现
6. 所有 Markdown 相对链接不失效
7. 全仓 JSON 数据里没有疑似手机号

用法：python3 scripts/lint.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "speak-like-naruto-mobile-player"
JSON_PATH = SKILL_DIR / "data" / "glossary.json"
MD_PATH = SKILL_DIR / "references" / "glossary.md"

REQUIRED_SECTIONS = ["什么时候用", "什么时候不用", "核心黑话", "说话方式", "例子", "不要做的事"]
REQUIRED_TERM_FIELDS = ["term", "pinyin", "meaning", "usage", "example", "source", "status"]
REQUIRED_CONSTRUCTION_FIELDS = ["id", "name", "pattern", "function", "examples", "status"]
REQUIRED_FUNCTION_FIELDS = ["scene", "options", "source"]
VALID_STATUS = {"verified", "pending"}
EXPECTED_SCHEMA = "1.0"
EXPECTED_ROOT_COUNT = 15

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


def load_model() -> dict:
    if not JSON_PATH.exists():
        err("data/glossary.json 不存在")
        return {}
    try:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"glossary.json 不是合法 JSON：{exc}")
        return {}

    for key in ("schema", "version", "model", "roots", "constructions", "functions", "pragmatics", "terms"):
        if key not in data:
            err(f"glossary.json 缺少顶层字段：{key}")

    if data.get("schema") != EXPECTED_SCHEMA:
        warn(f"glossary.json 的 schema 是「{data.get('schema')}」，预期 {EXPECTED_SCHEMA}（本脚本按 1.0 校验）")
    if data.get("model") != "generative":
        warn(f"glossary.json 的 model 是「{data.get('model')}」，预期 generative")
    return data


def check_structure(data: dict) -> None:
    if not data:
        return

    # --- roots ---
    roots = data.get("roots", {})
    thunder = roots.get("thunder", []) if isinstance(roots, dict) else []
    if len(thunder) != EXPECTED_ROOT_COUNT:
        err(f"雷霆词根应有 {EXPECTED_ROOT_COUNT} 个，实际 {len(thunder)} 个")
    for root in thunder:
        if not isinstance(root, str) or len(root) != 1:
            err(f"雷霆词根「{root}」不是单个汉字")
    if len(set(thunder)) != len(thunder):
        err("雷霆词根有重复")
    for key in ("particles", "action_animal", "combination_rule", "rule_source", "spelling_note", "ownership_note"):
        if not roots.get(key):
            err(f"roots 缺少字段：{key}")

    # --- constructions ---
    constructions = data.get("constructions", [])
    if not isinstance(constructions, list) or not constructions:
        err("constructions 必须是非空数组")
        constructions = []
    ids: list[str] = []
    for idx, c in enumerate(constructions, 1):
        label = c.get("id", f"第 {idx} 条") if isinstance(c, dict) else f"第 {idx} 条"
        if not isinstance(c, dict):
            err(f"constructions 第 {idx} 条不是对象")
            continue
        for field in REQUIRED_CONSTRUCTION_FIELDS:
            if not c.get(field):
                err(f"构式「{label}」缺少字段：{field}")
        if c.get("status") and c["status"] not in VALID_STATUS:
            err(f"构式「{label}」的 status「{c['status']}」不合法")
        if c.get("id"):
            ids.append(c["id"])
            if not re.fullmatch(r"C\d+", c["id"]):
                err(f"构式 id「{c['id']}」格式不合法，应为 C 加数字")
    for cid, count in {i: ids.count(i) for i in set(ids)}.items():
        if count > 1:
            err(f"构式 id「{cid}」重复出现 {count} 次")
    valid_ids = set(ids)

    # --- functions ---
    functions = data.get("functions", [])
    if not isinstance(functions, list) or not functions:
        err("functions 必须是非空数组")
        functions = []
    scenes: list[str] = []
    for idx, f in enumerate(functions, 1):
        label = f.get("scene", f"第 {idx} 条") if isinstance(f, dict) else f"第 {idx} 条"
        if not isinstance(f, dict):
            err(f"functions 第 {idx} 条不是对象")
            continue
        for field in REQUIRED_FUNCTION_FIELDS:
            if not f.get(field):
                err(f"功能位「{label}」缺少字段：{field}")
        if f.get("options") and not isinstance(f["options"], list):
            err(f"功能位「{label}」的 options 必须是数组")
        if f.get("scene"):
            scenes.append(f["scene"])
    for scene, count in {s: scenes.count(s) for s in set(scenes)}.items():
        if count > 1:
            err(f"功能位场景「{scene}」重复出现 {count} 次")

    # --- pragmatics ---
    prag = data.get("pragmatics", {})
    for key in ("why_it_exists", "why_source", "implications", "ka_le", "duan_le"):
        if not prag.get(key):
            err(f"pragmatics 缺少字段：{key}")

    # --- terms ---
    terms = data.get("terms", [])
    if not isinstance(terms, list) or not terms:
        err("terms 必须是非空数组")
        return
    names: list[str] = []
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
        if term.get("construction") and term["construction"] not in valid_ids:
            err(f"词条「{label}」引用了不存在的构式「{term['construction']}」")
        if term.get("term"):
            names.append(term["term"])
    for name, count in {n: names.count(n) for n in set(names)}.items():
        if count > 1:
            err(f"词条「{name}」重复出现 {count} 次")

    # --- 防回退：已合并进构式的词不得再作为独立词条出现 ---
    for c in constructions:
        if not isinstance(c, dict):
            continue
        for merged in c.get("merged_terms", []):
            if merged in names:
                err(f"「{merged}」已合并进构式 {c.get('id')}，不应再作为独立词条出现")


def md_section(text: str, header: str) -> str:
    match = re.search(r"\n##\s*" + re.escape(header) + r"[^\n]*\n(.*?)(?=\n##\s|\Z)", text, re.S)
    if not match:
        err(f"glossary.md 中找不到「## {header}」章节")
        return ""
    return match.group(1)


def md_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def check_md_consistency(data: dict) -> None:
    if not MD_PATH.exists():
        err("references/glossary.md 不存在")
        return
    if not data:
        return
    text = MD_PATH.read_text(encoding="utf-8")

    # 词条：第一列一一对应（跳过表头）
    term_rows = md_rows(md_section(text, "词表"))
    md_terms = [row[0] for row in term_rows[1:]] if term_rows else []
    json_terms = [t["term"] for t in data.get("terms", []) if isinstance(t, dict) and t.get("term")]
    if json_terms != md_terms:
        err(f"词条不一致：json {len(json_terms)} 条 / md {len(md_terms)} 条"
            + (f"，首个差异在第 "
               f"{next((i for i, (a, b) in enumerate(zip(json_terms, md_terms), 1) if a != b), '尾部')} 条" if len(json_terms) == len(md_terms) else ""))

    # 构式 id：第一列一一对应
    c_rows = md_rows(md_section(text, "构式"))
    md_ids = [row[0] for row in c_rows[1:]] if c_rows else []
    json_ids = [c["id"] for c in data.get("constructions", []) if isinstance(c, dict) and c.get("id")]
    if json_ids != md_ids:
        err(f"构式 id 不一致：json {json_ids} / md {md_ids}")

    # 功能位场景：第一列一一对应
    f_rows = md_rows(md_section(text, "场景"))
    md_scenes = [row[0] for row in f_rows[1:]] if f_rows else []
    json_scenes = [f["scene"] for f in data.get("functions", []) if isinstance(f, dict) and f.get("scene")]
    if json_scenes != md_scenes:
        err(f"功能位场景不一致：json {len(json_scenes)} 个 / md {len(md_scenes)} 个"
            + (f"，差异：{set(json_scenes) ^ set(md_scenes)}" if len(json_scenes) == len(md_scenes) else ""))

    # 词根池：15 个雷霆词根都要在人读版该节里出现
    root_section = md_section(text, "词根池")
    if root_section:
        for root in data.get("roots", {}).get("thunder", []):
            if root not in root_section:
                err(f"词根池人读版缺少词根「{root}」")


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


def check_privacy(data: dict) -> None:
    phone = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
    holes = phone.findall(json.dumps(data, ensure_ascii=False))
    if holes:
        err(f"JSON 数据里疑似出现手机号：{', '.join(holes)}")


def main() -> int:
    check_skill_md()
    data = load_model()
    check_structure(data)
    check_md_consistency(data)
    check_links()
    check_privacy(data)

    if errors:
        print(f"校验失败，{len(errors)} 个问题：")
        for item in errors:
            print(f"  x {item}")
        if warnings:
            print()
            for item in warnings:
                print(f"  ! {item}")
        return 1

    terms = data.get("terms", [])
    constructions = data.get("constructions", [])
    verified = sum(1 for t in terms if t.get("status") == "verified")
    pending = len(terms) - verified
    c_verified = sum(1 for c in constructions if c.get("status") == "verified")
    print("校验通过")
    print(f"  模型 schema {data.get('schema')} / 版本 {data.get('version')} / {data.get('model')}")
    print(f"  词条 {len(terms)} 条（verified {verified} / pending {pending}）")
    print(f"  构式 {len(constructions)} 条（verified {c_verified} / pending {len(constructions) - c_verified}）"
          f" · 词根 {len(data.get('roots', {}).get('thunder', []))} 个"
          f" · 功能位 {len(data.get('functions', []))} 个")
    print(f"  SKILL.md {(SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8').count(chr(10)) + 1} 行")
    for item in warnings:
        print(f"  ! {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""job-search-bw 词频表 frontmatter 门禁（B1，2026-09-27）

校验 01-知识/*.md 词频表页：
1. frontmatter YAML 可解析（内置最小检查：引号平衡 / 未引号冒号 / 重复键）
2. confirmed_at 必填（晋升 active 必须留痕）
3. corpus_size 与 00-raw/ 语料数一致（有则核，无则跳过；00-raw/README.md 占位不计入语料）

report-only：报告失败但由人决定是否修。退出码 0=通过，1=有失败。
运行：
  python3 scripts/check-wordlist.py                              # 独立使用（包根=工作区根）
  python3 scripts/check-wordlist.py --root vault/求职             # Core 挂载（指向领域目录）
"""
import argparse
import os
import re
import sys
import glob


def resolve_root(args_root):
    """检查根目录：--root 显式指定优先，否则回退包目录（独立使用模式）。"""
    if args_root:
        return os.path.abspath(args_root)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_fm_strict(text):
    """内置严格 frontmatter 检查：返回 (ok, err)。"""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return False, "无 frontmatter"
    fm = m.group(1)

    # 引号平衡（忽略转义符）
    s = re.sub(r"\\.", "", fm)
    for ch in ('"', "'"):
        if s.count(ch) % 2 != 0:
            return False, f"引号不平衡: {ch}"

    # 行级检查：重复键、值含未引号冒号（跳过缩进/列表项——多行列表是合法 YAML）
    key_seen = set()
    for line in fm.splitlines():
        line = line.rstrip()
        if not line or line.startswith((" ", "\t", "-")):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if not k:
            continue
        if k in key_seen:
            return False, f"重复键: {k}"
        key_seen.add(k)
        if v and ":" in v and not v.startswith(('"', "'")):
            return False, f"值含未引号冒号: {k}"
    return True, ""


def fm_block(text):
    """提取 frontmatter 文本块（无则空串）。"""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def main():
    parser = argparse.ArgumentParser(description="词频表 frontmatter 门禁（report-only）")
    parser.add_argument("--root", help="检查根目录（Core 挂载模式传领域目录如 vault/求职；默认=包目录，独立使用）")
    args = parser.parse_args()

    root = resolve_root(args.root)
    kb = os.path.join(root, "01-知识")
    raw = os.path.join(root, "00-raw")

    files = sorted(glob.glob(os.path.join(kb, "*.md")))
    if not files:
        print(f"⚠️ 01-知识/ 无词频表页（跳过，root={root}）")
        return 0

    fails = []
    raw_count = 0
    if os.path.isdir(raw):
        # 00-raw/README.md 是占位文件（.gitignore 白名单保留），不计入语料
        raw_count = len(
            [f for f in os.listdir(raw) if f.endswith((".md", ".txt", ".pdf")) and f != "README.md"]
        )

    for p in files:
        if os.path.basename(p) == "README.md":
            continue
        rel = os.path.relpath(p, kb)
        with open(p, encoding="utf-8") as f:
            text = f.read()
        blk = fm_block(text)
        problems = []

        ok, err = parse_fm_strict(text)
        if not ok:
            problems.append(err)

        if "confirmed_at" not in blk:
            problems.append("缺 confirmed_at（晋升 active 必须留痕）")

        m = re.search(r"corpus_size:\s*(\d+)", blk)
        if m and raw_count and int(m.group(1)) != raw_count:
            problems.append(
                f"corpus_size={m.group(1)} 但 00-raw 语料={raw_count}"
            )

        if problems:
            fails.append(f"{rel}: {'；'.join(problems)}")

    if fails:
        print("❌ 词频表 frontmatter 门禁失败:")
        for f in fails:
            print(f"  - {f}")
        return 1

    print(f"✅ 词频表 frontmatter 门禁通过（{len(files)} 页）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

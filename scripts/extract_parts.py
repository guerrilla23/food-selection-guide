#!/usr/bin/env python3
"""
detail SVG (svg/<id>.svg) から OK/NG 食材イラストだけを抽出して
svg/parts/<id>_ok.svg / <id>_ng.svg を生成する。

抽出条件:
  - <g transform="translate(280, 320)"> ... </g>  → OK
  - <g transform="translate(800, 320)"> ... </g>  → NG
  - 各グループ先頭の <circle>(○/×バッジ)と <text>(○/×文字)はスキップ
  - 残りの内容を新しい <svg> に詰めて出力 (viewBox は VIEWBOXES で指定)

新食材追加時の使い方:
  1. svg/<id>.svg を既存と同じ構造で用意
  2. 下の VIEWBOXES に <id> エントリを追加
     (OK 食材のローカル座標が収まる viewBox を指定)
  3. python3 scripts/extract_parts.py を実行
"""
import os
import re
import sys

# 各食材ごとの viewBox (OK 食材グループのローカル座標基準)
# 適切に設定すると食材本体だけが切り出される
VIEWBOXES = {
    'daikon': '-110 -250 220 440',
    'carrot': '-65 -220 130 410',
    'negi':   '-220 -110 440 220',
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_group(svg: str, transform: str) -> str | None:
    """<g transform="translate(transform)"> ... </g> の内側を取り出す。"""
    pattern = rf'<g\s+transform="translate\(\s*{re.escape(transform)}\s*\)"\s*>'
    m = re.search(pattern, svg)
    if not m:
        return None
    start = m.end()
    depth = 1
    pos = start
    while pos < len(svg):
        nxt_open = svg.find('<g', pos)
        nxt_close = svg.find('</g>', pos)
        if nxt_close == -1:
            return None
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 2
        else:
            depth -= 1
            if depth == 0:
                return svg[start:nxt_close]
            pos = nxt_close + 4
    return None


def strip_badge(content: str) -> str:
    """先頭の <circle>(バッジ)と <text>(○/×)を1つずつ取り除く。"""
    content = re.sub(r'^\s*<circle[^>]*?/>\s*', '', content, count=1)
    content = re.sub(r'^\s*<text[^>]*?>[○×]</text>\s*', '', content, count=1)
    return content


def main() -> int:
    parts_dir = os.path.join(ROOT, 'svg', 'parts')
    os.makedirs(parts_dir, exist_ok=True)

    rc = 0
    for food_id, vbox in VIEWBOXES.items():
        src = os.path.join(ROOT, 'svg', f'{food_id}.svg')
        if not os.path.exists(src):
            print(f'  SKIP {food_id} (no detail SVG)', file=sys.stderr)
            continue
        with open(src, encoding='utf-8') as f:
            svg = f.read()

        ok = extract_group(svg, '280, 320')
        ng = extract_group(svg, '800, 320')
        if ok is None or ng is None:
            print(f'  FAIL {food_id} (could not locate OK/NG groups)', file=sys.stderr)
            rc = 1
            continue

        for side, raw in (('ok', ok), ('ng', ng)):
            inner = strip_badge(raw).strip()
            out = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbox}" '
                f'font-family="Noto Sans CJK JP, sans-serif">\n'
                f'{inner}\n'
                f'</svg>\n'
            )
            dst = os.path.join(parts_dir, f'{food_id}_{side}.svg')
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(out)
            print(f'  WROTE svg/parts/{food_id}_{side}.svg')

    return rc


if __name__ == '__main__':
    sys.exit(main())

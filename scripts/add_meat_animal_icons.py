#!/usr/bin/env python3
"""
肉類5品(chicken/pork/beef/venison/boar)の detail SVG に
動物アイコンを追加し、parts SVG を再生成する。

配置: 各 OK / NG グループ内、ローカル座標 (95, 80) に半径28の白円背景 +
       動物頭部のシルエット。サムネイル(240x240)でも認識可能なサイズ。

使い方:
  python3 scripts/add_meat_animal_icons.py
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'svg')

# Each icon is a <g> placed inside the existing OK / NG translate group
# (which has the meat-blob centered at origin, viewBox -130 -110 260 220).
# Icon center: (95, 80), radius 28 → fits bottom-right corner.
# All icons share: white circle bg, ink outline (#3D2817 1.5pt), head profile facing right.
# Icon center: (88, 72), radius 38 (≈30% of 260-wide viewBox).
# Internal coordinates scaled ~1.4× from r=28 baseline so silhouette stays
# proportional inside the larger circle. All icons share: white circle bg,
# strong ink outline (#3D2817 2pt), head profile facing right.
ANIMAL_ICONS = {
    'chicken': '''
    <!-- animal-icon: chicken (head profile, red comb + yellow beak) -->
    <g transform="translate(88, 72)" data-icon="chicken">
      <circle cx="0" cy="0" r="38" fill="#FFFFFF" fill-opacity="0.96" stroke="#3D2817" stroke-width="2"/>
      <path d="M -14 -14 Q -10 -25 -4 -17 Q 1 -28 7 -17 Q 13 -25 16 -14 Z" fill="#D03030" stroke="#3D2817" stroke-width="1.5" stroke-linejoin="round"/>
      <ellipse cx="-3" cy="3" rx="20" ry="17" fill="#FFF4C8" stroke="#3D2817" stroke-width="2"/>
      <path d="M 16 0 L 31 3 L 16 9 Z" fill="#F4A030" stroke="#3D2817" stroke-width="1.5" stroke-linejoin="round"/>
      <ellipse cx="17" cy="14" rx="3.5" ry="5" fill="#D03030" stroke="#3D2817" stroke-width="1.3"/>
      <circle cx="4" cy="-2" r="2.5" fill="#3D2817"/>
    </g>
''',

    'pork': '''
    <!-- animal-icon: pork (snout + ear) -->
    <g transform="translate(88, 72)" data-icon="pork">
      <circle cx="0" cy="0" r="38" fill="#FFFFFF" fill-opacity="0.96" stroke="#3D2817" stroke-width="2"/>
      <path d="M -11 -16 L -3 -25 L 0 -11 Z" fill="#F8B0A0" stroke="#3D2817" stroke-width="2" stroke-linejoin="round"/>
      <path d="M -20 0 Q -20 -14 -6 -17 Q 11 -17 20 -6 Q 25 8 17 17 Q 0 20 -14 14 Q -22 6 -20 0 Z" fill="#F8B0A0" stroke="#3D2817" stroke-width="2"/>
      <ellipse cx="20" cy="6" rx="10" ry="8" fill="#F08878" stroke="#3D2817" stroke-width="2"/>
      <ellipse cx="20" cy="3" rx="1.4" ry="1.8" fill="#3D2817"/>
      <ellipse cx="20" cy="9" rx="1.4" ry="1.8" fill="#3D2817"/>
      <circle cx="3" cy="-4" r="2.3" fill="#3D2817"/>
    </g>
''',

    'beef': '''
    <!-- animal-icon: beef (horns + muzzle, brown) -->
    <g transform="translate(88, 72)" data-icon="beef">
      <circle cx="0" cy="0" r="38" fill="#FFFFFF" fill-opacity="0.96" stroke="#3D2817" stroke-width="2"/>
      <path d="M -11 -14 Q -22 -25 -14 -31" fill="none" stroke="#3D2817" stroke-width="2.6" stroke-linecap="round"/>
      <path d="M 11 -14 Q 22 -25 14 -31" fill="none" stroke="#3D2817" stroke-width="2.6" stroke-linecap="round"/>
      <ellipse cx="-18" cy="-9" rx="5" ry="8" fill="#7A5A3A" stroke="#3D2817" stroke-width="1.8" transform="rotate(-30 -18 -9)"/>
      <ellipse cx="18" cy="-9" rx="5" ry="8" fill="#7A5A3A" stroke="#3D2817" stroke-width="1.8" transform="rotate(30 18 -9)"/>
      <path d="M -15 -3 Q -15 -14 -4 -17 Q 7 -17 15 -14 Q 19 0 18 10 Q 10 20 0 20 Q -13 20 -18 11 Q -18 0 -15 -3 Z" fill="#7A5A3A" stroke="#3D2817" stroke-width="2"/>
      <ellipse cx="0" cy="13" rx="13" ry="7" fill="#D4B07A" stroke="#3D2817" stroke-width="1.7"/>
      <ellipse cx="-4" cy="13" rx="1.3" ry="2" fill="#3D2817"/>
      <ellipse cx="4" cy="13" rx="1.3" ry="2" fill="#3D2817"/>
      <circle cx="-6" cy="-3" r="2.2" fill="#3D2817"/>
      <circle cx="8" cy="-3" r="2.2" fill="#3D2817"/>
    </g>
''',

    'venison': '''
    <!-- animal-icon: venison (branching antlers, slim head, white spots) -->
    <g transform="translate(88, 72)" data-icon="venison">
      <circle cx="0" cy="0" r="38" fill="#FFFFFF" fill-opacity="0.96" stroke="#3D2817" stroke-width="2"/>
      <g fill="none" stroke="#3D2817" stroke-width="2.2" stroke-linecap="round">
        <path d="M -10 -14 L -17 -31"/>
        <path d="M -17 -31 L -24 -27"/>
        <path d="M -17 -31 L -14 -36"/>
        <path d="M -17 -31 L -10 -28"/>
        <path d="M 10 -14 L 17 -31"/>
        <path d="M 17 -31 L 24 -27"/>
        <path d="M 17 -31 L 14 -36"/>
        <path d="M 17 -31 L 10 -28"/>
      </g>
      <ellipse cx="-17" cy="-6" rx="4" ry="7" fill="#A87850" stroke="#3D2817" stroke-width="1.7" transform="rotate(-30 -17 -6)"/>
      <path d="M -14 -3 Q -14 -11 -6 -14 Q 6 -14 14 -8 Q 19 6 17 14 Q 8 20 -3 20 Q -14 17 -17 8 Q -17 0 -14 -3 Z" fill="#A87850" stroke="#3D2817" stroke-width="2"/>
      <ellipse cx="11" cy="14" rx="8" ry="5" fill="#7A5230" stroke="#3D2817" stroke-width="1.6"/>
      <circle cx="15" cy="13" r="2" fill="#3D2817"/>
      <circle cx="-3" cy="-3" r="2" fill="#3D2817"/>
      <circle cx="-7" cy="9" r="2.2" fill="#FFFFFF" opacity="0.9"/>
      <circle cx="-1" cy="13" r="1.4" fill="#FFFFFF" opacity="0.75"/>
    </g>
''',

    'boar': '''
    <!-- animal-icon: boar (tusks + bristles, dark) -->
    <g transform="translate(88, 72)" data-icon="boar">
      <circle cx="0" cy="0" r="38" fill="#FFFFFF" fill-opacity="0.96" stroke="#3D2817" stroke-width="2"/>
      <g fill="#3D2817" stroke="none">
        <path d="M -11 -14 L -14 -24 L -8 -15 Z"/>
        <path d="M -4 -17 L -6 -27 L 0 -17 Z"/>
        <path d="M 4 -17 L 6 -27 L 10 -17 Z"/>
        <path d="M 11 -14 L 14 -24 L 16 -15 Z"/>
      </g>
      <path d="M -17 -11 L -10 -20 L -7 -8 Z" fill="#3D2817" stroke="#3D2817" stroke-width="1.7" stroke-linejoin="round"/>
      <path d="M -17 -3 Q -17 -11 -4 -14 Q 10 -14 18 -8 Q 25 3 22 12 Q 14 20 0 20 Q -14 17 -19 8 Q -19 0 -17 -3 Z" fill="#5D4028" stroke="#3D2817" stroke-width="2"/>
      <ellipse cx="20" cy="9" rx="10" ry="6.5" fill="#3D2817" stroke="#3D2817" stroke-width="1.7"/>
      <path d="M 16 9 Q 16 -1 13 -7" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <path d="M 24 10 Q 24 0 21 -6" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <circle cx="18" cy="7" r="1.3" fill="#FFFFFF"/>
      <circle cx="18" cy="11" r="1.3" fill="#FFFFFF"/>
      <circle cx="0" cy="-3" r="2.2" fill="#3D2817"/>
    </g>
''',
}


def inject_icon(svg_text: str, transform: str, icon_xml: str) -> str:
    """
    detail SVG 内の <g transform="translate(<transform>)"> ... </g>
    の閉じタグ直前に icon_xml を挿入する。
    """
    pattern = rf'(<g\s+transform="translate\(\s*{re.escape(transform)}\s*\)"\s*>)'
    m = re.search(pattern, svg_text)
    if not m:
        raise ValueError(f'translate({transform}) group not found')
    start = m.end()
    depth = 1
    pos = start
    while pos < len(svg_text):
        nxt_open = svg_text.find('<g', pos)
        nxt_close = svg_text.find('</g>', pos)
        if nxt_close == -1:
            raise ValueError('unbalanced groups')
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 2
        else:
            depth -= 1
            if depth == 0:
                # insert before this closing tag
                return svg_text[:nxt_close] + icon_xml + svg_text[nxt_close:]
            pos = nxt_close + 4
    raise ValueError('group not closed')


def strip_existing_icons(svg: str) -> str:
    """Remove previously-injected animal-icon groups, walking nested <g> properly."""
    out = []
    i = 0
    pat = re.compile(r'<!--\s*animal-icon:[^>]*?-->\s*<g\b[^>]*?data-icon="[^"]*"[^>]*?>')
    while True:
        m = pat.search(svg, i)
        if not m:
            out.append(svg[i:])
            return ''.join(out)
        # absorb leading whitespace/newline before the comment
        cmt_start = m.start()
        while cmt_start > i and svg[cmt_start - 1] in ' \t':
            cmt_start -= 1
        if cmt_start > i and svg[cmt_start - 1] == '\n':
            cmt_start -= 1
        out.append(svg[i:cmt_start])
        # walk forward from after opening <g> tag, counting depth
        depth = 1
        pos = m.end()
        while depth > 0 and pos < len(svg):
            nxt_open = svg.find('<g', pos)
            nxt_close = svg.find('</g>', pos)
            if nxt_close == -1:
                raise ValueError('strip: unbalanced groups')
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                pos = nxt_open + 2
            else:
                depth -= 1
                pos = nxt_close + 4
        i = pos


def main() -> int:
    for food_id, icon_xml in ANIMAL_ICONS.items():
        path = os.path.join(SVG_DIR, f'{food_id}.svg')
        if not os.path.exists(path):
            print(f'  SKIP {food_id} (no detail SVG)', file=sys.stderr)
            continue
        with open(path, encoding='utf-8') as f:
            svg = f.read()

        svg = strip_existing_icons(svg)
        svg = inject_icon(svg, '280, 320', icon_xml)
        svg = inject_icon(svg, '800, 320', icon_xml)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f'  WROTE {food_id}.svg (+ animal icon × 2, refreshed)')

    # Regenerate parts so thumbnails inherit the icons
    print('\n  → re-running extract_parts.py …')
    rc = subprocess.call(
        [sys.executable, os.path.join(ROOT, 'scripts', 'extract_parts.py')]
    )
    return rc


if __name__ == '__main__':
    sys.exit(main())

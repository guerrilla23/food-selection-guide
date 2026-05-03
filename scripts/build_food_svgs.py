#!/usr/bin/env python3
"""
食材ごとの詳細 SVG (svg/<id>.svg) を仕様 dict から自動生成する。

OK 側: 水彩風 Pattern A (defs + bleeds + leaves + body + ink lines)
NG 側: フラット (dull colors + imperfections)

実行後、scripts/extract_parts.py の VIEWBOXES に
書き込みヒントが標準出力される。
"""
import os, json, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'svg')

# ============================================================
#  共通ヘルパー: SVG 部品ジェネレーター
# ============================================================

def wc_defs(suffix, body_stops, leaf_stops, seed,
            body_type='radial', body_xy=('35%', '25%')):
    """水彩用 <defs>: body/leaf gradient + rough/blur filter"""
    body_grad_open = (
        f'<radialGradient id="wcBody{suffix}" cx="{body_xy[0]}" cy="{body_xy[1]}">'
        if body_type == 'radial'
        else f'<linearGradient id="wcBody{suffix}" x1="0" y1="0" x2="0" y2="1">'
    )
    body_grad_close = '</radialGradient>' if body_type == 'radial' else '</linearGradient>'
    body_grad_stops = ''.join(
        f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>'
        for o, c, a in body_stops
    )
    leaf_grad_stops = ''.join(
        f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>'
        for o, c, a in leaf_stops
    )
    return f'''<defs>
      {body_grad_open}{body_grad_stops}{body_grad_close}
      <radialGradient id="wcLeaf{suffix}" cx="50%" cy="20%">{leaf_grad_stops}</radialGradient>
      <filter id="wcRough{suffix}" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence baseFrequency="0.04" numOctaves="3" seed="{seed}"/>
        <feDisplacementMap in="SourceGraphic" scale="4"/>
      </filter>
      <filter id="wcBlur{suffix}"><feGaussianBlur stdDeviation="1.5"/></filter>
    </defs>'''


def render_bleeds(suffix, bleeds):
    """bleeds = [(cx, cy, rx, ry, fill)]"""
    if not bleeds: return ''
    inner = ''.join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"/>'
        for cx, cy, rx, ry, fill in bleeds
    )
    return f'<g filter="url(#wcBlur{suffix})" opacity="0.4">{inner}</g>'


def render_leaves(suffix, leaf_paths):
    """leaf_paths = list of d strings (filled with wcLeaf gradient)"""
    if not leaf_paths: return ''
    inner = ''.join(
        f'<path d="{d}" fill="url(#wcLeaf{suffix})"/>'
        for d in leaf_paths
    )
    return f'<g filter="url(#wcRough{suffix})" opacity="0.8">{inner}</g>'


def render_body(suffix, body_paths):
    """body_paths = list of (d, opacity) — filled with wcBody gradient"""
    if not body_paths: return ''
    inner = ''.join(
        f'<path d="{d}" fill="url(#wcBody{suffix})"' +
        (f' opacity="{op}"' if op is not None else '') + '/>'
        for d, op in body_paths
    )
    return f'<g filter="url(#wcRough{suffix})">{inner}</g>'


def render_ink(ink_paths):
    """ink_paths = list of (d, opacity?, stroke_width?)"""
    if not ink_paths: return ''
    inner_parts = []
    for item in ink_paths:
        if isinstance(item, str):
            d, op, sw = item, None, None
        else:
            d = item[0]
            op = item[1] if len(item) > 1 else None
            sw = item[2] if len(item) > 2 else None
        attrs = f'd="{d}"'
        if op is not None: attrs += f' opacity="{op}"'
        if sw is not None: attrs += f' stroke-width="{sw}"'
        inner_parts.append(f'<path {attrs}/>')
    inner = ''.join(inner_parts)
    return (f'<g stroke="#3D2817" stroke-width="3" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0.9">{inner}</g>')


def render_ng_imperfections(imps):
    """imps = list of dicts: {kind: 'ellipse'|'line'|'path', ...}"""
    parts = []
    for i in imps:
        k = i['kind']
        if k == 'ellipse':
            parts.append(f'<ellipse cx="{i["cx"]}" cy="{i["cy"]}" rx="{i["rx"]}" ry="{i["ry"]}" '
                         f'fill="{i["fill"]}" opacity="{i.get("opacity", 0.5)}"/>')
        elif k == 'line':
            parts.append(f'<line x1="{i["x1"]}" y1="{i["y1"]}" x2="{i["x2"]}" y2="{i["y2"]}" '
                         f'stroke="{i.get("stroke", "#5D4E37")}" stroke-width="{i.get("sw", 1.5)}" '
                         f'opacity="{i.get("opacity", 0.6)}"/>')
        elif k == 'path':
            parts.append(f'<path d="{i["d"]}" stroke="{i.get("stroke", "#5D4E37")}" '
                         f'stroke-width="{i.get("sw", 1.5)}" fill="{i.get("fill", "none")}" '
                         f'opacity="{i.get("opacity", 0.6)}"/>')
    return ''.join(parts)


# ============================================================
#  詳細 SVG テンプレート (1080×600)
# ============================================================

DETAIL_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 600" font-family="Noto Sans CJK JP, sans-serif">
  <rect width="1080" height="600" fill="#FFFFFF" rx="20"/>

  <!-- Header -->
  <text x="60" y="60" font-size="44" font-weight="900" fill="{theme_color}">{name}</text>
  <line x1="60" y1="75" x2="{title_underline_end}" y2="75" stroke="{theme_color}" stroke-width="4"/>
  <text x="{season_text_x}" y="68" font-size="22" fill="#666">旬:{season_text}</text>

  <line x1="540" y1="100" x2="540" y2="540" stroke="#DDD" stroke-width="2" stroke-dasharray="6,6"/>

  <!-- OK side (watercolor Pattern A) -->
  <g transform="translate(280, 320)">
    <circle cx="-200" cy="-180" r="22" fill="#2C5F2D"/>
    <text x="-200" y="-172" font-size="26" font-weight="900" fill="white" text-anchor="middle">○</text>
    {ok_defs}
    {ok_bleeds}
    {ok_leaves}
    {ok_body}
    {ok_ink}
  </g>

  <!-- NG side (flat) -->
  <g transform="translate(800, 320)">
    <circle cx="-200" cy="-180" r="22" fill="#C62828"/>
    <text x="-200" y="-172" font-size="26" font-weight="900" fill="white" text-anchor="middle">×</text>
    {ng_content}
  </g>

  <!-- Comparison labels -->
  <g font-size="20" fill="#333">
    <rect x="60" y="495" width="460" height="80" rx="8" fill="#E8F5E9"/>
    <text x="80" y="520" font-weight="bold" fill="#2C5F2D">● {ok_caption_1}</text>
    <text x="80" y="545" font-weight="bold" fill="#2C5F2D">● {ok_caption_2}</text>
    <text x="80" y="568" fill="#666" font-size="17">{ok_sub}</text>

    <rect x="560" y="495" width="460" height="80" rx="8" fill="#FFEBEE"/>
    <text x="580" y="520" font-weight="bold" fill="#C62828">× {ng_caption_1}</text>
    <text x="580" y="545" font-weight="bold" fill="#C62828">× {ng_caption_2}</text>
    <text x="580" y="568" fill="#666" font-size="17">{ng_sub}</text>
  </g>
</svg>
'''


def build_detail_svg(spec):
    suffix = spec['id'].capitalize()
    ok = spec['ok']

    # OK 側
    ok_defs = wc_defs(
        suffix,
        ok['body_stops'],
        ok.get('leaf_stops', [
            ('0%', '#9BCB7A', 0.9),
            ('60%', '#5D8F3D', 0.7),
            ('100%', '#2C5F2D', 0.5),
        ]),
        ok.get('seed', 5),
        body_type=ok.get('body_type', 'radial'),
    )
    ok_bleeds = render_bleeds(suffix, ok.get('bleeds', []))
    ok_leaves = render_leaves(suffix, ok.get('leaves', []))
    body_paths = ok.get('body_paths', [])
    if isinstance(body_paths, str):
        body_paths = [(body_paths, None)]
    ok_body = render_body(suffix, [
        (p, None) if isinstance(p, str) else p for p in body_paths
    ])
    ok_ink = render_ink(ok.get('ink', []))

    # NG 側
    ng = spec['ng']
    ng_inner = []
    # NG body (filled, dull color)
    if ng.get('body_paths'):
        for p in ng['body_paths']:
            if isinstance(p, str):
                d, fill = p, ng['body_color']
            else:
                d, fill = p[0], p[1]
            ng_inner.append(f'<path d="{d}" fill="{fill}"/>')
    # NG leaves (dull)
    if ng.get('leaves'):
        for d in ng['leaves']:
            ng_inner.append(f'<path d="{d}" fill="{ng.get("leaf_color", "#9F8730")}"/>')
    # imperfections
    ng_inner.append(render_ng_imperfections(ng.get('imperfections', [])))
    # subtle outline
    if ng.get('outline_paths'):
        for d in ng['outline_paths']:
            ng_inner.append(f'<path d="{d}" stroke="#A89E7A" stroke-width="1.5" '
                            f'fill="none" opacity="0.7" stroke-linejoin="round"/>')
    ng_content = ''.join(ng_inner)

    # Header positioning
    name_len = len(spec['name'])
    underline_end = 60 + name_len * 30  # rough font-width estimate
    season_text_x = underline_end + 20

    return DETAIL_TEMPLATE.format(
        theme_color=spec['theme_color'],
        name=spec['name'],
        title_underline_end=underline_end,
        season_text=spec['season_text'],
        season_text_x=season_text_x,
        ok_defs=ok_defs,
        ok_bleeds=ok_bleeds,
        ok_leaves=ok_leaves,
        ok_body=ok_body,
        ok_ink=ok_ink,
        ng_content=ng_content,
        ok_caption_1=spec['ok_caption_1'],
        ok_caption_2=spec['ok_caption_2'],
        ok_sub=spec['ok_sub'],
        ng_caption_1=spec['ng_caption_1'],
        ng_caption_2=spec['ng_caption_2'],
        ng_sub=spec['ng_sub'],
    )


# ============================================================
#  9食材スペック (Phase A)
# ============================================================

# 共通ストップ群(再利用)
RED_BODY_STOPS = [
    ('0%', '#FFB0A8', 0.95),
    ('40%', '#FF6655', 0.9),
    ('80%', '#E33825', 0.85),
    ('100%', '#A02818', 0.7),
]
ORANGE_BODY_STOPS = [
    ('0%', '#FFD9B0', 0.95),
    ('40%', '#FFB07A', 0.9),
    ('80%', '#FF8C42', 0.85),
    ('100%', '#D45F1A', 0.7),
]
YELLOW_BODY_STOPS = [
    ('0%', '#FFF5C0', 0.95),
    ('40%', '#FFE066', 0.9),
    ('80%', '#F2C232', 0.85),
    ('100%', '#B88A1B', 0.7),
]
TAN_BODY_STOPS = [
    ('0%', '#F8E8C8', 0.95),
    ('40%', '#E0C088', 0.9),
    ('80%', '#B89058', 0.85),
    ('100%', '#7E5A2A', 0.7),
]
PINK_MEAT_STOPS = [
    ('0%', '#FCD8D0', 0.95),
    ('40%', '#F8AAA0', 0.9),
    ('80%', '#E07770', 0.85),
    ('100%', '#A0463F', 0.65),
]
GREEN_BODY_STOPS = [
    ('0%', '#D4E8B5', 0.95),
    ('40%', '#9BCB7A', 0.9),
    ('80%', '#5D8F3D', 0.85),
    ('100%', '#2C5F2D', 0.65),
]
CREAM_BODY_STOPS = [
    ('0%', '#FFFFFF', 0.95),
    ('40%', '#F8F0E0', 0.85),
    ('80%', '#E8D5B0', 0.7),
    ('100%', '#B89870', 0.5),
]


FOODS = {
    # 1. tomato — round red, green stem
    'tomato': {
        'id': 'tomato',
        'name': 'トマト',
        'theme_color': '#D43A2A',
        'season_text': '6〜9月',
        'viewbox': '-130 -160 260 280',
        'ok': {
            'seed': 11,
            'body_stops': RED_BODY_STOPS,
            'bleeds': [
                (0, -10, 95, 95, '#FF8077'),
                (0, -110, 35, 22, '#5D8F3D'),
            ],
            'leaves': [
                'M -28 -100 Q -32 -125 -10 -130 Q 0 -110 -8 -95 Z',
                'M -2 -100 Q -5 -135 18 -135 Q 22 -120 12 -95 Z',
                'M 18 -100 Q 22 -125 38 -120 Q 36 -108 28 -95 Z',
            ],
            'body_paths': [
                'M -85 0 Q -92 60 0 90 Q 92 60 85 0 Q 80 -85 0 -100 Q -80 -85 -85 0 Z',
            ],
            'ink': [
                ('M -85 0 Q -92 60 0 90 Q 92 60 85 0 Q 80 -85 0 -100 Q -80 -85 -85 0 Z',),
                ('M -28 -100 Q -32 -125 -10 -130',),
                ('M -10 -130 Q 0 -110 -8 -95',),
                ('M -2 -100 Q -5 -135 18 -135',),
                ('M 18 -135 Q 22 -120 12 -95',),
                ('M 18 -100 Q 22 -125 38 -120',),
                ('M 38 -120 Q 36 -108 28 -95',),
                ('M 0 -100 L 0 -90', 0.7),  # stem to body
            ],
        },
        'ng': {
            'body_color': '#C66B5C',
            'leaf_color': '#8B7740',
            'body_paths': [
                'M -85 0 Q -92 60 0 90 Q 92 60 85 0 Q 80 -85 0 -100 Q -80 -85 -85 0 Z',
            ],
            'leaves': [
                'M -28 -100 Q -32 -120 -12 -125 Q 0 -110 -10 -97 Z',
                'M 0 -100 Q -3 -125 16 -127 Q 20 -115 12 -95 Z',
                'M 18 -100 Q 22 -120 34 -118 Q 32 -108 28 -95 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -30, 'cy': 20, 'rx': 18, 'ry': 22,
                 'fill': '#7A4030', 'opacity': 0.45},
                {'kind': 'ellipse', 'cx': 25, 'cy': -20, 'rx': 12, 'ry': 15,
                 'fill': '#7A4030', 'opacity': 0.4},
                {'kind': 'path', 'd': 'M -50 40 Q -20 50 10 35', 'opacity': 0.6},
                {'kind': 'path', 'd': 'M 20 50 Q 50 55 65 40', 'opacity': 0.6},
            ],
        },
        'ok_caption_1': '鮮やかな赤、ヘタが緑でピン',
        'ok_caption_2': 'ハリ・ツヤ、ずっしり重い',
        'ok_sub': '完熟は底が黄色がかる(放射状の白い筋)',
        'ng_caption_1': 'くすんだ赤、ヘタが茶色く萎れ',
        'ng_caption_2': '柔らかい、シワや黒ずみ',
        'ng_sub': '青臭い=未熟・甘み少ない',
    },

    # 2. onion — round bulb, papery skin
    'onion': {
        'id': 'onion',
        'name': '玉ねぎ',
        'theme_color': '#B89048',
        'season_text': '春・秋',
        'viewbox': '-130 -180 260 320',
        'ok': {
            'seed': 13,
            'body_stops': TAN_BODY_STOPS,
            'bleeds': [
                (0, 10, 100, 110, '#E0C088'),
                (0, -130, 25, 18, '#5D8F3D'),
            ],
            'leaves': [
                'M -8 -130 L -3 -160 L 0 -130 Z',  # tiny dried stem
                'M 0 -130 L 5 -158 L 8 -130 Z',
            ],
            'body_paths': [
                'M -85 -50 Q -90 60 0 110 Q 90 60 85 -50 Q 75 -120 0 -130 Q -75 -120 -85 -50 Z',
            ],
            'ink': [
                ('M -85 -50 Q -90 60 0 110 Q 90 60 85 -50 Q 75 -120 0 -130 Q -75 -120 -85 -50 Z',),
                # Dried stem on top
                ('M -10 -130 L -3 -160 L 3 -160 L 10 -130', 0.7, 2),
                # Vertical lines on bulb (papery skin grain)
                ('M -55 -100 Q -50 0 -55 100', 0.5, 1.2),
                ('M -25 -120 Q -20 0 -25 110', 0.5, 1.2),
                ('M 25 -120 Q 20 0 25 110', 0.5, 1.2),
                ('M 55 -100 Q 50 0 55 100', 0.5, 1.2),
                # Roots (5 short lines at bottom)
                ('M -20 110 L -25 130', 0.7, 2),
                ('M -8 112 L -10 135', 0.7, 2),
                ('M 5 112 L 5 138', 0.7, 2),
                ('M 18 112 L 22 135', 0.7, 2),
                ('M 30 110 L 38 130', 0.7, 2),
            ],
        },
        'ng': {
            'body_color': '#A88858',
            'body_paths': [
                'M -85 -50 Q -90 60 0 110 Q 90 60 85 -50 Q 75 -120 0 -130 Q -75 -120 -85 -50 Z',
            ],
            'imperfections': [
                # Mold (greenish patch)
                {'kind': 'ellipse', 'cx': -30, 'cy': 30, 'rx': 22, 'ry': 28,
                 'fill': '#5D5A2A', 'opacity': 0.5},
                # Sprouting greens out the top
                {'kind': 'path', 'd': 'M -5 -130 Q -10 -170 -5 -200',
                 'stroke': '#6B7A38', 'sw': 3, 'opacity': 0.85},
                {'kind': 'path', 'd': 'M 5 -130 Q 10 -180 8 -210',
                 'stroke': '#6B7A38', 'sw': 3, 'opacity': 0.85},
                # Wrinkles
                {'kind': 'path', 'd': 'M -60 -30 Q -20 -25 20 -35',
                 'stroke': '#5D4E37', 'sw': 1.5, 'opacity': 0.55},
                {'kind': 'path', 'd': 'M -60 30 Q -20 25 20 35',
                 'stroke': '#5D4E37', 'sw': 1.5, 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '皮がパリッ、ハリ・ツヤあり',
        'ok_caption_2': 'ずっしり重い、芽が出ていない',
        'ok_sub': '頭・お尻が硬く締まる=新鮮',
        'ng_caption_1': '柔らかい、皮がベタつく',
        'ng_caption_2': '芽が出ている、青いカビ',
        'ng_sub': '芯が黒い=傷み始め(切ると分かる)',
    },

    # 3. egg — oval beige
    'egg': {
        'id': 'egg',
        'name': '卵',
        'theme_color': '#C8A878',
        'season_text': '通年',
        'viewbox': '-100 -140 200 260',
        'ok': {
            'seed': 17,
            'body_stops': CREAM_BODY_STOPS,
            'bleeds': [
                (0, 0, 80, 105, '#E8D5B0'),
            ],
            'leaves': [],
            'body_paths': [
                'M -55 0 Q -55 -85 0 -100 Q 55 -85 55 0 Q 55 85 0 100 Q -55 85 -55 0 Z',
            ],
            'ink': [
                ('M -55 0 Q -55 -85 0 -100 Q 55 -85 55 0 Q 55 85 0 100 Q -55 85 -55 0 Z',),
            ],
        },
        'ng': {
            'body_color': '#D5C0A0',
            'body_paths': [
                'M -55 0 Q -55 -85 0 -100 Q 55 -85 55 0 Q 55 85 0 100 Q -55 85 -55 0 Z',
            ],
            'imperfections': [
                # Crack lines
                {'kind': 'path', 'd': 'M -25 -50 L -15 -20 L -25 0 L -10 25',
                 'stroke': '#5D4E37', 'sw': 2, 'opacity': 0.85},
                {'kind': 'path', 'd': 'M 10 -65 L 25 -45',
                 'stroke': '#5D4E37', 'sw': 1.8, 'opacity': 0.7},
                # Brown stains
                {'kind': 'ellipse', 'cx': 20, 'cy': 30, 'rx': 12, 'ry': 8,
                 'fill': '#8B6F47', 'opacity': 0.4},
                {'kind': 'ellipse', 'cx': -30, 'cy': 50, 'rx': 8, 'ry': 6,
                 'fill': '#8B6F47', 'opacity': 0.4},
            ],
        },
        'ok_caption_1': 'ヒビ・割れがない、表面ザラつかない',
        'ok_caption_2': '振っても音がしない、形が整う',
        'ok_sub': '冷蔵庫から出した時に汗をかかない',
        'ng_caption_1': 'ヒビあり、汚れが付着',
        'ng_caption_2': '振るとカチャカチャ音(中の腐敗)',
        'ng_sub': '黄身が崩れる=古い、白身が広がる',
    },

    # 4. chicken — pink meat slab
    'chicken': {
        'id': 'chicken',
        'name': '鶏肉',
        'theme_color': '#D87878',
        'season_text': '通年',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 19,
            'body_stops': PINK_MEAT_STOPS,
            'bleeds': [
                (0, 0, 110, 70, '#F8AAA0'),
            ],
            'leaves': [],
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'ink': [
                ('M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',),
                # Muscle fiber lines (subtle)
                ('M -75 -25 Q 0 -20 75 -25', 0.6, 1.5),
                ('M -78 0 Q 0 5 78 0', 0.6, 1.5),
                ('M -72 25 Q 0 30 72 25', 0.6, 1.5),
                # Light fat marbling (small dots)
                ('M -40 -10 L -38 -8', 0.7, 2.5),
                ('M 30 5 L 32 7', 0.7, 2.5),
                ('M 0 -30 L 2 -28', 0.7, 2.5),
            ],
        },
        'ng': {
            'body_color': '#A88078',
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'imperfections': [
                # Gray patches
                {'kind': 'ellipse', 'cx': -30, 'cy': 0, 'rx': 25, 'ry': 18,
                 'fill': '#5D4E37', 'opacity': 0.35},
                {'kind': 'ellipse', 'cx': 35, 'cy': 15, 'rx': 18, 'ry': 12,
                 'fill': '#5D4E37', 'opacity': 0.35},
                # Drip pool below (suggesting drip loss)
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 50, 'ry': 8,
                 'fill': '#A05050', 'opacity': 0.4},
            ],
        },
        'ok_caption_1': '鮮やかなピンク、ツヤあり',
        'ok_caption_2': '弾力ある、ドリップ少',
        'ok_sub': '皮は黄色みかかった白で毛穴くっきり',
        'ng_caption_1': '色がくすむ・グレーがかる',
        'ng_caption_2': 'ドリップが赤茶色、ベタつく',
        'ng_sub': '酸っぱい・アンモニア臭は腐敗',
    },

    # 5. potato — brown oval with eyes
    'potato': {
        'id': 'potato',
        'name': 'じゃがいも',
        'theme_color': '#A07848',
        'season_text': '春・秋',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 23,
            'body_stops': TAN_BODY_STOPS,
            'bleeds': [
                (0, 0, 95, 75, '#C8A878'),
            ],
            'leaves': [],
            'body_paths': [
                'M -85 -10 Q -95 -55 -50 -75 Q 0 -85 50 -72 Q 90 -55 85 -10 Q 95 50 50 75 Q 0 80 -50 70 Q -95 50 -85 -10 Z',
            ],
            'ink': [
                ('M -85 -10 Q -95 -55 -50 -75 Q 0 -85 50 -72 Q 90 -55 85 -10 Q 95 50 50 75 Q 0 80 -50 70 Q -95 50 -85 -10 Z',),
                # Eyes (tiny circles)
                ('M -30 -20 a 4 4 0 0 1 8 0 a 4 4 0 0 1 -8 0 Z', 0.7, 1.5),
                ('M 20 0 a 4 4 0 0 1 8 0 a 4 4 0 0 1 -8 0 Z', 0.7, 1.5),
                ('M -10 30 a 4 4 0 0 1 8 0 a 4 4 0 0 1 -8 0 Z', 0.7, 1.5),
                ('M 35 -35 a 3 3 0 0 1 6 0 a 3 3 0 0 1 -6 0 Z', 0.6, 1.5),
            ],
        },
        'ng': {
            'body_color': '#988050',
            'body_paths': [
                'M -85 -10 Q -95 -55 -50 -75 Q 0 -85 50 -72 Q 90 -55 85 -10 Q 95 50 50 75 Q 0 80 -50 70 Q -95 50 -85 -10 Z',
            ],
            'imperfections': [
                # Green patches (solanine warning)
                {'kind': 'ellipse', 'cx': -45, 'cy': -20, 'rx': 25, 'ry': 20,
                 'fill': '#7BAB46', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 30, 'cy': 30, 'rx': 18, 'ry': 14,
                 'fill': '#7BAB46', 'opacity': 0.5},
                # Sprouting from eyes
                {'kind': 'path', 'd': 'M 20 -10 Q 25 -30 30 -55',
                 'stroke': '#5D8F3D', 'sw': 3, 'opacity': 0.85},
                {'kind': 'path', 'd': 'M -10 25 Q -5 45 -3 65',
                 'stroke': '#5D8F3D', 'sw': 3, 'opacity': 0.85},
                # Wrinkles
                {'kind': 'path', 'd': 'M -60 0 Q -20 5 20 0', 'opacity': 0.55},
                {'kind': 'path', 'd': 'M -50 40 Q 0 45 50 35', 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '皮にハリ、表面が硬い',
        'ok_caption_2': '緑色がない、芽が出ていない',
        'ok_sub': '同じ大きさで重い=でんぷん多い',
        'ng_caption_1': '緑色がかった部分(ソラニン)',
        'ng_caption_2': '芽が出ている、シワがある',
        'ng_sub': '緑・芽は必ず厚めに取り除く',
    },

    # 6. cabbage — round green
    'cabbage': {
        'id': 'cabbage',
        'name': 'キャベツ',
        'theme_color': '#5D9F3D',
        'season_text': '春・冬',
        'viewbox': '-140 -130 280 270',
        'ok': {
            'seed': 29,
            'body_stops': GREEN_BODY_STOPS,
            'bleeds': [
                (0, 0, 110, 100, '#9BCB7A'),
            ],
            'leaves': [],
            'body_paths': [
                'M 0 -100 Q -100 -90 -100 -10 Q -100 80 0 100 Q 100 80 100 -10 Q 100 -90 0 -100 Z',
            ],
            'ink': [
                # Outer outline
                ('M 0 -100 Q -100 -90 -100 -10 Q -100 80 0 100 Q 100 80 100 -10 Q 100 -90 0 -100 Z',),
                # Inner leaf veins/lines (suggesting layered leaves)
                ('M -85 -30 Q 0 -20 85 -30', 0.7, 1.8),
                ('M -90 0 Q 0 10 90 0', 0.7, 1.8),
                ('M -85 30 Q 0 40 85 30', 0.7, 1.8),
                # Center vein (top to center)
                ('M 0 -95 L 0 50', 0.6, 1.5),
                # Side ribs
                ('M -50 -90 Q -55 -10 -45 75', 0.5, 1.3),
                ('M 50 -90 Q 55 -10 45 75', 0.5, 1.3),
            ],
        },
        'ng': {
            'body_color': '#B8B860',
            'body_paths': [
                'M 0 -100 Q -100 -90 -100 -10 Q -100 80 0 100 Q 100 80 100 -10 Q 100 -90 0 -100 Z',
            ],
            'imperfections': [
                # Yellow outer leaves
                {'kind': 'path', 'd': 'M -100 -10 Q -110 -5 -115 10 Q -90 -5 -100 0',
                 'stroke': '#A0A040', 'sw': 2, 'opacity': 0.7},
                # Brown spots
                {'kind': 'ellipse', 'cx': -20, 'cy': 30, 'rx': 15, 'ry': 10,
                 'fill': '#7A5520', 'opacity': 0.45},
                {'kind': 'ellipse', 'cx': 40, 'cy': -10, 'rx': 10, 'ry': 8,
                 'fill': '#7A5520', 'opacity': 0.4},
                # Loose leaves lines
                {'kind': 'path', 'd': 'M -85 -30 Q 0 -25 85 -30', 'opacity': 0.5},
                {'kind': 'path', 'd': 'M -90 0 Q 0 5 90 0', 'opacity': 0.5},
            ],
        },
        'ok_caption_1': 'ずっしり重い(同サイズで)',
        'ok_caption_2': '外葉の緑が鮮やか、ハリあり',
        'ok_sub': '春キャベツ=軽くフワッ、冬=重く詰まる',
        'ng_caption_1': '軽い、外葉が黄色く萎れ',
        'ng_caption_2': '切り口が茶色、ベタつく',
        'ng_sub': 'カット品は切り口が白いものを選ぶ',
    },

    # 7. cucumber — long green, slight curve
    'cucumber': {
        'id': 'cucumber',
        'name': 'きゅうり',
        'theme_color': '#5D8F3D',
        'season_text': '6〜8月',
        'viewbox': '-180 -90 360 180',
        'ok': {
            'seed': 31,
            'body_stops': GREEN_BODY_STOPS,
            'bleeds': [
                (0, 0, 165, 30, '#9BCB7A'),
            ],
            'leaves': [],
            'body_paths': [
                'M -150 -8 Q -160 -25 -130 -25 L 130 -22 Q 158 -22 152 -5 L 150 8 Q 155 25 130 25 L -130 22 Q -160 22 -150 -8 Z',
            ],
            'ink': [
                ('M -150 -8 Q -160 -25 -130 -25 L 130 -22 Q 158 -22 152 -5 L 150 8 Q 155 25 130 25 L -130 22 Q -160 22 -150 -8 Z',),
                # Bumps (イボ) — tiny dots along the surface
                ('M -100 -22 L -98 -25', 0.8, 2.5),
                ('M -50 -23 L -48 -27', 0.8, 2.5),
                ('M 0 -22 L 2 -26', 0.8, 2.5),
                ('M 50 -22 L 52 -25', 0.8, 2.5),
                ('M 100 -23 L 102 -26', 0.8, 2.5),
                ('M -75 22 L -77 26', 0.8, 2.5),
                ('M -25 23 L -23 27', 0.8, 2.5),
                ('M 25 22 L 27 26', 0.8, 2.5),
                ('M 75 23 L 77 26', 0.8, 2.5),
                # Stem
                ('M -150 -3 L -165 -3', 0.7, 2),
            ],
        },
        'ng': {
            'body_color': '#A0A858',
            'body_paths': [
                'M -150 -8 Q -160 -25 -130 -25 L 130 -22 Q 158 -22 152 -5 L 150 8 Q 155 25 130 25 L -130 22 Q -160 22 -150 -8 Z',
            ],
            'imperfections': [
                # Yellow patches
                {'kind': 'ellipse', 'cx': -30, 'cy': 0, 'rx': 30, 'ry': 12,
                 'fill': '#C8B040', 'opacity': 0.5},
                {'kind': 'ellipse', 'cx': 60, 'cy': 0, 'rx': 25, 'ry': 10,
                 'fill': '#C8B040', 'opacity': 0.5},
                # Wrinkles (longitudinal)
                {'kind': 'path', 'd': 'M -120 -8 Q 0 -5 120 -8', 'opacity': 0.6},
                {'kind': 'path', 'd': 'M -120 8 Q 0 5 120 8', 'opacity': 0.6},
            ],
        },
        'ok_caption_1': 'イボがチクチク、皮にハリ',
        'ok_caption_2': '濃い緑、太さが均一',
        'ok_sub': '小さくとも太さがしっかり=みずみずしい',
        'ng_caption_1': 'イボがなく表面ツルツル(古い)',
        'ng_caption_2': '黄色い斑点、軟らかい',
        'ng_sub': '曲がりがある=味は変わらない、安い',
    },

    # 8. banana — curved yellow
    'banana': {
        'id': 'banana',
        'name': 'バナナ',
        'theme_color': '#E0B040',
        'season_text': '通年',
        'viewbox': '-150 -110 300 220',
        'ok': {
            'seed': 37,
            'body_stops': YELLOW_BODY_STOPS,
            'bleeds': [
                (0, 10, 140, 75, '#FFE066'),
            ],
            'leaves': [],
            'body_paths': [
                'M -120 -50 Q -135 -10 -120 35 Q -60 70 0 75 Q 80 80 120 60 Q 130 35 110 -5 Q 100 -50 60 -55 Q 0 -45 -120 -50 Z',
            ],
            'ink': [
                ('M -120 -50 Q -135 -10 -120 35 Q -60 70 0 75 Q 80 80 120 60 Q 130 35 110 -5 Q 100 -50 60 -55 Q 0 -45 -120 -50 Z',),
                # Stem (左端)
                ('M -120 -50 L -135 -68 L -125 -75', 0.85, 2.5),
                # Tip (右端 black tip)
                ('M 120 60 L 130 70 L 130 78', 0.85, 2.5),
                # Edges (longitudinal ridges on banana)
                ('M -100 -42 Q 0 -38 100 -8', 0.6, 1.5),
                ('M -100 25 Q 0 50 100 50', 0.6, 1.5),
            ],
        },
        'ng': {
            'body_color': '#988030',
            'body_paths': [
                'M -120 -50 Q -135 -10 -120 35 Q -60 70 0 75 Q 80 80 120 60 Q 130 35 110 -5 Q 100 -50 60 -55 Q 0 -45 -120 -50 Z',
            ],
            'imperfections': [
                # Black bruises (large)
                {'kind': 'ellipse', 'cx': -50, 'cy': 0, 'rx': 30, 'ry': 25,
                 'fill': '#3D2817', 'opacity': 0.7},
                {'kind': 'ellipse', 'cx': 30, 'cy': 20, 'rx': 25, 'ry': 22,
                 'fill': '#3D2817', 'opacity': 0.7},
                {'kind': 'ellipse', 'cx': 80, 'cy': -10, 'rx': 18, 'ry': 15,
                 'fill': '#3D2817', 'opacity': 0.65},
                # Stem dried
                {'kind': 'path', 'd': 'M -120 -50 L -135 -68 L -125 -75',
                 'stroke': '#3D2817', 'sw': 3, 'opacity': 0.8},
            ],
        },
        'ok_caption_1': '黄色が鮮やか、軸が緑',
        'ok_caption_2': 'シュガースポット少なめ',
        'ok_sub': '糖度ピーク=斑点出始め(完熟)',
        'ng_caption_1': '全体に黒い斑点が大きく広がる',
        'ng_caption_2': '軸が黒く折れそう、軟らかい',
        'ng_sub': '皮全体が黒くても、中が良ければ食べれる',
    },

    # 9. apple — round red
    'apple': {
        'id': 'apple',
        'name': 'りんご',
        'theme_color': '#C82828',
        'season_text': '9〜12月',
        'viewbox': '-120 -140 240 280',
        'ok': {
            'seed': 41,
            'body_stops': RED_BODY_STOPS,
            'bleeds': [
                (0, 0, 100, 100, '#FF8077'),
            ],
            'leaves': [
                # 小さな緑の葉(ヘタの根本)
                'M 5 -100 Q 18 -110 25 -98 Q 18 -92 8 -98 Z',
            ],
            'body_paths': [
                'M -90 -5 Q -100 50 -50 90 Q 0 100 50 90 Q 100 50 90 -5 Q 95 -75 50 -90 Q 25 -82 5 -90 Q -25 -100 -50 -85 Q -95 -75 -90 -5 Z',
            ],
            'ink': [
                ('M -90 -5 Q -100 50 -50 90 Q 0 100 50 90 Q 100 50 90 -5 Q 95 -75 50 -90 Q 25 -82 5 -90 Q -25 -100 -50 -85 Q -95 -75 -90 -5 Z',),
                # Stem (top center)
                ('M 0 -90 L -5 -115 L 5 -120', 0.85, 2.5),
                # Top dimple suggestion
                ('M -20 -85 Q 0 -78 20 -85', 0.6, 1.5),
                # Leaf
                ('M 5 -100 Q 18 -110 25 -98 Q 18 -92 8 -98', 0.85, 2),
            ],
        },
        'ng': {
            'body_color': '#A05858',
            'body_paths': [
                'M -90 -5 Q -100 50 -50 90 Q 0 100 50 90 Q 100 50 90 -5 Q 95 -75 50 -90 Q 25 -82 5 -90 Q -25 -100 -50 -85 Q -95 -75 -90 -5 Z',
            ],
            'imperfections': [
                # Bruises
                {'kind': 'ellipse', 'cx': -35, 'cy': 25, 'rx': 22, 'ry': 18,
                 'fill': '#5D2A20', 'opacity': 0.5},
                {'kind': 'ellipse', 'cx': 30, 'cy': -10, 'rx': 15, 'ry': 12,
                 'fill': '#5D2A20', 'opacity': 0.45},
                # Wrinkles (old apple)
                {'kind': 'path', 'd': 'M -70 -30 Q -30 -25 0 -35', 'opacity': 0.6},
                {'kind': 'path', 'd': 'M 5 35 Q 35 30 60 40', 'opacity': 0.55},
                # Dried stem
                {'kind': 'path', 'd': 'M 0 -90 L -5 -115',
                 'stroke': '#5D4E37', 'sw': 2, 'opacity': 0.7},
            ],
        },
        'ok_caption_1': '色が濃い、ツヤあり',
        'ok_caption_2': 'お尻が黄色みかかる(完熟)',
        'ok_sub': 'ずっしり重い=蜜入りの可能性',
        'ng_caption_1': '色がくすむ、傷・打痕あり',
        'ng_caption_2': 'シワ、ヘタが乾いて黒い',
        'ng_sub': 'フワッと軽い=水分抜け、ぼけ',
    },
}


# ============================================================
#  メイン処理: SVG 出力 + 設定エクスポート
# ============================================================

def main():
    written = []
    for fid, spec in FOODS.items():
        svg = build_detail_svg(spec)
        path = os.path.join(SVG_DIR, f'{fid}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        written.append(fid)
        print(f'  WROTE svg/{fid}.svg ({len(svg)} bytes)')

    # extract_parts.py に書き加えるべき viewBox 値を出力
    print('\n--- VIEWBOXES additions for scripts/extract_parts.py ---')
    for fid in written:
        print(f"    '{fid}': '{FOODS[fid]['viewbox']}',")


if __name__ == '__main__':
    main()

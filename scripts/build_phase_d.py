#!/usr/bin/env python3
"""
Phase D (ステップ1): ジビエ2食材のドラフトSVGを生成。
- 鹿肉 (venison)
- 猪肉 (boar)

ヒロキ(現役ハンター)の専門知識による補強はステップ2で実施。
ここでは標準的な情報源 (家庭料理ガイド・食品成分表) に基づいたドラフト。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_food_svgs import build_detail_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'svg')

# ============================================================
#  Phase D 用カラーストップ
# ============================================================
# 鹿肉: 深い赤(ヘモグロビン濃度高)、ほぼ脂なし
VENISON_DEEP_RED = [
    ('0%', '#E0A090', 0.95),
    ('40%', '#C04030', 0.9),
    ('80%', '#7A1810', 0.85),
    ('100%', '#3A0808', 0.65),
]
# 猪肉: ピンクがかった赤、白い脂層が特徴
BOAR_PINK_RED = [
    ('0%', '#F8C8B8', 0.95),
    ('40%', '#D87060', 0.9),
    ('80%', '#9A3020', 0.85),
    ('100%', '#581008', 0.65),
]


PHASE_D_FOODS = {

    # 鹿肉 — lean deep red slab
    'venison': {
        'id': 'venison', 'name': '鹿肉',
        'theme_color': '#7A1810',
        'season_text': '11〜2月(狩猟期)',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 223,
            'body_stops': VENISON_DEEP_RED,
            'bleeds': [(0, 0, 110, 70, '#C04030')],
            'leaves': [],
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'ink': [
                ('M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',),
                # Fine fiber lines (赤身肉の繊維、細かく密)
                ('M -78 -30 Q 0 -25 78 -30', 0.6, 1.3),
                ('M -82 -10 Q 0 -5 82 -10', 0.6, 1.3),
                ('M -80 10 Q 0 15 80 10', 0.6, 1.3),
                ('M -75 30 Q 0 35 75 30', 0.6, 1.3),
                ('M -70 50 Q 0 55 70 50', 0.6, 1.3),
                # Suggesting density (very fine cross-hatching)
                ('M -50 -20 L -45 30', 0.4, 1),
                ('M 0 -25 L 5 35', 0.4, 1),
                ('M 50 -20 L 45 30', 0.4, 1),
            ],
        },
        'ng': {
            'body_color': '#5A3030',
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'imperfections': [
                # Brown discoloration
                {'kind': 'ellipse', 'cx': -25, 'cy': 0, 'rx': 30, 'ry': 22, 'fill': '#3D2010', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 30, 'cy': 20, 'rx': 18, 'ry': 14, 'fill': '#3D2010', 'opacity': 0.5},
                # Drip pool (heavy bleed)
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 60, 'ry': 8, 'fill': '#601810', 'opacity': 0.65},
            ],
        },
        'ok_caption_1': '色が深い赤、繊維が細かい',
        'ok_caption_2': '脂が極めて少ない(赤身)',
        'ok_sub': '血抜きの良いものはドリップ少なく無臭',
        'ng_caption_1': '色が茶色く変色',
        'ng_caption_2': '強い獣臭、ドリップ多',
        'ng_sub': '血抜き不十分=臭み強・処理要注意',
    },

    # 猪肉 — pink-red slab with white fat band
    'boar': {
        'id': 'boar', 'name': '猪肉',
        'theme_color': '#9A3020',
        'season_text': '11〜2月(狩猟期)',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 227,
            'body_stops': BOAR_PINK_RED,
            'bleeds': [(0, 0, 110, 70, '#D87060')],
            'leaves': [],
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'ink': [
                ('M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',),
                # 脂層と肉の境界線(細く控えめに)
                ('M -85 -28 Q 0 -25 85 -28', 0.55, 1.6),
                # Muscle fiber lines
                ('M -82 -8 Q 0 -3 82 -8', 0.65, 1.5),
                ('M -78 12 Q 0 17 78 12', 0.65, 1.5),
                ('M -72 32 Q 0 37 72 32', 0.65, 1.5),
                ('M -65 52 Q 0 57 65 52', 0.65, 1.5),
                # Subtle marbling (脂が混じる)
                ('M -45 0 Q -25 5 -5 -5', 0.7, 2.2),
                ('M 15 22 Q 35 27 55 18', 0.7, 2.2),
                ('M -55 40 Q -30 45 -10 38', 0.65, 2),
            ],
        },
        'ng': {
            'body_color': '#783030',
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'imperfections': [
                # Yellowed fat
                {'kind': 'path', 'd': 'M -85 -35 Q 0 -30 85 -35',
                 'stroke': '#A88830', 'sw': 4, 'opacity': 0.7},
                # Dark patches
                {'kind': 'ellipse', 'cx': -25, 'cy': 10, 'rx': 25, 'ry': 18, 'fill': '#3D1818', 'opacity': 0.5},
                {'kind': 'ellipse', 'cx': 30, 'cy': 30, 'rx': 18, 'ry': 12, 'fill': '#3D1818', 'opacity': 0.5},
                # Heavy drip
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 60, 'ry': 8, 'fill': '#702018', 'opacity': 0.6},
            ],
        },
        'ok_caption_1': '色が鮮ピンク赤、脂が白い',
        'ok_caption_2': '脂と肉の境がくっきり',
        'ok_sub': '冬場の脂のった個体=甘い・旨味強',
        'ng_caption_1': '色が暗赤、脂が黄ばむ',
        'ng_caption_2': '強い獣臭・ベタつき',
        'ng_sub': '夏場の個体=脂少なく硬め・臭い強',
    },
}


def main():
    for fid, spec in PHASE_D_FOODS.items():
        svg = build_detail_svg(spec)
        path = os.path.join(SVG_DIR, f'{fid}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f'  WROTE svg/{fid}.svg ({len(svg)} bytes)')

    print('\n--- VIEWBOXES additions for scripts/extract_parts.py ---')
    for fid, spec in PHASE_D_FOODS.items():
        print(f"    '{fid}':{' ' * (10 - len(fid))}'{spec['viewbox']}',")


if __name__ == '__main__':
    main()

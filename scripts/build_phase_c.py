#!/usr/bin/env python3
"""
Phase C: 11食材(タンパク質系)の詳細SVGを生成。
- 豆腐, 納豆, ヨーグルト
- 豚肉, 牛肉, ひき肉
- 鮭, 鯖, アジ, エビ, 一尾魚の見方
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_food_svgs import build_detail_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'svg')

# ============================================================
#  Phase C 用カラーストップ
# ============================================================
PORK_PINK = [
    ('0%', '#FFE0D8', 0.95),
    ('40%', '#F8B0A0', 0.9),
    ('80%', '#E08070', 0.85),
    ('100%', '#A05040', 0.65),
]
BEEF_RED = [
    ('0%', '#F8B8A8', 0.95),
    ('40%', '#D87060', 0.9),
    ('80%', '#A03020', 0.85),
    ('100%', '#601810', 0.65),
]
SALMON_ORANGE = [
    ('0%', '#FFD8C0', 0.95),
    ('40%', '#FFA070', 0.9),
    ('80%', '#E07050', 0.85),
    ('100%', '#A04030', 0.65),
]
SILVER_FISH = [
    ('0%', '#F8F8FA', 0.95),
    ('40%', '#D0D8DC', 0.9),
    ('80%', '#90A0A8', 0.85),
    ('100%', '#506068', 0.65),
]
NATTO_BEAN = [
    # 明るい暖色系 (#E8C49A - #C19A6B 範囲) で美味しそうに
    ('0%', '#F8DDB0', 0.95),
    ('40%', '#E8C49A', 0.92),
    ('80%', '#C19A6B', 0.85),
    ('100%', '#8B6F47', 0.55),
]
SHRIMP_GREY_PINK = [
    ('0%', '#F0DCD0', 0.95),
    ('40%', '#D0A898', 0.9),
    ('80%', '#A07060', 0.85),
    ('100%', '#604040', 0.65),
]
TOFU_WHITE = [
    ('0%', '#FFFFFF', 0.95),
    ('40%', '#F8F4E8', 0.9),
    ('80%', '#E8E0CC', 0.75),
    ('100%', '#B0A88C', 0.5),
]
YOGURT_WHITE = [
    ('0%', '#FFFFFF', 0.95),
    ('40%', '#FAF5E8', 0.9),
    ('80%', '#E8DCC0', 0.7),
    ('100%', '#B89870', 0.4),
]
GROUND_MEAT_PINK = [
    ('0%', '#FFD0C0', 0.95),
    ('40%', '#F8907A', 0.9),
    ('80%', '#C85040', 0.85),
    ('100%', '#803020', 0.65),
]


# ============================================================
#  Phase C FOODS
# ============================================================

PHASE_C_FOODS = {

    # =================== 豆製品 (2) ===================

    # 1. tofu — white block
    'tofu': {
        'id': 'tofu', 'name': '豆腐',
        'theme_color': '#C8A878',
        'season_text': '通年',
        'viewbox': '-110 -90 220 180',
        'ok': {
            'seed': 157,
            'body_stops': TOFU_WHITE,
            'bleeds': [(0, 0, 100, 65, '#F0E8D0')],
            'leaves': [],
            'body_paths': [
                # Rectangular block (slight 3D feel)
                'M -85 -55 L 85 -55 Q 92 -55 92 -48 L 92 48 Q 92 55 85 55 L -85 55 Q -92 55 -92 48 L -92 -48 Q -92 -55 -85 -55 Z',
            ],
            'ink': [
                ('M -85 -55 L 85 -55 Q 92 -55 92 -48 L 92 48 Q 92 55 85 55 L -85 55 Q -92 55 -92 48 L -92 -48 Q -92 -55 -85 -55 Z',),
                # Subtle top edge highlight
                ('M -80 -55 L 80 -55', 0.5, 1.4),
                # Surface texture (smooth)
                ('M -70 -25 Q 0 -22 70 -25', 0.4, 1.2),
                ('M -75 5 Q 0 7 75 5', 0.4, 1.2),
                ('M -70 30 Q 0 32 70 30', 0.4, 1.2),
            ],
        },
        'ng': {
            'body_color': '#D8C898',
            'body_paths': [
                'M -85 -55 L 85 -55 Q 92 -55 92 -48 L 92 48 Q 92 55 85 55 L -85 55 Q -92 55 -92 48 L -92 -48 Q -92 -55 -85 -55 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -30, 'cy': 10, 'rx': 22, 'ry': 18, 'fill': '#A8A050', 'opacity': 0.4},
                {'kind': 'ellipse', 'cx': 35, 'cy': -15, 'rx': 18, 'ry': 14, 'fill': '#A8A050', 'opacity': 0.4},
                # Cracks
                {'kind': 'path', 'd': 'M -10 -55 L -5 0 L -15 55', 'opacity': 0.6},
                {'kind': 'path', 'd': 'M 20 -55 L 25 0 L 18 55', 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '形が整う、角が綺麗',
        'ok_caption_2': '水が透き通る、無臭',
        'ok_sub': '絹=つるん、木綿=ザラ・しっかり',
        'ng_caption_1': '形が崩れる、ベタつき',
        'ng_caption_2': '水が濁る、酸っぱい臭',
        'ng_sub': '黄ばみ・ヌメリ=傷み始め',
    },

    # 2. natto — appetizing warm-toned beans with highlights and silky strings
    'natto': {
        'id': 'natto', 'name': '納豆',
        'theme_color': '#C19A6B',
        'season_text': '通年',
        'viewbox': '-130 -120 260 240',
        'ok': {
            'seed': 163,
            'body_stops': NATTO_BEAN,
            'bleeds': [
                # 暖色のにじみで美味しそう
                (0, 20, 125, 85, '#D8B888'),
            ],
            'leaves': [],
            # 大粒12個 + 小粒3個 = 15粒。山積み
            'body_paths': [
                # 底層 (大きめ)
                'M -85 65 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0 Z',
                'M -50 72 m -17 0 a 17 13 0 1 0 34 0 a 17 13 0 1 0 -34 0 Z',
                'M -12 68 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0 Z',
                'M 25 72 m -17 0 a 17 13 0 1 0 34 0 a 17 13 0 1 0 -34 0 Z',
                'M 60 65 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0 Z',
                # 中層
                'M -65 35 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                'M -28 40 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0 Z',
                'M 8 36 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                'M 42 38 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                # 上層
                'M -42 5 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M -8 8 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                'M 25 4 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                # 山頂
                'M -18 -25 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
                'M 14 -28 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
                'M -2 -52 m -11 0 a 11 9 0 1 0 22 0 a 11 9 0 1 0 -22 0 Z',
            ],
            # extra_svg: 各粒のハイライト + 艶やかな糸引き
            'extra_svg': '''
                <!-- 粒のハイライト (各粒に小さな白い艶) -->
                <g fill="#FFF5DC" opacity="0.7">
                    <ellipse cx="-89" cy="60" rx="5" ry="3"/>
                    <ellipse cx="-54" cy="67" rx="6" ry="3.5"/>
                    <ellipse cx="-16" cy="63" rx="5" ry="3"/>
                    <ellipse cx="21" cy="67" rx="6" ry="3.5"/>
                    <ellipse cx="56" cy="60" rx="5" ry="3"/>
                    <ellipse cx="-69" cy="30" rx="5" ry="3"/>
                    <ellipse cx="-32" cy="35" rx="5" ry="3"/>
                    <ellipse cx="4" cy="31" rx="5" ry="3"/>
                    <ellipse cx="38" cy="33" rx="5" ry="3"/>
                    <ellipse cx="-46" cy="0" rx="4" ry="2.5"/>
                    <ellipse cx="-12" cy="3" rx="5" ry="3"/>
                    <ellipse cx="21" cy="-1" rx="4" ry="2.5"/>
                    <ellipse cx="-22" cy="-30" rx="4" ry="2.5"/>
                    <ellipse cx="10" cy="-33" rx="4" ry="2.5"/>
                    <ellipse cx="-6" cy="-56" rx="3.5" ry="2"/>
                </g>
                <!-- 糸引き (白〜半透明の細曲線) -->
                <g stroke="#FFF5E0" stroke-width="1.5" fill="none" opacity="0.85" stroke-linecap="round">
                    <path d="M -2 -55 Q -15 -85 -40 -105"/>
                    <path d="M 14 -55 Q 30 -90 60 -110"/>
                    <path d="M -18 -32 Q 0 -65 25 -55"/>
                    <path d="M -8 8 Q 5 -10 25 4"/>
                    <path d="M -28 40 Q -10 22 8 36"/>
                    <path d="M -50 72 Q -30 50 -12 68"/>
                </g>
                <!-- 糸引きの輝く中心線 (より細く明るく) -->
                <g stroke="#FFFFFF" stroke-width="0.8" fill="none" opacity="0.6" stroke-linecap="round">
                    <path d="M -2 -55 Q -15 -85 -40 -105"/>
                    <path d="M 14 -55 Q 30 -90 60 -110"/>
                </g>
            ''',
            'ink': [
                # 各粒の輪郭 (細めで柔らかく)
                ('M -85 65 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0', 0.85, 2),
                ('M -50 72 m -17 0 a 17 13 0 1 0 34 0 a 17 13 0 1 0 -34 0', 0.85, 2),
                ('M -12 68 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0', 0.85, 2),
                ('M 25 72 m -17 0 a 17 13 0 1 0 34 0 a 17 13 0 1 0 -34 0', 0.85, 2),
                ('M 60 65 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0', 0.85, 2),
                ('M -65 35 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0', 0.85, 2),
                ('M -28 40 m -16 0 a 16 13 0 1 0 32 0 a 16 13 0 1 0 -32 0', 0.85, 2),
                ('M 8 36 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0', 0.85, 2),
                ('M 42 38 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0', 0.85, 2),
                ('M -42 5 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0', 0.85, 2),
                ('M -8 8 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0', 0.85, 2),
                ('M 25 4 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0', 0.85, 2),
                ('M -18 -25 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0', 0.85, 2),
                ('M 14 -28 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0', 0.85, 2),
                ('M -2 -52 m -11 0 a 11 9 0 1 0 22 0 a 11 9 0 1 0 -22 0', 0.85, 2),
            ],
        },
        'ng': {
            'body_color': '#988050',
            'body_paths': [
                # 同じ粒配置だが乾燥・粒不揃いを表現
                'M -82 65 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M -52 70 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                'M -18 67 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M 18 70 m -15 0 a 15 12 0 1 0 30 0 a 15 12 0 1 0 -30 0 Z',
                'M 52 65 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M -68 35 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
                'M -38 38 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M -8 35 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
                'M 22 38 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M -22 8 m -14 0 a 14 11 0 1 0 28 0 a 14 11 0 1 0 -28 0 Z',
                'M 8 5 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
                'M 0 -25 m -13 0 a 13 10 0 1 0 26 0 a 13 10 0 1 0 -26 0 Z',
            ],
            'imperfections': [
                # 糸引き弱・カビ
                {'kind': 'ellipse', 'cx': -55, 'cy': 0, 'rx': 22, 'ry': 14, 'fill': '#3D3018', 'opacity': 0.6},
                {'kind': 'ellipse', 'cx': 35, 'cy': -10, 'rx': 18, 'ry': 12, 'fill': '#3D3018', 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '豆が均一、ふっくら',
        'ok_caption_2': '糸引き(粘り)が強い',
        'ok_sub': '匂いは独特だが新鮮な発酵臭',
        'ng_caption_1': '豆が乾燥・粒揃わず',
        'ng_caption_2': '糸引きが弱い・ない',
        'ng_sub': '異臭(アンモニア強)=傷み',
    },

    # =================== 肉類 (3) ===================

    # 3. pork — pink slab
    'pork': {
        'id': 'pork', 'name': '豚肉',
        'theme_color': '#E08878',
        'season_text': '通年',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 167,
            'body_stops': PORK_PINK,
            'bleeds': [(0, 0, 110, 70, '#F8B0A0')],
            'leaves': [],
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'ink': [
                ('M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',),
                # Muscle fiber lines
                ('M -75 -25 Q 0 -20 75 -25', 0.6, 1.5),
                ('M -78 0 Q 0 5 78 0', 0.6, 1.5),
                ('M -72 25 Q 0 30 72 25', 0.6, 1.5),
                # Fat marbling (white veins)
                ('M -45 -10 Q -20 -5 0 -15', 0.7, 2),
                ('M 20 5 Q 40 15 60 5', 0.7, 2),
                ('M -30 30 Q 0 38 30 30', 0.7, 2),
            ],
        },
        'ng': {
            'body_color': '#A87878',
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -30, 'cy': 0, 'rx': 25, 'ry': 18, 'fill': '#5D4E37', 'opacity': 0.4},
                {'kind': 'ellipse', 'cx': 35, 'cy': 15, 'rx': 18, 'ry': 12, 'fill': '#5D4E37', 'opacity': 0.4},
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 50, 'ry': 8, 'fill': '#A03828', 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '色が淡いピンク、ツヤあり',
        'ok_caption_2': '脂は白く、肉と境がくっきり',
        'ok_sub': '弾力あり、ドリップ少なめ',
        'ng_caption_1': '色が暗い赤・グレー',
        'ng_caption_2': '脂が黄ばむ・ベタつく',
        'ng_sub': 'ドリップ多+赤茶=要注意',
    },

    # 4. beef — red slab with marbling
    'beef': {
        'id': 'beef', 'name': '牛肉',
        'theme_color': '#A04030',
        'season_text': '通年',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 173,
            'body_stops': BEEF_RED,
            'bleeds': [(0, 0, 110, 70, '#D87060')],
            'leaves': [],
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'ink': [
                ('M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',),
                # Muscle fiber lines (more prominent for beef)
                ('M -75 -30 Q 0 -25 75 -30', 0.65, 1.5),
                ('M -78 -5 Q 0 0 78 -5', 0.65, 1.5),
                ('M -72 20 Q 0 25 72 20', 0.65, 1.5),
                ('M -65 45 Q 0 50 65 45', 0.65, 1.5),
                # Fat marbling (bright white lines)
                ('M -55 -18 Q -25 -12 5 -22', 0.75, 2.2),
                ('M -10 -3 Q 20 5 50 -5', 0.75, 2.2),
                ('M 25 18 Q 50 22 70 12', 0.75, 2.2),
                ('M -45 32 Q -15 38 15 30', 0.75, 2.2),
                ('M 30 45 Q 50 50 65 42', 0.7, 2),
            ],
        },
        'ng': {
            'body_color': '#683838',
            'body_paths': [
                'M -90 -45 Q -100 0 -90 50 Q 0 75 90 50 Q 100 0 90 -45 Q 0 -65 -90 -45 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -25, 'cy': 0, 'rx': 30, 'ry': 22, 'fill': '#3D2817', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 30, 'cy': 20, 'rx': 18, 'ry': 14, 'fill': '#3D2817', 'opacity': 0.45},
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 55, 'ry': 8, 'fill': '#601810', 'opacity': 0.6},
            ],
        },
        'ok_caption_1': '色が鮮やかな赤、ツヤあり',
        'ok_caption_2': '脂が白く、霜降りが綺麗',
        'ok_sub': '弾力あり、繊維が均一',
        'ng_caption_1': '色がどす黒い赤、グレー',
        'ng_caption_2': '脂が黄ばむ、ベタつく',
        'ng_sub': '空気に長く触れた=酸化(切る前なら鮮)',
    },

    # 5. ground_meat — pile/mound
    'ground_meat': {
        'id': 'ground_meat', 'name': 'ひき肉',
        'theme_color': '#D87878',
        'season_text': '通年',
        'viewbox': '-130 -110 260 220',
        'ok': {
            'seed': 179,
            'body_stops': GROUND_MEAT_PINK,
            'bleeds': [(0, 5, 115, 75, '#F8907A')],
            'leaves': [],
            'body_paths': [
                # Irregular pile
                'M -100 30 Q -110 -10 -85 -35 Q -55 -55 -25 -45 Q 0 -60 30 -45 Q 60 -60 85 -35 Q 110 -10 100 30 Q 80 55 0 60 Q -80 55 -100 30 Z',
            ],
            'ink': [
                ('M -100 30 Q -110 -10 -85 -35 Q -55 -55 -25 -45 Q 0 -60 30 -45 Q 60 -60 85 -35 Q 110 -10 100 30 Q 80 55 0 60 Q -80 55 -100 30 Z',),
                # Texture lines (suggesting ground meat strands)
                ('M -75 -10 L -68 -5', 0.6, 1.5),
                ('M -45 -25 L -38 -20', 0.6, 1.5),
                ('M -20 -10 L -13 -5', 0.6, 1.5),
                ('M 10 -25 L 17 -20', 0.6, 1.5),
                ('M 40 -10 L 47 -5', 0.6, 1.5),
                ('M 65 -20 L 72 -15', 0.6, 1.5),
                ('M -60 15 L -53 20', 0.6, 1.5),
                ('M -25 25 L -18 30', 0.6, 1.5),
                ('M 15 20 L 22 25', 0.6, 1.5),
                ('M 50 25 L 57 30', 0.6, 1.5),
                ('M -40 45 L -33 50', 0.6, 1.5),
                ('M 30 45 L 37 50', 0.6, 1.5),
            ],
        },
        'ng': {
            'body_color': '#9D6868',
            'body_paths': [
                'M -100 30 Q -110 -10 -85 -35 Q -55 -55 -25 -45 Q 0 -60 30 -45 Q 60 -60 85 -35 Q 110 -10 100 30 Q 80 55 0 60 Q -80 55 -100 30 Z',
            ],
            'imperfections': [
                # Dark patches
                {'kind': 'ellipse', 'cx': -40, 'cy': -10, 'rx': 22, 'ry': 18, 'fill': '#3D2817', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 30, 'cy': 10, 'rx': 18, 'ry': 14, 'fill': '#3D2817', 'opacity': 0.5},
                # Drip pool below
                {'kind': 'ellipse', 'cx': 0, 'cy': 65, 'rx': 75, 'ry': 8, 'fill': '#A03828', 'opacity': 0.55},
            ],
        },
        'ok_caption_1': '色が均一なピンク',
        'ok_caption_2': 'べた付かず、ふんわり',
        'ok_sub': '当日加工品=最も新鮮',
        'ng_caption_1': '部分的に色が濃い、グレー',
        'ng_caption_2': 'ドリップ多、ベタベタ',
        'ng_sub': '混ざり物が出る=酸化進行',
    },

    # =================== 魚介 (5) ===================

    # 6. salmon — filet (cut)
    'salmon': {
        'id': 'salmon', 'name': '鮭(切り身)',
        'theme_color': '#E07050',
        'season_text': '9〜11月(秋鮭)',
        'viewbox': '-140 -90 280 180',
        'ok': {
            'seed': 181,
            'body_stops': SALMON_ORANGE,
            'bleeds': [(0, 0, 125, 70, '#FFA070')],
            'leaves': [],
            'body_paths': [
                # Filet cross-section (roughly trapezoid)
                'M -120 -50 Q -130 -10 -120 30 Q -100 55 -50 60 L 100 55 Q 130 50 125 0 Q 120 -50 80 -55 Q 0 -60 -120 -50 Z',
            ],
            'ink': [
                ('M -120 -50 Q -130 -10 -120 30 Q -100 55 -50 60 L 100 55 Q 130 50 125 0 Q 120 -50 80 -55 Q 0 -60 -120 -50 Z',),
                # Fat lines (white striations on salmon)
                ('M -100 -30 Q 0 -20 100 -30', 0.75, 2.2),
                ('M -100 -5 Q 0 0 100 -5', 0.75, 2.2),
                ('M -100 25 Q 0 30 100 25', 0.75, 2.2),
                # Skin edge (darker line at bottom)
                ('M -110 50 Q 0 58 105 52', 0.7, 2),
            ],
        },
        'ng': {
            'body_color': '#A06848',
            'body_paths': [
                'M -120 -50 Q -130 -10 -120 30 Q -100 55 -50 60 L 100 55 Q 130 50 125 0 Q 120 -50 80 -55 Q 0 -60 -120 -50 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -50, 'cy': 0, 'rx': 30, 'ry': 22, 'fill': '#5D4E37', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 40, 'cy': 10, 'rx': 22, 'ry': 18, 'fill': '#5D4E37', 'opacity': 0.5},
                # Drip
                {'kind': 'ellipse', 'cx': 0, 'cy': 70, 'rx': 70, 'ry': 8, 'fill': '#A03828', 'opacity': 0.5},
            ],
        },
        'ok_caption_1': 'オレンジ色が鮮やか',
        'ok_caption_2': '脂(白いライン)がくっきり',
        'ok_sub': '皮目に銀色の艶=新鮮',
        'ng_caption_1': '色が褐色、くすむ',
        'ng_caption_2': '白いラインが不明瞭',
        'ng_sub': 'ドリップ多+表面ヌメ=傷み',
    },

    # 7. saba — whole mackerel
    'saba': {
        'id': 'saba', 'name': '鯖',
        'theme_color': '#506068',
        'season_text': '10〜2月',
        'viewbox': '-160 -80 320 160',
        'ok': {
            'seed': 191,
            'body_stops': SILVER_FISH,
            'bleeds': [(0, 0, 145, 55, '#90A0A8')],
            'leaves': [],
            'body_paths': [
                # Fish body (oval) + tail
                'M -130 0 Q -125 -45 -50 -50 Q 60 -50 110 -28 L 130 -22 Q 145 -10 145 0 Q 145 10 130 22 L 110 28 Q 60 50 -50 50 Q -125 45 -130 0 Z',
                # Tail
                'M 130 -22 L 155 -45 L 150 0 L 155 45 L 130 22 Z',
            ],
            'ink': [
                ('M -130 0 Q -125 -45 -50 -50 Q 60 -50 110 -28 L 130 -22 Q 145 -10 145 0 Q 145 10 130 22 L 110 28 Q 60 50 -50 50 Q -125 45 -130 0 Z',),
                ('M 130 -22 L 155 -45 L 150 0 L 155 45 L 130 22',),
                # Eye
                ('M -110 -15 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0 Z', 0.95, 2.2),
                # Mouth
                ('M -130 0 Q -135 5 -125 12', 0.85, 1.8),
                # Saba's signature wave pattern (back markings)
                ('M -80 -38 Q -50 -45 -20 -38', 0.75, 2),
                ('M 0 -42 Q 30 -48 60 -40', 0.75, 2),
                ('M -60 -28 Q -30 -35 -10 -28', 0.6, 1.6),
                ('M 20 -32 Q 50 -38 80 -30', 0.6, 1.6),
                # Lateral line
                ('M -100 5 Q 0 8 110 5', 0.5, 1.4),
                # Gill
                ('M -90 -30 Q -85 0 -88 30', 0.6, 1.6),
            ],
        },
        'ng': {
            'body_color': '#787878',
            'body_paths': [
                'M -130 0 Q -125 -45 -50 -50 Q 60 -50 110 -28 L 130 -22 Q 145 -10 145 0 Q 145 10 130 22 L 110 28 Q 60 50 -50 50 Q -125 45 -130 0 Z',
                'M 130 -22 L 155 -45 L 150 0 L 155 45 L 130 22 Z',
            ],
            'imperfections': [
                # Cloudy eye
                {'kind': 'ellipse', 'cx': -110, 'cy': -15, 'rx': 5, 'ry': 5, 'fill': '#C8C0B0', 'opacity': 0.85},
                # Brown gill (oxidized)
                {'kind': 'ellipse', 'cx': -90, 'cy': 0, 'rx': 8, 'ry': 18, 'fill': '#7A4828', 'opacity': 0.55},
                # Dull body patches
                {'kind': 'ellipse', 'cx': 0, 'cy': 0, 'rx': 50, 'ry': 25, 'fill': '#5D4E37', 'opacity': 0.35},
            ],
        },
        'ok_caption_1': '目が黒く澄む、エラ赤',
        'ok_caption_2': '銀色の輝き、青波紋くっきり',
        'ok_sub': '腹がしっかり、押すと弾力',
        'ng_caption_1': '目が白く濁る、エラ茶色',
        'ng_caption_2': '体表のヌメリ多、臭い',
        'ng_sub': '腹が柔らか・破れ=傷み',
    },

    # 8. aji — horse mackerel
    'aji': {
        'id': 'aji', 'name': 'アジ',
        'theme_color': '#506068',
        'season_text': '5〜8月',
        'viewbox': '-140 -80 280 160',
        'ok': {
            'seed': 193,
            'body_stops': SILVER_FISH,
            'bleeds': [(0, 0, 125, 55, '#90A0A8')],
            'leaves': [],
            'body_paths': [
                'M -110 0 Q -105 -42 -40 -48 Q 50 -50 95 -28 L 115 -22 Q 128 -10 128 0 Q 128 10 115 22 L 95 28 Q 50 50 -40 48 Q -105 42 -110 0 Z',
                # Tail
                'M 115 -22 L 135 -38 L 130 0 L 135 38 L 115 22 Z',
            ],
            'ink': [
                ('M -110 0 Q -105 -42 -40 -48 Q 50 -50 95 -28 L 115 -22 Q 128 -10 128 0 Q 128 10 115 22 L 95 28 Q 50 50 -40 48 Q -105 42 -110 0 Z',),
                ('M 115 -22 L 135 -38 L 130 0 L 135 38 L 115 22',),
                # Eye
                ('M -90 -15 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0 Z', 0.95, 2.2),
                # Mouth
                ('M -110 0 Q -115 5 -105 12', 0.85, 1.8),
                # Aji's signature: yellow lateral streak (zeigo)
                ('M -70 5 Q 0 10 95 8', 0.85, 3),  # thick line for zeigo
                # Gill cover
                ('M -80 -25 Q -75 0 -78 25', 0.6, 1.6),
                # Scales hint
                ('M -50 -25 Q -20 -20 10 -25', 0.5, 1.4),
                ('M 20 -25 Q 50 -20 80 -25', 0.5, 1.4),
            ],
        },
        'ng': {
            'body_color': '#787878',
            'body_paths': [
                'M -110 0 Q -105 -42 -40 -48 Q 50 -50 95 -28 L 115 -22 Q 128 -10 128 0 Q 128 10 115 22 L 95 28 Q 50 50 -40 48 Q -105 42 -110 0 Z',
                'M 115 -22 L 135 -38 L 130 0 L 135 38 L 115 22 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -90, 'cy': -15, 'rx': 5, 'ry': 5, 'fill': '#C8C0B0', 'opacity': 0.85},
                {'kind': 'ellipse', 'cx': -80, 'cy': 0, 'rx': 8, 'ry': 18, 'fill': '#7A4828', 'opacity': 0.55},
                {'kind': 'ellipse', 'cx': 30, 'cy': 0, 'rx': 60, 'ry': 25, 'fill': '#5D4E37', 'opacity': 0.3},
            ],
        },
        'ok_caption_1': '目が澄む、エラ赤、銀光る',
        'ok_caption_2': 'ぜいご(尾近の硬鱗)固',
        'ok_sub': 'ハリあり、腹に張りがある',
        'ng_caption_1': '目が濁る、エラ茶色',
        'ng_caption_2': '体表ヌメ、軟らか',
        'ng_sub': 'お腹が柔→内臓劣化',
    },

    # 9. ebi — curled shrimp (C-shape body with tail fan + antennae)
    'ebi': {
        'id': 'ebi', 'name': 'エビ',
        'theme_color': '#A07060',
        'season_text': '通年',
        'viewbox': '-130 -120 260 240',
        'ok': {
            'seed': 197,
            'body_stops': SHRIMP_GREY_PINK,
            'bleeds': [(0, 10, 110, 80, '#D0A898')],
            'leaves': [],
            'body_paths': [
                # Curled C-shape body (thick arc)
                # Outer back curve (head→back→tail) then inner belly back to head
                'M -85 -55 Q -115 -10 -100 50 Q -70 95 -10 95 Q 60 90 95 55 L 75 25 Q 55 0 15 5 Q -25 15 -55 -10 Q -75 -30 -85 -55 Z',
                # Tail fan (right end, fanning out)
                'M 95 55 L 115 75 L 105 50 L 120 35 L 95 30 Z',
            ],
            'ink': [
                ('M -85 -55 Q -115 -10 -100 50 Q -70 95 -10 95 Q 60 90 95 55 L 75 25 Q 55 0 15 5 Q -25 15 -55 -10 Q -75 -30 -85 -55 Z',),
                ('M 95 55 L 115 75 L 105 50 L 120 35 L 95 30',),
                # Body segments (curved bands across the back)
                ('M -88 -25 Q -75 -10 -60 -20', 0.65, 1.5),
                ('M -100 5 Q -82 18 -65 5', 0.65, 1.5),
                ('M -98 35 Q -75 48 -55 38', 0.65, 1.5),
                ('M -75 70 Q -50 80 -25 70', 0.65, 1.5),
                ('M -25 85 Q 5 90 30 80', 0.65, 1.5),
                ('M 30 75 Q 55 78 80 65', 0.65, 1.5),
                # Antennae (long, from head)
                ('M -88 -55 Q -110 -75 -125 -100', 0.85, 2),
                ('M -75 -55 Q -90 -80 -100 -110', 0.7, 1.8),
                # Eye (head)
                ('M -75 -45 m -3 0 a 3 3 0 1 0 6 0 a 3 3 0 1 0 -6 0 Z', 0.95, 2),
                # Legs (small downward strokes)
                ('M -90 50 L -95 75', 0.65, 1.5),
                ('M -55 80 L -55 100', 0.65, 1.5),
                ('M -15 90 L -10 110', 0.65, 1.5),
                ('M 30 88 L 35 108', 0.65, 1.5),
            ],
        },
        'ng': {
            'body_color': '#705048',
            'body_paths': [
                'M -85 -55 Q -115 -10 -100 50 Q -70 95 -10 95 Q 60 90 95 55 L 75 25 Q 55 0 15 5 Q -25 15 -55 -10 Q -75 -30 -85 -55 Z',
                'M 95 55 L 115 75 L 105 50 L 120 35 L 95 30 Z',
            ],
            'imperfections': [
                # Black head (傷み始め)
                {'kind': 'ellipse', 'cx': -85, 'cy': -45, 'rx': 18, 'ry': 14, 'fill': '#1A1008', 'opacity': 0.75},
                # Soft middle
                {'kind': 'ellipse', 'cx': -20, 'cy': 50, 'rx': 35, 'ry': 25, 'fill': '#3D2817', 'opacity': 0.5},
            ],
        },
        'ok_caption_1': '殻が透き通る、節くっきり',
        'ok_caption_2': '頭・尾が黒くない',
        'ok_sub': '触ってハリ、ヒゲ折れず',
        'ng_caption_1': '頭が黒い・赤い斑点',
        'ng_caption_2': '殻と身が離れる、軟らか',
        'ng_sub': '色変=長期冷凍→冷凍焼け',
    },

    # 10. whole_fish — generic guide
    'whole_fish': {
        'id': 'whole_fish', 'name': '一尾魚の見方',
        'theme_color': '#506068',
        'season_text': '魚種により',
        'viewbox': '-160 -90 320 180',
        'ok': {
            'seed': 199,
            'body_stops': SILVER_FISH,
            'bleeds': [(0, 0, 145, 60, '#A0B0B8')],
            'leaves': [],
            'body_paths': [
                'M -130 0 Q -125 -50 -50 -55 Q 60 -55 110 -32 L 130 -25 Q 145 -12 145 0 Q 145 12 130 25 L 110 32 Q 60 55 -50 55 Q -125 50 -130 0 Z',
                'M 130 -25 L 158 -50 L 152 0 L 158 50 L 130 25 Z',
            ],
            'ink': [
                ('M -130 0 Q -125 -50 -50 -55 Q 60 -55 110 -32 L 130 -25 Q 145 -12 145 0 Q 145 12 130 25 L 110 32 Q 60 55 -50 55 Q -125 50 -130 0 Z',),
                ('M 130 -25 L 158 -50 L 152 0 L 158 50 L 130 25',),
                # Eye (highlighted as key check point)
                ('M -110 -18 m -7 0 a 7 7 0 1 0 14 0 a 7 7 0 1 0 -14 0 Z', 0.95, 2.5),
                # Gill (highlighted)
                ('M -90 -35 Q -85 0 -88 35', 0.85, 2.5),
                # Mouth
                ('M -130 0 Q -135 8 -123 15', 0.85, 1.8),
                # Lateral line
                ('M -100 5 Q 0 8 110 5', 0.55, 1.4),
                # Scales hint
                ('M -50 -30 Q -20 -25 10 -30', 0.5, 1.3),
                ('M 20 -30 Q 50 -25 80 -30', 0.5, 1.3),
                # Belly highlight
                ('M -80 35 Q 0 40 90 35', 0.5, 1.4),
            ],
        },
        'ng': {
            'body_color': '#787878',
            'body_paths': [
                'M -130 0 Q -125 -50 -50 -55 Q 60 -55 110 -32 L 130 -25 Q 145 -12 145 0 Q 145 12 130 25 L 110 32 Q 60 55 -50 55 Q -125 50 -130 0 Z',
                'M 130 -25 L 158 -50 L 152 0 L 158 50 L 130 25 Z',
            ],
            'imperfections': [
                {'kind': 'ellipse', 'cx': -110, 'cy': -18, 'rx': 7, 'ry': 7, 'fill': '#C8C0B0', 'opacity': 0.85},
                {'kind': 'ellipse', 'cx': -90, 'cy': 0, 'rx': 9, 'ry': 22, 'fill': '#7A4828', 'opacity': 0.6},
                {'kind': 'ellipse', 'cx': 0, 'cy': 0, 'rx': 60, 'ry': 30, 'fill': '#5D4E37', 'opacity': 0.3},
            ],
        },
        'ok_caption_1': '目:黒く澄む / エラ:赤',
        'ok_caption_2': '体表:銀ピカ / 弾力あり',
        'ok_sub': '腹が固い=内臓新鮮',
        'ng_caption_1': '目:白濁 / エラ:茶〜黒',
        'ng_caption_2': '体表:ヌメ・乾 / 軟',
        'ng_sub': '腹が破れる=内臓崩れ',
    },

    # 11. yogurt — pot/container
    'yogurt': {
        'id': 'yogurt', 'name': 'ヨーグルト',
        'theme_color': '#C8A878',
        'season_text': '通年',
        'viewbox': '-90 -130 180 260',
        'ok': {
            'seed': 211,
            'body_stops': YOGURT_WHITE,
            'bleeds': [(0, 0, 80, 110, '#F8F0E0')],
            'leaves': [],
            'body_paths': [
                # Container
                'M -75 -100 Q -78 -110 -65 -110 L 65 -110 Q 78 -110 75 -100 L 78 100 Q 80 115 60 115 L -60 115 Q -80 115 -78 100 Z',
            ],
            'ink': [
                ('M -75 -100 Q -78 -110 -65 -110 L 65 -110 Q 78 -110 75 -100 L 78 100 Q 80 115 60 115 L -60 115 Q -80 115 -78 100 Z',),
                # Lid line (top)
                ('M -75 -90 L 75 -90', 0.7, 1.6),
                # Surface (smooth ripple)
                ('M -65 -75 Q 0 -78 65 -75', 0.5, 1.4),
                ('M -60 -50 Q 0 -53 60 -50', 0.4, 1.2),
                # Label area (rectangle suggestion)
                ('M -55 -10 L 55 -10 L 55 50 L -55 50 Z', 0.45, 1.4),
            ],
        },
        'ng': {
            'body_color': '#C8B898',
            'body_paths': [
                'M -75 -100 Q -78 -110 -65 -110 L 65 -110 Q 78 -110 75 -100 L 78 100 Q 80 115 60 115 L -60 115 Q -80 115 -78 100 Z',
            ],
            'imperfections': [
                # Whey separation (yellow liquid on top)
                {'kind': 'path', 'd': 'M -70 -85 Q -30 -75 0 -85 Q 30 -95 70 -83',
                 'stroke': '#C8B040', 'sw': 3, 'opacity': 0.7},
                # Lumps in body
                {'kind': 'ellipse', 'cx': -25, 'cy': 30, 'rx': 18, 'ry': 14, 'fill': '#A88830', 'opacity': 0.5},
                {'kind': 'ellipse', 'cx': 25, 'cy': 60, 'rx': 14, 'ry': 10, 'fill': '#A88830', 'opacity': 0.45},
            ],
        },
        'ok_caption_1': '表面が滑らか、白色',
        'ok_caption_2': '容器が膨らんでいない',
        'ok_sub': '蓋を開けて酸味の良い香り',
        'ng_caption_1': '表面に黄色い液(ホエイ)分離大',
        'ng_caption_2': '容器が膨らむ(発酵過剰)',
        'ng_sub': 'カビ・異臭=即廃棄',
    },
}


def main():
    for fid, spec in PHASE_C_FOODS.items():
        svg = build_detail_svg(spec)
        path = os.path.join(SVG_DIR, f'{fid}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f'  WROTE svg/{fid}.svg ({len(svg)} bytes)')

    print('\n--- VIEWBOXES additions for scripts/extract_parts.py ---')
    for fid, spec in PHASE_C_FOODS.items():
        print(f"    '{fid}':{' ' * (12 - len(fid))}'{spec['viewbox']}',")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Phase 3-B: 果物11品の英訳ドラフトを foods.json に適用。

【翻訳方針】
- name: 国際的に通じる英語名 + 日本固有のものは ({English補足}) 形式
  - みかん: Mikan (Satsuma Mandarin) — 日本のみかんは Satsuma が最も近い
  - 柿:    Kaki (Japanese Persimmon)
  - 梨:    Asian Pear (Nashi)
- ぶどう (Grape): 「ブルーム」 → "bloom" (果実表面の自然な白い粉)
- バナナ: シュガースポット → "sugar spots", 軸 → "stem"
- 文化依存表現は補足:「医者いらず」 → "An apple a day keeps the doctor away"
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


TRANSLATIONS = {
    # ============================ 1. banana ============================
    'banana': {
        'name': 'Banana',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the skin color',
            'judgment': 'Yellow with green stem = OK',
        },
        'ok_short': [
            'Color: Vivid yellow',
            'Stem: Greenish',
            'Spots: Few',
            'Firmness: Yes',
        ],
        'ng_short': [
            'Black: Widespread',
            'Stem: Black/Snappable',
            'Feel: Soft',
            'Skin: Torn',
        ],
        'ok_points': [
            'Vivid yellow color throughout',
            'Stem (the base of the bunch) is greenish and not broken',
            'Few or just-emerging sugar spots (small brown speckles)',
            'Firm skin with solid shape',
        ],
        'ng_points': [
            'Large black spots spreading across the skin',
            'Stem is black, dry, and thin enough to snap',
            'Too soft when pressed',
            'Skin is torn, juice leaking out',
        ],
        'summary_ok': 'Vivid yellow, green stem, few spots',
        'summary_ng': 'Blackened, dry stem, soft',
        'storage': {
            'method': 'Hang at room temperature, or separate the hands so the underside doesn\'t bruise',
            'duration': 'Room temp: 3-5 days. Refrigerated: skin darkens but flesh keeps 1 week',
            'tips': 'Refrigerate to halt ripening once mature. Peak sweetness is when sugar spots just begin to appear',
        },
        'usage_tips': 'Pre-ripe: salads/cooking; ripe: eat as-is or in smoothies; overripe: bread/baking. Can be frozen with the skin on',
        'nutrition_highlight': 'Potassium (blood pressure), vitamin B6, dietary fiber. Excellent for energy (medium GI)',
    },

    # ============================ 2. apple ============================
    'apple': {
        'name': 'Apple',
        'subcategory': '',
        'season_peak': 'Autumn–Early winter',
        'key_check': {
            'action': 'Check the bottom (stem-opposite end) color',
            'judgment': 'Yellowing = ripe',
        },
        'ok_short': [
            'Color: Deep/Vivid',
            'Shine: Yes',
            'Bottom: Yellowing',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Color: Dull/Spotted',
            'Feel: Soft',
            'Stem: Dry/Black',
            'Skin: Wrinkled',
        ],
        'ok_points': [
            'Deep, vivid color with shine',
            'Bottom (calyx end) yellows (sign of ripeness)',
            'Heavy for its size (possibly contains a "honey core")',
            'Stem is firmly green, not dried out',
        ],
        'ng_points': [
            'Dull color, with bruises or impact marks',
            'Soft when pressed, with a fluffy lightness (mealy = dehydrated)',
            'Stem is dried out, blackened, or fallen off',
            'Wrinkles in the skin',
        ],
        'summary_ok': 'Deep color, shiny, yellow bottom',
        'summary_ng': 'Dull, soft, wrinkled',
        'storage': {
            'method': 'Bag and refrigerate (suppresses ethylene gas)',
            'duration': 'Refrigerated: 1 month / Room temp: 2 weeks',
            'tips': 'Store separately from other fruits/vegetables (ethylene causes damage). OK with potatoes (delays sprouting)',
        },
        'usage_tips': 'Eat with skin for more nutrients (pectin, polyphenols). Honey core = ripe and very sweet. Soak cut pieces in salt water to prevent browning',
        'nutrition_highlight': 'Pectin (gut health), polyphenols (antioxidant), vitamin C. As the saying goes, "An apple a day keeps the doctor away"',
    },

    # ============================ 3. mikan ============================
    'mikan': {
        'name': 'Mikan (Satsuma Mandarin)',
        'subcategory': 'Citrus',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Look at the stem (calyx) size',
            'judgment': 'Small and green = sweet',
        },
        'ok_short': [
            'Color: Deep orange',
            'Skin: Thin/Tight',
            'Stem: Small/Green',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Color: Dull',
            'Skin: Loose',
            'Stem: Large/Brown',
            'Feel: Soft',
        ],
        'ok_points': [
            'Deep, even orange color throughout',
            'Thin skin with tightness and shine',
            'Small stem with a green base (sign of a sweet variety)',
            'Heavy for its size (lots of juice)',
        ],
        'ng_points': [
            'Dull color with dents',
            'Gap between skin and flesh (called "puffy skin")',
            'Large, brown, dried stem',
            'Too soft when pressed',
        ],
        'summary_ok': 'Deep orange, thin skin, small stem',
        'summary_ng': 'Dull, puffy skin, brown stem',
        'storage': {
            'method': 'Cool, dark, well-ventilated place, stem-side down',
            'duration': '1-2 weeks at room temperature',
            'tips': 'One spoiled fruit affects the others — check often. Refrigeration reduces sweetness',
        },
        'usage_tips': 'The white pith (albedo) and inner skin layer are nutritious. Roasting whole creates a marmalade-like flavor',
        'nutrition_highlight': 'Vitamin C, β-cryptoxanthin (bone/skin health), synephrine (metabolism)',
    },

    # ============================ 4. lemon ============================
    'lemon': {
        'name': 'Lemon',
        'subcategory': 'Citrus',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Lift and check the weight',
            'judgment': 'Heavy = OK',
        },
        'ok_short': [
            'Color: Deep yellow',
            'Skin: Tight/Bumpy',
            'Weight: Heavy',
            'Shine: Yes',
        ],
        'ng_short': [
            'Color: Dull',
            'Skin: Wrinkled',
            'Feel: Soft',
            'Spots: Brown',
        ],
        'ok_points': [
            'Deep, even yellow color',
            'Tight skin with even fine bumps',
            'Heavy for its size (lots of juice)',
            'Glossy throughout',
        ],
        'ng_points': [
            'Dull or greenish color (unripe)',
            'Wrinkles in the skin',
            'Soft when pressed (dehydrated)',
            'Brown spots or impact marks',
        ],
        'summary_ok': 'Deep yellow, tight skin, heavy',
        'summary_ng': 'Dull, wrinkled, soft',
        'storage': {
            'method': 'Bag and refrigerate',
            'duration': '2-3 weeks refrigerated',
            'tips': 'Can also be sliced and frozen',
        },
        'usage_tips': 'Skin is highly fragrant and nutritious (organic recommended). Salt-preserved lemons keep much longer',
        'nutrition_highlight': 'Highest vitamin C among citrus, citric acid (fatigue recovery), hesperidin (circulation)',
    },

    # ============================ 5. avocado ============================
    'avocado': {
        'name': 'Avocado',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Press gently',
            'judgment': 'Slightly springy = ready to eat',
        },
        'ok_short': [
            'Skin: Dark green to black',
            'Feel: Springy',
            'Stem: Attached',
            'Shape: Even',
        ],
        'ng_short': [
            'Skin: Bright green (hard)',
            'Mushy: Overripe',
            'Stem: Falls off',
            'Black: Overripe',
        ],
        'ok_points': [
            'Skin is dark green to black (ripe)',
            'Slightly springy when pressed lightly (ready to eat)',
            'Stem is still attached (fresh)',
            'Even shape with firmness',
        ],
        'ng_points': [
            'Black skin with mushy spots (overripe)',
            'Bright green and hard (unripe)',
            'Stem fallen off, leaving a black hole (deteriorated)',
            'Large black spots (damage)',
        ],
        'summary_ok': 'Dark green/black, springy, even shape',
        'summary_ng': 'Hard (unripe), mushy, blackened',
        'storage': {
            'method': 'Unripe at room temp (with apples to ripen faster); ripe in the fridge',
            'duration': 'Ripe: 2-3 days refrigerated',
            'tips': 'Lemon juice prevents browning of cut surfaces. Store with the pit',
        },
        'usage_tips': 'Cut lengthwise → remove pit → peel. The pit is best removed by hand (knives slip)',
        'nutrition_highlight': 'Oleic acid (healthy fat), vitamin E, dietary fiber. One of the most nutritious fruits in the world',
    },

    # ============================ 6. ichigo ============================
    'ichigo': {
        'name': 'Strawberry',
        'subcategory': 'Berry',
        'season_peak': 'Spring',
        'key_check': {
            'action': 'Look at the stem (calyx) color',
            'judgment': 'Bright green and curling back = OK',
        },
        'ok_short': [
            'Color: Vivid red',
            'Stem: Green/Curling back',
            'Firmness: Yes',
            'Seeds: Raised',
        ],
        'ng_short': [
            'Color: Dark red',
            'Stem: Brown/Wilted',
            'Feel: Soft',
            'Seeds: Sunken',
        ],
        'ok_points': [
            'Vivid red color (intensity depends on variety)',
            'Stem is bright green and curling back (fully ripe)',
            'Firm skin with shine',
            'Seeds visibly raised on the surface (mature)',
        ],
        'ng_points': [
            'Dark color with wrinkly patches',
            'Brown, wilted stem',
            'Soft skin (overripe)',
            'Seeds sunken into the surface',
        ],
        'summary_ok': 'Vivid red, curled stem, firm',
        'summary_ng': 'Dark red, brown stem, soft',
        'storage': {
            'method': 'Store in original pack with stems on, unwashed, refrigerated',
            'duration': '2-3 days refrigerated (eat soon)',
            'tips': 'Wash just before eating. Freezing OK for smoothies',
        },
        'usage_tips': 'Removing stems before washing causes nutrient loss. The tip is sweetest. Tastes great even with little sugar or condensed milk',
        'nutrition_highlight': 'Vitamin C (daily allowance in 7-8 berries), folate, anthocyanins',
    },

    # ============================ 7. kiwi ============================
    'kiwi': {
        'name': 'Kiwi',
        'subcategory': '',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Press gently',
            'judgment': 'Slightly springy = OK',
        },
        'ok_short': [
            'Skin: Even fuzz',
            'Feel: Springy',
            'Shape: Even',
            'Stem: Dry',
        ],
        'ng_short': [
            'Skin: Mold',
            'Feel: Mushy',
            'Shape: Misshapen',
            'Skin: Damaged',
        ],
        'ok_points': [
            'Even, fine fuzz on the skin',
            'Slight give when pressed (ready to eat)',
            'Even shape, no damage',
            'Stem area is dry',
        ],
        'ng_points': [
            'Fuzz fallen off, mold growing',
            'Mushy when pressed (overripe or rotting)',
            'Too hard (unripe and sour)',
            'Large cuts or dents in the skin',
        ],
        'summary_ok': 'Even fuzz, slightly springy',
        'summary_ng': 'Mold, mushy, damaged',
        'storage': {
            'method': 'Unripe at room temperature to ripen; ripe in the refrigerator',
            'duration': '1-2 weeks refrigerated',
            'tips': 'Ripens faster with apples. Keep separate to slow ripening',
        },
        'usage_tips': 'The skin is edible (though scooping with a spoon is more common). Its protein-digesting enzyme tenderizes meat',
        'nutrition_highlight': 'Vitamins C and E, dietary fiber, actinidin (aids digestion)',
    },

    # ============================ 8. grape ============================
    'grape': {
        'name': 'Grape',
        'subcategory': '',
        'season_peak': 'Autumn',
        'key_check': {
            'action': 'Check for the white powder ("bloom")',
            'judgment': 'Bloom present = fresh',
        },
        'ok_short': [
            'Bloom: Yes',
            'Berries: Dense/Firm',
            'Stem: Green/Firm',
            'Color: Deep',
        ],
        'ng_short': [
            'Bloom: None',
            'Berries: Falling',
            'Stem: Brown/Dry',
            'Color: Pale',
        ],
        'ok_points': [
            'White powder ("bloom") is present (sign of freshness and natural protection)',
            'Berries are dense and firm',
            'Stem is green, firm, and lively',
            'Deep, even color throughout',
        ],
        'ng_points': [
            'Bloom worn off, skin is too shiny',
            'Berries fall off when touched',
            'Stem is brown and dried out',
            'Uneven color with pale areas',
        ],
        'summary_ok': 'Bloom, dense berries, green stem',
        'summary_ng': 'No bloom, falling berries, brown stem',
        'storage': {
            'method': 'Bag and refrigerate without washing',
            'duration': '3-5 days refrigerated',
            'tips': 'Cut individual berries from the stem with scissors (leaving tiny stems) to keep them fresh longer',
        },
        'usage_tips': 'Skin is rich in polyphenols. Edible-skin varieties like Shine Muscat are increasingly popular',
        'nutrition_highlight': 'Polyphenols (antioxidant), glucose (instant energy), potassium',
    },

    # ============================ 9. peach ============================
    'peach': {
        'name': 'Peach',
        'subcategory': '',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Sniff for aroma',
            'judgment': 'Sweet aroma = ready to eat',
        },
        'ok_short': [
            'Aroma: Sweet',
            'Color: Even',
            'Firmness: Yes',
            'Fuzz: Even',
        ],
        'ng_short': [
            'Aroma: None',
            'Color: Uneven',
            'Feel: Hard or mushy',
            'Bruises: Yes',
        ],
        'ok_points': [
            'Sweet aroma fills the air (ready to eat)',
            'Even color with firmness',
            'Fine white fuzz spread evenly across the surface',
            'White juice marks around the stem (fully ripe)',
        ],
        'ng_points': [
            'No aroma (unripe)',
            'Uneven color, with bruises',
            'Too hard (unripe) or mushy (overripe)',
            'Black spots or signs of rot',
        ],
        'summary_ok': 'Sweet aroma, even color, firm',
        'summary_ng': 'No aroma, uneven, bruised',
        'storage': {
            'method': 'Ripen at room temperature; refrigerate ripe ones briefly',
            'duration': 'Room temp: 2-3 days. Brief refrigeration only (flavor declines)',
            'tips': 'Refrigerate 2-3 hours before eating for the best temperature',
        },
        'usage_tips': 'Eat with the skin for more nutrients. To peel: dip in hot water for 30 seconds, then ice water — the skin slides right off',
        'nutrition_highlight': 'Pectin (gut health), potassium, catechins (antioxidant)',
    },

    # ============================ 10. kaki ============================
    'kaki': {
        'name': 'Kaki (Japanese Persimmon)',
        'subcategory': '',
        'season_peak': 'Autumn',
        'key_check': {
            'action': 'Look at the calyx (top leaves)',
            'judgment': 'Tightly attached = sweet',
        },
        'ok_short': [
            'Color: Deep orange',
            'Firmness: Yes',
            'Calyx: Tight/Green',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Color: Dull',
            'Feel: Mushy',
            'Calyx: Lifting',
            'Spots: Black',
        ],
        'ok_points': [
            'Deep, even orange color',
            'Tight skin with shine',
            'Green calyx tightly attached to the fruit (sign of sweet variety)',
            'Heavy for its size',
        ],
        'ng_points': [
            'Dull color with darkened patches',
            'Too soft, mushy feel',
            'Gap between calyx and fruit (possibly an astringent variety)',
            'Black spots or bruises',
        ],
        'summary_ok': 'Deep orange, firm, tight calyx',
        'summary_ng': 'Dull, mushy, gapped calyx',
        'storage': {
            'method': 'Store stem-down in a bag, refrigerated',
            'duration': '1-2 weeks refrigerated',
            'tips': 'Astringent varieties: deastringe with shochu (Japanese spirit), or apply alcohol to the calyx for 1 week',
        },
        'usage_tips': 'Pre-ripe: crunchy texture. Ripe: jam-like. The skin is also nutritious. Acetaldehyde near the seeds is said to help with hangovers',
        'nutrition_highlight': 'Vitamin C (2× a mikan), β-cryptoxanthin, tannins. As they say, "A persimmon a day keeps the doctor away"',
    },

    # ============================ 11. pear ============================
    'pear': {
        'name': 'Asian Pear (Nashi)',
        'subcategory': '',
        'season_peak': 'Autumn',
        'key_check': {
            'action': 'Lift and check the weight',
            'judgment': 'Heavy = OK',
        },
        'ok_short': [
            'Skin: Tight/Glossy',
            'Shape: Even/Round',
            'Weight: Heavy',
            'Bottom: Rough',
        ],
        'ng_short': [
            'Skin: Wrinkled/Brown',
            'Feel: Soft',
            'Light',
            'Spots: Brown',
        ],
        'ok_points': [
            'Tight, glossy skin',
            'Even, round shape with no damage',
            'Heavy with lots of juice',
            'Rough texture at the bottom (calyx end) = high sugar content',
        ],
        'ng_points': [
            'Wrinkles or brown spots on the skin',
            'Soft when pressed (overripe or dehydrated)',
            'Light weight',
            'Bruises or signs of rot',
        ],
        'summary_ok': 'Firm, round, heavy',
        'summary_ng': 'Wrinkled, soft, light',
        'storage': {
            'method': 'Bag and refrigerate',
            'duration': 'About 1 week refrigerated',
            'tips': 'Lemon juice prevents browning of cut surfaces',
        },
        'usage_tips': 'The skin is also nutritious. Over-chilling reduces flavor. The crisp texture shines in compotes and salads',
        'nutrition_highlight': 'Aspartic acid (fatigue recovery), potassium, dietary fiber, sorbitol (digestion)',
    },
}


def apply_translations(items, force=False):
    """foods.json items に EN 翻訳を適用。"""
    text_fields = ['name', 'subcategory', 'season_peak', 'summary_ok', 'summary_ng',
                   'usage_tips', 'nutrition_highlight']
    array_fields = ['ok_short', 'ng_short', 'ok_points', 'ng_points']
    n_updated = 0

    for item in items:
        if item['id'] not in TRANSLATIONS:
            continue
        trans = TRANSLATIONS[item['id']]
        n_fields = 0

        for fld in text_fields:
            if fld in trans and fld in item and isinstance(item[fld], dict):
                if force or not item[fld].get('en'):
                    item[fld]['en'] = trans[fld]
                    n_fields += 1

        for fld in array_fields:
            if fld in trans and fld in item and isinstance(item[fld], dict):
                if force or not item[fld].get('en'):
                    item[fld]['en'] = trans[fld]
                    n_fields += 1

        if 'key_check' in trans and 'key_check' in item:
            for sub in ['action', 'judgment']:
                kc_field = item['key_check'].get(sub)
                if sub in trans['key_check'] and isinstance(kc_field, dict):
                    if force or not kc_field.get('en'):
                        kc_field['en'] = trans['key_check'][sub]
                        n_fields += 1

        if 'storage' in trans and 'storage' in item:
            for sub in ['method', 'duration', 'tips']:
                st_field = item['storage'].get(sub)
                if sub in trans['storage'] and isinstance(st_field, dict):
                    if force or not st_field.get('en'):
                        st_field['en'] = trans['storage'][sub]
                        n_fields += 1

        if n_fields > 0:
            n_updated += 1
            print(f'  TRANSLATED {item["id"]:>10}  {item["name"]["ja"]:>10}  ({n_fields} fields)')

    return n_updated


def main():
    force = '--force' in sys.argv
    path = os.path.join(ROOT, 'data', 'foods.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    n = apply_translations(data['items'], force=force)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\n  {n} fruits updated. (Total items: {len(data["items"])})')


if __name__ == '__main__':
    main()

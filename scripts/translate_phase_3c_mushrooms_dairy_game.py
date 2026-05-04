#!/usr/bin/env python3
"""
Phase 3-C: きのこ5 + 卵・乳・豆4 + ジビエ2 = 11品の英訳ドラフト。

【翻訳方針】
- きのこ: 国際的に通じる日本語名 + 一般名 (Hen of the Woods 等)
- 納豆: Natto (Fermented Soybeans) — 補足
- ジビエ: 標準英訳 (Venison, Wild Boar)
- 文化的補足:
  - botan-nabe → "miso-based hot pot"
  - shochu → "Japanese spirit"
  - 「香りまつたけ味しめじ」→ "Matsutake for aroma, shimeji for taste"
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


TRANSLATIONS = {
    # ============================ Mushrooms (5) ============================
    'shiitake': {
        'name': 'Shiitake Mushroom',
        'subcategory': '',
        'season_peak': 'Spring & Autumn',
        'key_check': {
            'action': 'Look under the cap (gills)',
            'judgment': 'White gills = OK',
        },
        'ok_short': ['Cap: Curled inward', 'Gills: White', 'Flesh: Thick', 'Stem: Thick/Firm'],
        'ng_short': ['Cap: Opened up', 'Gills: Brown', 'Flesh: Thin', 'Moisture: Excess'],
        'ok_points': [
            'Cap is curled inward (sign of thick flesh)',
            'Gills underneath are white and even',
            'Stem is thick and firm (rich in umami)',
            'Slightly moist throughout but not sticky',
        ],
        'ng_points': [
            'Cap is fully opened (already released spores)',
            'Gills darkened, moist',
            'Thin flesh, light weight',
            'Sticky, discolored',
        ],
        'summary_ok': 'Curled cap, white gills, thick',
        'summary_ng': 'Open cap, brown gills, thin',
        'storage': {
            'method': 'Wrap in paper towel, bag, refrigerate',
            'duration': '4-5 days refrigerated / 1 month sun-dried',
            'tips': 'Sun-drying boosts vitamin D. Even 30 minutes of light drying helps',
        },
        'usage_tips': 'The tough stem base (ishizuki) should be cut off; the rest of the stem is edible. Dried shiitake gain umami when rehydrated',
        'nutrition_highlight': 'Vitamin D (bone health), eritadenine (cholesterol-lowering), dietary fiber',
    },

    'shimeji': {
        'name': 'Shimeji Mushroom',
        'subcategory': '',
        'season_peak': 'Autumn',
        'key_check': {
            'action': 'Check the cluster\'s compactness',
            'judgment': 'Firm and dense = OK',
        },
        'ok_short': ['Cluster: Dense/Firm', 'Caps: Tight', 'Stems: White', 'Color: Even'],
        'ng_short': ['Cluster: Falling apart', 'Caps: Opened up', 'Stems: Brown', 'Moisture: Excess'],
        'ok_points': [
            'Cluster holds together with firmness',
            'Caps are small and curled inward',
            'Stems are pure white and firm',
            'Even color throughout',
        ],
        'ng_points': [
            'Cluster falling apart',
            'Caps fully opened',
            'Stems are sticky or brown',
            'Excess moisture, discolored',
        ],
        'summary_ok': 'Compact cluster, firm, white',
        'summary_ng': 'Falling apart, opened, brown',
        'storage': {
            'method': "Don't cut off the base; wrap in paper towel and refrigerate",
            'duration': '4-5 days refrigerated',
            'tips': 'Freezes well: separate into small clusters and bag. Boosts umami',
        },
        'usage_tips': "Old saying: 'Matsutake for aroma, shimeji for taste.' Excellent in soups, stir-fries, and rice dishes",
        'nutrition_highlight': 'Ornithine (liver function), β-glucan (immunity), B vitamins',
    },

    'enoki': {
        'name': 'Enoki Mushroom',
        'subcategory': '',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Check the stem color',
            'judgment': 'Pure white = OK',
        },
        'ok_short': ['Stems: Pure white', 'Caps: Small/Even', 'Cluster: Firm', 'Bag: Dry'],
        'ng_short': ['Stems: Yellowing', 'Caps: Opened up', 'Cluster: Loose', 'Bag: Wet'],
        'ok_points': [
            'Stems are pure white and firm',
            'Caps are small and roundly even',
            'Cluster base is densely packed',
            'Bag interior is dry',
        ],
        'ng_points': [
            'Stems yellowing',
            'Caps open and darker',
            'Cluster has fallen apart',
            'Water droplets in the bag (deteriorated)',
        ],
        'summary_ok': 'White stems, even caps, dry',
        'summary_ng': 'Yellowed, open caps, wet',
        'storage': {
            'method': 'Store in original bag or portioned, refrigerated',
            'duration': '4-5 days refrigerated',
            'tips': "Freezing boosts umami and extends life to 1 month. Don't cut off the base before bagging",
        },
        'usage_tips': 'Cut off the base, separate into small clusters. Great in hot pots, soups, and namul. Texture is the appeal — cook briefly',
        'nutrition_highlight': 'GABA (relaxation), enoki linoleic acid (fat suppression), dietary fiber',
    },

    'eringi': {
        'name': 'Eringi (King Trumpet Mushroom)',
        'subcategory': '',
        'season_peak': 'Autumn–Early winter',
        'key_check': {
            'action': 'Check the stem thickness',
            'judgment': 'Thick and pure white = OK',
        },
        'ok_short': ['Stem: Thick/White', 'Cap: Light brown', 'Surface: Dry', 'Firmness: Yes'],
        'ng_short': ['Stem: Thin/Yellow', 'Cap: Wide open', 'Surface: Sticky', 'Spots: Black'],
        'ok_points': [
            'Stem is thick and pure white with firmness',
            'Cap is light brown and curled inward',
            'Surface is dry, not sticky',
            'Springy throughout',
        ],
        'ng_points': [
            'Stem is thin and yellowing',
            'Cap is fully opened wide',
            'Surface is sticky',
            'Black spots or discoloration',
        ],
        'summary_ok': 'Thick stem, white, dry',
        'summary_ng': 'Thin, yellow, sticky',
        'storage': {
            'method': 'Wrap in paper towel, bag, refrigerate',
            'duration': '1 week refrigerated',
            'tips': 'Freezes well: slice and bag for ready-to-use convenience',
        },
        'usage_tips': 'Has an abalone-like texture. Tearing along the fibers (lengthwise) enhances chewiness. Excellent grilled or in butter sauté',
        'nutrition_highlight': 'Vitamin D, β-glucan, dietary fiber. Low calorie, diet-friendly',
    },

    'maitake': {
        'name': 'Maitake (Hen of the Woods)',
        'subcategory': '',
        'season_peak': 'Autumn',
        'key_check': {
            'action': "Check the cluster's color",
            'judgment': 'Deep brown and meaty = OK',
        },
        'ok_short': ['Cluster: Firm/Dense', 'Color: Deep brown', 'Flesh: Thick', 'Aroma: Strong'],
        'ng_short': ['Cluster: Falling apart', 'Color: Dull', 'Flesh: Thin', 'Moisture: Excess'],
        'ok_points': [
            'Cluster is firmly bound with density',
            'Deep, even brown color',
            'Caps (petal-like) are thick',
            'Strong, fragrant aroma',
        ],
        'ng_points': [
            'Cluster falling apart',
            'Dull color, partially blackened',
            'Caps are thin and light',
            'Excess moisture, sticky',
        ],
        'summary_ok': 'Firm cluster, deep brown, meaty',
        'summary_ng': 'Falling apart, dull, moist',
        'storage': {
            'method': 'Wrap in paper towel, bag, refrigerate',
            'duration': '4-5 days refrigerated',
            'tips': 'Freezing enhances umami. Tear by hand into small clusters before bagging',
        },
        'usage_tips': 'Aroma shines in tempura, takikomi rice (mixed rice), and foil-baked dishes. Contains a protein-digesting enzyme that tenderizes meat',
        'nutrition_highlight': "β-glucan (immune boost), vitamin D, niacin. Name means 'mushroom of dancing joy'",
    },

    # ============================ Egg / Dairy / Legume (4) ============================
    'egg': {
        'name': 'Egg',
        'subcategory': 'Egg',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the shell',
            'judgment': 'No cracks = OK',
        },
        'ok_short': ['Shell: No cracks', 'Surface: Smooth', 'Cleanliness: Good', 'Best by: Plenty'],
        'ng_short': ['Shell: Cracked', 'Surface: Stained', 'Sound: Sloshing', 'Freshness: Marginal'],
        'ok_points': [
            'No cracks, chips, or holes in the shell',
            'Surface is smooth without rough patches',
            'No droppings, blood, or feathers attached',
            'No sound when shaken (contents firmly intact)',
        ],
        'ng_points': [
            'Cracks, chips, or holes in the shell',
            'Droppings or blood attached',
            'Sloshing sound when shaken (yolk has broken inside)',
            'Best-by date approaching, or improper storage temperature',
        ],
        'summary_ok': 'No cracks, smooth, odorless',
        'summary_ng': 'Cracked, stained, old',
        'storage': {
            'method': 'Refrigerate pointed-end down. Avoid the door pocket (temperature fluctuations)',
            'duration': '2-3 weeks refrigerated (best-by date plus a few days for cooked use)',
            'tips': 'Raw consumption only within best-by date; cooked is OK a few days after. Fresh yolk stands tall when cracked',
        },
        'usage_tips': 'Raw eggs only when very fresh. For half-cooked or onsen tamago, heat to 65-70°C through the center. Bringing to room temperature prevents cracking',
        'nutrition_highlight': 'Nearly complete nutrition (all essentials except vitamin C). High-quality protein, choline (brain), vitamin D',
    },

    'tofu': {
        'name': 'Tofu',
        'subcategory': 'Soy product',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the water and surface',
            'judgment': 'Clear water, odorless = OK',
        },
        'ok_short': ['Shape: Even', 'Water: Clear', 'Color: Milky white', 'Odor: None'],
        'ng_short': ['Shape: Crumbling', 'Water: Cloudy', 'Color: Yellowed', 'Odor: Sour'],
        'ok_points': [
            'Even shape with sharp corners',
            'Water is clear and odorless',
            'Even milky white color throughout',
            'Springy when pressed (silken: soft; cotton: firm)',
        ],
        'ng_points': [
            'Crumbling, falling apart shape',
            'Cloudy water, slimy feel',
            'Yellowing color',
            'Sour smell, slimy surface',
        ],
        'summary_ok': 'Even shape, clear water, odorless',
        'summary_ng': 'Crumbling, cloudy, sour',
        'storage': {
            'method': 'Refrigerate in original water; replace water daily once opened',
            'duration': 'Unopened: until best-by date / Opened: 1-2 days',
            'tips': 'Replace water daily. Freezing OK but turns spongy',
        },
        'usage_tips': 'Silken: smooth (cold tofu, soup); cotton: firm (sautéed, mapo tofu). Press to remove water before frying',
        'nutrition_highlight': 'High-quality plant protein, soy isoflavones, calcium, iron',
    },

    'natto': {
        'name': 'Natto (Fermented Soybeans)',
        'subcategory': 'Soy product',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Stir and check the threads',
            'judgment': 'Strong stickiness = OK',
        },
        'ok_short': ['Threads: Strong/Sticky', 'Beans: Even', 'Color: Even brown', 'Odor: Healthy ferment'],
        'ng_short': ['Threads: Weak', 'Beans: Dried', 'Color: Black/Mold', 'Odor: Strong ammonia'],
        'ok_points': [
            'Strong stretchy threads (the iconic natto stickiness)',
            'Beans are evenly sized and plump',
            'Even brown to dark-brown color throughout',
            'Distinctive but pleasant fermentation aroma (not ammonia)',
        ],
        'ng_points': [
            'Threads are weak or absent',
            'Beans are dried out and rough',
            'Discolored black, with white mold spots',
            'Strong ammonia smell',
        ],
        'summary_ok': 'Strong threads, plump beans, even color',
        'summary_ng': 'Weak threads, dried, moldy',
        'storage': {
            'method': 'Refrigerate to slow fermentation',
            'duration': 'Within best-by date; consume soon after opening',
            'tips': 'Freezing keeps 1 month. Leaving at room temp accelerates fermentation, causing bitterness',
        },
        'usage_tips': 'Stir well before serving over rice to draw out the threads. Adjust flavor with raw egg or condiments',
        'nutrition_highlight': 'Nattokinase (improves circulation), vitamin K2 (bone health), soy isoflavones, dietary fiber',
    },

    'yogurt': {
        'name': 'Yogurt',
        'subcategory': 'Dairy',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the container and surface',
            'judgment': 'No bulging = OK',
        },
        'ok_short': ['Container: Flat', 'Surface: Smooth', 'Color: Milky white', 'Acidity: Pleasant'],
        'ng_short': ['Container: Bulging', 'Surface: Heavy whey', 'Color: Yellow', 'Mold'],
        'ok_points': [
            'Container is flat, not bulging',
            'Surface is smooth and even',
            'Milky white to pale cream color',
            'Refreshing tartness when opened',
        ],
        'ng_points': [
            'Container is swollen (over-fermentation)',
            'Large amount of yellow whey separation on top',
            'Yellowing or browning',
            'Mold or off-smell (rotting)',
        ],
        'summary_ok': 'Flat container, smooth, milky white',
        'summary_ng': 'Bulging, separated, mold',
        'storage': {
            'method': 'Refrigerator at 10°C or below. Avoid the door pocket',
            'duration': 'Within best-by date; 2-3 days after opening',
            'tips': 'Can freeze for a frozen-yogurt feel. Slight whey separation is normal',
        },
        'usage_tips': 'Eat with honey or fruit. Also great in cooking (tenderizes meat, adds richness)',
        'nutrition_highlight': 'Lactic acid bacteria (gut health), calcium, protein, vitamin B2',
    },

    # ============================ Game Meats (2) ============================
    'venison': {
        'name': 'Venison',
        'subcategory': '',
        'season_peak': 'Winter (hunting season)',
        'key_check': {
            'action': 'Check the color and smell',
            'judgment': 'Deep red, odorless = OK',
        },
        'ok_short': ['Color: Deep red', 'Fibers: Fine', 'Fat: Very minimal', 'Drip: Minimal'],
        'ng_short': ['Color: Brown to black', 'Stickiness', 'Strong gamey smell', 'Drip: Heavy'],
        'ok_points': [
            'Deep, rich red color (high in hemoglobin)',
            'Fine, dense muscle fibers',
            'Very minimal fat (lean meat)',
            'Properly bled animals: little drip and a clean iron-like smell',
        ],
        'ng_points': [
            'Brownish or black discoloration (old/oxidized)',
            'Sticky surface, slimy feel',
            'Strong gamey smell (poor bleeding/processing)',
            'Heavy reddish-brown drip',
        ],
        'summary_ok': 'Deep red, fine fibers, odorless',
        'summary_ng': 'Brown/black, sticky, gamey',
        'storage': {
            'method': 'Buy from a trusted butcher and freeze immediately. Vacuum-pack ideal',
            'duration': '2-3 months frozen. Use thawed meat quickly',
            'tips': 'Thaw slowly in the refrigerator (8-12 hours). Quick thawing causes drip loss',
        },
        'usage_tips': 'Very lean — avoid overcooking (rare or slow-stewed is best). Marinate in red wine, sake, or herbs to soften gameyness. Beginners: try loin steaks or shank stews',
        'nutrition_highlight': "High protein, low fat, low calorie. Heme iron (well-absorbed), zinc, vitamin B12. Known as the 'queen of red meats'",
    },

    'boar': {
        'name': 'Wild Boar',
        'subcategory': '',
        'season_peak': 'Winter (peak fat)',
        'key_check': {
            'action': 'Look at the fat-meat boundary',
            'judgment': 'Crisp white fat = OK',
        },
        'ok_short': ['Color: Bright pink-red', 'Fat: White/Distinct', 'Springiness: Yes', 'Gamey: Mild'],
        'ng_short': ['Color: Dark red', 'Fat: Yellowing', 'Feel: Soft', 'Gamey: Strong'],
        'ok_points': [
            'Vivid pink to red meat color',
            'Pure white fat with a clear boundary from the meat',
            'Springy, bounces back when pressed',
            'Mild gamey scent; sweet aroma in winter (peak-fat) animals',
        ],
        'ng_points': [
            'Dark red color, with discoloration',
            'Yellowed, sticky fat',
            'Too soft, fibers loosening',
            'Strong gamey smell (sign of poor processing or age)',
        ],
        'summary_ok': 'Pink-red, white fat, springy',
        'summary_ng': 'Dark, yellow fat, soft, gamey',
        'storage': {
            'method': 'Freeze (raw consumption is unsafe — same as pork, parasites possible)',
            'duration': '2-3 months frozen',
            'tips': 'Thaw slowly in the refrigerator. Cook completely (75°C / 167°F or higher for 1+ minutes through the center)',
        },
        'usage_tips': 'Fat carries the umami; truly shines in stews. Classic dish: botan-nabe (miso-based hot pot). Thin slices for shabu-shabu or yakiniku; loin for steaks. Beginners: start with botan-nabe (miso and fat make it approachable)',
        'nutrition_highlight': 'Rich in B vitamins (B1, B2, B12) for fatigue recovery and metabolism. Plenty of zinc and iron. Fat is high in unsaturated fatty acids — lower melting point than pork',
    },
}


def apply_translations(items, force=False):
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

    print(f'\n  {n} items updated. (Total items: {len(data["items"])})')


if __name__ == '__main__':
    main()

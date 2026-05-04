#!/usr/bin/env python3
"""
Phase 3-D: 肉類4 + 魚介5 = 9品の英訳ドラフト + cucumber 修正。

【翻訳方針】
- 肉類: 標準英訳 (Pork, Beef 等) + 専門用語の訳出
  - 「霜降り」 → "marbling"
  - 「ドリップ」 → "drip"
  - 「下味冷凍」 → "marinated freezing"
- 魚介: 国際的に通じる魚種名 + 日本語名併記
  - 鮭 (Salmon Fillet)
  - 鯖 (Mackerel/Saba) — Saba と併記
  - アジ (Horse Mackerel/Aji)
  - エビ (Shrimp/Prawn)
  - 一尾魚の見方 (Whole Fish Buying Guide)
- 専門用語:
  - ぜいご → "zeigo (scutes)" 補足
  - アニサキス → "anisakis"
  - 〆鯖 → "shime-saba (vinegar-cured)"
  - なめろう → "namero (chopped)"

【併せて修正】
cucumber の Prickly → Bumpy (Phase 3-A 後のフィードバック反映)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


TRANSLATIONS = {
    # ============================ Meats (4) ============================
    'chicken': {
        'name': 'Chicken',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check color and drip',
            'judgment': 'Pink with minimal drip = OK',
        },
        'ok_short': ['Color: Vivid pink', 'Shine: Yes', 'Drip: Clear/Minimal', 'Springiness: Yes'],
        'ng_short': ['Color: Dull/Gray', 'Drip: Heavy/Brown-red', 'Stickiness: Yes', 'Smell: Sour'],
        'ok_points': [
            'Vivid pink color with shine',
            'Skin is yellowish white with visible follicles',
            'Springs back immediately when pressed',
            'Little drip in the pack; clear to light color',
        ],
        'ng_points': [
            'Dull or gray-tinted color',
            'Heavy drip, brown-red or murky',
            'Sticky surface, slimy threads',
            'Sour smell or ammonia odor',
        ],
        'summary_ok': 'Vivid pink, springy, minimal drip',
        'summary_ng': 'Dull, heavy drip, smelly',
        'storage': {
            'method': 'Chilled compartment or coldest fridge spot',
            'duration': 'Refrigerated: 1-2 days / Frozen: 2-3 weeks',
            'tips': 'Portion and freeze right after buying. Marinated freezing (salt, sake) extends life and adds flavor',
        },
        'usage_tips': 'Cook center to 75°C+ for 1+ minutes (safety standard). Sear skin-side first for crispness. Avoid overcooking breast meat (gets dry)',
        'nutrition_highlight': 'High protein, low fat (especially breast and tenderloin). Imidazole dipeptide (fatigue recovery). Skin contains collagen',
    },

    'pork': {
        'name': 'Pork',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check color and drip',
            'judgment': 'Light pink with minimal drip = OK',
        },
        'ok_short': ['Color: Light pink', 'Fat: White/Distinct', 'Drip: Minimal', 'Shine: Yes'],
        'ng_short': ['Color: Dark red/Gray', 'Fat: Yellowing', 'Drip: Heavy/Brown', 'Stickiness'],
        'ok_points': [
            'Even, light pink color',
            'White fat with clear boundary from the meat',
            'Springy with minimal, clear drip',
            'Glossy throughout, not sticky',
        ],
        'ng_points': [
            'Dark red color, grayish tint',
            'Yellowed fat, discolored',
            'Heavy drip, brown-red or murky',
            'Sticky surface, slimy threads',
        ],
        'summary_ok': 'Light pink, white fat, minimal drip',
        'summary_ng': 'Dark, yellowed fat, heavy drip',
        'storage': {
            'method': 'Chilled compartment or coldest fridge spot',
            'duration': 'Refrigerated: 1-2 days / Frozen: 2-3 weeks',
            'tips': 'Marinated freezing (salt, sake, sugar) tenderizes and extends shelf life',
        },
        'usage_tips': 'Cook center to 75°C+ for 1+ minutes (safety standard). Each cut has its specialty (e.g., shoga-yaki for sliced loin)',
        'nutrition_highlight': 'Vitamin B1 (fatigue recovery, carb metabolism — about 10× beef), zinc, quality protein',
    },

    'beef': {
        'name': 'Beef',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the color and fat',
            'judgment': 'Vivid red with white fat = OK',
        },
        'ok_short': ['Color: Vivid red', 'Fat: White/Marbled', 'Fibers: Even', 'Shine: Yes'],
        'ng_short': ['Color: Darkened', 'Fat: Yellowing', 'Drip: Heavy', 'Fibers: Coarse'],
        'ok_points': [
            'Vivid, even red color',
            'White marbling distributed evenly through the meat',
            'Fine, even fibers with springiness',
            'Cut surface is glossy',
        ],
        'ng_points': [
            'Darkened, dark red to grayish',
            'Yellowed fat, sticky',
            'Heavy, brown-red drip',
            'Coarse fibers, indents remain when pressed',
        ],
        'summary_ok': 'Vivid red, white fat, fine fibers',
        'summary_ng': 'Darkened, yellow fat, heavy drip',
        'storage': {
            'method': 'Chilled compartment, wrap tightly to remove air',
            'duration': 'Refrigerated: 2-3 days / Frozen: 1 month',
            'tips': 'For steaks, use right after buying or season and freeze',
        },
        'usage_tips': 'Bring to room temp before cooking (even heat penetration). Fat carries flavor; marbling = wagyu-style',
        'nutrition_highlight': 'Heme iron (high absorption), zinc, vitamin B12, L-carnitine (fat burning)',
    },

    'ground_meat': {
        'name': 'Ground Meat',
        'subcategory': '',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check color uniformity',
            'judgment': 'Even pink = OK',
        },
        'ok_short': ['Color: Even pink', 'Feel: Fluffy', 'Drip: Minimal', 'Stickiness: None'],
        'ng_short': ['Color: Mottled/Gray', 'Feel: Sticky', 'Drip: Heavy', 'Smell: Off'],
        'ok_points': [
            'Evenly pink color',
            'Fluffy texture, not sticky',
            'Minimal drip, clean pack',
            'Same-day grind in store = freshest',
        ],
        'ng_points': [
            'Patchy darker areas, gray or black spots',
            'Sticky, slimy threads',
            'Heavy brown-red drip',
            'Sour smell',
        ],
        'summary_ok': 'Even pink, fluffy',
        'summary_ng': 'Mottled, sticky, heavy drip',
        'storage': {
            'method': 'Use within 1-2 days from chilled compartment, or freeze',
            'duration': 'Refrigerated: 1 day / Frozen: 2 weeks',
            'tips': 'Spread thin and freeze; break off portions as needed. Removing air is essential',
        },
        'usage_tips': 'Chicken: dries easily; pork: umami; beef: richness; mixed: balanced. When forming patties, avoid overmixing',
        'nutrition_highlight': 'Same nutrients as whole meat. Higher fat content, so watch portions. Convenient protein source',
    },

    # ============================ Seafood (5) ============================
    'salmon': {
        'name': 'Salmon (Fillet)',
        'subcategory': 'Fillet',
        'season_peak': 'Autumn (autumn salmon)',
        'key_check': {
            'action': 'Check the orange color and fat lines',
            'judgment': 'Vivid orange with white fat lines = OK',
        },
        'ok_short': ['Color: Vivid orange', 'Fat: Distinct white lines', 'Shine: Yes', 'Skin: Silvery'],
        'ng_short': ['Color: Brown/Dull', 'Fat: Unclear', 'Slime: Yes', 'Drip: Heavy'],
        'ok_points': [
            'Vivid orange color throughout',
            'Distinct, regularly spaced white fat lines',
            'Cut surface is glossy',
            'Skin shines silver',
        ],
        'ng_points': [
            'Brown discoloration, dull',
            'Fat lines are blurry or absent',
            'Slimy surface, stringy threads',
            'Heavy, brown-red drip',
        ],
        'summary_ok': 'Vivid orange, distinct white lines',
        'summary_ng': 'Brown, blurry lines, slimy',
        'storage': {
            'method': 'Chilled compartment, sealed with plastic wrap',
            'duration': 'Refrigerated: 1-2 days / Frozen: 2-3 weeks',
            'tips': 'Salting before freezing extends life and reduces fishy smell (water removal)',
        },
        'usage_tips': 'Sear skin-side first for crispness. Salted salmon: pan-fry as is. Fresh salmon: salt to firm flesh before cooking',
        'nutrition_highlight': 'Astaxanthin (antioxidant, source of the orange color), DHA/EPA, vitamin D',
    },

    'saba': {
        'name': 'Mackerel (Saba)',
        'subcategory': 'Blue-backed fish',
        'season_peak': 'Autumn–Winter',
        'key_check': {
            'action': 'Look at the eyes and gills',
            'judgment': 'Clear eyes, red gills = OK',
        },
        'ok_short': ['Eyes: Black/Clear', 'Gills: Vivid red', 'Belly: Firm', 'Skin: Silver shine'],
        'ng_short': ['Eyes: Cloudy', 'Gills: Brown', 'Belly: Soft', 'Skin: Slimy'],
        'ok_points': [
            'Eyes are black and clear, pupils visible',
            'Gills are vivid red',
            'Belly is firm and bounces back when pressed',
            'Skin shines silver, wave pattern is distinct',
        ],
        'ng_points': [
            'Eyes are cloudy and white',
            'Gills are brown to black',
            'Belly is soft, may tear',
            'Heavy surface slime, smelly',
        ],
        'summary_ok': 'Clear eyes, red gills, firm belly',
        'summary_ng': 'Cloudy eyes, brown gills, soft belly',
        'storage': {
            'method': 'Newspaper → plastic wrap → chilled compartment. On ice is ideal',
            'duration': 'Refrigerated: 1 day / Frozen (after gutting): 2 weeks',
            'tips': 'Blue-backed fish lose freshness fast. Remove guts early for anisakis prevention',
        },
        'usage_tips': 'Salted saba: grill as is. Fresh saba: salt to remove fishy smell. Vinegar-cured (shime-saba) only with very fresh fish',
        'nutrition_highlight': 'EPA/DHA (champion blue-backed fish), vitamin D, niacin, abundant protein',
    },

    'aji': {
        'name': 'Horse Mackerel (Aji)',
        'subcategory': 'Blue-backed fish',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Touch the zeigo (hard scutes near tail)',
            'judgment': 'Hard and firm = OK',
        },
        'ok_short': ['Eyes: Clear', 'Gills: Red', 'Zeigo: Hard', 'Skin: Silvery'],
        'ng_short': ['Eyes: Cloudy', 'Gills: Brown', 'Zeigo: Soft', 'Skin: Slimy'],
        'ok_points': [
            'Eyes are black and clear',
            'Gills are vivid red',
            'Zeigo (hard scales near the tail) are firm and taut',
            'Skin shines silver, firm to touch',
        ],
        'ng_points': [
            'Eyes are cloudy white',
            'Gills are discolored brown',
            'Zeigo are soft and bend',
            'Slimy surface, skin drying out',
        ],
        'summary_ok': 'Clear eyes, red gills, hard zeigo',
        'summary_ng': 'Cloudy eyes, brown gills, soft zeigo',
        'storage': {
            'method': 'Refrigerate on ice; remove guts quickly',
            'duration': 'Refrigerated: 1 day / Butterflied + frozen: 2 weeks',
            'tips': 'Sashimi-grade only on day of purchase. Salt and overnight rest for himono (dried fish)',
        },
        'usage_tips': 'Grilled (shio-yaki), sashimi, namero (chopped), tataki. Fatty summer aji is exceptional',
        'nutrition_highlight': 'EPA/DHA, taurine (liver function), potassium. Low calorie, high protein',
    },

    'ebi': {
        'name': 'Shrimp (Prawn)',
        'subcategory': 'Crustacean',
        'season_peak': 'Year-round',
        'key_check': {
            'action': 'Check the head and shell',
            'judgment': 'Head not blackened, translucent shell = OK',
        },
        'ok_short': ['Shell: Translucent', 'Segments: Distinct', 'Head: Not black', 'Firmness: Yes'],
        'ng_short': ['Head: Black/Red spots', 'Shell: Loose', 'Feel: Soft', 'Tail: Discolored'],
        'ok_points': [
            'Shell is translucent with shine',
            'Body segments are distinct',
            'Head is not blackened, no discoloration',
            'Firm to touch, antennae intact',
        ],
        'ng_points': [
            'Head is darkened, with red spots',
            'Shell separating from flesh, gaps visible',
            'Soft when pressed',
            'Tail is discolored (black or green)',
        ],
        'summary_ok': 'Translucent shell, distinct segments, light head',
        'summary_ng': 'Black head, loose shell, soft',
        'storage': {
            'method': 'Cool immediately on ice, use within 1-2 days',
            'duration': 'Refrigerated: 1 day / Frozen: 2 weeks',
            'tips': 'Shell-on freezing extends shelf life and flavor. Remove all air to prevent freezer burn',
        },
        'usage_tips': 'Devein to remove smell. Saltwater rinse for snap. Avoid overcooking (gets tough)',
        'nutrition_highlight': 'Taurine, low fat / high protein, astaxanthin (in the shell), minerals',
    },

    'whole_fish': {
        'name': 'Whole Fish Buying Guide',
        'subcategory': 'General guide',
        'season_peak': 'Varies by species',
        'key_check': {
            'action': 'Look at the eyes and gills',
            'judgment': 'Clear eyes, red gills = OK',
        },
        'ok_short': ['Eyes: Black/Clear', 'Gills: Vivid red', 'Belly: Firm', 'Skin: Firm/Silvery'],
        'ng_short': ['Eyes: Cloudy', 'Gills: Brown to black', 'Belly: Soft', 'Skin: Slimy/Dry'],
        'ok_points': [
            '[Eyes] Black and clear, pupils visible (cloudy = lost freshness)',
            '[Gills] Vivid red (brown or black means old)',
            '[Belly] Firm and taut (soft or torn = organ degradation)',
            '[Skin] Silver shine and firmness, with natural light slime',
        ],
        'ng_points': [
            'Eyes are cloudy white, pupils blurred',
            'Gills discolored brown to black',
            'Belly is soft or torn',
            'Excessive surface slime, or completely dried out',
        ],
        'summary_ok': 'Clear eyes, red gills, firm belly',
        'summary_ng': 'Cloudy eyes, brown gills, soft belly',
        'storage': {
            'method': 'On ice in refrigerator; remove guts and gills quickly',
            'duration': 'Refrigerated: 1-2 days / Frozen: 2 weeks–1 month',
            'tips': 'Scale → gut → rinse with saltwater → pat dry → wrap',
        },
        'usage_tips': 'Three-piece filleting: sashimi, simmered. Whole: shio-yaki (salt-grilled). The trick is extracting guts without breaking them',
        'nutrition_highlight': 'EPA/DHA (especially blue-backed fish), vitamin D, protein. Varies by species',
    },
}


# Cucumber 修正 (Phase 3-A 後のフィードバック反映)
# Prickly → Bumpy (「ぼつぼつ」を表す)
CUCUMBER_FIX = {
    'cucumber': {
        'key_check': {
            'judgment': 'Bumpy = OK (fresh)',
        },
        'ok_short': ['Bumps: Bumpy', 'Color: Deep green', 'Thickness: Even', 'Firmness: Yes'],
    }
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
            print(f'  TRANSLATED {item["id"]:>12}  {item["name"]["ja"]:>10}  ({n_fields} fields)')

    return n_updated


def apply_cucumber_fix(items):
    """既存の cucumber 翻訳を上書き修正 (Prickly → Bumpy)。"""
    for item in items:
        if item['id'] != 'cucumber':
            continue
        fix = CUCUMBER_FIX['cucumber']
        # judgment 修正
        item['key_check']['judgment']['en'] = fix['key_check']['judgment']
        # ok_short 修正 (配列全体を上書き)
        item['ok_short']['en'] = fix['ok_short']
        print(f'  FIXED      cucumber  きゅうり  (Prickly → Bumpy)')
        return 1
    return 0


def main():
    force = '--force' in sys.argv
    path = os.path.join(ROOT, 'data', 'foods.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    n = apply_translations(data['items'], force=force)
    n_fix = apply_cucumber_fix(data['items'])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\n  {n} items translated, {n_fix} fix applied. (Total items: {len(data["items"])})')


if __name__ == '__main__':
    main()

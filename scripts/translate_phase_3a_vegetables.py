#!/usr/bin/env python3
"""
Phase 3-A: 野菜17品の英訳ドラフトを foods.json に適用。

【翻訳方針】
- name: 国際的に通じる英語名(必要に応じて Japanese name + 一般名)
- key_check: 海外スーパーでも通じる動作・判定表現
- ok_short / ng_short: 'Part: Keyword' の形式で日本語と対応
- ok_points / ng_points: 詳細な説明、料理初心者向け
- 単位: メートル法、500円玉などは "quarter-coin size" で補足
- 食材名既出は標準語化 (e.g., Cabbage / Napa Cabbage 等)

冪等性: 既に en が入っている場合は上書きしない (--force で強制上書き)。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


TRANSLATIONS = {
    # ============================ 1. daikon ============================
    'daikon': {
        'name': 'Daikon Radish',
        'subcategory': 'Root vegetable',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Gently press the white part',
            'judgment': 'Springy = OK',
        },
        'ok_short': [
            'Leaves: Green/Firm',
            'Skin: Tight/Glossy',
            'Weight: Heavy',
            'Holes: Aligned',
        ],
        'ng_short': [
            'Leaves: Yellow/Wilted',
            'Skin: Wrinkled',
            'Weight: Light',
            'Holes: Zigzag',
        ],
        'ok_points': [
            'Vibrant green, fresh leaves',
            'Tight, glossy white body',
            'Heavy with no bruises or dark spots',
            'Hair root holes aligned in a straight line (sign of straight growth)',
        ],
        'ng_points': [
            'Yellow, wilted leaves',
            'Wrinkled or spongy surface',
            'Light weight (water has escaped)',
            'Hair root holes in zigzag pattern (poor growth)',
        ],
        'summary_ok': 'Firm, heavy, vibrant leaves',
        'summary_ng': 'Wrinkled, light, yellow leaves',
        'storage': {
            'method': 'Cut and store leaves and root separately',
            'duration': 'Leaves: 2-3 days / Root: about 2 weeks',
            'tips': 'Wrap in newspaper and refrigerate. Storing upright keeps it fresh longer',
        },
        'usage_tips': 'Top = sweet (salads, grated radish); middle = balanced (simmered dishes); bottom = spicy (pickles, condiments)',
        'nutrition_highlight': 'Vitamin C and digestive enzymes (diastase). Leaves are rich in β-carotene',
    },

    # ============================ 2. carrot ============================
    'carrot': {
        'name': 'Carrot',
        'subcategory': 'Root vegetable',
        'season_peak': 'Autumn–Winter',
        'key_check': {
            'action': 'Look at the top stem cut',
            'judgment': 'Smaller than a quarter coin = OK',
        },
        'ok_short': [
            'Color: Vivid orange',
            'Skin: Smooth',
            'Top cut: Small',
            'Roots: Few',
        ],
        'ng_short': [
            'Color: Dull',
            'Skin: Wrinkled/Spotted',
            'Top cut: Large/Dark',
            'Roots: Many',
        ],
        'ok_points': [
            'Vivid, even orange color throughout',
            'Smooth surface with firmness',
            'Small top stem cut (sign of tender carrot)',
            'Few hair roots, straight shape',
        ],
        'ng_points': [
            'Dull color or visible spots',
            'Wrinkles or soft areas on the surface',
            'Large, blackened top cut',
            'Many rough hair roots',
        ],
        'summary_ok': 'Vivid orange, smooth, small top cut',
        'summary_ng': 'Dull color, spots, large cut',
        'storage': {
            'method': 'Cut off greens, wrap in newspaper or paper towel',
            'duration': '2-3 weeks in the refrigerator',
            'tips': 'Dislikes humidity. Wipe off moisture and store upright',
        },
        'usage_tips': 'Most nutrients are near the skin. Use with skin on or peel thinly',
        'nutrition_highlight': 'Exceptionally rich in β-carotene (vitamin A). Absorption improves when eaten with oil',
    },

    # ============================ 3. negi ============================
    'negi': {
        'name': 'Negi (Japanese Long Onion)',
        'subcategory': 'Leafy / Aromatic',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Squeeze the white part',
            'judgment': 'Tightly packed = OK',
        },
        'ok_short': [
            'White: Thick',
            'Boundary: Sharp',
            'Leaves: Firm',
            'Weight: Heavy',
        ],
        'ng_short': [
            'White: Thin/Hollow',
            'Leaves: Yellowed',
            'Tip: Wilted',
            'Cut end: Dry',
        ],
        'ok_points': [
            'White part is thick and tightly packed',
            'Sharp boundary between green and white',
            'Leaves firm all the way to the tip',
            'Feels heavy when held',
        ],
        'ng_points': [
            'White part is thin with a hollow feel',
            'Green leaves are yellowing',
            'Leaf tips are wilted',
            'Cut end is dry and brown',
        ],
        'summary_ok': 'Thick white, sharp boundary, firm leaves',
        'summary_ng': 'Thin white, yellowing, dry cut',
        'storage': {
            'method': 'Separate green and white parts. Wrap white in newspaper for refrigerator; store green in airtight container',
            'duration': 'White: about 1 week / Green: 3-4 days',
            'tips': 'Negi with soil keeps 2+ weeks in a cool, dark place. Freezing also works',
        },
        'usage_tips': 'White = sweetens when heated (hot pots, simmered dishes); green = condiment, stir-fry',
        'nutrition_highlight': 'Allicin (fatigue recovery, antibacterial). Green parts have β-carotene and vitamin C',
    },

    # ============================ 4. tomato ============================
    'tomato': {
        'name': 'Tomato',
        'subcategory': 'Fruit vegetable',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Look at the stem (calyx)',
            'judgment': 'Green and firm = OK',
        },
        'ok_short': [
            'Color: Vivid red',
            'Stem: Green/Firm',
            'Skin: Tight/Glossy',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Color: Dull',
            'Stem: Brown/Wilted',
            'Skin: Wrinkled/Dark',
            'Feel: Soft',
        ],
        'ok_points': [
            'Evenly vivid red throughout',
            'Calyx is bright green and stands firm',
            'Tight, glossy skin with no blemishes',
            'Feels heavy; star-shaped white lines on the bottom (ripeness mark)',
        ],
        'ng_points': [
            'Dull or partly unripe green color',
            'Calyx is brown, wilted, or dark at the base',
            'Wrinkles, dark spots, or softened areas',
            'Light weight; mushy when pressed',
        ],
        'summary_ok': 'Vivid red, green stem, firm',
        'summary_ng': 'Dull, dry stem, soft',
        'storage': {
            'method': 'Refrigerate when ripe; ripen unripe ones at room temperature',
            'duration': 'Ripe: 3-4 days / Unripe: 2-3 days at room temp',
            'tips': 'Storing stem-side down prevents bruising. Freezes well for long-term storage',
        },
        'usage_tips': 'Cooking with skin on boosts umami and lycopene absorption. Ripe ones for salads; firmer ones hold up better in cooking',
        'nutrition_highlight': 'Lycopene (antioxidant), vitamin C, potassium. Heating with oil increases lycopene absorption 2-3×',
    },

    # ============================ 5. onion ============================
    'onion': {
        'name': 'Onion',
        'subcategory': 'Leafy / Aromatic',
        'season_peak': 'Spring & Autumn',
        'key_check': {
            'action': 'Squeeze the top and bottom',
            'judgment': 'Hard and tight = OK',
        },
        'ok_short': [
            'Skin: Crisp',
            'Top: Hard/Tight',
            'Weight: Heavy',
            'Sprouts: None',
        ],
        'ng_short': [
            'Skin: Sticky',
            'Top: Soft',
            'Center: Sprouting',
            'Bottom: Mold',
        ],
        'ok_points': [
            'Skin is crisp and dry, with shine and firmness',
            'Top (sprout end) and bottom (root end) are hard and tight',
            'Heavy weight with symmetrical shape',
            'No sprouts emerging, no blue mold',
        ],
        'ng_points': [
            'Sticky or moist skin',
            'Green sprouts emerging from top or center',
            'Soft when pressed, shape collapsing',
            'Blue mold or black spots on the bottom',
        ],
        'summary_ok': 'Crisp skin, tight, no sprouts',
        'summary_ng': 'Moist, sprouting, mold',
        'storage': {
            'method': 'Cool, dry, well-ventilated area. Avoid humidity',
            'duration': '1-2 months at room temp; new onions 1 week in the fridge',
            'tips': 'Hang in a mesh bag to last longer. Avoid the vegetable drawer (humidity causes rot)',
        },
        'usage_tips': 'Cutting activates pungent compounds. For raw use, slice thin and rinse (also washes away nutrients). Heating brings out sweetness',
        'nutrition_highlight': 'Allicin (blood circulation, fatigue recovery), quercetin (antioxidant). Most nutrients are near the skin',
    },

    # ============================ 6. potato ============================
    'potato': {
        'name': 'Potato',
        'subcategory': 'Tuber',
        'season_peak': 'Spring & Autumn',
        'key_check': {
            'action': 'Check the skin and eyes',
            'judgment': 'No green, no sprouts = OK',
        },
        'ok_short': [
            'Skin: Tight/Glossy',
            'Color: Brown/Tan',
            'Sprouts: None',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Green: Skin/Flesh',
            'Sprouts: Long',
            'Skin: Wrinkled/Soft',
            'Spots: Dark',
        ],
        'ok_points': [
            'Tight skin and a firm surface',
            'No green-tinted areas (solanine warning)',
            'No sprouts, or only very small ones',
            'Heavy for its size (high starch, fluffy texture)',
        ],
        'ng_points': [
            'Skin or flesh tinted green (solanine = bitter, harmful)',
            'Long sprouts with green areas around them',
            'Wrinkles or softness when pressed',
            'Dark spots or rotten smell',
        ],
        'summary_ok': 'Tight skin, no green, heavy',
        'summary_ng': 'Green, sprouting, wrinkled',
        'storage': {
            'method': 'Cool, dark, well-ventilated place at room temperature (avoid light)',
            'duration': '1-2 months at room temp; new potatoes 2 weeks',
            'tips': 'Storing with apples slows sprouting (ethylene effect). Do NOT refrigerate (starch turns to sugar)',
        },
        'usage_tips': 'Cut away green and sprouted parts thickly (solanine removal). Danshaku = fluffy (croquettes); May Queen = firm (stews)',
        'nutrition_highlight': 'Vitamin C (heat-stable, protected by starch), potassium (anti-edema), dietary fiber',
    },

    # ============================ 7. cabbage ============================
    'cabbage': {
        'name': 'Cabbage',
        'subcategory': 'Leafy vegetable',
        'season_peak': 'Spring & Winter',
        'key_check': {
            'action': 'Lift and check the weight',
            'judgment': 'Heavy = OK',
        },
        'ok_short': [
            'Weight: Heavy',
            'Outer leaves: Green/Firm',
            'Cut end: White',
            'Leaves: Tight',
        ],
        'ng_short': [
            'Weight: Light/Hollow',
            'Outer leaves: Yellow/Wilted',
            'Cut end: Brown',
            'Leaves: Loose',
        ],
        'ok_points': [
            'Heavy for its size (leaves are tightly packed)',
            'Outer leaves are vivid green and firm',
            'Cut end is white and fresh (no discoloration)',
            'Leaves are tightly packed with little gap between them',
        ],
        'ng_points': [
            'Light weight (hollow inside)',
            'Outer leaves are yellow, wilted, or darkened',
            'Cut end is brown, dry, or sticky',
            'Leaves spread outward with large gaps',
        ],
        'summary_ok': 'Heavy, firm green, white cut',
        'summary_ng': 'Light, yellowed, brown cut',
        'storage': {
            'method': 'Keep one outer leaf on, scoop out core and pack with damp paper towel. Refrigerate',
            'duration': 'Whole: 2 weeks / Cut: 3-4 days',
            'tips': 'Cover cut surface with plastic wrap. Freezing OK after blanching and salting',
        },
        'usage_tips': 'Spring cabbage = soft (raw, salads); winter cabbage = dense (stir-fry, stews). The core is also nutritious',
        'nutrition_highlight': 'Vitamin C and K, cabagin (stomach lining protection). Eaten raw for best vitamin C absorption',
    },

    # ============================ 8. cucumber ============================
    'cucumber': {
        'name': 'Cucumber',
        'subcategory': 'Fruit vegetable',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Touch the bumps lightly',
            'judgment': 'Prickly = OK (fresh)',
        },
        'ok_short': [
            'Bumps: Prickly',
            'Color: Deep green',
            'Thickness: Even',
            'Firmness: Yes',
        ],
        'ng_short': [
            'Bumps: None (old)',
            'Color: Yellowish',
            'Thickness: Uneven',
            'Feel: Soft',
        ],
        'ok_points': [
            'Bumps (called "ibo") are sharp and prickly (sign of freshness)',
            'Deep green color with shine',
            'Even thickness from end to end',
            'Firm and taut when held',
        ],
        'ng_points': [
            'Smooth surface with no bumps (old)',
            'Yellowish or with white spots',
            'Uneven thickness, bends easily',
            'Soft, mushy ends',
        ],
        'summary_ok': 'Prickly bumps, deep green, firm',
        'summary_ng': 'Smooth, yellowed, soft',
        'storage': {
            'method': 'Wrap each in paper towel, store upright (stem up) in the refrigerator',
            'duration': '4-5 days refrigerated',
            'tips': 'Sensitive to cold (damage below 10°C). Vegetable drawer is best. Keep dry',
        },
        'usage_tips': 'Curved ones taste the same (often cheaper). Salt-roll for color and to remove bitterness. Most nutrients near the skin',
        'nutrition_highlight': '95% water. Potassium (diuretic), vitamin K. Low calorie, perfect for summer hydration',
    },

    # ============================ 9. garlic ============================
    'garlic': {
        'name': 'Garlic',
        'subcategory': 'Leafy / Aromatic',
        'season_peak': 'Early summer',
        'key_check': {
            'action': 'Squeeze to check firmness',
            'judgment': 'Hard and packed = OK',
        },
        'ok_short': [
            'Skin: Crisp',
            'Shape: Even',
            'Weight: Heavy',
            'Sprouts: None',
        ],
        'ng_short': [
            'Skin: Loose',
            'Inside: Hollow',
            'Sprouts: Growing',
            'Bottom: Mold',
        ],
        'ok_points': [
            'Skin is crisp and dry, firm and shiny',
            'Bulb is hard with cloves tightly packed',
            'No green sprouts emerging',
            'Even shape, no extremely small cloves',
        ],
        'ng_points': [
            'Skin is loose or starting to peel',
            'Hollow inside, feels light',
            'Green sprouts visible from outside',
            'Blue mold or black spots on the bottom',
        ],
        'summary_ok': 'Crisp skin, hard, no sprouts',
        'summary_ng': 'Hollow, sprouting, moldy',
        'storage': {
            'method': 'Cool, dark, well-ventilated area. Avoid humidity',
            'duration': '1-2 months at room temperature',
            'tips': 'Hanging in a mesh bag or wrapping in newspaper extends life',
        },
        'usage_tips': 'Cutting and exposing to air activates aroma. Sprouts cause bitterness, so remove them',
        'nutrition_highlight': 'Allicin (immune boost), vitamin B1. Classic for fatigue recovery and cold prevention',
    },

    # ============================ 10. komatsuna ============================
    'komatsuna': {
        'name': 'Komatsuna (Japanese Mustard Spinach)',
        'subcategory': 'Leafy vegetable',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Look at the leaf tips',
            'judgment': 'Firm = OK',
        },
        'ok_short': [
            'Leaves: Deep green',
            'Stems: Firm',
            'Cut end: White',
            'Shine: Yes',
        ],
        'ng_short': [
            'Leaves: Yellowed',
            'Stems: Wilted',
            'Cut end: Brown',
            'Spots: Black',
        ],
        'ok_points': [
            'Vibrant deep green leaves, firm to the very tip',
            'Stem base is solid with white cut surface',
            'Leaves and stems are firm and shiny',
            'Overall fresh and crisp',
        ],
        'ng_points': [
            'Yellowed, wilted leaves',
            'Stem cut is brown, dry, or sticky',
            'Black spots or holes (insect or disease damage)',
            'Whole vegetable looks limp',
        ],
        'summary_ok': 'Firm leaves, solid stem, white cut',
        'summary_ng': 'Yellowed, wilted, spots',
        'storage': {
            'method': 'Wrap in damp newspaper, store upright in the refrigerator',
            'duration': '3-4 days refrigerated',
            'tips': 'Freezes well: blanch, drain, and portion into small bags',
        },
        'usage_tips': 'Low in bitterness, no need to blanch (easier than spinach). Even works raw in salads',
        'nutrition_highlight': 'Rich in calcium and iron (more than spinach). Also vitamin K, C, and β-carotene',
    },

    # ============================ 11. lettuce ============================
    'lettuce': {
        'name': 'Lettuce',
        'subcategory': 'Leafy vegetable',
        'season_peak': 'Spring–Autumn',
        'key_check': {
            'action': 'Lift it up',
            'judgment': 'Light and airy = OK',
        },
        'ok_short': [
            'Weight: Light/Airy',
            'Leaves: Vivid green',
            'Pack: Loose',
            'Core: White/Small',
        ],
        'ng_short': [
            'Weight: Too heavy',
            'Leaves: Browning',
            'Core: Reddish',
            'Cut end: Brown',
        ],
        'ok_points': [
            'Light to lift (loose pack with air)',
            'Leaf tips are vivid green and firm',
            'Core cut surface is white and about coin-sized',
            'Loose layered leaves with gaps',
        ],
        'ng_points': [
            'Too heavy (overgrown = bitter)',
            'Brown or wilted leaf tips',
            'Reddish or rusty core (old)',
            'Darkening of leaves, sticky feel',
        ],
        'summary_ok': 'Light, green tips, white core',
        'summary_ng': 'Heavy, browning, red core',
        'storage': {
            'method': 'Hollow out the core and pack with damp paper towel; bag and refrigerate',
            'duration': '1 week refrigerated',
            'tips': 'Tear by hand instead of cutting with metal (prevents discoloration)',
        },
        'usage_tips': 'For salads, tear → soak in cold water → drain. Heat briefly only (texture is the appeal)',
        'nutrition_highlight': 'High water content, potassium, folate, β-carotene. Low calorie with good satiety',
    },

    # ============================ 12. hakusai ============================
    'hakusai': {
        'name': 'Napa Cabbage',
        'subcategory': 'Leafy vegetable',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Lift and check the weight',
            'judgment': 'Heavy = OK',
        },
        'ok_short': [
            'Weight: Heavy',
            'Tips: Crisp',
            'Cut: White',
            'Leaves: Tight',
        ],
        'ng_short': [
            'Weight: Light',
            'Tips: Wilted',
            'Cut: Black',
            'Leaves: Loose',
        ],
        'ok_points': [
            'Heavier than other heads of similar size (densely packed leaves)',
            'Outer leaves are vivid green with crisp tips',
            'Cut end is white and glossy',
            'Leaves are tightly packed together',
        ],
        'ng_points': [
            'Light weight (hollow inside)',
            'Wilted, yellowed leaf tips',
            'Cut end is darkened or sticky',
            'Leaves opening outward, falling apart',
        ],
        'summary_ok': 'Heavy, crisp tips, white cut',
        'summary_ng': 'Light, wilted, black cut',
        'storage': {
            'method': 'Whole: wrap in newspaper, cool dark place. Cut: wrap with plastic, refrigerate',
            'duration': 'Whole: 2-3 weeks / Cut: 3-5 days',
            'tips': 'Black specks are "goma-sho" (harmless taste). Press plastic wrap firmly on cut surfaces',
        },
        'usage_tips': 'Outer leaves: stir-fry/stew; inner leaves: salads/light pickles; core: makes great soup stock',
        'nutrition_highlight': 'Vitamin C, potassium, dietary fiber. Absorbs flavors well in hot pots',
    },

    # ============================ 13. nasu ============================
    'nasu': {
        'name': 'Eggplant',
        'subcategory': 'Fruit vegetable',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Touch the calyx (stem cap)',
            'judgment': 'Sharp prickles = OK',
        },
        'ok_short': [
            'Color: Deep purple/Glossy',
            'Calyx: Sharp prickles',
            'Skin: Tight',
            'Weight: Solid',
        ],
        'ng_short': [
            'Color: Faded',
            'Calyx: Wilted',
            'Skin: Wrinkled',
            'Feel: Soft',
        ],
        'ok_points': [
            'Deep purple color with glossy shine',
            'Calyx (green cap) has sharp, prickly thorns',
            'Skin is tight; bounces back when pressed',
            'Heavy for its size with even shape',
        ],
        'ng_points': [
            'Faded or brownish color',
            'Calyx is dry with prickles fallen off',
            'Wrinkles in the skin, soft to the touch',
            'Light weight; discolored areas',
        ],
        'summary_ok': 'Deep purple, glossy, sharp prickles',
        'summary_ng': 'Faded, wrinkled, soft',
        'storage': {
            'method': 'Wrap each in plastic and store in the vegetable drawer',
            'duration': '4-5 days refrigerated',
            'tips': 'Sensitive to cold (damage below 10°C). Room temp OK but shorter shelf life',
        },
        'usage_tips': 'Soak cut pieces in water to remove bitterness. Cooking with skin in oil maximizes anthocyanin absorption',
        'nutrition_highlight': 'Nasunin (antioxidant, in the purple skin), potassium, dietary fiber',
    },

    # ============================ 14. piman ============================
    'piman': {
        'name': 'Green Bell Pepper',
        'subcategory': 'Fruit vegetable',
        'season_peak': 'Summer',
        'key_check': {
            'action': 'Check color and firmness',
            'judgment': 'Deep green, no give = OK',
        },
        'ok_short': [
            'Color: Deep green',
            'Calyx: Green/Firm',
            'Skin: Tight/Glossy',
            'Flesh: Thick',
        ],
        'ng_short': [
            'Color: Faded',
            'Calyx: Brown',
            'Skin: Wrinkled',
            'Flesh: Thin',
        ],
        'ok_points': [
            'Deep, even green color',
            'Vibrant green calyx with fresh cut',
            'Tight, glossy skin; no give when pressed',
            'Thick flesh with solid weight',
        ],
        'ng_points': [
            'Faded color, slightly brownish',
            'Dry, brown calyx',
            'Wrinkles, softening',
            'Thin flesh, light weight; gives way when pressed',
        ],
        'summary_ok': 'Deep green, firm, thick flesh',
        'summary_ng': 'Faded, wrinkled, thin',
        'storage': {
            'method': 'Bag and store in vegetable drawer',
            'duration': '1 week refrigerated',
            'tips': 'Wrap each in paper towel for longer shelf life',
        },
        'usage_tips': 'For less bitterness, cut along the fibers (vertical). Seeds and white parts are also nutritious',
        'nutrition_highlight': 'Vitamin C (heat-stable), β-carotene, dietary fiber',
    },

    # ============================ 15. broccoli ============================
    'broccoli': {
        'name': 'Broccoli',
        'subcategory': 'Flower vegetable',
        'season_peak': 'Winter',
        'key_check': {
            'action': 'Check the floret color',
            'judgment': 'Deep green, dense = OK',
        },
        'ok_short': [
            'Florets: Dense/Deep green',
            'Stem: Fresh cut',
            'Weight: Heavy',
            'Color: Purplish',
        ],
        'ng_short': [
            'Florets: Yellow/Open',
            'Stem: Hollow',
            'Cut: Brown',
            'Color: Dull',
        ],
        'ok_points': [
            'Florets are dense and deep green',
            'Stem cut is fresh and white',
            'Heavy and compact in shape',
            'Slight purple tint = sweet, nutritious (cold-induced color)',
        ],
        'ng_points': [
            'Florets are yellowing and opening (going to flower)',
            'Stem is hollow inside (su-bori)',
            'Cut end is brown or sticky',
            'Overall dull color',
        ],
        'summary_ok': 'Dense green, white cut, heavy',
        'summary_ng': 'Yellow florets, hollow, brown',
        'storage': {
            'method': 'Stem-down, wrap with plastic and refrigerate',
            'duration': '3-4 days refrigerated',
            'tips': 'Boiled and frozen in florets keeps 1 month',
        },
        'usage_tips': 'Stems are also nutritious; peel thickly. For boiling, use salted water; microwaving preserves more nutrients',
        'nutrition_highlight': 'Vitamin C (2× lemon), sulforaphane (detox), dietary fiber',
    },

    # ============================ 16. ginger ============================
    'ginger': {
        'name': 'Ginger',
        'subcategory': 'Root vegetable',
        'season_peak': 'Summer (new ginger)',
        'key_check': {
            'action': 'Check the skin firmness',
            'judgment': 'Tight, glossy = OK',
        },
        'ok_short': [
            'Skin: Thin/Glossy',
            'Flesh: Hard/Firm',
            'Color: Vivid yellow',
            'Aroma: Strong',
        ],
        'ng_short': [
            'Skin: Wrinkled/Dry',
            'Flesh: Soft',
            'Color: Dull',
            'Spots: Black',
        ],
        'ok_points': [
            'Skin is thin with shine',
            'Flesh is plump and firm',
            'Vivid yellow to orange color throughout',
            'Strong aroma',
        ],
        'ng_points': [
            'Skin is wrinkled and dry',
            'Soft when pressed',
            'Dull color with black spots',
            'Hollow or fibrous cut surface',
        ],
        'summary_ok': 'Firm, glossy, strong aroma',
        'summary_ng': 'Wrinkled, soft, spotted',
        'storage': {
            'method': 'Wrap in damp newspaper, cool dark place or refrigerate',
            'duration': '1 week at room temp; 3 weeks refrigerated',
            'tips': 'Freeze grated or thinly sliced for convenience',
        },
        'usage_tips': 'Aroma is strongest near the skin. Use unpeeled or peel thinly. Grated ginger removes meat/fish odors',
        'nutrition_highlight': 'Gingerol (antibacterial, anti-inflammatory), shogaol (warming effect). Great for cold sensitivity',
    },

    # ============================ 17. pumpkin ============================
    'pumpkin': {
        'name': 'Kabocha Squash',
        'subcategory': 'Fruit vegetable',
        'season_peak': 'Summer–Autumn',
        'key_check': {
            'action': 'Look at the stem',
            'judgment': 'Cork-like, dry = OK',
        },
        'ok_short': [
            'Stem: Thick/Corky',
            'Skin: Hard/Bumpy',
            'Cut: Deep orange',
            'Weight: Heavy',
        ],
        'ng_short': [
            'Stem: Green/Wet',
            'Skin: Soft',
            'Cut: Pale orange',
            'Seeds: Hollow',
        ],
        'ok_points': [
            'Stem is thick and dried like cork',
            'Skin is hard with bumpy texture',
            'Cut surface shows deep orange',
            'Seeds are densely packed',
        ],
        'ng_points': [
            'Stem is green and wet (picked too early)',
            'Soft skin with bruises',
            'Pale orange cut surface',
            'Hollow space around seeds (watery)',
        ],
        'summary_ok': 'Thick stem, deep orange, heavy',
        'summary_ng': 'Green stem, pale, hollow',
        'storage': {
            'method': 'Whole: cool dark place. Cut: remove seeds and pith, wrap and refrigerate',
            'duration': 'Whole: 2-3 months / Cut: 5-7 days',
            'tips': 'Cut quickly deteriorates. Cooking before freezing works best for long-term storage',
        },
        'usage_tips': 'Skin is also nutritious. Cooking with skin prevents falling apart. Microwaving softens hard skin for cutting',
        'nutrition_highlight': 'β-carotene (antioxidant, mucous membranes), vitamin E, dietary fiber. Traditional winter solstice food',
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

    print(f'\n  {n} foods updated. (Total items: {len(data["items"])})')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Phase C (11食材・タンパク質系) を data/foods.json に追加。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL_MONTHS = [f"{m}月" for m in range(1, 13)]


FOODS = [
    # =================== 豆製品 (2) ===================
    {
        "id": "tofu", "name": "豆腐", "name_kana": "とうふ", "name_en": "Tofu",
        "category": "egg_dairy_bean", "category_label": "卵・乳・豆", "subcategory": "豆製品",
        "color_theme": "#FFF8E8", "accent_color": "#C8A878",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "水と表面を見る", "judgment": "透明・無臭 = OK"},
        "ok_short": ["形:整う", "水:透明", "色:乳白", "無臭"],
        "ng_short": ["形:崩", "水:濁", "色:黄", "酸臭"],
        "ok_points": [
            "形が整い、角がしっかりしている",
            "水が透き通っていて無臭",
            "色が乳白色で均一",
            "押すと弾力がある(絹は柔らかく、木綿はしっかり)"
        ],
        "ng_points": [
            "形が崩れている、ボロボロ",
            "水が濁っている、ぬめりがある",
            "黄色っぽく変色",
            "酸っぱい臭い、表面のヌメリ"
        ],
        "summary_ok": "形整・水透明・無臭",
        "summary_ng": "崩・水濁・酸臭",
        "storage": {"method": "パックの水ごと冷蔵、開封後は新しい水に",
                    "duration": "未開封:賞味期限内 / 開封:1〜2日",
                    "tips": "毎日水を替える。冷凍可だがスポンジ状になる"},
        "usage_tips": "絹=つるん滑らか(冷奴・スープ)、木綿=しっかり(炒り豆腐・麻婆)。湯通しで水分抜く",
        "nutrition_highlight": "良質な植物性タンパク質、大豆イソフラボン、カルシウム、鉄分"
    },
    {
        "id": "natto", "name": "納豆", "name_kana": "なっとう", "name_en": "Natto",
        "category": "egg_dairy_bean", "category_label": "卵・乳・豆", "subcategory": "豆製品",
        "color_theme": "#F0E0C5", "accent_color": "#A07848",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "🥄", "action": "混ぜて糸を見る", "judgment": "強い糸引き = OK"},
        "ok_short": ["糸:強・粘", "豆:粒揃う", "色:茶均一", "発酵臭:良"],
        "ng_short": ["糸:弱", "豆:乾燥", "色:黒・カビ", "アンモニア臭"],
        "ok_points": [
            "糸引き(粘り)が強くしっかり",
            "豆の粒が揃ってふっくら",
            "色が均一な茶〜濃茶色",
            "独特の発酵臭(アンモニア臭ではない)"
        ],
        "ng_points": [
            "糸引きが弱い、ない",
            "豆が乾燥してパサパサ",
            "黒く変色、白い斑点(カビ)",
            "強烈なアンモニア臭"
        ],
        "summary_ok": "糸強・粒揃・茶均一",
        "summary_ng": "糸弱・乾・カビ",
        "storage": {"method": "冷蔵保存(発酵を遅らせる)",
                    "duration": "賞味期限内、開封後は早めに",
                    "tips": "冷凍可で1ヶ月。室温に出すと発酵進み苦み出る"},
        "usage_tips": "ご飯に乗せる前にしっかり混ぜて糸を引かせる。生卵・薬味で味調整",
        "nutrition_highlight": "ナットウキナーゼ(血液サラサラ)、ビタミンK2(骨)、大豆イソフラボン、食物繊維"
    },

    # =================== 肉類 (3) ===================
    {
        "id": "pork", "name": "豚肉", "name_kana": "ぶたにく", "name_en": "Pork",
        "category": "meat", "category_label": "肉類", "subcategory": "",
        "color_theme": "#FCE5DC", "accent_color": "#E08878",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "色とドリップを見る", "judgment": "淡ピンク・少 = OK"},
        "ok_short": ["色:淡ピンク", "脂:白くっきり", "ドリップ:少", "ツヤ:あり"],
        "ng_short": ["色:暗赤・グレー", "脂:黄", "ドリップ:多・赤茶", "ベタつき"],
        "ok_points": [
            "肉色が淡いピンク色で均一",
            "脂が白く、肉と境がはっきり",
            "弾力があり、ドリップが少なく透明",
            "全体にツヤがあり、ベタつかない"
        ],
        "ng_points": [
            "色が暗い赤、灰色がかる",
            "脂が黄ばんでいる、変色",
            "ドリップが赤茶〜濁った色で多い",
            "表面がベタつく、糸を引く"
        ],
        "summary_ok": "淡ピンク・脂白・ドリップ少",
        "summary_ng": "暗・脂黄・ドリップ多",
        "storage": {"method": "チルド室か最も冷える場所で",
                    "duration": "冷蔵で1〜2日 / 冷凍で2〜3週間",
                    "tips": "下味冷凍(塩・酒・砂糖)で柔らかさUP+保存性◎"},
        "usage_tips": "中心部 75℃ 以上 1分加熱が安全基準。生姜焼き等で部位ごとの食感を活かす",
        "nutrition_highlight": "ビタミンB1(疲労回復・糖質代謝、牛肉の約10倍)、亜鉛、良質タンパク質"
    },
    {
        "id": "beef", "name": "牛肉", "name_kana": "ぎゅうにく", "name_en": "Beef",
        "category": "meat", "category_label": "肉類", "subcategory": "",
        "color_theme": "#F8D8D0", "accent_color": "#A04030",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "色と脂を見る", "judgment": "鮮赤・脂白 = OK"},
        "ok_short": ["色:鮮赤", "脂:白・霜降", "繊維:均一", "ツヤ:あり"],
        "ng_short": ["色:どす黒", "脂:黄", "ドリップ:多", "繊維:粗"],
        "ok_points": [
            "肉色が鮮やかな赤で均一",
            "脂(霜降り)が白く、肉に均等に入る",
            "繊維が細かく均一、弾力あり",
            "切り口がツヤツヤしている"
        ],
        "ng_points": [
            "色がどす黒い、暗赤色〜灰色",
            "脂が黄色く変色、ベタつく",
            "ドリップが多く赤茶色",
            "繊維が粗く、押すと跡が残る"
        ],
        "summary_ok": "鮮赤・脂白・繊維細",
        "summary_ng": "どす黒・脂黄・ドリップ多",
        "storage": {"method": "チルド室、空気を抜いてラップ",
                    "duration": "冷蔵で2〜3日 / 冷凍で1ヶ月",
                    "tips": "ステーキ用は買ったらすぐ使うか、下味付けて冷凍"},
        "usage_tips": "焼く前は常温に戻す(中心まで均一に火が通る)。脂は風味、霜降り=和牛系",
        "nutrition_highlight": "ヘム鉄(吸収率高)、亜鉛、ビタミンB12、L-カルニチン(脂肪燃焼)"
    },
    {
        "id": "ground_meat", "name": "ひき肉", "name_kana": "ひきにく", "name_en": "Ground Meat",
        "category": "meat", "category_label": "肉類", "subcategory": "",
        "color_theme": "#FCD8D0", "accent_color": "#D87878",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "色の均一性を見る", "judgment": "均一ピンク = OK"},
        "ok_short": ["色:均一ピンク", "感触:ふんわり", "ドリップ:少", "ベタ:なし"],
        "ng_short": ["色:濃淡・グレー", "感触:ベタ", "ドリップ:多", "臭:ある"],
        "ok_points": [
            "色が均一なピンク色",
            "ふんわりした手触り、ベタつかない",
            "ドリップが少なく、パックが綺麗",
            "店頭で当日加工=最も新鮮"
        ],
        "ng_points": [
            "部分的に色が濃い、グレーや黒",
            "ベタつく、糸を引く",
            "ドリップが赤茶色で多い",
            "酸っぱい臭い"
        ],
        "summary_ok": "均一ピンク・ふんわり",
        "summary_ng": "濃淡・ベタ・ドリップ",
        "storage": {"method": "チルド室で当日〜翌日中に使い切る or 冷凍",
                    "duration": "冷蔵1日 / 冷凍2週間",
                    "tips": "薄く広げて冷凍→使う分だけ折って解凍。空気抜き重要"},
        "usage_tips": "鶏=パサつきやすい、豚=旨味、牛=コク、合挽き=バランス。塊にして焼くなら混ぜすぎ注意",
        "nutrition_highlight": "肉と同じ栄養素。脂質が多めなので使用量に注意。タンパク質補給に手軽"
    },

    # =================== 魚介 (5) ===================
    {
        "id": "salmon", "name": "鮭(切り身)", "name_kana": "さけ きりみ", "name_en": "Salmon Fillet",
        "category": "fish", "category_label": "魚介", "subcategory": "切り身",
        "color_theme": "#FFE0D0", "accent_color": "#E07050",
        "season": ["9月", "10月", "11月"], "season_peak": "秋(秋鮭)",
        "key_check": {"icon": "👀", "action": "オレンジ色と脂を見る", "judgment": "鮮橙・白脂線 = OK"},
        "ok_short": ["色:鮮橙", "脂:白線くっきり", "ツヤ:あり", "皮:銀光"],
        "ng_short": ["色:茶・くすみ", "脂:不明", "ヌメ:あり", "ドリップ:多"],
        "ok_points": [
            "全体が鮮やかなオレンジ色",
            "脂(白い筋)がくっきり、規則的",
            "切り口にツヤがある",
            "皮目が銀色に光る"
        ],
        "ng_points": [
            "色が褐色に変色、くすむ",
            "脂のラインがぼやける、ない",
            "表面にヌメリ、糸を引く",
            "ドリップが多く赤茶色"
        ],
        "summary_ok": "鮮橙・白線くっきり",
        "summary_ng": "褐・線ぼや・ヌメ",
        "storage": {"method": "チルド室、ラップで密閉",
                    "duration": "冷蔵で1〜2日 / 冷凍で2〜3週間",
                    "tips": "塩を振って冷凍すると保存性UP+水分抜けで臭み軽減"},
        "usage_tips": "皮目から焼くとパリッ。塩鮭は焼き、生鮭は塩を振って身を締めてから調理",
        "nutrition_highlight": "アスタキサンチン(抗酸化、オレンジ色の正体)、DHA・EPA、ビタミンD"
    },
    {
        "id": "saba", "name": "鯖", "name_kana": "さば", "name_en": "Mackerel",
        "category": "fish", "category_label": "魚介", "subcategory": "青魚",
        "color_theme": "#E5E8EC", "accent_color": "#506068",
        "season": ["10月", "11月", "12月", "1月", "2月"], "season_peak": "秋〜冬",
        "key_check": {"icon": "👀", "action": "目とエラを見る", "judgment": "目澄む・エラ赤 = OK"},
        "ok_short": ["目:黒澄む", "エラ:鮮赤", "腹:固", "肌:銀ピカ"],
        "ng_short": ["目:白濁", "エラ:茶", "腹:柔", "肌:ヌメ"],
        "ok_points": [
            "目が黒く澄み、瞳が明瞭",
            "エラが鮮やかな赤色",
            "腹がしっかり固く、押して弾力",
            "体表が銀色に光り、波模様くっきり"
        ],
        "ng_points": [
            "目が白く濁って曇る",
            "エラが茶色〜黒色",
            "腹が柔らかい、破れる",
            "体表のヌメリ多く、臭い"
        ],
        "summary_ok": "目澄・エラ赤・腹固",
        "summary_ng": "目濁・エラ茶・腹柔",
        "storage": {"method": "新聞紙→ラップ→チルド室。氷の上が理想",
                    "duration": "冷蔵で1日 / 内臓除去後冷凍で2週間",
                    "tips": "鮮度落ちが早い青魚。アニサキス対策で内臓は早めに除去"},
        "usage_tips": "塩鯖はそのまま焼き、生鯖は塩を振って臭み抜き。〆鯖は新鮮なものだけ",
        "nutrition_highlight": "EPA・DHA(青魚の代表)、ビタミンD、ナイアシン、タンパク質豊富"
    },
    {
        "id": "aji", "name": "アジ", "name_kana": "あじ", "name_en": "Horse Mackerel",
        "category": "fish", "category_label": "魚介", "subcategory": "青魚",
        "color_theme": "#E5E8EC", "accent_color": "#506068",
        "season": ["5月", "6月", "7月", "8月"], "season_peak": "夏",
        "key_check": {"icon": "👀", "action": "ぜいごを触る", "judgment": "硬く張る = OK"},
        "ok_short": ["目:澄む", "エラ:赤", "ぜいご:固", "肌:銀光"],
        "ng_short": ["目:濁", "エラ:茶", "ぜいご:柔", "肌:ヌメ"],
        "ok_points": [
            "目が黒く澄む",
            "エラが鮮やかな赤色",
            "尾近くのぜいご(硬鱗)が硬く張る",
            "体表が銀色に光って、ハリあり"
        ],
        "ng_points": [
            "目が白く濁る",
            "エラが茶色く変色",
            "ぜいごが柔らかくしなる",
            "体表ヌメリ、肌が乾く"
        ],
        "summary_ok": "目澄・エラ赤・ぜいご硬",
        "summary_ng": "目濁・エラ茶・ぜいご柔",
        "storage": {"method": "氷の上で冷蔵、内臓は早く除去",
                    "duration": "冷蔵で1日 / 開いて冷凍で2週間",
                    "tips": "刺身用は当日中、塩を振って一晩寝かせて干物にも"},
        "usage_tips": "塩焼き・刺身・なめろう・タタキ。脂のった夏アジは絶品",
        "nutrition_highlight": "EPA・DHA、タウリン(肝機能)、カリウム、低カロリー高タンパク"
    },
    {
        "id": "ebi", "name": "エビ", "name_kana": "えび", "name_en": "Shrimp",
        "category": "fish", "category_label": "魚介", "subcategory": "甲殻類",
        "color_theme": "#FCE5D8", "accent_color": "#A07060",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "頭と殻を見る", "judgment": "頭黒くない・殻透 = OK"},
        "ok_short": ["殻:透", "節:くっきり", "頭:黒くない", "ハリ:あり"],
        "ng_short": ["頭:黒・赤斑", "殻:離", "感触:柔", "尾:変色"],
        "ok_points": [
            "殻が透き通り艶がある",
            "節(セグメント)がくっきり",
            "頭が黒くない、変色なし",
            "触ってハリ、ヒゲ折れず"
        ],
        "ng_points": [
            "頭が黒く変色、赤い斑点",
            "殻と身が離れる、隙間",
            "押すと柔らかい",
            "尾が変色(黒や緑)"
        ],
        "summary_ok": "殻透・節くっきり・頭白",
        "summary_ng": "頭黒・殻離・柔",
        "storage": {"method": "氷を当てて即冷却、当日〜翌日に使う",
                    "duration": "冷蔵で1日 / 冷凍で2週間",
                    "tips": "殻付きで冷凍が長持ち+風味◎。冷凍焼け対策で空気抜き徹底"},
        "usage_tips": "背わたを取って臭み抜き。塩水で洗うとプリッ。加熱しすぎると硬くなる",
        "nutrition_highlight": "タウリン、低脂質高タンパク、アスタキサンチン(殻に含む)、ミネラル"
    },
    {
        "id": "whole_fish", "name": "一尾魚の見方", "name_kana": "いちびざかな", "name_en": "Whole Fish Guide",
        "category": "fish", "category_label": "魚介", "subcategory": "汎用ガイド",
        "color_theme": "#E5E8EC", "accent_color": "#506068",
        "season": ALL_MONTHS, "season_peak": "魚種により",
        "key_check": {"icon": "👀", "action": "目とエラを見る", "judgment": "目澄・エラ赤 = OK"},
        "ok_short": ["目:黒澄", "エラ:鮮赤", "腹:固", "肌:ハリ・銀光"],
        "ng_short": ["目:白濁", "エラ:茶〜黒", "腹:柔", "肌:ヌメ・乾"],
        "ok_points": [
            "【目】黒く澄み、瞳が明瞭(濁ったら鮮度落ち)",
            "【エラ】鮮やかな赤色(茶色・黒は古い)",
            "【腹】固く張る(柔らか・破れは内臓劣化)",
            "【体表】銀色の光沢・ハリ、自然なヌメリ"
        ],
        "ng_points": [
            "目が白く濁る、瞳がぼやける",
            "エラが茶色〜黒色に変色",
            "腹が柔らかい、破れている",
            "体表のヌメリ過多 or カラカラに乾燥"
        ],
        "summary_ok": "目澄・エラ赤・腹固",
        "summary_ng": "目濁・エラ茶・腹柔",
        "storage": {"method": "氷の上で冷蔵、内臓・エラは早めに除去",
                    "duration": "冷蔵で1〜2日 / 冷凍で2週間〜1ヶ月",
                    "tips": "うろこ・内臓除去 → 塩水洗い → ペーパーで水気拭き取り → ラップ"},
        "usage_tips": "三枚下ろし=刺身・煮付け、丸ごと=塩焼き。内臓を傷つけずに取り出すのがコツ",
        "nutrition_highlight": "EPA・DHA(青魚)、ビタミンD、タンパク質。魚種により異なる"
    },

    # =================== 乳製品 (1) ===================
    {
        "id": "yogurt", "name": "ヨーグルト", "name_kana": "よーぐると", "name_en": "Yogurt",
        "category": "egg_dairy_bean", "category_label": "卵・乳・豆", "subcategory": "乳製品",
        "color_theme": "#FFF8E8", "accent_color": "#C8A878",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👀", "action": "容器と表面を見る", "judgment": "膨らみなし = OK"},
        "ok_short": ["容器:平坦", "表面:滑か", "色:乳白", "酸味:良"],
        "ng_short": ["容器:膨", "表面:ホエイ過", "色:黄", "カビ"],
        "ok_points": [
            "容器が膨らんでいない、平坦",
            "表面が滑らかで均一",
            "色が乳白色〜淡クリーム",
            "蓋を開けて爽やかな酸味の香り"
        ],
        "ng_points": [
            "容器が膨らんでいる(発酵過剰)",
            "表面に黄色い液(ホエイ)が大量分離",
            "色が黄ばむ・茶色がかる",
            "カビ・異臭(腐敗)"
        ],
        "summary_ok": "平坦・滑か・乳白",
        "summary_ng": "膨・分離・カビ",
        "storage": {"method": "10℃以下の冷蔵庫、ドアポケット避ける",
                    "duration": "賞味期限内、開封後は早めに(2〜3日)",
                    "tips": "凍らせるとフローズン風に。少量のホエイ分離は正常"},
        "usage_tips": "そのままはちみつや果物と。料理にも(肉柔らかく、コク出し)",
        "nutrition_highlight": "乳酸菌(腸内環境)、カルシウム、タンパク質、ビタミンB2"
    },
]


def main():
    path = os.path.join(ROOT, 'data', 'foods.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    existing = {it['id'] for it in data['items']}
    added = 0
    for spec in FOODS:
        if spec['id'] in existing:
            print(f"  SKIP {spec['id']} (exists)")
            continue
        data['items'].append(spec)
        added += 1
        print(f"  ADDED {spec['id']:>12}  {spec['name']}")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n  {added} added. Total items: {len(data['items'])}")


if __name__ == '__main__':
    main()

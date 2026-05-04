#!/usr/bin/env python3
"""
Phase D ステップ1: ジビエ2食材 (鹿肉・猪肉) のドラフトデータを追加。

注意:
これらは標準的な情報源 (家庭料理ガイド・食品成分表・ジビエ料理本)
に基づくドラフト。ヒロキ(現役ハンター)による以下の補強がステップ2で予定:
- 血抜きの状態判別
- 季節別の肉質の違い
- 部位ごとの特徴
- ジビエ料理初心者向けの注意点
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


FOODS = [
    {
        "id": "venison",
        "name": "鹿肉",
        "name_kana": "しかにく",
        "name_en": "Venison",
        "category": "game_meat",
        "category_label": "ジビエ",
        "subcategory": "",
        "color_theme": "#FFD8C8",
        "accent_color": "#7A1810",
        "season": ["11月", "12月", "1月", "2月", "3月"],
        "season_peak": "冬(狩猟期)",
        "key_check": {
            "icon": "👀",
            "action": "色と臭いを確認",
            "judgment": "深い赤・無臭 = OK"
        },
        "ok_short": ["色:深紅", "繊維:細密", "脂:極少", "ドリップ:少"],
        "ng_short": ["色:茶〜黒", "ベタつき", "獣臭強", "ドリップ多"],
        "ok_points": [
            "色が深く濃い赤色(ヘモグロビンが豊富)",
            "繊維が細かく密で、断面がきめ細やか",
            "脂肪が非常に少ない(赤身肉)",
            "血抜きが良い個体は無臭〜微かな鉄分の香り、ドリップ少"
        ],
        "ng_points": [
            "色が褐色〜黒に変色(古い・酸化)",
            "表面がベタつく、糸を引く",
            "強い獣臭(血抜き不十分・処理が悪い)",
            "ドリップが多く赤茶色"
        ],
        "summary_ok": "深紅・繊維細・無臭",
        "summary_ng": "茶〜黒・ベタ・獣臭",
        "storage": {
            "method": "信頼できる業者から購入後、すぐに冷凍。真空パックが理想",
            "duration": "冷凍で2〜3ヶ月、解凍後は早めに使い切る",
            "tips": "解凍は冷蔵庫でじっくり(8〜12時間)。急速解凍はドリップ流出の原因"
        },
        "usage_tips": "脂が極めて少ないため加熱しすぎに注意(レアまたは煮込みが基本)。下味に赤ワイン・日本酒・ハーブで臭み軽減。初心者はステーキ(ロース)・煮込み(スネ・モモ)から",
        "nutrition_highlight": "高タンパク・低脂質・低カロリー。ヘム鉄(吸収率良い)・亜鉛・ビタミンB12が豊富。「赤身肉の女王」と呼ばれる栄養価"
    },
    {
        "id": "boar",
        "name": "猪肉",
        "name_kana": "いのししにく",
        "name_en": "Wild Boar",
        "category": "game_meat",
        "category_label": "ジビエ",
        "subcategory": "",
        "color_theme": "#FCD0C0",
        "accent_color": "#9A3020",
        "season": ["11月", "12月", "1月", "2月"],
        "season_peak": "冬(脂のった旬)",
        "key_check": {
            "icon": "👀",
            "action": "脂と肉の境を見る",
            "judgment": "脂が白くくっきり = OK"
        },
        "ok_short": ["色:鮮ピンク赤", "脂:白くっきり", "弾力:あり", "獣臭:少"],
        "ng_short": ["色:暗赤", "脂:黄ばみ", "感触:軟", "獣臭:強"],
        "ok_points": [
            "肉色が鮮やかなピンク〜赤色",
            "脂が真っ白で、肉と境がくっきり分かれる",
            "弾力があり、押すと跳ね返る",
            "獣臭は少なく、脂は甘い香り(冬の脂のった個体)"
        ],
        "ng_points": [
            "色が暗い赤、変色・くすみがある",
            "脂が黄ばんでいる、ベタつく",
            "押すと柔らかすぎる、繊維が緩む",
            "強い獣臭(処理の悪さ・古さの兆候)"
        ],
        "summary_ok": "鮮ピンク・脂白・弾力",
        "summary_ng": "暗赤・脂黄・軟・獣臭",
        "storage": {
            "method": "冷凍が基本(豚肉と同じく寄生虫対策で生食 NG)",
            "duration": "冷凍で2〜3ヶ月",
            "tips": "解凍は冷蔵庫でゆっくり。中心まで完全加熱(75℃以上1分以上)が必須"
        },
        "usage_tips": "脂に旨味が凝縮、煮込みで真価発揮。定番=牡丹鍋(味噌仕立て)、薄切りはしゃぶしゃぶ・焼肉、ロースはステーキ。初心者は牡丹鍋から(脂と味噌で食べやすい)",
        "nutrition_highlight": "ビタミンB群(B1・B2・B12)豊富で疲労回復・代謝促進。亜鉛・鉄分も多い。脂は不飽和脂肪酸が多く豚肉より融点低い"
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
        print(f"  ADDED {spec['id']:>10}  {spec['name']}")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n  {added} added. Total: {len(data['items'])}")


if __name__ == '__main__':
    main()

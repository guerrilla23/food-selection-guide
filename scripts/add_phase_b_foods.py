#!/usr/bin/env python3
"""Phase B (23食材) を data/foods.json に追加."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 共通: 通年フィールド
ALL_MONTHS = [f"{m}月" for m in range(1, 13)]

FOODS = [
    # =================== 野菜 (9) ===================
    {
        "id": "garlic", "name": "ニンニク", "name_kana": "にんにく", "name_en": "Garlic",
        "category": "vegetable", "category_label": "野菜", "subcategory": "葉物・香味",
        "color_theme": "#F0E0C5", "accent_color": "#A07848",
        "season": ["5月", "6月", "7月"], "season_peak": "初夏",
        "key_check": {"icon": "🤲", "action": "握って固さ確認", "judgment": "硬く詰まる = OK"},
        "ok_short": ["皮:パリッ", "形:整う", "重さ:重い", "芽:なし"],
        "ng_short": ["皮:カラカラ", "中:スカ", "芽:伸び", "底:カビ"],
        "ok_points": [
            "皮がパリッと乾燥していてハリがある",
            "球が硬く、ずっしり詰まっている",
            "芽が出ていない、緑色の芽が見えない",
            "形が整っていて、片方が極端に小さくない"
        ],
        "ng_points": [
            "皮がスカスカ、剥がれかけている",
            "中に空洞ができ、軽い",
            "緑の芽が外に出ている",
            "底に青カビや黒い斑点がある"
        ],
        "summary_ok": "皮パリ・固い・芽なし",
        "summary_ng": "スカスカ・芽伸び・カビ",
        "storage": {"method": "風通しの良い冷暗所、湿気を避ける",
                    "duration": "常温で1〜2ヶ月", "tips": "ネットや新聞紙に包んで吊るすと長持ち"},
        "usage_tips": "切ってから空気に触れさせると香り強くなる。芽は苦味の原因なので除去推奨",
        "nutrition_highlight": "アリシン(免疫力UP)、ビタミンB1。疲労回復・風邪予防の定番"
    },
    {
        "id": "komatsuna", "name": "小松菜", "name_kana": "こまつな", "name_en": "Komatsuna",
        "category": "vegetable", "category_label": "野菜", "subcategory": "葉物",
        "color_theme": "#E0F0D0", "accent_color": "#5D8F3D",
        "season": ["11月", "12月", "1月", "2月"], "season_peak": "冬",
        "key_check": {"icon": "👀", "action": "葉先を見る", "judgment": "ピンと張る = OK"},
        "ok_short": ["葉:濃緑・ピン", "茎:しっかり", "切口:白", "ツヤ:あり"],
        "ng_short": ["葉:黄ばみ", "茎:萎れ", "切口:茶色", "斑点:黒"],
        "ok_points": [
            "葉が鮮やかな濃緑色で、葉先までピンと張る",
            "茎の付け根がしっかりして切り口が白い",
            "葉や茎にハリ・ツヤがある",
            "全体的にみずみずしい"
        ],
        "ng_points": [
            "葉が黄ばんで萎れている",
            "茎の切り口が茶色く乾燥またはベタつく",
            "黒い斑点や穴がある(虫食い・病気)",
            "全体的に元気がなく、しんなり"
        ],
        "summary_ok": "葉ピン・茎硬・切口白",
        "summary_ng": "葉黄ばみ・萎れ・斑点",
        "storage": {"method": "湿らせた新聞紙で包み立てて冷蔵",
                    "duration": "冷蔵で3〜4日", "tips": "冷凍保存可: 茹でて水気を絞って小分け"},
        "usage_tips": "アクが少なく下茹で不要(ホウレンソウより手軽)。生でもサラダで使える",
        "nutrition_highlight": "カルシウム・鉄分が豊富。ホウレンソウより多い。ビタミンK・C・βカロテン"
    },
    {
        "id": "lettuce", "name": "レタス", "name_kana": "れたす", "name_en": "Lettuce",
        "category": "vegetable", "category_label": "野菜", "subcategory": "葉物",
        "color_theme": "#E5F0CC", "accent_color": "#7BAB46",
        "season": ["4月", "5月", "6月", "7月", "8月", "9月"], "season_peak": "春〜秋",
        "key_check": {"icon": "🤲", "action": "持ち上げる", "judgment": "軽くフワッ = OK"},
        "ok_short": ["軽さ:フワッ", "葉:鮮緑", "巻き:緩い", "芯:白・小"],
        "ng_short": ["重い:ぎゅう詰", "葉:茶ばみ", "芯:赤い", "切口:茶"],
        "ok_points": [
            "持って軽い(巻きがフワッとして空気を含む)",
            "葉先が鮮やかな緑、ハリあり",
            "芯の切り口が白く10円玉程度のサイズ",
            "葉の重なりが緩く、隙間がある"
        ],
        "ng_points": [
            "重すぎる(成長しすぎ=苦味)",
            "葉先が茶色く萎れている",
            "芯の切り口が赤い・赤茶(古い)",
            "葉が黒ずんでいる、ベタつく"
        ],
        "summary_ok": "軽い・緑・芯白",
        "summary_ng": "重い・茶・芯赤",
        "storage": {"method": "芯をくり抜いて湿らせたペーパーを詰めポリ袋で冷蔵",
                    "duration": "冷蔵で1週間", "tips": "金属で切ると変色するので手でちぎる"},
        "usage_tips": "サラダはちぎる→冷水にさらす→水切り。加熱はサッと(食感命)",
        "nutrition_highlight": "水分豊富、カリウム・葉酸・βカロテン。低カロリーで満腹感"
    },
    {
        "id": "hakusai", "name": "白菜", "name_kana": "はくさい", "name_en": "Napa Cabbage",
        "category": "vegetable", "category_label": "野菜", "subcategory": "葉物",
        "color_theme": "#E5F0D0", "accent_color": "#7BAB46",
        "season": ["11月", "12月", "1月", "2月"], "season_peak": "冬",
        "key_check": {"icon": "🤲", "action": "持って重さ確認", "judgment": "ずっしり = OK"},
        "ok_short": ["重さ:ずっしり", "葉先:パリ", "切口:白", "葉:詰まる"],
        "ng_short": ["軽い:スカ", "葉先:萎れ", "切口:黒", "葉:離れ"],
        "ok_points": [
            "持って同サイズの中で重い(葉が詰まる)",
            "外葉が鮮やかな緑で葉先がパリッ",
            "切り口が白くツヤあり",
            "葉と葉の間がしっかり詰まっている"
        ],
        "ng_points": [
            "持って軽い(中身がスカスカ)",
            "葉先が萎れて黄ばんでいる",
            "切り口が黒く変色、ベタつく",
            "葉が外側に開いてバラバラ"
        ],
        "summary_ok": "重い・葉ピン・切口白",
        "summary_ng": "軽い・萎れ・切口黒",
        "storage": {"method": "丸ごとは新聞紙で包み冷暗所、カットはラップで冷蔵",
                    "duration": "丸ごと:2〜3週間 / カット:3〜5日",
                    "tips": "黒い斑点はゴマ症で味は問題なし。カット品は切り口にラップ密着"},
        "usage_tips": "外葉=炒め物・煮物、内葉=サラダ・浅漬け、芯=スープでだし",
        "nutrition_highlight": "ビタミンC、カリウム、食物繊維。鍋で煮込むと吸収UP"
    },
    {
        "id": "nasu", "name": "なす", "name_kana": "なす", "name_en": "Eggplant",
        "category": "vegetable", "category_label": "野菜", "subcategory": "果菜",
        "color_theme": "#E0D0E8", "accent_color": "#5D2A6F",
        "season": ["6月", "7月", "8月", "9月"], "season_peak": "夏",
        "key_check": {"icon": "👆", "action": "ヘタを触る", "judgment": "トゲがチクチク = OK"},
        "ok_short": ["色:濃紫・ツヤ", "ヘタ:トゲ鋭", "肌:ハリ", "重さ:ある"],
        "ng_short": ["色:ぼやけ", "ヘタ:萎れ", "肌:シワ", "感触:柔"],
        "ok_points": [
            "色が濃い紫色で全体にツヤがある",
            "ヘタ(緑)のトゲが鋭くチクチクする",
            "皮にハリがあり押すと跳ね返る",
            "持つとずっしり重く形が整う"
        ],
        "ng_points": [
            "色がぼやけて茶色がかる",
            "ヘタが乾燥してトゲが取れている",
            "皮にシワができ柔らかい",
            "持って軽い、変色した部分がある"
        ],
        "summary_ok": "濃紫・ツヤ・トゲ鋭",
        "summary_ng": "ぼやけ・シワ・柔",
        "storage": {"method": "1本ずつラップで包み冷蔵庫の野菜室",
                    "duration": "冷蔵で4〜5日",
                    "tips": "低温に弱い(10℃以下で傷み)。常温保存も可だが日持ち短"},
        "usage_tips": "切ったら水にさらしてアク抜き。皮ごと油で炒めるとアントシアニン効率UP",
        "nutrition_highlight": "ナスニン(抗酸化)、カリウム、食物繊維。皮の紫色に栄養豊富"
    },
    {
        "id": "piman", "name": "ピーマン", "name_kana": "ぴーまん", "name_en": "Green Pepper",
        "category": "vegetable", "category_label": "野菜", "subcategory": "果菜",
        "color_theme": "#E5F0D5", "accent_color": "#5D8F3D",
        "season": ["6月", "7月", "8月", "9月"], "season_peak": "夏",
        "key_check": {"icon": "👀", "action": "色とハリを見る", "judgment": "濃緑・凹まず = OK"},
        "ok_short": ["色:濃緑", "ヘタ:緑ピン", "肌:ハリ・ツヤ", "肉:厚い"],
        "ng_short": ["色:ぼやけ", "ヘタ:茶", "肌:シワ", "肉:薄"],
        "ok_points": [
            "色が濃く均一な緑色",
            "ヘタが鮮やかな緑、断面が瑞々しい",
            "皮にハリがあり、押すと凹まない",
            "肉厚でしっかりした重み"
        ],
        "ng_points": [
            "色がぼやけ、茶色がかる",
            "ヘタが乾燥して茶色",
            "シワが寄り、柔らかい",
            "肉薄で軽く、押すと凹む"
        ],
        "summary_ok": "濃緑・ハリ・肉厚",
        "summary_ng": "ぼやけ・シワ・薄",
        "storage": {"method": "ポリ袋に入れ野菜室",
                    "duration": "冷蔵で1週間", "tips": "1個ずつキッチンペーパーで包むとより長持ち"},
        "usage_tips": "苦味が苦手なら縦切り(繊維沿い)で柔らげる。種・ワタにも栄養あり",
        "nutrition_highlight": "ビタミンC(加熱に強い)、βカロテン、食物繊維"
    },
    {
        "id": "broccoli", "name": "ブロッコリー", "name_kana": "ぶろっこりー", "name_en": "Broccoli",
        "category": "vegetable", "category_label": "野菜", "subcategory": "花菜",
        "color_theme": "#D0E0BC", "accent_color": "#2C5F2D",
        "season": ["11月", "12月", "1月", "2月", "3月"], "season_peak": "冬",
        "key_check": {"icon": "👀", "action": "つぼみの色を見る", "judgment": "濃緑・密 = OK"},
        "ok_short": ["つぼみ:密・濃緑", "茎:切口瑞々", "重い:ずっしり", "色:紫がかる"],
        "ng_short": ["つぼみ:黄・開", "茎:空洞", "切口:茶", "色:くすみ"],
        "ok_points": [
            "つぼみが濃い緑色で密集している",
            "茎の切り口が瑞々しく白い",
            "持つとずっしり重く、形がコンパクト",
            "紫がかる=甘み・栄養豊富(寒さで色付く)"
        ],
        "ng_points": [
            "つぼみが黄色く開いている(花咲き)",
            "茎が空洞、ス入り",
            "切り口が茶色、ベタつく",
            "全体的に色がくすむ"
        ],
        "summary_ok": "濃緑密・切口白・重い",
        "summary_ng": "黄花咲き・空洞・茶",
        "storage": {"method": "茎を下にしてラップで包み冷蔵",
                    "duration": "冷蔵で3〜4日", "tips": "茹でて小房に分け冷凍で1ヶ月"},
        "usage_tips": "茎にも栄養豊富。皮を厚めに剥いて使う。茹でるなら塩入り、レンジ加熱が栄養保持◎",
        "nutrition_highlight": "ビタミンC(レモンの2倍)、スルフォラファン(解毒)、食物繊維"
    },
    {
        "id": "ginger", "name": "生姜", "name_kana": "しょうが", "name_en": "Ginger",
        "category": "vegetable", "category_label": "野菜", "subcategory": "根菜",
        "color_theme": "#F0E0C5", "accent_color": "#A07848",
        "season": ["6月", "7月", "8月"], "season_peak": "夏(新生姜)",
        "key_check": {"icon": "👀", "action": "皮のハリを見る", "judgment": "ハリ・ツヤ = OK"},
        "ok_short": ["皮:薄・ツヤ", "肉:固・ハリ", "色:鮮黄", "香:強"],
        "ng_short": ["皮:シワ・乾", "肉:柔", "色:くすみ", "斑点:黒"],
        "ok_points": [
            "皮が薄くツヤがある",
            "肉がふくよかでハリ感",
            "全体が鮮やかな黄〜橙色",
            "香りが強い"
        ],
        "ng_points": [
            "皮にシワが寄り乾燥",
            "押すと柔らかい",
            "色がくすみ、黒い斑点",
            "断面に空洞や繊維質が目立つ"
        ],
        "summary_ok": "ハリ・ツヤ・香り強",
        "summary_ng": "シワ・柔・斑点",
        "storage": {"method": "湿らせた新聞紙で包み冷暗所か冷蔵",
                    "duration": "常温で1週間、冷蔵で3週間",
                    "tips": "冷凍はすりおろし or 薄切りで小分け、便利"},
        "usage_tips": "皮の近くに香り成分。皮ごと使うか薄く剥く。すりおろしは肉・魚の臭み消しに",
        "nutrition_highlight": "ジンゲロール(殺菌・抗炎症)、ショウガオール(温熱効果)。冷え性対策"
    },
    {
        "id": "pumpkin", "name": "かぼちゃ", "name_kana": "かぼちゃ", "name_en": "Pumpkin",
        "category": "vegetable", "category_label": "野菜", "subcategory": "果菜",
        "color_theme": "#D0E0BC", "accent_color": "#2C5F2D",
        "season": ["7月", "8月", "9月", "10月"], "season_peak": "夏〜秋",
        "key_check": {"icon": "👀", "action": "ヘタを見る", "judgment": "コルク状 = OK"},
        "ok_short": ["ヘタ:太・コルク", "皮:硬・凹凸", "切口:橙・濃", "重さ:ずっしり"],
        "ng_short": ["ヘタ:青・湿", "皮:柔", "切口:薄橙", "種:空洞"],
        "ok_points": [
            "ヘタ(軸)が太くコルク状に乾燥",
            "皮が硬く凹凸がしっかり",
            "切り口が濃いオレンジ色",
            "種がしっかり詰まっている"
        ],
        "ng_points": [
            "ヘタが青く湿っている(若取り)",
            "皮が柔らかく打痕がある",
            "切り口が薄いオレンジ色",
            "種の周りに空洞=水っぽい"
        ],
        "summary_ok": "ヘタ太・橙濃・重い",
        "summary_ng": "ヘタ青・薄橙・空洞",
        "storage": {"method": "丸ごとは冷暗所、カットは種・ワタ除去後ラップで冷蔵",
                    "duration": "丸ごと:2〜3ヶ月 / カット:5〜7日",
                    "tips": "カットすると傷みが早い。冷凍保存は加熱後がおすすめ"},
        "usage_tips": "皮にも栄養。皮ごと煮ると煮崩れにくい。電子レンジ加熱で固い皮も楽に切れる",
        "nutrition_highlight": "βカロテン(抗酸化・粘膜保護)、ビタミンE、食物繊維。冬至に食べる風習"
    },

    # =================== きのこ (5) ===================
    {
        "id": "shiitake", "name": "椎茸", "name_kana": "しいたけ", "name_en": "Shiitake",
        "category": "mushroom", "category_label": "きのこ", "subcategory": "",
        "color_theme": "#E5D5B5", "accent_color": "#7E5A2A",
        "season": ["3月", "4月", "5月", "9月", "10月", "11月"], "season_peak": "春・秋",
        "key_check": {"icon": "👀", "action": "カサの裏を見る", "judgment": "ヒダ白 = OK"},
        "ok_short": ["カサ:内巻", "ヒダ:白", "肉:厚", "軸:太・固"],
        "ng_short": ["カサ:開く", "ヒダ:茶", "肉:薄", "湿気:多"],
        "ok_points": [
            "カサが内側に巻いている(肉厚の証)",
            "カサの裏のヒダが白く整っている",
            "軸が太く硬い(旨味豊富)",
            "全体に湿り気はあるがベタつかない"
        ],
        "ng_points": [
            "カサが開ききっている(花咲き=胞子放出後)",
            "ヒダが黒ずんでいる、湿る",
            "肉が薄く軽い",
            "ベタつき、変色"
        ],
        "summary_ok": "内巻き・ヒダ白・肉厚",
        "summary_ng": "開く・ヒダ茶・薄",
        "storage": {"method": "キッチンペーパーで包みポリ袋で冷蔵",
                    "duration": "冷蔵で4〜5日 / 干して天日干しなら1ヶ月",
                    "tips": "天日干しでビタミンD増。生干し30分でも効果あり"},
        "usage_tips": "石づき(根元)は固いので除去。軸も使える。乾椎茸は水戻しで旨味UP",
        "nutrition_highlight": "ビタミンD(骨)、エリタデニン(コレステロール抑制)、食物繊維"
    },
    {
        "id": "shimeji", "name": "しめじ", "name_kana": "しめじ", "name_en": "Shimeji",
        "category": "mushroom", "category_label": "きのこ", "subcategory": "",
        "color_theme": "#EDE5D8", "accent_color": "#9B8870",
        "season": ["9月", "10月", "11月"], "season_peak": "秋",
        "key_check": {"icon": "👀", "action": "株のまとまりを見る", "judgment": "ハリ・密 = OK"},
        "ok_short": ["株:密・固", "カサ:張", "軸:白", "色:均一"],
        "ng_short": ["株:バラけ", "カサ:開", "軸:茶", "湿:多"],
        "ok_points": [
            "株がしっかりまとまり、ハリがある",
            "カサが小ぶりで内巻き",
            "軸が真っ白でしっかり",
            "全体の色が均一"
        ],
        "ng_points": [
            "株がバラバラに崩れる",
            "カサが大きく開ききっている",
            "軸がベタつく・茶色",
            "湿気が多く、変色"
        ],
        "summary_ok": "株まとまり・ハリ・白",
        "summary_ng": "バラけ・開く・茶",
        "storage": {"method": "石づきを切らず、キッチンペーパーで包み冷蔵",
                    "duration": "冷蔵で4〜5日", "tips": "冷凍可: 小房に分けジップ袋で。旨味UP"},
        "usage_tips": "「香りまつたけ味しめじ」と言われるほど旨味豊富。汁物・炒め物・炊き込みに",
        "nutrition_highlight": "オルニチン(肝機能)、βグルカン(免疫)、ビタミンB群"
    },
    {
        "id": "enoki", "name": "エノキ", "name_kana": "えのき", "name_en": "Enoki",
        "category": "mushroom", "category_label": "きのこ", "subcategory": "",
        "color_theme": "#F0E8D0", "accent_color": "#B89870",
        "season": ["11月", "12月", "1月", "2月"], "season_peak": "冬",
        "key_check": {"icon": "👀", "action": "軸の色を見る", "judgment": "真っ白 = OK"},
        "ok_short": ["軸:真白", "カサ:小・整", "株:固", "袋:乾"],
        "ng_short": ["軸:黄", "カサ:開", "株:崩", "袋:水滴"],
        "ok_points": [
            "軸が真っ白でハリがある",
            "カサが小さく丸く整う",
            "株のお尻がしっかり詰まっている",
            "袋の中が乾燥している"
        ],
        "ng_points": [
            "軸が黄ばんでいる",
            "カサが開いて色が濃い",
            "株が崩れバラける",
            "袋に水滴(古い・劣化)"
        ],
        "summary_ok": "白・カサ整う・乾",
        "summary_ng": "黄・開・水滴",
        "storage": {"method": "袋ごと、または小分けで冷蔵",
                    "duration": "冷蔵で4〜5日", "tips": "冷凍で旨味UP+1ヶ月。石づき側を切らずに袋へ"},
        "usage_tips": "石づきを切って小房に分ける。鍋・汁物・ナムルに。食感命なので加熱は短く",
        "nutrition_highlight": "GABA(リラックス)、エノキタケリノール酸(脂肪抑制)、食物繊維"
    },
    {
        "id": "eringi", "name": "エリンギ", "name_kana": "えりんぎ", "name_en": "King Trumpet",
        "category": "mushroom", "category_label": "きのこ", "subcategory": "",
        "color_theme": "#F0E5D0", "accent_color": "#A07848",
        "season": ["9月", "10月", "11月", "12月"], "season_peak": "秋〜初冬",
        "key_check": {"icon": "👀", "action": "軸の太さを見る", "judgment": "太く真白 = OK"},
        "ok_short": ["軸:太・白", "カサ:薄茶", "肌:乾", "ハリ:あり"],
        "ng_short": ["軸:細・黄", "カサ:広", "肌:ベタ", "斑点:黒"],
        "ok_points": [
            "軸が太く真っ白でハリあり",
            "カサが薄茶で内巻き",
            "表面が乾燥していてベタつかない",
            "全体に弾力がある"
        ],
        "ng_points": [
            "軸が細く黄ばむ",
            "カサが大きく開ききっている",
            "表面がベタつく",
            "黒い斑点や変色"
        ],
        "summary_ok": "軸太・白・乾燥",
        "summary_ng": "細・黄・ベタ",
        "storage": {"method": "キッチンペーパーで包みポリ袋で冷蔵",
                    "duration": "冷蔵で1週間", "tips": "冷凍可: スライスしてジップ袋。料理にすぐ使える"},
        "usage_tips": "アワビのような食感が魅力。縦に裂くと繊維沿いで歯ごたえUP。グリル・バター焼きに",
        "nutrition_highlight": "ビタミンD、βグルカン、食物繊維。低カロリーでダイエット向き"
    },
    {
        "id": "maitake", "name": "舞茸", "name_kana": "まいたけ", "name_en": "Maitake",
        "category": "mushroom", "category_label": "きのこ", "subcategory": "",
        "color_theme": "#E5D5B5", "accent_color": "#5D4E37",
        "season": ["9月", "10月"], "season_peak": "秋",
        "key_check": {"icon": "👀", "action": "株の色を見る", "judgment": "深茶・肉厚 = OK"},
        "ok_short": ["株:固・密", "色:濃茶", "肉:厚", "香:強"],
        "ng_short": ["株:崩", "色:くすみ", "肉:薄", "湿:多"],
        "ok_points": [
            "株がしっかりまとまり、密度がある",
            "色が深い茶色で均一",
            "カサ(花びら状)が肉厚",
            "香りが強く、芳ばしい"
        ],
        "ng_points": [
            "株がバラバラに崩れる",
            "色がくすむ・部分的に黒ずむ",
            "カサが薄く、軽い",
            "湿気が多く、ベタつく"
        ],
        "summary_ok": "株固・濃茶・肉厚",
        "summary_ng": "バラけ・くすみ・湿",
        "storage": {"method": "キッチンペーパーで包みポリ袋で冷蔵",
                    "duration": "冷蔵で4〜5日", "tips": "冷凍で旨味増。手で割いて小分け"},
        "usage_tips": "天ぷら・炊き込みご飯・ホイル焼きで香り活きる。タンパク質分解酵素ありで肉も柔らかく",
        "nutrition_highlight": "βグルカン(免疫力UP)、ビタミンD、ナイアシン。「舞い踊るほど嬉しい」が名前の由来"
    },

    # =================== 果物 (9) ===================
    {
        "id": "mikan", "name": "みかん", "name_kana": "みかん", "name_en": "Mandarin",
        "category": "fruit", "category_label": "果物", "subcategory": "柑橘",
        "color_theme": "#FFE5C8", "accent_color": "#FF8C42",
        "season": ["11月", "12月", "1月", "2月"], "season_peak": "冬",
        "key_check": {"icon": "👀", "action": "ヘタの大きさを見る", "judgment": "小さい・緑 = 甘い"},
        "ok_short": ["色:濃橙", "皮:薄・ハリ", "ヘタ:小・緑", "重さ:ずっしり"],
        "ng_short": ["色:くすみ", "皮:浮く", "ヘタ:大・茶", "感触:柔"],
        "ok_points": [
            "色が濃いオレンジ色で均一",
            "皮が薄く、ハリ・ツヤがある",
            "ヘタが小さく、軸が緑色(甘い品種の証)",
            "持つとずっしり重い(果汁多)"
        ],
        "ng_points": [
            "色がくすんでいる、凹みあり",
            "皮と実の間に隙間(浮皮)",
            "ヘタが大きく茶色く乾燥",
            "押すと柔らかすぎる"
        ],
        "summary_ok": "濃橙・薄皮・ヘタ小",
        "summary_ng": "くすみ・浮皮・ヘタ茶",
        "storage": {"method": "風通しの良い冷暗所、ヘタを下にして",
                    "duration": "常温で1〜2週間",
                    "tips": "傷んだ1個から広がるので、こまめにチェック。冷蔵すると甘み減"},
        "usage_tips": "白い筋(アルベド)に栄養。皮の内側にも栄養豊富。皮ごと焼くとマーマレード風",
        "nutrition_highlight": "ビタミンC、βクリプトキサンチン(骨・肌)、シネフリン(代謝)"
    },
    {
        "id": "lemon", "name": "レモン", "name_kana": "れもん", "name_en": "Lemon",
        "category": "fruit", "category_label": "果物", "subcategory": "柑橘",
        "color_theme": "#FFF5C8", "accent_color": "#F2C232",
        "season": ["10月", "11月", "12月", "1月", "2月", "3月"], "season_peak": "冬",
        "key_check": {"icon": "🤲", "action": "持って重さ確認", "judgment": "ずっしり = OK"},
        "ok_short": ["色:濃黄", "皮:ハリ・凹凸", "重さ:重い", "ツヤ:あり"],
        "ng_short": ["色:くすみ", "皮:シワ", "感触:柔", "斑点:茶"],
        "ok_points": [
            "色が濃い黄色で均一",
            "皮にハリがあり、細かい凹凸が均一",
            "持つとずっしり重い(果汁多)",
            "全体にツヤがある"
        ],
        "ng_points": [
            "色がくすむ、緑がかる(未熟)",
            "皮にシワが寄っている",
            "押すと柔らかい(水分抜け)",
            "茶色い斑点や打痕"
        ],
        "summary_ok": "濃黄・ハリ・重い",
        "summary_ng": "くすみ・シワ・柔",
        "storage": {"method": "ポリ袋で冷蔵",
                    "duration": "冷蔵で2〜3週間", "tips": "輪切りにして冷凍も可"},
        "usage_tips": "皮にも香りと栄養豊富(無農薬・国産推奨)。塩レモンで保存性UP",
        "nutrition_highlight": "ビタミンC(柑橘で最多)、クエン酸(疲労回復)、ヘスペリジン(血流)"
    },
    {
        "id": "avocado", "name": "アボカド", "name_kana": "あぼかど", "name_en": "Avocado",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#D5E8C0", "accent_color": "#4A7C2E",
        "season": ALL_MONTHS, "season_peak": "通年",
        "key_check": {"icon": "👆", "action": "軽く押す", "judgment": "弾力あり = 食べ頃"},
        "ok_short": ["皮:暗緑〜黒", "感触:弾力", "ヘタ:付く", "形:整う"],
        "ng_short": ["皮:鮮緑(硬)", "ブヨ:過熟", "ヘタ:取れる", "黒:過熟"],
        "ok_points": [
            "皮が暗緑〜黒色になっている(完熟)",
            "軽く押して弾力がある(食べ頃)",
            "ヘタが取れていない(新鮮)",
            "形が整いハリがある"
        ],
        "ng_points": [
            "皮が黒く部分的にブヨブヨ(過熟)",
            "皮が鮮やかな緑色で硬い(未熟)",
            "ヘタが取れて穴が黒い(劣化)",
            "大きな黒い斑点(傷み)"
        ],
        "summary_ok": "暗緑〜黒・弾力・整う",
        "summary_ng": "硬(未熟)・ブヨ・黒",
        "storage": {"method": "未熟は常温(りんごと一緒で早く熟す)、完熟は冷蔵",
                    "duration": "完熟:冷蔵で2〜3日",
                    "tips": "切ってからレモン汁で変色防止。種付きで保存"},
        "usage_tips": "切る向きは縦半分→種を取る→皮を剥く。包丁が滑りやすいので種は手で取る",
        "nutrition_highlight": "オレイン酸(良質脂質)、ビタミンE、食物繊維。世界一栄養価高い果物"
    },
    {
        "id": "ichigo", "name": "いちご", "name_kana": "いちご", "name_en": "Strawberry",
        "category": "fruit", "category_label": "果物", "subcategory": "ベリー",
        "color_theme": "#FFE5E0", "accent_color": "#E33825",
        "season": ["12月", "1月", "2月", "3月", "4月", "5月"], "season_peak": "春",
        "key_check": {"icon": "👀", "action": "ヘタの色を見る", "judgment": "鮮緑・反る = OK"},
        "ok_short": ["色:鮮赤", "ヘタ:緑・反", "ハリ:あり", "種:浮く"],
        "ng_short": ["色:暗赤", "ヘタ:茶・萎", "感触:柔", "種:沈"],
        "ok_points": [
            "色が鮮やかな赤(品種により濃淡)",
            "ヘタが鮮やかな緑色で反り返る(完熟)",
            "皮にハリ・ツヤがある",
            "種が表面に浮いて見える(成熟)"
        ],
        "ng_points": [
            "色が暗く部分的にしわしわ",
            "ヘタが茶色く萎れている",
            "皮が柔らかい(過熟)",
            "種が表面に沈んで凹む"
        ],
        "summary_ok": "鮮赤・ヘタ反・ハリ",
        "summary_ng": "暗赤・ヘタ茶・柔",
        "storage": {"method": "ヘタ付きのまま洗わずパックで冷蔵",
                    "duration": "冷蔵で2〜3日(早めに食べる)",
                    "tips": "洗うのは食べる直前。冷凍も可(スムージーに)"},
        "usage_tips": "ヘタを取ってから洗うと栄養流出。先端の方が甘い。練乳・砂糖は控えめでも美味",
        "nutrition_highlight": "ビタミンC(7〜8粒で1日分)、葉酸、アントシアニン"
    },
    {
        "id": "kiwi", "name": "キウイ", "name_kana": "きうい", "name_en": "Kiwi",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#E5D5B0", "accent_color": "#7E5A2A",
        "season": ["10月", "11月", "12月", "1月", "2月", "3月", "4月"], "season_peak": "冬",
        "key_check": {"icon": "👆", "action": "軽く押す", "judgment": "わずかに弾力 = OK"},
        "ok_short": ["皮:毛・均一", "感触:弾力", "形:整う", "ヘタ:乾"],
        "ng_short": ["皮:カビ", "感触:ブヨ", "形:歪", "皮:傷"],
        "ok_points": [
            "うぶ毛が均一に生えている",
            "軽く押すとわずかに弾力(食べ頃)",
            "形が整い、傷がない",
            "ヘタ部分が乾燥している"
        ],
        "ng_points": [
            "毛が抜けてカビが生える",
            "押してブヨブヨ(過熟・腐敗)",
            "硬すぎる(未熟・酸っぱい)",
            "皮に大きな傷や凹み"
        ],
        "summary_ok": "毛均一・軽弾力",
        "summary_ng": "カビ・ブヨ・傷",
        "storage": {"method": "未熟は常温で追熟、完熟は冷蔵",
                    "duration": "冷蔵で1〜2週間",
                    "tips": "りんごと一緒で追熟早い。逆に硬くしたいなら離す"},
        "usage_tips": "皮も食べられる(スプーンですくうのが一般的)。タンパク質分解酵素で肉柔らかく",
        "nutrition_highlight": "ビタミンC・E、食物繊維、アクチニジン(消化促進)"
    },
    {
        "id": "grape", "name": "ぶどう", "name_kana": "ぶどう", "name_en": "Grape",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#E5D5E5", "accent_color": "#5D2A6F",
        "season": ["8月", "9月", "10月"], "season_peak": "秋",
        "key_check": {"icon": "👀", "action": "白い粉(ブルーム)を確認", "judgment": "粉あり = 新鮮"},
        "ok_short": ["粉:あり", "実:密・固", "軸:緑・固", "色:深"],
        "ng_short": ["粉:なし", "実:落ちる", "軸:茶・乾", "色:薄"],
        "ok_points": [
            "白い粉(ブルーム)がついている(新鮮の証)",
            "実が密集、しっかり固い",
            "軸が緑色で硬く生き生き",
            "色が深く均一"
        ],
        "ng_points": [
            "白い粉が落ち、皮にツヤ過ぎる",
            "触ると実がボロっと落ちる",
            "軸が茶色く乾燥",
            "色がムラ、薄い部分がある"
        ],
        "summary_ok": "粉・実密・軸緑",
        "summary_ng": "粉なし・落・軸茶",
        "storage": {"method": "洗わずポリ袋で冷蔵",
                    "duration": "冷蔵で3〜5日", "tips": "粒を1つずつ軸を残してハサミで切ると傷みにくい"},
        "usage_tips": "皮にもポリフェノール豊富。皮ごと食べる品種(シャインマスカット等)が増えている",
        "nutrition_highlight": "ポリフェノール(抗酸化)、ブドウ糖(即エネルギー)、カリウム"
    },
    {
        "id": "peach", "name": "桃", "name_kana": "もも", "name_en": "Peach",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#FFE5DC", "accent_color": "#F8AAA0",
        "season": ["6月", "7月", "8月", "9月"], "season_peak": "夏",
        "key_check": {"icon": "👃", "action": "香りを嗅ぐ", "judgment": "甘い香り = 食べ頃"},
        "ok_short": ["香:甘", "色:均一", "ハリ:あり", "うぶ毛:均"],
        "ng_short": ["香:なし", "色:ムラ", "感触:硬orブヨ", "打痕:あり"],
        "ok_points": [
            "甘い香りが漂う(食べ頃)",
            "色が均一でハリがある",
            "うぶ毛(白い細毛)が均一に生える",
            "ヘタ周辺に白い果汁の跡(完熟)"
        ],
        "ng_points": [
            "香りがしない(未熟)",
            "色のムラ、打痕がある",
            "硬すぎ(未熟)or ブヨブヨ(過熟)",
            "黒い斑点や腐敗"
        ],
        "summary_ok": "甘香・色均・ハリ",
        "summary_ng": "無香・ムラ・打痕",
        "storage": {"method": "常温で食べ頃まで追熟、完熟は冷蔵で短時間",
                    "duration": "常温:2〜3日、冷蔵で短期(風味落ちる)",
                    "tips": "食べる2〜3時間前に冷蔵で適温に"},
        "usage_tips": "皮ごと食べると栄養UP。皮を剥く時は熱湯30秒→冷水でツルッと",
        "nutrition_highlight": "ペクチン(腸内環境)、カリウム、カテキン(抗酸化)"
    },
    {
        "id": "kaki", "name": "柿", "name_kana": "かき", "name_en": "Persimmon",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#FFE5C8", "accent_color": "#FF8C42",
        "season": ["9月", "10月", "11月"], "season_peak": "秋",
        "key_check": {"icon": "👀", "action": "ヘタを見る", "judgment": "ぴったり張付 = 甘"},
        "ok_short": ["色:濃橙", "ハリ:あり", "ヘタ:張・緑", "重さ:ずっしり"],
        "ng_short": ["色:くすみ", "感触:ブヨ", "ヘタ:浮", "斑点:黒"],
        "ok_points": [
            "色が濃いオレンジ色で均一",
            "皮にハリ・ツヤがある",
            "ヘタが緑で実にぴったり張り付く(甘柿)",
            "持つとずっしり重い"
        ],
        "ng_points": [
            "色がくすむ、部分的に黒ずむ",
            "ブヨブヨして柔らかすぎ",
            "ヘタと実の間に隙間(渋柿の可能性)",
            "黒い斑点や打痕"
        ],
        "summary_ok": "濃橙・ハリ・ヘタ張",
        "summary_ng": "くすみ・ブヨ・隙間",
        "storage": {"method": "ヘタを下にしてポリ袋で冷蔵",
                    "duration": "冷蔵で1〜2週間",
                    "tips": "渋柿は焼酎で渋抜き or ヘタにアルコール塗布で1週間"},
        "usage_tips": "完熟前=シャキッ、完熟=トロ。皮にも栄養。種の周りにアセトアルデヒドで二日酔い対策にも",
        "nutrition_highlight": "ビタミンC(みかんの2倍)、βクリプトキサンチン、タンニン。「医者いらず」"
    },
    {
        "id": "pear", "name": "梨", "name_kana": "なし", "name_en": "Pear",
        "category": "fruit", "category_label": "果物", "subcategory": "",
        "color_theme": "#F0E5D0", "accent_color": "#A07848",
        "season": ["8月", "9月", "10月"], "season_peak": "秋",
        "key_check": {"icon": "🤲", "action": "持って重さ確認", "judgment": "ずっしり = OK"},
        "ok_short": ["皮:ハリ・ツヤ", "形:整・丸", "重さ:ずっしり", "尻:ゴワゴワ"],
        "ng_short": ["皮:シワ・茶", "感触:柔", "軽い", "斑点:茶"],
        "ok_points": [
            "皮にハリ・ツヤがある",
            "形が整って丸く、傷がない",
            "ずっしり重く果汁多い",
            "お尻(花落ち)がゴワゴワ=糖度高"
        ],
        "ng_points": [
            "皮にシワや茶色斑点",
            "押すと柔らかい(過熟・水分抜け)",
            "持って軽い",
            "打痕や腐敗"
        ],
        "summary_ok": "ハリ・丸・重い",
        "summary_ng": "シワ・柔・軽",
        "storage": {"method": "ポリ袋で冷蔵",
                    "duration": "冷蔵で1週間程度",
                    "tips": "切ったらレモン汁で変色防止"},
        "usage_tips": "皮にも栄養。冷やしすぎると風味落ちる。コンポート・サラダで生かす食感",
        "nutrition_highlight": "アスパラギン酸(疲労回復)、カリウム、食物繊維、ソルビトール(便通)"
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

    print(f"\n  {added} added. Total items: {len(data['items'])}")


if __name__ == '__main__':
    main()

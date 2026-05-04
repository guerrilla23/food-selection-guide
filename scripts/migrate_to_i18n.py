#!/usr/bin/env python3
"""
foods.json と foods_template.json のテキストフィールドを {ja, en} 構造に変換。

【変換対象 (テキスト)】
  - name, category_label, subcategory, season_peak
  - summary_ok, summary_ng, usage_tips, nutrition_highlight
  - key_check.action, key_check.judgment
  - storage.method, storage.duration, storage.tips

【変換対象 (配列)】
  - ok_short, ng_short, ok_points, ng_points

【変換しない (言語非依存)】
  - id, name_en, name_kana
  - color_theme, accent_color
  - season (配列、'X月' フォーマット)
  - category, key_check.icon

冪等性: 既に {ja, en} 形式の値はスキップ (再実行可能)。
英訳は空文字 '' or 空配列 [] で初期化 (フォールバックロジックで ja に解決)。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


TEXT_FIELDS = [
    'name', 'category_label', 'subcategory', 'season_peak',
    'summary_ok', 'summary_ng', 'usage_tips', 'nutrition_highlight',
]
ARRAY_FIELDS = ['ok_short', 'ng_short', 'ok_points', 'ng_points']
KEY_CHECK_TEXT = ['action', 'judgment']
STORAGE_FIELDS = ['method', 'duration', 'tips']


def is_already_migrated(value):
    return isinstance(value, dict) and 'ja' in value and 'en' in value


def wrap_text(value):
    if is_already_migrated(value):
        return value
    return {'ja': value if isinstance(value, str) else '', 'en': ''}


def wrap_array(value):
    if is_already_migrated(value):
        return value
    return {'ja': value if isinstance(value, list) else [], 'en': []}


def migrate_item(item):
    """1食材分を変換。"""
    for fld in TEXT_FIELDS:
        if fld in item:
            item[fld] = wrap_text(item[fld])
    for fld in ARRAY_FIELDS:
        if fld in item:
            item[fld] = wrap_array(item[fld])

    if 'key_check' in item and isinstance(item['key_check'], dict):
        kc = item['key_check']
        for sub in KEY_CHECK_TEXT:
            if sub in kc:
                kc[sub] = wrap_text(kc[sub])

    if 'storage' in item and isinstance(item['storage'], dict):
        st = item['storage']
        for sub in STORAGE_FIELDS:
            if sub in st:
                st[sub] = wrap_text(st[sub])


def migrate_file(path, items_key='items'):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if items_key not in data:
        print(f'  SKIP {path} (no items)')
        return
    n = 0
    for item in data[items_key]:
        migrate_item(item)
        n += 1
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'  MIGRATED {path}: {n} items')


def main():
    targets = [
        os.path.join(ROOT, 'data', 'foods.json'),
        os.path.join(ROOT, 'data', 'foods_template.json'),
    ]
    for p in targets:
        if not os.path.exists(p):
            print(f'  SKIP {p} (not found)', file=sys.stderr)
            continue
        migrate_file(p)


if __name__ == '__main__':
    main()

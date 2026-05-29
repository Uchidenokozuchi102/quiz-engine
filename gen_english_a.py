#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中1英単語「きほんドリル」(english-a-2026-05.json) 生成スクリプト。
頻度優先で「絶対に使う語」をコアセットにし、英→日／日→英の段階式に組む。
- hint = ローマ字読み（覚え方）。本物の発音は say(=英単語) を 🔊 で再生。
- 4択の誤答は pool からエンジンが自動生成（同カテゴリ・打ち間違い防止）。
単語を足したいときは各 tier に (英語, 意味, 覚え方ローマ字読み) を1行足すだけ。
"""
import json
import os

# (英語, 意味, 覚え方=ローマ字読み)
tier1 = [  # きほん：人称・be動詞・do・つなぎ・最頻出
    ("I", "私は", "アイ"),
    ("you", "あなた（たち）", "ユー"),
    ("he", "彼は", "ヒー"),
    ("she", "彼女は", "シー"),
    ("we", "私たちは", "ウィー"),
    ("my", "私の", "マイ"),
    ("your", "あなたの", "ユア"),
    ("am", "〜です（I のとき）", "アム"),
    ("is", "〜です（he/she/it のとき）", "イズ"),
    ("are", "〜です（you/we/they のとき）", "アー"),
    ("do", "する／（疑問文をつくる）", "ドゥ"),
    ("not", "〜ない", "ノット"),
    ("yes", "はい", "イエス"),
    ("no", "いいえ", "ノー"),
    ("a", "1つの", "ア"),
    ("the", "その", "ザ"),
    ("this", "これ", "ジス"),
    ("that", "あれ", "ザット"),
    ("and", "〜と…", "アンド"),
    ("but", "しかし", "バット"),
    ("can", "〜できる", "キャン"),
    ("here", "ここに", "ヒア"),
    ("like", "〜が好きだ", "ライク"),
    ("have", "持っている", "ハヴ"),
]

tier2 = [  # よく使う動詞・形容詞
    ("want", "〜がほしい", "ウォント"),
    ("make", "作る", "メイク"),
    ("play", "（スポーツを）する", "プレイ"),
    ("read", "読む", "リード"),
    ("see", "見える／わかる", "シー"),
    ("watch", "（注意して）見る", "ウォッチ"),
    ("meet", "会う", "ミート"),
    ("take", "取る", "テイク"),
    ("think", "考える", "シンク"),
    ("run", "走る", "ラン"),
    ("sing", "歌う", "シング"),
    ("draw", "（絵を）かく", "ドロー"),
    ("love", "大好きである", "ラブ"),
    ("call", "呼ぶ", "コール"),
    ("good", "よい", "グッド"),
    ("nice", "すてきな", "ナイス"),
    ("new", "新しい", "ニュー"),
    ("cool", "かっこいい", "クール"),
    ("cute", "かわいい", "キュート"),
    ("great", "すばらしい", "グレート"),
    ("strong", "強い", "ストロング"),
    ("hot", "暑い／熱い", "ホット"),
    ("white", "白い", "ホワイト"),
    ("black", "黒い", "ブラック"),
    ("red", "赤い", "レッド"),
]

nums = [  # 数字（絶対に使う）
    ("zero", "0", "ゼロ"),
    ("one", "1", "ワン"),
    ("two", "2", "トゥー"),
    ("three", "3", "スリー"),
    ("four", "4", "フォー"),
    ("five", "5", "ファイブ"),
    ("six", "6", "シックス"),
    ("seven", "7", "セブン"),
    ("eight", "8", "エイト"),
    ("nine", "9", "ナイン"),
    ("ten", "10", "テン"),
    ("eleven", "11", "イレブン"),
    ("twelve", "12", "トゥエルブ"),
    ("thirteen", "13", "サーティーン"),
    ("twenty", "20", "トゥエンティ"),
    ("hundred", "100", "ハンドレッド"),
]


def e2j_mode(label, icon, desc, words):
    """英語を見て意味を選ぶ。英単語が見えているので🔊ボタンも出す(sayPrompt)。"""
    pool = [m for (_, m, _) in words]
    qs = []
    for (en, jp, ro) in words:
        qs.append({
            "jp": en,
            "hint": "発音：" + ro,
            "say": en,
            "sayPrompt": True,
            "pool": pool,
            "answer": jp,
        })
    return {"label": label, "icon": icon, "description": desc, "questions": qs}


def j2e_mode(label, icon, desc, words):
    """意味を見て英語を選ぶ。答えを先にバラさないため🔊は回答後のみ(sayPromptなし)。"""
    pool = [en for (en, _, _) in words]
    qs = []
    for (en, jp, ro) in words:
        qs.append({
            "jp": jp,
            "hint": "発音：" + ro,
            "say": en,
            "pool": pool,
            "answer": en,
        })
    return {"label": label, "icon": icon, "description": desc, "questions": qs}


data = {
    "title": "中1 英単語 きほんドリル",
    "subtitle": "よく使う単語から覚えよう｜🔊音声つき",
    "icon": "📗",
    "modes": {
        "core1_e2j": e2j_mode("① きほんの単語　英→日", "📗", "", tier1),
        "core1_j2e": j2e_mode("② きほんの単語　日→英", "📙", "", tier1),
        "core2_e2j": e2j_mode("③ よく使う語　英→日", "📗", "", tier2),
        "core2_j2e": j2e_mode("④ よく使う語　日→英", "📙", "", tier2),
        "num_e2j": e2j_mode("⑤ 数字　英→日", "🔢", "", nums),
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "english-a-2026-05.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = sum(len(m["questions"]) for m in data["modes"].values())
distinct = len(tier1) + len(tier2) + len(nums)
print("=== 生成完了 ===")
print("出力:", out)
print("モード数:", len(data["modes"]), "／ 総問題数:", total, "／ 異なり語数:", distinct)

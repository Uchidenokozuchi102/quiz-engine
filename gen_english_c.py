#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""english-c-2026-06.json generator (key: en-c)
中1 英語 期末対策 P22〜41（ゆめちゃん用・別の学校）。
v1方針（2026-06-21）: 範囲が海輝君(P20〜33)と被るため、海輝君の en-b セットを流用して
  ゆめちゃんの P22〜33 をカバーする第1版。P34〜41 と本物の単語プリントは授業後に追加・精密化する。
  音声は en-b の既存MP3を再利用する（同じ単語＝同じ発音なので aud() は /audio/en-b/ のまま）。
方針（2026-06-19 オーナー要望で改訂）:
  単語が苦手な生徒向けに「覚える価値の高い語」へ絞り、動詞・形容詞を最優先にする。
  - 削除: 固有名詞(Canada/America/China/May)、代名詞の短縮形(he's等8語)、
          前置詞(on/at/for)、基本機能語(our/your/it/that/the/he/she/what/who/oops)、
          ほぼ既知の易語(book/day/juice/cheese/e-mail/Thank you./You're welcome./Here you are.)
  - 並び: ①動詞 ②形容詞 を先頭に置き優先学習。③名詞 ④副詞・表現。
  - ⑤仕上げ: 動詞・形容詞だけ「日→英(書き)」＋まちがえやすい語の2択。
忠実性メモ: 意味は印刷のとおり。長い注釈ラベル(【所属】[正式名称…]等)は可読性のため省略。
  family は印刷表記どおり「一族」。
"""
import json, os, re


def slug(s):
    """say文字列 → 音声ファイル名スラッグ（英小文字と数字、区切りは_）"""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def aud(say):
    return "/audio/en-b/" + slug(say) + ".mp3"

# (English, 日本語の意味, TTS読み上げ)
verbs = [   # 動詞・助動詞（最優先）
    ("can", "…することができる", "can"),
    ("cannot", "…できない", "cannot"),
    ("make", "…を作る、得る", "make"),
    ("read", "（…を）読む、読んで知る", "read"),
    ("see", "（…が）わかる、理解する", "see"),
    ("excuse", "…を許す", "excuse"),
    ("thank", "…に感謝する", "thank"),
    ("are", "（…に）いる、ある", "are"),
    ("cook", "（…を）料理する", "cook"),
    ("drink", "…を飲む", "drink"),
    ("speak", "（ある言語）を話す", "speak"),
]

adjs = [    # 形容詞（最優先）
    ("new", "新しい、新任の", "new"),
    ("cool", "かっこいい", "cool"),
    ("good", "じょうずな、うまい", "good"),
    ("English", "英語の、英語で書かれた", "English"),
    ("Chinese", "中国の", "Chinese"),
    ("some", "いくつかの、いくらかの、少しの", "some"),
    ("welcome", "歓迎される", "welcome"),
    ("interesting", "おもしろい、興味深い", "interesting"),
    ("favorite", "いちばん好きな、お気に入りの", "favorite"),
    ("brave", "勇かんな、勇ましい", "brave"),
    ("kind", "親切な、やさしい", "kind"),
    ("rainy", "雨の、雨の多い", "rainy"),
    ("green", "緑（の）", "green"),
    ("blue", "青（い）", "blue"),
]

nouns = [   # 名詞
    ("class", "学級、組、クラス", "class"),
    ("team", "チーム、組", "team"),
    ("food", "食べ物", "food"),
    ("father", "父、お父さん", "father"),
    ("teacher", "先生、教師", "teacher"),
    ("bird", "鳥", "bird"),
    ("parent(s)", "親、親たち、両親", "parents"),
    ("tea", "茶、紅茶", "tea"),
    ("rain", "雨", "rain"),
    ("glue", "接着剤、のり", "glue"),
    ("fruit", "果物、果実", "fruit"),
    ("beef", "牛肉", "beef"),
    ("sea", "海、海洋", "sea"),
    ("season", "季節", "season"),
    ("peach", "モモ", "peach"),
    ("beach", "浜、海辺、ビーチ", "beach"),
    ("room", "部屋", "room"),
    ("classroom", "教室", "classroom"),
    ("swimming pool", "（水泳用の）プール", "swimming pool"),
    ("cooking", "料理、料理法", "cooking"),
    ("textbook", "教科書", "textbook"),
    ("notebook", "ノート", "notebook"),
    ("green tea", "緑茶", "green tea"),
    ("symbol", "シンボル、象徴、記号", "symbol"),
    ("family", "一族", "family"),
    ("character", "登場人物", "character"),
    ("train", "列車、電車", "train"),
    ("zoo", "動物園", "zoo"),
]

advs = [    # 副詞・会話表現
    ("very", "非常に、とても、あまり（…でない）", "very"),
    ("well", "じょうずに、うまく、よく", "well"),
    ("really", "本当ですか、へえ、そうなんだ", "really"),
    ("usually", "たいてい、ふつう", "usually"),
    ("today", "今日（は）、現在では", "today"),
    ("also", "…もまた、そのうえ", "also"),
    ("why", "なぜ、どうして", "why"),
    ("I see.", "なるほど。わかった。", "I see"),
    ("Excuse me.", "すみません。失礼ですが。", "Excuse me"),
    ("be good at (...ing)", "（…することが）じょうずだ、得意だ", "be good at"),
]

# ひっかけ2択: (英語, 正しい意味, まぎらわしい誤答, TTS) ※全て上の収録語から
traps = [
    ("can", "…することができる", "…できない", "can"),
    ("cannot", "…できない", "…することができる", "cannot"),
    ("rain", "雨", "雨の、雨の多い", "rain"),
    ("rainy", "雨の、雨の多い", "雨", "rainy"),
    ("cook", "（…を）料理する", "料理、料理法", "cook"),
    ("cooking", "料理、料理法", "（…を）料理する", "cooking"),
    ("tea", "茶、紅茶", "海、海洋", "tea"),
    ("sea", "海、海洋", "茶、紅茶", "sea"),
    ("peach", "モモ", "浜、海辺、ビーチ", "peach"),
    ("beach", "浜、海辺、ビーチ", "モモ", "beach"),
    ("textbook", "教科書", "ノート", "textbook"),
    ("notebook", "ノート", "教科書", "notebook"),
]


def e2j(items):  # 英→日（意味えらび）出題時に音声
    pool = [ja for _, ja, _ in items]
    return [{"jp": en, "say": say, "audio": aud(say), "sayPrompt": True, "pool": pool, "answer": ja}
            for en, ja, say in items]


def j2e(items):  # 日→英（英語えらび）回答後に音声
    pool = [en for en, _, _ in items]
    return [{"jp": ja, "say": say, "audio": aud(say), "pool": pool, "answer": en}
            for en, ja, say in items]


trap_q = [{"jp": en, "say": say, "audio": aud(say), "sayPrompt": True, "choices": [corr, wrong], "answer": corr}
          for en, corr, wrong, say in traps]

# ⑤ 仕上げ: 動詞・形容詞の日→英（書きの確認）＋ ひっかけ2択
review_q = j2e(verbs + adjs) + trap_q

data = {
    "title": "英語 P22〜41 期末対策",
    "subtitle": "中1 重要単語にしぼって（まずはP22〜33）｜🔊音声つき",
    "icon": "📖",
    "modes": {
        "verb": {"label": "① 動詞（最優先）", "icon": "🏃",
                 "description": "", "questions": e2j(verbs)},
        "adj": {"label": "② 形容詞（最優先）", "icon": "🎨",
                "description": "", "questions": e2j(adjs)},
        "noun": {"label": "③ 名詞", "icon": "📦",
                 "description": "", "questions": e2j(nouns)},
        "adv": {"label": "④ 副詞・会話表現", "icon": "💬",
                "description": "", "questions": e2j(advs)},
        "review": {"label": "⑤ 仕上げ（書き＋ひっかけ）", "icon": "🎯",
                   "description": "", "questions": review_q},
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "english-c-2026-06.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = len(verbs) + len(adjs) + len(nouns) + len(advs)
print("written:", out)
print(f"単語: 動詞{len(verbs)} 形容詞{len(adjs)} 名詞{len(nouns)} 副詞・表現{len(advs)} = 計{total}語")
print(f"⑤仕上げ: 日→英{len(verbs)+len(adjs)} + ひっかけ{len(trap_q)} = {len(review_q)}問")

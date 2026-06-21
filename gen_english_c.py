#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""english-c-2026-06.json generator (key: en-c)
中1 英語 期末対策 P22〜41（ゆめちゃん用・別の学校）。
出典: ゆめちゃんの単語帳「教科書に出てきた単語・表現」Unit 2(pp.21-25)＋Unit 3(pp.33-37) の写真4枚
      （inbox 1000103352/354/356/357.jpg）を Opus が読取り、Codex でダブルチェック。

方針（2026-06-21 オーナー確定）:
  - 「新出（Unit 3）中心 ＋ 中間範囲（Unit 2）は"おさらい"の別モード」。
  - 単語が苦手な子向けに重要語へ絞り、品詞別＋動詞・形容詞優先（海輝君 en-b と同じ思想）。
  - 範囲外として除外（オーナー指示）: class / our / Canada / America / be good at / he's / she's。
  - 絞りで落とすもの: 固有名詞(China)・短縮形(that's/can't/you're/it's/what's/who's/when's/where's)・
    間投詞(oops)・易しい挨拶(here you are/thank you/you're welcome)・純機能の前置詞(for)。
  - 残す前置詞は意味を覚える価値があるもの(around/after/near)＝内容語扱い。
忠実性メモ: 意味は単語帳の印刷どおり。cannot は意味「…できない」で出題（印刷の「can の否定形」を学習用に）。
音声: en-c 専用に gTTS で生成（/audio/en-c/）。
"""
import json, os, re


def slug(s):
    """say文字列 → 音声ファイル名スラッグ（英小文字と数字、区切りは_）"""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def aud(say):
    return "/audio/en-c/" + slug(say) + ".mp3"

# (English, 日本語の意味, TTS読み上げ)

# ───────── 新出（Unit 3） ─────────
new_av = [   # 新出 動詞・形容詞（最優先）
    ("win", "勝つ、…を得る、獲得する", "win"),
    ("interesting", "おもしろい、興味深い", "interesting"),
    ("favorite", "好きな、お気に入りの", "favorite"),
    ("next", "次の、隣の", "next"),
]

new_n = [    # 新出 名詞
    ("symbol", "シンボル、象徴、記号", "symbol"),
    ("character", "登場人物", "character"),
    ("hallway", "ろうか", "hallway"),
    ("luck", "幸運", "luck"),
    ("after school", "放課後", "after school"),
]

new_adv = [  # 新出 副詞・前置詞・会話表現
    ("also", "…もまた、そのうえ", "also"),
    ("around", "…のまわりに", "around"),
    ("after", "…のあとに、…のあとで", "after"),
    ("near", "…の近くに", "near"),
    ("online", "オンラインで", "online"),
    ("Good luck.", "がんばって。幸運を祈ります。", "Good luck"),
]

# ───────── 中間範囲（Unit 2）＝おさらい ─────────
review_mid = [
    ("Chinese", "中国の", "Chinese"),
    ("cannot", "…できない", "cannot"),
    ("some", "いくつかの、いくらかの、少しの", "some"),
    ("parent", "親", "parent"),
    ("here", "さあ、ほら、ここに", "here"),
    ("welcome", "歓迎されて、ようこそ", "welcome"),
    ("excuse", "…を許す", "excuse"),
    ("I see.", "なるほど。わかった。", "I see"),
    ("Excuse me.", "すみません。失礼ですが。", "Excuse me"),
]

# ⑤ 仕上げ: 新出の重要語を 日→英（書きの確認）。短くて高価値のものを中心に。
finish_j2e = [
    ("win", "勝つ、…を得る、獲得する", "win"),
    ("next", "次の、隣の", "next"),
    ("symbol", "シンボル、象徴、記号", "symbol"),
    ("luck", "幸運", "luck"),
    ("also", "…もまた、そのうえ", "also"),
    ("near", "…の近くに", "near"),
    ("after", "…のあとに、…のあとで", "after"),
    ("online", "オンラインで", "online"),
]

# ひっかけ2択: (英語, 正しい意味, まぎらわしい誤答, TTS) ※全て収録語から
traps = [
    ("around", "…のまわりに", "…の近くに", "around"),
    ("near", "…の近くに", "…のまわりに", "near"),
    ("interesting", "おもしろい、興味深い", "好きな、お気に入りの", "interesting"),
    ("favorite", "好きな、お気に入りの", "おもしろい、興味深い", "favorite"),
    ("character", "登場人物", "シンボル、象徴、記号", "character"),
    ("symbol", "シンボル、象徴、記号", "登場人物", "symbol"),
    ("after", "…のあとに、…のあとで", "…の近くに", "after"),
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

review_q = j2e(finish_j2e) + trap_q

data = {
    "title": "英語 P22〜41 期末対策",
    "subtitle": "中1 期末の新出を中心に（中間はおさらい）｜🔊音声つき",
    "icon": "📖",
    "modes": {
        "newav": {"label": "① 新出 動詞・形容詞（最優先）", "icon": "🏃",
                  "description": "", "questions": e2j(new_av)},
        "newn": {"label": "② 新出 名詞", "icon": "📦",
                 "description": "", "questions": e2j(new_n)},
        "newadv": {"label": "③ 新出 副詞・前置詞・表現", "icon": "💬",
                   "description": "", "questions": e2j(new_adv)},
        "review": {"label": "④ 中間のおさらい（復習）", "icon": "🔁",
                   "description": "", "questions": e2j(review_mid)},
        "finish": {"label": "⑤ 仕上げ（書き＋ひっかけ）", "icon": "🎯",
                   "description": "", "questions": review_q},
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "english-c-2026-06.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

n_new = len(new_av) + len(new_n) + len(new_adv)
print("written:", out)
print(f"新出: 動詞形容詞{len(new_av)} 名詞{len(new_n)} 副詞前置詞表現{len(new_adv)} = {n_new}語")
print(f"中間おさらい: {len(review_mid)}語")
print(f"⑤仕上げ: 日→英{len(finish_j2e)} + ひっかけ{len(trap_q)} = {len(review_q)}問")
print(f"合計収録語(ユニーク): {n_new + len(review_mid)}語")

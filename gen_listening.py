#!/usr/bin/env python3
"""
人狼英語リスニング特訓アプリ（/ls）のデータ・音声生成スクリプト

- フレーズ102個（cat=カテゴリ, tier=1最重要/2よく使う/3応用）＋単複等の聞き分けペア10組
- 出力1: listening-2026-07.json（アプリが読むデータ）
- 出力2: audio/ls/*.mp3（gTTSで生成。--audio を付けた時だけ）
- 用語は jinroh-chat の翻訳用語集と統一: Seer/Robber/Tanner/Madman/Villager/Werewolf,
  center cards, swap, vote out。lynch等のBAN回避語は使わない
  （memory/reference_jinroh_chat_translation_ban_words.md）

使い方:
  python3 gen_listening.py            # JSONのみ再生成
  python3 gen_listening.py --audio    # JSON + 不足MP3を生成（gtts必要）
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
AUDIO_DIR = ROOT / "audio" / "ls"
JSON_PATH = ROOT / "listening-2026-07.json"

# (id, tier, en, jp, note)
P = [
    # ---- 役職CO (claim) ----
    ("c01", 1, "I claim Seer.", "占い師をCOします。", ""),
    ("c02", 1, "I claim Robber.", "怪盗をCOします。", ""),
    ("c03", 1, "I'm a Villager.", "私は村人です。", ""),
    ("c04", 1, "I'm not a werewolf.", "私は人狼ではありません。", ""),
    ("c05", 1, "My role is Villager.", "私の役職は村人です。", ""),
    ("c06", 2, "I claimed Seer first.", "先に占い師をCOしたのは私です。", "claimed の -ed（過去形）に注意"),
    ("c07", 2, "Two people claimed Seer.", "占い師COが2人います。", ""),
    ("c08", 2, "Nobody claimed Robber.", "怪盗をCOした人はいません。", ""),
    ("c09", 2, "I was a Werewolf at first.", "最初は人狼でした。", "怪盗に交換された後の説明でよく出る"),
    ("c10", 2, "I claim Madman.", "狂人をCOします。", "海外の定番One Night Ultimate WerewolfではMinionと呼ぶ"),

    # ---- 夜の情報 (night) ----
    ("n01", 1, "I checked the center cards.", "中央のカードを確認しました。", "cards の s まで聞く"),
    ("n02", 1, "I checked two center cards.", "中央のカードを2枚確認しました。", ""),
    ("n03", 1, "I saw a werewolf.", "人狼を1枚見ました。", ""),
    ("n04", 1, "I saw two werewolves.", "人狼を2枚見ました。", "wolves（複数形）の音の変化"),
    ("n05", 1, "I swapped with Red.", "Redさんとカードを交換しました。", ""),
    ("n06", 1, "I checked Red's card.", "Redさんのカードを確認しました。", ""),
    ("n07", 1, "Red is a Villager.", "Redさんは村人でした。", ""),
    ("n08", 1, "Red is a Werewolf.", "Redさんは人狼でした。", ""),
    ("n09", 2, "There was a Tanner in the center.", "中央に吊人がありました。", ""),
    ("n10", 2, "Both werewolves might be in the center.", "人狼は2枚とも中央にあるかもしれません。", "平和村の可能性の話でよく出る"),
    ("n11", 2, "Maybe my card was swapped.", "私のカードは交換されたかもしれません。", ""),
    ("n12", 2, "The Robber might have swapped my card.", "怪盗が私のカードを交換したかもしれません。", ""),
    ("n13", 2, "I didn't swap any cards.", "カードは交換しませんでした。", ""),
    ("n14", 2, "Now I'm a Villager.", "今は村人になっています。", "怪盗が交換後の自分を説明する言い方"),

    # ---- 疑い (suspect) ----
    ("s01", 1, "Red is suspicious.", "Redさんが怪しいです。", "suspicious はDay1で練習した単語"),
    ("s02", 1, "I suspect Red.", "Redさんを疑っています。", ""),
    ("s03", 1, "I think Red is lying.", "Redさんは嘘をついていると思います。", ""),
    ("s04", 1, "That doesn't make sense.", "それは筋が通りません。", ""),
    ("s05", 1, "I don't believe you.", "あなたを信じられません。", ""),
    ("s06", 2, "You changed your story.", "さっきと話が変わっていますよ。", ""),
    ("s07", 2, "You said something different before.", "さっきは違うことを言っていました。", ""),
    ("s08", 2, "Why did you claim so late?", "どうしてCOがそんなに遅かったのですか。", ""),
    ("s09", 2, "One of them is lying.", "どちらかが嘘をついています。", "占い師CO2人の時の定番"),
    ("s10", 2, "Your story doesn't match.", "あなたの話はつじつまが合いません。", ""),

    # ---- 質問 (question) ----
    ("q01", 1, "Why do you suspect me?", "どうして私を疑うのですか。", ""),
    ("q02", 1, "What did you see?", "何を見ましたか。", ""),
    ("q03", 1, "Who did you check?", "誰を確認しましたか。", ""),
    ("q04", 1, "What's your role?", "あなたの役職は何ですか。", ""),
    ("q05", 1, "Are you the Seer?", "あなたが占い師ですか。", ""),
    ("q06", 1, "Who do you suspect?", "誰を疑っていますか。", ""),
    ("q07", 2, "What did you do at night?", "夜に何をしましたか。", ""),
    ("q08", 2, "Which cards did you check?", "どのカードを確認しましたか。", ""),
    ("q09", 2, "What do you think, Red?", "Redさんはどう思いますか。", ""),
    ("q10", 2, "Can you prove it?", "それを証明できますか。", ""),
    ("q11", 2, "Anyone else?", "他にいませんか。", "短いので通常速度だと消えやすい"),

    # ---- 弁明 (defense) ----
    ("d01", 1, "I'm telling the truth.", "本当のことを言っています。", ""),
    ("d02", 1, "Trust me.", "信じてください。", ""),
    ("d03", 1, "It wasn't me.", "私ではありません。", ""),
    ("d04", 1, "That's not true.", "それは違います。", ""),
    ("d05", 1, "I can explain.", "説明できます。", "can が can't に聞こえないか注意"),
    ("d06", 2, "I really am the Seer.", "本当に占い師なんです。", ""),
    ("d07", 2, "I have no reason to lie.", "嘘をつく理由がありません。", ""),
    ("d08", 3, "If I were a werewolf, I wouldn't say that.", "もし私が人狼なら、そんなことは言いません。", "長め。文の保持力トレーニング"),
    ("d09", 2, "Please listen to me.", "聞いてください。", ""),
    ("d10", 2, "I'm just a Villager, so I have no information.", "ただの村人なので、情報はありません。", ""),

    # ---- 投票 (vote) ----
    ("v01", 1, "Let's vote out Red.", "Redさんに投票しましょう。", "vote out = 投票で追放する（人狼の標準用語）"),
    ("v02", 1, "I'll vote for Red.", "私はRedさんに投票します。", ""),
    ("v03", 1, "Who are you voting for?", "誰に投票しますか。", ""),
    ("v04", 1, "Don't vote for me.", "私に投票しないでください。", ""),
    ("v05", 1, "I changed my mind.", "気が変わりました。", ""),
    ("v06", 2, "Let's all vote for the same person.", "全員で同じ人に投票しましょう。", ""),
    ("v07", 2, "I'm switching my vote to Blue.", "投票先をBlueさんに変えます。", ""),
    ("v08", 2, "Are we ready to vote?", "投票の準備はいいですか。", ""),
    ("v09", 2, "It's a tie.", "同数です。", "短い。tie（タイ）＝引き分け・同数"),
    ("v10", 3, "Last chance to change your vote.", "投票を変える最後のチャンスです。", ""),

    # ---- 会話・あいづち (talk) ----
    ("t01", 1, "Sorry, I didn't catch that.", "すみません、聞き取れませんでした。", "実戦で一番大事な保険フレーズ"),
    ("t02", 1, "Can you say that again?", "もう一度言ってもらえますか。", ""),
    ("t03", 1, "Can you speak more slowly?", "もっとゆっくり話してもらえますか。", ""),
    ("t04", 1, "Got it.", "わかりました。", "短い定型。Day2で課題になった系統"),
    ("t05", 1, "Wait a second.", "ちょっと待ってください。", ""),
    ("t06", 1, "Let me think.", "考えさせてください。", ""),
    ("t07", 1, "Anytime.", "どういたしまして。", "Day2で聞き取れなかった実績あり"),
    ("t08", 1, "Great job.", "よくできました。", "Day2で聞き取れなかった実績あり"),
    ("t09", 2, "I agree with Red.", "Redさんに賛成です。", ""),
    ("t10", 2, "I disagree.", "反対です。", ""),
    ("t11", 2, "That's a good point.", "いい指摘ですね。", ""),
    ("t12", 2, "How about you?", "あなたはどうですか。", ""),
    ("t13", 2, "Fair enough.", "まあ、それもそうですね。", ""),
    ("t14", 2, "I take it back.", "今のは取り消します。", ""),
    ("t15", 3, "You convinced me.", "納得しました（説得されました）。", ""),
    ("t16", 3, "Nice bluff!", "いいブラフでしたね！", ""),
    ("t17", 3, "You got me.", "やられました。", ""),
    ("t18", 3, "Well played.", "お見事でした。", ""),
    ("t19", 3, "No hard feelings.", "恨みっこなしですよ。", ""),
    ("t20", 3, "My gut says Red.", "直感ではRedさんです。", "gut＝直感。カジュアル表現"),

    # ---- 進行・結果 (game) ----
    ("g01", 1, "Let's start the game.", "ゲームを始めましょう。", ""),
    ("g02", 2, "Discussion time starts now.", "議論タイムを始めます。", ""),
    ("g03", 2, "Please vote now.", "投票してください。", ""),
    ("g04", 2, "Time's almost up.", "時間がもうすぐ終わります。", ""),
    ("g05", 2, "The game is over.", "ゲーム終了です。", ""),
    ("g06", 2, "The Villagers win!", "村人チームの勝ちです！", ""),
    ("g07", 2, "The Werewolves win!", "人狼チームの勝ちです！", ""),
    ("g08", 2, "The Tanner wins!", "吊人の勝ちです！", ""),
    ("g09", 1, "Good game.", "いい試合でした。", "対戦後の定番あいさつ（GGと略される）"),
    ("g10", 2, "One more game?", "もう1回やりますか。", ""),
    ("g11", 3, "Ten seconds left.", "残り10秒です。", ""),
    ("g12", 3, "Let's decide now.", "もう決めましょう。", ""),
    ("g13", 3, "Night falls. Everyone, close your eyes.", "夜になります。全員目を閉じてください。", ""),
    ("g14", 3, "It's morning. Everyone, open your eyes.", "朝になりました。全員目を開けてください。", ""),
    ("g15", 3, "The Madman is on the werewolf team.", "狂人は人狼チームです。", "海外定番ルールではMinion"),
    ("g16", 3, "The Tanner wants to be voted out.", "吊人は投票されたい役職です。", ""),
    ("g17", 2, "Maybe there are no werewolves.", "人狼はいないのかもしれません。", "平和村の相談で出る"),
]

CATS = {
    "c": ("claim", "役職CO"),
    "n": ("night", "夜の情報"),
    "s": ("suspect", "疑い"),
    "q": ("question", "質問"),
    "d": ("defense", "弁明"),
    "v": ("vote", "投票"),
    "t": ("talk", "会話・あいづち"),
    "g": ("game", "進行・結果"),
}

# 聞き分けペア: (id, focus, en_a, en_b, jp解説)
PAIRS = [
    ("pr01", "単数か複数か", "I checked the center card.", "I checked the center cards.",
     "最後の s だけの差。Day2でつまずいた本命ペア。s は弱い音なので文末に集中"),
    ("pr02", "1枚か2枚か", "I saw a werewolf.", "I saw two werewolves.",
     "a / two と、wolf→wolves（ウルフ→ウルヴズ）の変化"),
    ("pr03", "今か過去か", "I claim Seer.", "I claimed Seer.",
     "claimed の -ed は「ド」と軽く付くだけ。次の S とつながって消えやすい"),
    ("pr04", "これからか、した後か", "I'll vote for Red.", "I voted for Red.",
     "I'll（アイル）と voted の -ed。時制の聞き分け"),
    ("pr05", "is か are か", "There is a werewolf in the center.", "There are two werewolves in the center.",
     "There is / There are。後ろの単複とセットで確認"),
    ("pr06", "can か can't か", "I can explain.", "I can't explain.",
     "can't の t はほぼ聞こえない。can't は「キャーント」と母音が強く、canは弱く読まれる"),
    ("pr07", "he か she か", "He is suspicious.", "She is suspicious.",
     "h と sh の出だしの音だけの差"),
    ("pr08", "Who か What か", "Who did you check?", "What did you check?",
     "疑問詞の聞き分け。答え方が変わるので実戦で重要"),
    ("pr09", "肯定か否定か", "Vote for Red.", "Don't vote for Red.",
     "Don't の聞き逃しは致命的。文頭に集中"),
    ("pr10", "a か the ＋ 複数か", "I swapped a card.", "I swapped the cards.",
     "a / the の違いと最後の s。冠詞はDay1からの課題"),
]


def build_json():
    phrases = []
    for pid, tier, en, jp, note in P:
        cat, cat_jp = CATS[pid[0]]
        item = {
            "id": pid, "en": en, "jp": jp, "cat": cat, "catJp": cat_jp,
            "tier": tier, "audio": f"/audio/ls/{pid}.mp3",
        }
        if note:
            item["note"] = note
        phrases.append(item)
    pairs = []
    for pid, focus, en_a, en_b, jp in PAIRS:
        pairs.append({
            "id": pid, "focus": focus, "jp": jp,
            "a": {"en": en_a, "audio": f"/audio/ls/{pid}a.mp3"},
            "b": {"en": en_b, "audio": f"/audio/ls/{pid}b.mp3"},
        })
    data = {
        "version": 1,
        "updated": "2026-07-13",
        "title": "人狼英語 リスニング特訓",
        "cats": [{"key": k, "jp": j} for k, j in
                 [CATS[c] for c in ["c", "n", "s", "q", "d", "v", "t", "g"]]],
        "phrases": phrases,
        "pairs": pairs,
    }
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    t1 = sum(1 for p in phrases if p["tier"] == 1)
    t2 = sum(1 for p in phrases if p["tier"] == 2)
    t3 = sum(1 for p in phrases if p["tier"] == 3)
    print(f"JSON: {JSON_PATH.name}  phrases={len(phrases)} (T1={t1} T2={t2} T3={t3})  pairs={len(pairs)}")
    return data


def gen_audio(data):
    from gtts import gTTS
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    jobs = [(p["id"], p["en"]) for p in data["phrases"]]
    for pr in data["pairs"]:
        jobs.append((pr["id"] + "a", pr["a"]["en"]))
        jobs.append((pr["id"] + "b", pr["b"]["en"]))
    made = skipped = 0
    for fid, text in jobs:
        out = AUDIO_DIR / f"{fid}.mp3"
        if out.exists() and out.stat().st_size > 1000:
            skipped += 1
            continue
        for attempt in range(3):
            try:
                gTTS(text=text, lang="en", tld="com").save(str(out))
                made += 1
                print(f"  {fid}.mp3  {text}")
                break
            except Exception as e:
                print(f"  RETRY {fid} ({attempt+1}/3): {e}")
                time.sleep(2 + attempt * 3)
        else:
            print(f"  FAILED: {fid}")
        time.sleep(0.4)
    print(f"audio: made={made} skipped={skipped} total_jobs={len(jobs)}")


if __name__ == "__main__":
    data = build_json()
    if "--audio" in sys.argv:
        gen_audio(data)

import speech_recognition as sr

recognizer = sr.Recognizer()
results = []

print("🎤 詠唱受付開始！「アクティベート」と言うまで続けます…")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)  # 周囲の雑音対策

    while True:
        print("🕒 詠唱を待っています...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='ja-JP')
            print("📝 認識結果:", text)
            results.append(text)

            if "アクティベート" == text:
                print("🛑 「アクティベート」が検出されたので終了します！")
                break

        except sr.UnknownValueError:
            print("😕 音声を聞き取れませんでした")
        except sr.RequestError as e:
            print("❌ 音声認識サービスに接続できませんでした:", e)
            break

#MagicElements
#魔法を発動するために必要な言葉を格納
magicElements_F = ["ファイヤー","メテオ"]
magicElements_W = ["ウォーター","ティア","ドリップ"]
#魔法の発動、判別のために使う
SPELL_flag_F=0
SPELL_flag_W=0

print("📋 集まった発言リスト:")
for i, item in enumerate(results, 1):
    #itemがmagicElements 似ない場合の単語を表示するために使う
    flag = 0
    if (item in magicElements_F):
        SPELL_flag_F += 1 
        flag += 1

    if (item in magicElements_W):
        SPELL_flag_W += 1 
        flag += 1

    if SPELL_flag_F == 2:
        print("☄️")
        break

    elif SPELL_flag_W == 3:
        print("💧")
        break

    elif flag==0:
        print(f"{i}. {item}")

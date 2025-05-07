import speech_recognition as sr

recognizer = sr.Recognizer()
results = []

print("🎤 音声認識開始！「フィニッシュ」と言うまで続けます…")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)  # 周囲の雑音対策

    while True:
        print("🕒 発話を待っています...")
        audio = recognizer.listen(source)

        #if waitKey(1) == 

        try:
            text = recognizer.recognize_google(audio, language='ja-JP')
            print("📝 認識結果:", text)
            results.append(text)

            if "フィニッシュ" in text:
                print("🛑 「フィニッシュ」が検出されたので終了します！")
                break

        except sr.UnknownValueError:
            print("😕 音声を聞き取れませんでした")
        except sr.RequestError as e:
            print("❌ 音声認識サービスに接続できませんでした:", e)
            break

print("📋 集まった発言リスト:")
for i, item in enumerate(results, 1):
    print(f"{i}. {item}")

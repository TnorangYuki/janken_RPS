import speech_recognition as sr

# 音声認識の準備
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 なにか喋ってみて！")
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ja-JP')
        print("📝 認識結果:", text)
    except sr.UnknownValueError:
        print("😅 聞き取れませんでした")
    except sr.RequestError:
        print("❌ サービスにアクセスできませんでした")

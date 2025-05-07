import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
data_captured = False  # データ取得が完了したかを追跡するフラグ

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks and not data_captured:
        print("検出された手のランドマーク (1セット):")
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            print(f"  手 {i+1}:")
            for j, landmark in enumerate(hand_landmarks.landmark):
                print(f"    ランドマーク {j}: x={landmark.x:.4f}, y={landmark.y:.4f}, z={landmark.z:.4f}")
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        data_captured = True  # データの取得が完了したのでフラグをTrueにする
        break  # ループを終了する

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()

print("ランドマークデータの取得を終了しました。")
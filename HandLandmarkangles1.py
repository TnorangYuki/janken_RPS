import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,  # 動画ストリーム用
                      max_num_hands=1,          # 検出する手の数
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(p1, p2, p3):
    """3点の座標からベクトル間の角度を計算する関数 (ラジアン)"""
    v1 = np.array([p1.x - p2.x, p1.y - p2.y, p1.z - p2.z])
    v2 = np.array([p3.x - p2.x, p3.y - p2.y, p3.z - p2.z])

    unit_v1 = v1 / np.linalg.norm(v1)
    unit_v2 = v2 / np.linalg.norm(v2)

    dot_product = np.dot(unit_v1, unit_v2)
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0)) # -1から1の範囲にクリップ
    return angle_rad

def get_finger_angles(hand_landmarks):
    """手のランドマークから各指の開閉に関連する角度を計算する関数"""
    angles = {}

    # 人差し指の開閉判定 (0, 5, 6)
    if hand_landmarks and len(hand_landmarks.landmark) >= 7:
        p1 = hand_landmarks.landmark[6]
        p2 = hand_landmarks.landmark[5]
        p3 = hand_landmarks.landmark[0]
        angle_rad = calculate_angle(p1, p2, p3)
        angles["index_finger_angle"] = math.degrees(angle_rad)

    # 中指の開閉判定 (0, 9, 10)
    if hand_landmarks and len(hand_landmarks.landmark) >= 11:
        p1 = hand_landmarks.landmark[10]
        p2 = hand_landmarks.landmark[9]
        p3 = hand_landmarks.landmark[0]
        angle_rad = calculate_angle(p1, p2, p3)
        angles["middle_finger_angle"] = math.degrees(angle_rad)

    # 薬指の開閉判定 (0, 13, 14)
    if hand_landmarks and len(hand_landmarks.landmark) >= 15:
        p1 = hand_landmarks.landmark[14]
        p2 = hand_landmarks.landmark[13]
        p3 = hand_landmarks.landmark[0]
        angle_rad = calculate_angle(p1, p2, p3)
        angles["ring_finger_angle"] = math.degrees(angle_rad)

    # 小指の開閉判定 (0, 17, 18)
    if hand_landmarks and len(hand_landmarks.landmark) >= 19:
        p1 = hand_landmarks.landmark[18]
        p2 = hand_landmarks.landmark[17]
        p3 = hand_landmarks.landmark[0]
        angle_rad = calculate_angle(p1, p2, p3)
        angles["pinky_finger_angle"] = math.degrees(angle_rad)

    return angles

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

            # 指の角度を取得
            finger_angles = get_finger_angles(hand_landmarks)
            print("指の角度 (手のひら基点):")
            for finger, angle in finger_angles.items():
                print(f"  {finger}: {angle:.2f} 度")

        data_captured = True  # データの取得が完了したのでフラグをTrueにする
        break  # ループを終了する

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()

print("ランドマークデータと指の角度の取得を終了しました。")
import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,   # 動画ストリーム用
                        max_num_hands=1,         # 検出する手の数
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
    return math.degrees(angle_rad)

def detect_finger_status(hand_landmarks):
    """手のランドマークから各指の開閉状態と角度を判定する関数"""
    finger_info = {}

    if hand_landmarks and len(hand_landmarks.landmark) >= 21:
        # 各指の角度計算
        thumb_angle = calculate_angle(hand_landmarks.landmark[4], hand_landmarks.landmark[2], hand_landmarks.landmark[0])
        index_finger_angle = calculate_angle(hand_landmarks.landmark[6], hand_landmarks.landmark[5], hand_landmarks.landmark[0])
        middle_finger_angle = calculate_angle(hand_landmarks.landmark[10], hand_landmarks.landmark[9], hand_landmarks.landmark[0])
        ring_finger_angle = calculate_angle(hand_landmarks.landmark[14], hand_landmarks.landmark[13], hand_landmarks.landmark[0])
        pinky_finger_angle = calculate_angle(hand_landmarks.landmark[18], hand_landmarks.landmark[17], hand_landmarks.landmark[0])

        # 開閉の閾値 (調整が必要)
        finger_open_threshold = 160
        thumb_open_threshold = 130
        pinky_finger_threshold = 160   # ← ここで定義する (値は適宜調整)

        finger_info["thumb"] = {"status": "Open" if thumb_angle > thumb_open_threshold else "Closed", "angle": f"{thumb_angle:.2f}"}
        finger_info["index"] = {"status": "Open" if index_finger_angle > finger_open_threshold else "Closed", "angle": f"{index_finger_angle:.2f}"}
        finger_info["middle"] = {"status": "Open" if middle_finger_angle > finger_open_threshold else "Closed", "angle": f"{middle_finger_angle:.2f}"}
        finger_info["ring"] = {"status": "Open" if ring_finger_angle > finger_open_threshold else "Closed", "angle": f"{ring_finger_angle:.2f}"}
        finger_info["pinky"] = {"status": "Open" if pinky_finger_angle > pinky_finger_threshold else "Closed", "angle": f"{pinky_finger_angle:.2f}"}

    return finger_info

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(image, 1)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_info = detect_finger_status(hand_landmarks)
                print("指の状態 (HandLandmarkangles3.py):", finger_info)

        cv2.imshow('HandLandmarkangles3', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()
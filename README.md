# モーションじゃんけん

## 遊び方

1. スピーカーやイヤホンで音を聞ける状態にする。           
2. コマンドで実行（`python DetectHandStatus.py HandLandmarkangles3.py voice_player1.py`）。
3. 「じゃんけん」と聞こえたら、PCのカメラの前で「グー」「チョキ」「パー」のいずれかを出す。
4. 手の形が検出され、コンピューターとの勝敗が判定される。

## じゃんけんをするために

### インストール
- mediapipe: 0.10.21
- numpy: 1.26.4
- opencv-contrib-python: 4.11.0.86
- opencv-python: 4.11.0.86
- playsound: 1.3.0

### 実行コマンド
```
python DetectHandStatus.py HandLandmarkangles3.py voice_player1.py

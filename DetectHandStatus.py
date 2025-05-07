import HandLandmarkangles3  # HandLandmarkangles3.py をインポート
import mediapipe as mp
import cv2
import random
import time
import voice_player1



start = time.time()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


#n回でループを終わらすために利用
#count=0

#ループの回数計測
loop_counter = 0
#sleepの回数計測
sleep_counter = 0
#一回だけCUIの表示
flag=0

waitTimer_start = time.time()


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

#インターフェース的なイメージ
    if flag==0:
        print(f'{"じゃんけん"}{"."*5}')
        flag += 1

        
        #スペースを開けて見やすく
        i=0
        for i in range(2):
            print(" ")
        

        time.sleep(0.1)

        voice_player1.VUI(0)

        time.sleep(0.5)

        #手の状態をリセット(直後のif文内だと、初めに手がないときにエラーになる)
        hand_status = None
        #ジャンケン結果リセット(直後のif文内だと、初めに手がないときにエラーになる)
        result = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # HandLandmarkangles3.py の detect_finger_status 関数を呼び出し、finger_status を取得
            finger_status = HandLandmarkangles3.detect_finger_status(hand_landmarks)
            #print("取得した指の状態 (DetectHandStatus.py):", finger_status)


            


            # ここで取得した finger_status を使った処理を記述できます
            if finger_status["index"]["status"] == "Open" and finger_status["middle"]["status"] == "Open" :
                hand_status="チョキ"
                if all(info["status"] == "Open" for finger, info in finger_status.items() if finger != "thumb"):
                    hand_status="パ  ー"

            elif all(info["status"] == "Closed" for finger, info in finger_status.items() if finger != "thumb"):
                hand_status="グ  ー"

                
            
            CP_hand = ["チョキ","パ  ー","グ  ー"]
            cp_hand_status = random.choice(CP_hand)

            #ジャンケン



            #ジャンケン判定
            if hand_status==cp_hand_status:
                result="   あいこ   "
            elif (hand_status=="チョキ" and cp_hand_status=="パ  ー") or (hand_status=="パ  ー" and cp_hand_status=="グ  ー") or (hand_status=="グ  ー" and cp_hand_status=="チョキ"):
                result="あなたの勝ち"
            elif (hand_status=="チョキ" and cp_hand_status=="グ  ー") or (hand_status=="パ  ー" and cp_hand_status=="チョキ") or (hand_status=="グ  ー" and cp_hand_status=="パ  ー"):
                result="あなたの負け"
            
            if cp_hand_status!=None and result!=None:
                #result 用の CUI
                print(f'{"-"*7}{"ポンッ!"}{"-"*7}')
                print("-"*21)
                   

                print(f'{"*"*5}{"HAND STATUS"}{"*"*5}')
                print(f'{"*"}{"あなた  "}{hand_status}{" "*5}{"*"}') 
                print(f'{"*"}{"CP      "}{cp_hand_status}{" "*5}{"*"}') 
                print(f'{"*"}{" "*5}{result}{" "*2}{"*"}') 
                print("*"*21)


                    

                for result_UIcounter in range(2):
                    print("-"*21)
                    result_UIcounter+=1


                if result == "あなたの勝ち":
                    time.sleep(1.0)

                    voice_player1.VUI(1)

                    time.sleep(1.0)

                    voice_player1.VUI(2)
                    
                elif result  == "あなたの負け":
                    time.sleep(1.0)

                    voice_player1.VUI(1)

                    time.sleep(1.0)

                    voice_player1.VUI(3)
                elif result  == "   あいこ   ":
                    time.sleep(1.0)

                    voice_player1.VUI(11)

                    time.sleep(1.0)
    loop_counter += 1
    
    waitTimer_stop = time.time()
    waitTimer_gap = waitTimer_stop - waitTimer_start
    if loop_counter != 0 and (hand_status != None) and (result != None) :
        break
    #長時間稼働を避けるためタイムアウト時間を設ける
    elif int(waitTimer_gap) >20:

        print("タイムアウト")
        break

    #一定時間ごとにインターフェースを再度流す    
    elif int(waitTimer_gap)!=0 and int(waitTimer_gap)%10==0:
        #print(f'{int(waitTimer_gap)}s')
        print("手の形が判定できません")
        print(f'{"じゃんけん"}{"."*5}')
        print(" ")
        time.sleep(1.0)

        voice_player1.VUI(0)


        sleep_counter += 1

        time.sleep(3.0)
        


    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break


hands.close()
cap.release()
cv2.destroyAllWindows()

end = time.time()
print("    ")
print(f'{"手の検出と指の状態の処理を終了しました (DetectHandStatus.py)。"}{end-start:.3f}{"秒"}')
print(f'{loop_counter}{"回ループ,"}{sleep_counter}{"回sleep"}')

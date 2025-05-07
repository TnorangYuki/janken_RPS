#voce_player1.py

import numpy as np
import time
from playsound import playsound

def VUI(voice_flag):
    match voice_flag:
        case 0:
            try:
                #playsound('.\\sounds\\blank.wav', block=True)
                playsound('.\\sounds\\RPS_vo.wav', block=True)
                time.sleep(0.5)

            except Exception as e:
                print(f"パターン1の再生中にエラーが発生しました: {e}")
        case 1:
            try:
                
                playsound('.\\sounds\\pon_vo.wav', block=True)
                time.sleep(0.5)

            except Exception as e:
                print(f"パターン2の再生中にエラーが発生しました: {e}")
        case 2:
            try:
                
                playsound('.\\sounds\\kachi_vo.wav', block=True)
                time.sleep(0.5)

            except Exception as e:
                print(f"パターン3の再生中にエラーが発生しました: {e}")
        case 3:
            try:
                
                playsound('.\\sounds\\make_vo.wav', block=True)
                time.sleep(0.5)

            except Exception as e:
                print(f"パターン4の再生中にエラーが発生しました: {e}")
        case 11:
            try:
                
                playsound('.\\sounds\\aiko_vo.wav', block=True)
                time.sleep(0.5)

            except Exception as e:
                print(f"パターン5の再生中にエラーが発生しました: {e}")
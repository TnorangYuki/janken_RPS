import time
import keyboard
from playsound import playsound

timer_start=time.time()
timer_stop=0.0
time_gap = 0.0

while (time_gap)<10:
    timer_stop=time.time()
    time_gap=timer_stop-timer_start
    print(time_gap)
    print(int(time_gap))
    if int(time_gap)%2==0:
        playsound('.\\sounds\\pon_vo.wav', block=True)
    
    

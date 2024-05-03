'''
实验名称：定时器
版本：v1.0
日期：2022.4
作者：01Studio
说明：通过定时器让LED周期性每秒闪烁1次
'''
from machine import Pin,Timer

LED=Pin(46,Pin.OUT)
Counter = 0
Fun_Num = 0

def fun(tim):

    global Counter
    Counter = Counter + 1
    print(Counter)
    LED.value(Counter%2)

#使用定时器1
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC,callback=fun) #周期为1000ms

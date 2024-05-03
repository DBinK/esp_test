'''
实验名称：超声波传感器HCSR04
版本：v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：通过超声波传感器测距，并在OLED上显示。
'''

from HCSR04 import HCSR04  #将HCSR04.py文件发送到开发板
from machine import Pin,Timer

#初始化超声波模块接口
trig = Pin(17,Pin.OUT)
echo = Pin(18,Pin.IN)
sonar = HCSR04(trig,echo)

#中断回调函数
def fun(tim):

    Distance = sonar.getDistance() #测量距离

    # 终端打印距离,单位cm,保留2位小数。
    print(str('%.2f'%(Distance)) + ' CM')

#开启RTOS定时器
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s

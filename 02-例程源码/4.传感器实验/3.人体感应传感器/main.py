'''
实验名称：人体感应传感器
版本：v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：人体红外感应传感器应用
'''

import time
from machine import Pin   #从machine模块导入I2C、Pin子模块

Human=Pin(10,Pin.IN,Pin.PULL_UP) #构建人体红外对象
LED=Pin(46,Pin.OUT) #构建led对象，GPIO46,输出

def fun(Human): #Get People闪烁5次效果！

    print("Get People!!!")  # 提示有人
    LED.value(1)  # 点亮LED
    
    #等待传感器高电平结束
    while Human.value():
        pass
    
    LED.value(0)  # 熄灭LED

Human.irq(fun,Pin.IRQ_RISING) #定义中断，上升沿触发

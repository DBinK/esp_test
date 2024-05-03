'''
实验名称：点亮LED蓝灯
版本：v1.0
'''

from machine import Pin #导入Pin模块

LED=Pin(46,Pin.OUT) #构建led对象，GPIO46,输出
LED.value(0) #点亮LED，也可以使用led.on()

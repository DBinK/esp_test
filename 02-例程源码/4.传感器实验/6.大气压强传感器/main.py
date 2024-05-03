'''
实验名称：大气压强传感器
版本：v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：测量BMP280温度、气压和计算海拔值，并在终端打印。
'''

import bmp280
from machine import Pin,Timer,SoftI2C

#构建I2C对象
i2c1 = SoftI2C(scl=Pin(17), sda=Pin(18))

#构建BMP280对象
bmp = bmp280.BMP280(i2c1)

#中断回调函数
def fun(tim):

    # 温度信息打印
    print(str(bmp.getTemp()) + ' C')
    # 湿度信息打印
    print(str(bmp.getPress()) + ' Pa')
    # 海拔信息打印
    print(str(bmp.getAltitude()) + ' m')

#开启定时器
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s

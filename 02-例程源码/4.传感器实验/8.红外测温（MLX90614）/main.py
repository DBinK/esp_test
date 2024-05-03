'''
实验名称：红外测温模块MLX90614
版本：v1.0
作者：WalnutPi
平台：核桃派PicoW
说明：测量物体温度和环境温度并在终端打印。
'''

from machine import Pin,SoftI2C
import mlx90614,time

#构建红外测温对象
i2c1 = SoftI2C( scl=Pin(17), sda=Pin(18),freq=100000)
mlx = mlx90614.MLX90614(i2c1)

while True:
    
    #物体温度
    print('ObjTemp:'+str('%.2f'%mlx.ObjectTemp()+' C'))
    
    #环境温度
    print('AmbTemp:'+str('%.2f'%mlx.AmbientTemp()+' C'))
    
    time.sleep(1)

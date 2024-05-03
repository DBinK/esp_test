'''
实验名称：温湿度传感器DHT11
版本：v1.0
作者：WalnutPi
说明：通过编程采集温湿度数据，并在终端打印。
'''

#引入相关模块
from machine import Pin,Timer
import dht,time

#创建DTH11对象
d = dht.DHT11(Pin(2)) #传感器连接引脚
time.sleep(2)   #首次启动停顿2秒让传感器稳定

def dht_get(tim):

    d.measure()  #温湿度采集
    
    #终端打印温湿度信息
    print(str(d.temperature() )+' C') 
    print(str(d.humidity())+' %') 

#开启RTOS定时器，编号为1
tim = Timer(1)
tim.init(period=2000, mode=Timer.PERIODIC,callback=dht_get) #周期为2000ms

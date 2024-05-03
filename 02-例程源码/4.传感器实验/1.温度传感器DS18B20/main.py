'''
实验名称：温度传感器DS18B20
版本：v1.0
作者：WalnutPi
说明：通过编程采集温度数据，并在终端打印。
'''

#引用相关模块
from machine import Pin,Timer
import onewire,ds18x20,time

#初始化DS18B20
ow= onewire.OneWire(Pin(1)) #使能单总线
ds = ds18x20.DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接

def temp_get(tim):
    ds.convert_temp()
    temp = ds.read_temp(rom[0]) #温度显示,rom[0]为第1个DS18B20
    
    print(str('%.2f'%temp)+' C') #终端打印温度信息

#开启RTOS定时器1
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC,callback=temp_get) #周期为1000ms

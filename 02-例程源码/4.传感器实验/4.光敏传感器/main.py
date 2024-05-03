'''
实验名称：光敏传感器
版本：v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：通过光敏传感器对外界环境光照强度测量并在终端打印。
'''

#导入相关模块

from machine import Pin,ADC,Timer

#初始化ADC,Pin=10，11DB衰减，测量电压0-3.3V
Light = ADC(Pin(10))
Light.atten(ADC.ATTN_11DB)

#中断回调函数
def fun(tim):

    value=Light.read() #获取ADC数值

    #显示数值
    print(str(value)+' (4095)')
    #计算电压值，获得的数据0-4095相当于0-3.3V，（'%.2f'%）表示保留2位小数
    print(str('%.2f'%(value/4095*3.3))+'V')

    #判断光照强度，分3档显示。
    if 0 < value <=1365:
        print('Bright')

    if 1365 < value <= 2730:
        print('Normal')

    if 2730 < value <= 4095:
        print('Weak')

#开启RTOS定时器
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s


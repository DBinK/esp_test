'''
实验名称：ADC-电压测量
版本：v1.0
作者：WalnutPi
说明：通过对ADC数据采集，转化成电压在显示屏上显示。ADC精度12位（0~4095），测量电压0-3.3V。
'''

#导入相关模块
from machine import Pin,SoftI2C,ADC,Timer

#构建ADC对象
adc = ADC(Pin(9)) #使用引脚9
adc.atten(ADC.ATTN_11DB) #开启衰减器，测量量程增大到3.3V

def ADC_Test(tim):

    #打印ADC原始值
    print(adc.read())

    #计算电压值，获得的数据0-4095相当于0-3.3V，（'%.2f'%）表示保留2位小数
    print('%.2f'%(adc.read()/4095*3.3) +'V')


#开启定时器
tim = Timer(1)
tim.init(period=300, mode=Timer.PERIODIC, callback=ADC_Test) #周期300ms
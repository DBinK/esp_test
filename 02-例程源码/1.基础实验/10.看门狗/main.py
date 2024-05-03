'''
实验名称：线程
版本： v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：看门狗测试。
'''

from machine import WDT #导入线程模块
import time

#构建看门狗对象，喂狗周期2秒内。
wdt = WDT(timeout=2000)


#每隔1秒喂一次狗，执行3次。
for i in range(3):
    
    time.sleep(1)
    print(i)
    
    wdt.feed() #喂狗

#停止喂狗，系统会重启。
while True:
    pass


'''
实验名称：RTC实时时钟
版本：v1.0
作者：WalnutPi
说明：使用Thonny连接开发板会自动更新RTC时间
'''

# 导入相关模块
from machine import Pin, SoftI2C, RTC
import time

# 构建RTC对象
rtc = RTC()

# 首次上电配置时间，按顺序分别是：年，月，日，星期，时，分，秒，次秒级；这里做了
# 一个简单的判断，检查到当前年份不对就修改当前时间，开发者可以根据自己实际情况来
# 修改。（使用Thonny IDE连接开发板会自动同步RTC时间。）
if rtc.datetime()[0] != 2024:
    rtc.datetime((2024, 1, 1, 0, 0, 0, 0, 0))

while True:
    
    print(rtc.datetime()) #打印时间
    
    time.sleep(1) #延时1秒

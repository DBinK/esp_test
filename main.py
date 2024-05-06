from machine import SoftI2C, Pin, PWM
import time
import math


KEY  = Pin(0,Pin.IN,Pin.PULL_UP)         # 构建KEY对象

lf_ft_bcak = PWM(Pin(15), freq=50)
lf_ft_go   = PWM(Pin(16), freq=50)
lf_bh_back = PWM(Pin(17), freq=50)
lf_bh_go   = PWM(Pin(18), freq=50)

rt_bh_bcak = PWM(Pin(21), freq=50)
rt_bh_go   = PWM(Pin(34), freq=50)
rt_ft_bcak = PWM(Pin(35), freq=50)
rt_ft_go   = PWM(Pin(36), freq=50)

sw = 1
s = 0.05 # 采样时间间隔

# 中值滤波参数
filter_size = 5  # 中值滤波窗口大小
roll_buffer = []  # 滑动窗口

# 中值滤波函数
def median_filter(value):
    roll_buffer.append(value)
    if len(roll_buffer) > filter_size:
        roll_buffer.pop(0)
    sorted_buffer = sorted(roll_buffer)
    median_value = sorted_buffer[len(sorted_buffer) // 2]
    
    return median_value

# 状态翻转函数
def car_sw(KEY):
    global sw
    time.sleep_ms(10) #消除抖动
    if KEY.value()==0: #确认按键被按下
        if sw == 0:
            sw = 1
        else:
            sw = 0
            pwm_down()

def pwm_down():
    
    lf_ft_bcak.duty(0)
    lf_ft_go.duty(0)
    lf_bh_back.duty(0)
    lf_bh_go.duty(0)

    rt_bh_bcak.duty(0)
    rt_bh_go.duty(0)
    rt_ft_bcak.duty(0)
    rt_ft_go.duty(0)
            
KEY.irq(car_sw,Pin.IRQ_FALLING)

while True:
    if sw == 1:

        rt_ft_bcak.duty(500)

        rt_ft_go.duty(0)

        
    elif sw == 0:
    
        pwm_down()


    time.sleep(s) # 采样时间间隔





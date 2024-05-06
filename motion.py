from machine import SoftI2C, Pin, PWM # type: ignore  # noqa: F401
import time


KEY  = Pin(0,Pin.IN,Pin.PULL_UP)         # 构建KEY对象

lf_bh_back = PWM(Pin(15), freq=50)
lf_bh_go   = PWM(Pin(16), freq=50)

lf_ft_back = PWM(Pin(17), freq=50)
lf_ft_go   = PWM(Pin(18), freq=50)

rt_bh_back = PWM(Pin(21), freq=50)
rt_bh_go   = PWM(Pin(34), freq=50)

rt_ft_back = PWM(Pin(35), freq=50)
rt_ft_go   = PWM(Pin(36), freq=50)


# 四个轮子单独控制函数
def lf_ft(pwm_val, direction=1):
    if direction == 1:
        lf_ft_go.duty(pwm_val)
        lf_ft_back.duty(0)
    else:
        lf_ft_back.duty(pwm_val)
        lf_ft_go.duty(0)

def lf_bh(pwm_val, direction):
    if direction == 1:
        lf_bh_go.duty(pwm_val)
        lf_bh_back.duty(0)
    else:
        lf_bh_back.duty(pwm_val)
        lf_bh_go.duty(0)

def rt_ft(pwm_val, direction):
    if direction == 1:
        rt_ft_go.duty(pwm_val)
        rt_ft_back.duty(0)
    else:
        rt_ft_back.duty(pwm_val)
        rt_ft_go.duty(0)

def rt_bh(pwm_val, direction):
    if direction == 1:
        rt_bh_go.duty(pwm_val)
        rt_bh_back.duty(0)
    else:
        rt_bh_back.duty(pwm_val)
        rt_bh_go.duty(0)
    

# 四个轮子同时控制函数

def go_forward(pwm_val):
    lf_ft(pwm_val, 1)
    lf_bh(pwm_val, 1)

    rt_ft(pwm_val, 1)
    rt_bh(pwm_val, 1)

def go_backward(pwm_val):
    lf_ft(pwm_val, 0)
    lf_bh(pwm_val, 0)

    rt_ft(pwm_val, 0)
    rt_bh(pwm_val, 0)

def go_left(pwm_val):
    lf_ft(pwm_val, 0)
    rt_ft(pwm_val, 1)

    lf_bh(pwm_val, 1)
    rt_bh(pwm_val, 0)

def go_right(pwm_val):
    lf_ft(pwm_val, 1)
    rt_bh(pwm_val, 1)

    rt_ft(pwm_val, 0)
    lf_bh(pwm_val, 0)


def turn_left(pwm_val):
    lf_ft(pwm_val, 0)
    lf_bh(pwm_val, 0)

    rt_ft(pwm_val, 1)
    rt_bh(pwm_val, 1)


def turn_right(pwm_val):
    lf_ft(pwm_val, 1)
    lf_bh(pwm_val, 1)

    rt_ft(pwm_val, 0)
    rt_bh(pwm_val, 0)
    
def stop():
    go_forward(0)

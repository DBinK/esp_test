from machine import SoftI2C, Pin, PWM
import mpu6050
import time
import math


i2c1 = SoftI2C(scl=Pin(17), sda=Pin(18)) # 构建I2C对象
mpu  = mpu6050.accel(i2c1)               # 构建MPU6050对象
KEY  = Pin(0,Pin.IN,Pin.PULL_UP)         # 构建KEY对象

pwm_11 = PWM(Pin(11), freq=50)
pwm_12 = PWM(Pin(12), freq=50)

# 初始化姿态角变量
roll = 0
pitch = 0
yaw = 0
pwm = 0
sw = 1

zero_angle   = 0     # 水平偏移0点角度
linmit_angle = 90

zero_pwm = 150

s = 0.05 # 采样时间间隔

last_angle_error = 0  # 上一次的角度误差
integral         = 0  # 积分项初始值

# PID 参数
kp = 0.4
ki = 0
kd = 0.02


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

#LED状态翻转函数
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
    pwm_11.duty(0)
    pwm_12.duty(0)
            

KEY.irq(car_sw,Pin.IRQ_FALLING)

while True:
    # 获取六轴加速度计原始值
    try:
        raw_values = mpu.get_values()

    except (OSError, RuntimeError) as e:  # 捕获可能的IO或运行时错误
        mpu = mpu6050.accel(i2c1)
        # pwm_down()
        print(f"未获取mpu信息，错误原因：{e}")
    
    
    # 计算加速度值
    accel_x = raw_values['AcX'] 
    accel_y = raw_values['AcY'] 
    accel_z = raw_values['AcZ'] 
    
    # 计算角速度值
    gyro_x = raw_values['GyX'] 
    gyro_y = raw_values['GyY'] 
    gyro_z = raw_values['GyZ'] 
    
    # 计算 roll 和 pitch
    roll = math.atan2(accel_y, accel_z) * 180 / math.pi
    pitch = math.atan2(-accel_x, math.sqrt(accel_y * accel_y + accel_z * accel_z)) * 180 / math.pi
    
    # 计算 yaw
    # 这里使用简单的积分方法来估计 yaw
    # yaw += gyro_z * s  # 假设采样时间间隔为0.01秒
    # yaw = 0
    
    # 打印计算好的数值
    # print("加速度 (g)  : X={:.2f}, Y={:.2f}, Z={:.2f}".format(accel_x, accel_y, accel_z))
    # print(f"角速度 (°/s): X= {gyro_x}, Y= {gyro_y}, Z= {gyro_z}")
    # print("姿态角 (°)  : Roll={:.2f}, Pitch={:.2f}, Yaw={:.2f}\n".format(roll, pitch, yaw))
    
    # 在计算 roll 值之前应用中值滤波
    #filtered_roll = median_filter(roll)

    # 计算角度误差
    # angle = filtered_roll - zero_angle
    angle = roll - zero_angle

    if roll != 0 and abs(angle) <= linmit_angle:
        
        # 计算当前角度误差
        current_angle_error = roll - zero_angle

        # 计算微分项
        derivative_term = kd * (current_angle_error - last_angle_error) / s

        # 更新积分项
        integral += current_angle_error * s

        # 积分项限制，防止饱和
        if abs(integral) > 1023:
            integral = 1023 if integral > 0 else -1023

        # 计算总的控制量
        pwm = int(kp * (current_angle_error / 180 * 2046) + ki * integral + derivative_term)
        
        # 更新上一次的角度误差
        last_angle_error = current_angle_error


        if pwm > 0 and sw == 1:
            
            pwm += zero_pwm
            if pwm > 1023: pwm = 1023
            
            pwm_12.duty(0)
            pwm_11.duty(pwm)
            
        if pwm < 0 and sw == 1:
            
            pwm -= zero_pwm
            if pwm < -1023: pwm = -1023
            
            pwm_12.duty(abs(pwm))
            pwm_11.duty(0)


    elif abs(angle) > linmit_angle or sw == 0:
    
        pwm_down()
        
    # print(f"Roll = {roll}, Pitch={pitch}, Angle = {angle}, PWM = {pwm * 0.1}")
    print(f"Roll = {roll} ,  Angle = {angle} ,  PWM = {pwm * 0.1}")


    time.sleep(s) # 采样时间间隔



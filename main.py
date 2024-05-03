from machine import SoftI2C, Pin, PWM
import mpu6050
import time
import math

# 构建I2C对象
i2c1 = SoftI2C(scl=Pin(17), sda=Pin(18))

# 构建MPU6050对象
mpu = mpu6050.accel(i2c1)

pwm_11 = PWM(Pin(11), freq=50)
pwm_12 = PWM(Pin(12), freq=50)

# 初始化姿态角变量
roll = 0
pitch = 0
yaw = 0

pwm = 0

initial_angle = 96
linmit_angle = 45

initial_pwm = 300

s = 0.1 # 采样时间间隔

sw = 1


while True:
    # 获取六轴加速度计原始值
    try:
        raw_values = mpu.get_values()
    except: 
        mpu = mpu6050.accel(i2c1)
        print("未获取mpu信息")
    
    
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
    #print("加速度 (g)  : X={:.2f}, Y={:.2f}, Z={:.2f}".format(accel_x, accel_y, accel_z))
    #print("角速度 (°/s): X={:.2f}, Y={:.2f}, Z={:.2f}".format(gyro_x, gyro_y, gyro_z))
    #print("姿态角 (°)  : Roll={:.2f}, Pitch={:.2f}, Yaw={:.2f}\n".format(roll, pitch, yaw))
    
    angle = roll - initial_angle

    if roll != 0 and abs(angle) <= linmit_angle and sw == 1:
        
        kp = 0.5
        kd = 0.02
        
        pwm = int(kp * (angle / 180 * 2046) + kd * angle)
        
        
        
        if pwm > 1023: pwm = 1023
        if pwm < -1023: pwm = -1023

        if pwm > 0:
            pwm += initial_pwm
            pwm_12.duty(pwm)
            pwm_11.duty(0)
            
        if pwm < 0: 
            pwm -= initial_pwm
            pwm_12.duty(0)
            pwm_11.duty(abs(pwm))
        
    elif abs(angle) > linmit_angle or sw == 0:
    
        pwm_11.duty(0)
        pwm_12.duty(0)
        
    print(f"Roll = {roll}, Angle = {angle}, PWM = {pwm}")

    time.sleep(s) # 采样时间间隔

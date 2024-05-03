'''
实验名称：六轴加速度计（MPU6050）
版本：v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：编程实现测量MPU6050加速度、角速度和温度值并在终端显示。
'''

from machine import SoftI2C, Pin
import mpu6050
import time

# 构建I2C对象
i2c1 = SoftI2C(scl=Pin(17), sda=Pin(18))

# 构建MPU6050对象
mpu = mpu6050.accel(i2c1)

while True:
    # 获取六轴加速度计原始值
    raw_values = mpu.get_values()
    
    # 计算加速度值
    accel_x = raw_values['AcX'] 
    accel_y = raw_values['AcY'] 
    accel_z = raw_values['AcZ'] 
    
    # 计算角速度值
    gyro_x = raw_values['GyX'] 
    gyro_y = raw_values['GyY'] 
    gyro_z = raw_values['GyZ'] 
    
    # 打印计算好的数值
    print("加速度 (g)  : X={:.2f}, Y={:.2f}, Z={:.2f}".format(accel_x, accel_y, accel_z))
    print("角速度 (°/s): X={:.2f}, Y={:.2f}, Z={:.2f}\n".format(gyro_x, gyro_y, gyro_z))
    
    # 延时1秒
    time.sleep(0.01)
#!/usr/bin/env python

import os
import sys
import time
import matplotlib.pyplot as plt
from simple_pid import PID

class WaterBoiler:
    """
    水壶类，简单模拟了一个能加热水并且水温会随时间逐渐降低的水壶
    """

    def __init__(self):
        self.water_temp = 20  # 初始化水温为20摄氏度

    def update(self, boiler_power, dt):
        """
        更新水温，考虑加热水和热量逐渐散失
        :param boiler_power: 加热器功率
        :param dt: 时间间隔
        :return: 更新后的水温
        """
        if boiler_power > 0:
            # 加热器只能产生热量，不能产生冷
            self.water_temp += 1 * boiler_power * dt

        # 一些热量逐渐散失
        self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    # 设置PID参数并限制输出范围
    pid = PID(90, 0.01, 0, setpoint=water_temp)
    pid.output_limits = (0, 100)

    start_time = time.time()
    last_time = start_time

    # 用于绘图的数值追踪
    setpoint, y, x = [], [], []

    while time.time() - start_time < 10:
        current_time = time.time()
        dt = current_time - last_time

        # 计算PID输出并更新水温
        power = pid(water_temp)
        water_temp = boiler.update(power, dt)

        # 记录时间和温度数据
        x += [current_time - start_time]
        y += [water_temp]
        setpoint += [pid.setpoint]

        # 如果运行时间超过1秒，则将PID设定值设置为100
        if current_time - start_time > 1:
            pid.setpoint = 100

        last_time = current_time

    # 绘制温度随时间变化的图形
    plt.plot(x, y, label='measured')
    plt.plot(x, setpoint, label='target')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    if os.getenv('NO_DISPLAY'):
        # 如果在CI中运行，则将图保存到文件，而不是显示给用户
        plt.savefig(f"result-py{'.'.join([str(x) for x in sys.version_info[:2]])}.png")
    else:
        plt.show()
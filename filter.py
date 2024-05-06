
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

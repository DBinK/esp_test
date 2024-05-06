import bluetooth,ble_simple_peripheral,time
import sys

#构建BLE对象
ble = bluetooth.BLE()

#构建从机对象,广播名称为WalnutPi，名称最多支持8个字符。
ble_client = ble_simple_peripheral.BLESimplePeripheral(ble,name='WalnutPi')


Kp = 3
Ki = 0.0001
Kd = 0.0001

sw = 0
zero_pwm = 100
pid_update = 0

# 接收到主机发来的蓝牙数据处理函数
def on_rx(text):
    global sw, Kp, Ki, Kd, zero_pwm, pid_update
    
    try:
        pid_update = 1
        
        print("RX:",text) #打印接收到的数据,数据格式为字节数组。
        
        #回传数据给主机。
        ble_client.send("I got: ") 
        ble_client.send(text)
        
        hex_data = ['{:02x}'.format(byte) for byte in text]
        
        print(hex_data)
        
        if len(hex_data) > 6:

            if hex_data[6] == '01':  # up
                Kp += 0.1
                
            if hex_data[6] == '02':  # down
                Kp -= 0.1
                
            if hex_data[6] == '08':  # left
                Kd += 0.001
                
            if hex_data[6] == '01':  # right
                Kd -= 0.001
                
            if hex_data[5] == '04':  # y
                Ki *= 10
                
            if hex_data[5] == '02':  # x
                Ki *= 0.1
                
            if hex_data[5] == '08':  # b
                zero_pwm += 10
                
            if hex_data[5] == '10':  # a
                zero_pwm -= 10
                
            if hex_data[5] == '02':  # select
                print("停止接收主机数据")
                ble_client.on_write(None)
                sys.exit()
                
            if hex_data[5] == '01':  # start
                
                if sw == 0:
                    sw = 1
                else:
                    sw = 0
                    #pwm_down()
                    
                print(f"开关电机控制: {sw}")
                
        print(f"Kp = {Kp}, Ki = {Ki}, Kd = {Kd}, zero_pwm = {zero_pwm}")
        
        
    except (OSError, RuntimeError) as e:
    
        print(f"错误原因：{e}")
        ble_client.on_write(None)
        sys.exit()


#从机接收回调函数，收到数据会进入on_rx函数。
ble_client.on_write(on_rx)

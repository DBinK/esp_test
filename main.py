import bluetooth,ble_simple_peripheral,time
import sys
import motion

#构建BLE对象
ble = bluetooth.BLE()

#构建从机对象,广播名称为WalnutPi，名称最多支持8个字符。
ble_client = ble_simple_peripheral.BLESimplePeripheral(ble,name='WalnutPi')

car_sw = 0
rotate_sw = 0
go_sw = 0

# 接收到主机发来的蓝牙数据处理函数
def on_rx(text):
    global car_sw, rotate_sw
    
    try:        
        print("RX:",text) #打印接收到的数据,数据格式为字节数组。
        
        #回传数据给主机。
        ble_client.send("I got: ") 
        ble_client.send(text)
        
        hex_data = ['{:02x}'.format(byte) for byte in text]
        
        print(hex_data)
        
        if len(hex_data) > 6:
            
            
            if (hex_data[6] == '00' or hex_data[7] == '00') and rotate_sw == 0:
                motion.stop()
                    
            if hex_data[6] == '01':  # up
                motion.go_forward(800)
                
            if hex_data[6] == '02':  # down
                motion.go_backward(800)
                
            if hex_data[6] == '04':  # left
                motion.go_left(600)
                
            if hex_data[6] == '08':  # right
                motion.go_right(600)
                
            if hex_data[5] == '04':  # y
                
                if rotate_sw == 0 :
                    rotate_sw = 1 
                    motion.turn_right(50)
                else:
                    rotate_sw = 0
                    motion.stop()
                
            if hex_data[5] == '20':  # x
                if rotate_sw == 0 :
                    rotate_sw = 1 
                    motion.turn_left(200)
                else:
                    rotate_sw = 0
                    motion.stop()
                
            if hex_data[5] == '08':  # b
                motion.turn_right(100)
                
            if hex_data[5] == '10':  # a
                motion.turn_left(300)
                
            if hex_data[5] == '02':  # select
                print("停止接收主机数据")
                
                if car_sw == 0 :
                    car_sw = 1 
                else:
                    car_sw = 0
                    motion.stop()

                ble_client.on_write(None)
                sys.exit()
                
            if hex_data[5] == '01':  # start
                
                if car_sw == 0:
                    car_sw = 1
                else:
                    car_sw = 0
                    motion.stop()
                    
                print(f"开关电机控制: {car_sw}")
        
    except (OSError, RuntimeError) as e:
    
        print(f"错误原因：{e}")
        ble_client.on_write(None)
        sys.exit()

#从机接收回调函数，收到数据会进入on_rx函数。
ble_client.on_write(on_rx)

while True:
    
    time.sleep(0.5)


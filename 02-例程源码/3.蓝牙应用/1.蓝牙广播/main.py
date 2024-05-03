'''
实验名称：蓝牙广播
版本：v1.0
作者：WalnutPi
说明：编程实现核桃派PicoW进行蓝牙广播（从机），让手机搜索到该设备。
'''

import bluetooth,ble_simple_peripheral,time

#构建BLE对象
ble = bluetooth.BLE()

#构建从机对象,广播名称为WalnutPi，名称最多支持8个字符。
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='WalnutPi')
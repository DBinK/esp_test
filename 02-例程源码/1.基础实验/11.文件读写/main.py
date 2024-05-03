'''
实验名称：线程
版本： v1.0
作者：WalnutPi
实验平台：核桃派PicoW
说明：文件读写，将WalnutPi写入文件后再读取出来。
'''

###########
## 写文件
###########
f = open('1.txt', 'w') #以写的方式打开一个文件，没有该文件就自动新建
f.write('WalnutPi') #写入数据
f.close() #每次操作完记得关闭文件

###########
## 读文件
###########
f = open('1.txt', 'r') #以读方式打开一个文件
text = f.read()
print(text) #读取数据并在终端打印
f.close() #每次操作完记得关闭文件



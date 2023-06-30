# coding=utf-8
import asyncio
import json
import sys
import threading
import time
from socket import *
import ctypes
import base64
import re
import datetime

Objdll = ctypes.windll.LoadLibrary("SWHidApi.dll")
# Objdll = ctypes.cdll.LoadLibrary("libSWHidApi.so")
# print(Objdll)

iUsbNum = int(0)
iUsbNum = Objdll.SWHid_GetUsbCount()
if iUsbNum == 0:
    print("没有USB设备")
if Objdll.SWHid_OpenDevice(0) == 1:  # open device
    print("设备打开成功")
else:
    print("设备打开失败，请连接设备并重启应用")

Objdll.SWHid_ClearTagBuf()  # start to get data
Objdll.SWHid_SetDeviceOneParam(255, 2, 0)  # set Workmode as AnswerMode

try:
    HOST = sys.argv[2]
except:
    HOST = '10.0.0.226'
    print("错误：未设置通讯地址，正在使用默认地址", HOST)

PORT = 8003
BUF_SIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


def doConnect():
    # socket连接服务器

    # 握手
    dic = "aaaaaaaaaaaaaaaaa"
    woshou = json.dumps(dic)
    tcpCliSock.sendall(woshou.encode('utf-8'))
    woshou = tcpCliSock.recv(BUF_SIZE)
    print("连接服务器成功")
    # print(woshou)

    try:
        mid = sys.argv[1]
        print("当前登录设备：", mid)
    except:
        mid = 17
        print("错误:没有设备参数，联系管理员，当前使用设备号：", mid)

    # 发送设备编号
    dic = {'task': "terminal_rfid", 'mid': mid}
    data1 = json.dumps(dic)
    tcpCliSock.sendall(data1.encode('utf-8'))
    data1 = tcpCliSock.recv(BUF_SIZE)  # 接收
    recv_data = data1.decode('utf-8', errors='ignore')  # 解码
    recv_data = recv_data[1:]  # 去掉前缀
    recv_data = json.loads(recv_data)  # 转换成JSON格式
    # print(recv_data)


def is_hex_string(s):
    # s = s.upper().lstrip("OX")
    # if all(c.isdigit() or c.isalpha() for c in s):
    #     return True
    # else:
    #     return False
    pattern = "^[0-9A-Fa-f]+$"
    return re.match(pattern, s) is not None


def write_hex(data):
    password = bytes(b'\x00\x00\x00\x00')
    # WriteEPC = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xDD'
    data = base64.b16decode(data)
    wait_time = 0
    while True:
        if Objdll.SWHid_WriteEPCG2(255, password, data, 6) == 1:
            timestamp = str(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'))
            print("写入成功! ", '写入数据: ', write_data, '写入时间：', timestamp)  # 打印写入数据和时间
            break
        else:
            wait_time += 1
            print("请将标签放置在写卡器上，超时等待", wait_time, "秒")
            if wait_time >= 20:
                print("写入超时")
                break
        time.sleep(1)


doConnect()


def test():
    while True:
        test_str = "aaaaaaaaaaaaaaaaaaaaaaaa"
        test_message = json.dumps(test_str)
        tcpCliSock.sendall(test_message.encode('utf-8'))
        time.sleep(15)


def socket():
    # 循环接收服务器信息
    global tcpCliSock
    global write_data
    while True:
        # if not data1:
        #     break
        # data1 = input('>')

        try:
            data1 = tcpCliSock.recv(BUF_SIZE)  # 接收
            recv_data = data1.decode('utf-8', errors='ignore')  # 解码
            recv_data = recv_data[1:]  # 去掉前缀
            recv_data = json.loads(recv_data)  # 转换成JSON格式

            # print(recv_data)

            if recv_data['success']:
                if len(recv_data['hex']) == 24 and is_hex_string(recv_data['hex']):
                    write_data = recv_data['hex'].upper()
                    write_hex(write_data)
                else:
                    print("接收数据有误")

        except error:
            pass
            try:
                tcpCliSock = socket(AF_INET, SOCK_STREAM)
                tcpCliSock.connect(ADDR)
                doConnect()
            except error:
                print("无法与服务器连接，尝试重连")
                time.sleep(1)
                pass
            continue
            # time.sleep(1)
            # print("error 1")
            # while True:
            #     try:
            #         doConnect()
            #     except error:
            #         time.sleep(1)
            #         print("error 2")
            #         pass


thread1 = threading.Thread(target=socket)
thread2 = threading.Thread(target=test)


thread1.start()
thread2.start()

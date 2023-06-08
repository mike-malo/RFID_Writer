#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ctypes
import time

Objdll = ctypes.windll.LoadLibrary('D:\\project\\Python\\X64\\USB\\SWHidApi.dll')
# Objdll = cdll.LoadLibrary("./libSWHidApi.so")
print(Objdll)

iUsbNum = int(0)
iUsbNum = Objdll.SWHid_GetUsbCount()
if iUsbNum == 0:
    print("No USB Device")
if Objdll.SWHid_OpenDevice(0) == 1:  # open device
    print("OpenSuccess")
else:
    print("OpenError")

Objdll.SWHid_ClearTagBuf()  # start to get data
Objdll.SWHid_SetDeviceOneParam(255, 2, 0)  # set Workmode as AnswerMode

# def read():
#     while True:
#         arrBuffer = bytes(9182)
#         iTagLength = c_int(0)
#         iTagNumber = c_int(0)
#         ret = Objdll.SWHid_GetTagBuf(arrBuffer, byref(iTagLength), byref(iTagNumber))
#         if iTagNumber.value > 0:
#             iIndex = int(0)
#             iLength = int(0)
#             bPackLength = c_byte(0)
#             for iIndex in range(0, iTagNumber.value):
#                 bPackLength = arrBuffer[iLength]
#                 str2 = ""
#                 str1 = ""
#                 str1 = hex(arrBuffer[1 + iLength + 0])
#                 str2 = str2 + "Type:" + str1 + " "  # Tag Type
#                 str1 = hex(arrBuffer[1 + iLength + 1])
#                 str2 = str2 + "Ant:" + str1 + " Tag:"  # Ant
#                 str3 = ""
#                 i = int(0)
#                 for i in range(2, bPackLength - 1):
#                     str1 = hex(arrBuffer[1 + iLength + i])
#                     str3 = str3 + str1 + " "
#                 str2 = str2 + str3  # TagID
#
#                 str1 = hex(arrBuffer[1 + iLength + i + 1])
#                 str2 = str2 + "RSSI:" + str1  # RSSI
#                 iLength = iLength + bPackLength + 1
#                 print(str2)  # print information


while True:
    password = bytes(b'\x00\x00\x00\x00')
    WriteEPC = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xDD'
    if Objdll.SWHid_WriteEPCG2(255, password, WriteEPC,
                               6) == 1:
        # 255 mean address, use 255.  password is tag password default is 00000000,  WriteEPC is
        # "00112233445566778899AABB" 12bytes, 6 mean 12/2=6 word
        print("WriteSuccess")
        # read()
        now = time.time()
        break
    else:
        print("WriteError")
    # if you want to write user area, SWHid_WriteCardG2(unsigned char bDevAdr, unsigned char * Password,
    # unsigned char Mem, unsigned char WordPtr,unsigned char Writelen, unsigned char * Writedata);

    # mem = c_int(0)  # 3 mean user area,
    # wordptr = c_int(0)  # 0 mean first address
    # writelen = c_int(6)  # 6 mean 12bytes
    # Writedata = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB'
    # if Objdll.SWHid_WriteCardG2(255, password, mem, wordptr, writelen, WriteEPC) == 1:
    #     print("WriteSuccess")
    # else:
    #     print("WriteError")

    time.sleep(1)

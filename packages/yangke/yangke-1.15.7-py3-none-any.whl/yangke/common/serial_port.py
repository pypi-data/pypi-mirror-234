import serial
from yangke.common.config import logger
import re
import time

portx = "COM1"
bps = 9600

ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE, stopbits=1)


def main():
    while True:
        count = ser.inWaiting()  # 获取串口缓冲区数据
        if count != 0:
            recv = ser.read(ser.in_waiting).decode("gbk")
            logger.debug(recv)
            send = str(float(recv) + 1)
            logger.debug(send.encode())
            ser.write(send.encode())


main()

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : utils.py
@Author  : Gyanano
@Time    : 2023/9/22 14:33
"""
import platform
import socket


# 获取本机IP地址
def get_ip_address():
    if platform.system() == 'Windows':
        # print(socket.gethostbyname(socket.gethostname()))  # 192.168.123.238 = socket.gethostbyname('Gyan')
        return socket.gethostbyname(socket.gethostname())
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        sock_name = sock.getsockname()[0]
        sock.close()
        return sock_name


# 获取设备信息
def get_device_info():
    device_name = socket.gethostname()
    device_ip = get_ip_address()  # 替换成你的网卡名称
    return {
        'name': device_name,
        'ip': device_ip
    }


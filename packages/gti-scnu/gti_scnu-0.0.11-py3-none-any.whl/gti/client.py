#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stream_client.py
@Author  : Gyanano
@Time    : 2023/9/19 17:06
"""
import json
import os.path
import socket
import struct
import threading
import time

from gti import utils
from gti.data_packet import *
from gti.decoder import Decoder
from gti.encoder import Encoder
from gti.parser import Parser


class GTIClient:
    """
    GTI 客户端，用于利用 UDP 搜索设备，并向 GTI 的 Socket 服务器发送数据包，并接收 GTI 服务器返回的数据包
    1. 搜索设备：广播方式发送搜索命令，接收设备的回复，并将设备的 address 信息添置到列表中，一个设备为一个字典
    2. 连接设备：只用 TCP 连接设备
    - UDP 仅用于搜索设备
    """

    def __init__(self, broadcast_address=('255.255.255.255', 14999), udp_listen_port=14998, tcp_port=16999):
        """
        初始化客户端，获取当前设备信息并创建 TCP 客户端和 UDP 广播客户端以及可连接设备空列表
        :param broadcast_address: 广播地址和端口
        :param tcp_port: TCP 端口，由于 TCP 的 IP 会跟连接的设备有关，所以这里只设置端口
        """
        self.broadcast, self.response_listener, self.tcp_client = None, None, None
        self.device_info = utils.get_device_info()  # 获取本机设备信息
        self.broadcast_address, self.udp_listen_port, self.tcp_port = broadcast_address, udp_listen_port, tcp_port
        self.create_broadcast_client()
        self.create_response_listener()
        self.create_tcp_client()
        self.active_devices = {}
        self.history_addr = None
        self.search_device()

    """
    ========== UDP 模式 ==========
    """

    def search_device(self):
        """
        搜索设备，广播方式发送搜索命令，接收设备的回复，并将设备的 address 信息添置到列表中
        :return: None
        """
        # 清空设备列表
        self.active_devices.clear()

        # 利用 UDP 广播搜索设备，持续搜索一段时间
        thread1 = threading.Thread(target=self.response_listen_thread)
        thread1.start()
        self.broadcast.sendto(json.dumps({
            'cmd': 'search_device',
            'device_info': self.device_info
        }).encode('utf-8'), self.broadcast_address)
        # 因为 udp socket 设置了 3 秒的超时时间，所以这里只需要等线程结束即可
        thread1.join()

    def choice_device(self):
        if not self.active_devices:
            exit()
        # if 'robot1' in self.active_devices:
        #     self.connect(self.active_devices['robot1']['ip'], self.active_devices['robot1']['port'])
        #     print(self.active_devices['robot1'])
        #     return
        device_to_connect = input('请输入要连接的设备代号（例：robot1）：')
        if device_to_connect in self.active_devices:
            print('开始连接设备')
            self.connect(self.active_devices[device_to_connect]['ip'],
                         self.active_devices[device_to_connect]['port'])
            print(self.active_devices[device_to_connect])
        else:
            print('输入的设备名不存在')
            exit(0)

    def create_broadcast_client(self):
        # 创建 UDP 客户端并设置广播模式，用于广播搜索设备
        self.broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def create_response_listener(self):
        # 创建 UDP 客户端，用于监听设备搜索请求的回应
        self.response_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.response_listener.bind(('', self.udp_listen_port))
        self.response_listener.settimeout(3)

    def response_listen_thread(self):
        # 监听设备搜索请求的回应，一直监听
        print('正在搜索设备')
        while True:
            try:
                # print('等待设备回应')
                data, addr = self.response_listener.recvfrom(1024)
                # 收到设备回应后，将设备的 address 信息添加到列表中
                parsed_data = json.loads(data.decode('utf-8'))  # {'name': device_name,'ip': device_ip}
                # print(f'从 {addr} 处收到设备回应，内容为：{data}')
                self.active_devices[f'robot{len(self.active_devices) + 1}'] = {
                    'name': parsed_data.get('name'),  # 'name': device_name
                    'ip': parsed_data.get('ip'),
                    'port': self.tcp_port
                }
                # print(f'当前可连接设备列表：{self.active_devices}')
            except socket.timeout:
                print('搜索设备完成')
                # print(f'当前可连接设备列表：{self.active_devices}')
                print(f'当前可连接设备列表:\n',
                      '\n'.join([f'\t{k}: [设备名：{v["name"]}，设备IP：{v["ip"]}]' for k, v in self.active_devices.items()]))
                break

    """
    ========== TCP 模式 ==========
    """

    def create_tcp_client(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.settimeout(60)  # 设置超时时间为 30 秒

    def connect(self, address, port):
        self.tcp_client.connect((address, port))
        self.history_addr = (address, port)
        print('连接成功')

    def if_connected(self):
        """
        判断当前的 tcp socket 对象是否已经连接设备
        :return: True or False
        """
        try:
            self.tcp_client.getpeername()
            return True
        except OSError:
            return False

    def send(self, data_to_send, data_type: int = 0, timeout: int = 10):
        """
        发送数据，会先自动对内容进行预处理和编码，再打包成数据包，然后再发送
        :param data_to_send: 指定要发送的数据，如果是文件则是文件路径，如果是代码则是代码字符串或者文件路径，如果是图像或者视频则是文件路径，如果是音频则是文件路径
        :param data_type: 数据类型，目前支持 0:file | 1:code | 2:image/video | 3:audio
        :param timeout: 超时时间
        :return: 返回函数执行结果
        """
        # 先判断 history_addr 是否存在，如果不存在则说明没有连接设备，需要先连接设备
        if not self.if_connected() and self.history_addr:
            print('重新连接设备')
            self.create_tcp_client()
            self.connect(self.history_addr[0], self.history_addr[1])
        # 设置超时时间
        self.tcp_client.settimeout(timeout)
        try:
            if data_type == 0:
                # 下面这句是检查文件是否存在以及是否是支持的文件类型，如果是则返回内容
                self.send_file(data_to_send)
            elif data_type == 1:
                data_frame, data = self.send_code(data_to_send)
                return data
            elif data_type == 2:
                self.send_video(data_to_send)
            elif data_type == 3:
                self.send_audio(data_to_send)
            else:
                raise TypeError('你正在尝试发送不支持的数据类型！')
        except socket.timeout:
            print('发送数据超时')
            # 关闭连接
            self.close()
            # 杀死进程
            os.kill(os.getpid(), 9)

    def send_file(self, file_path):
        data_packet = Parser.parse_file(file_path)
        self.tcp_client.send(data_packet)

    def send_code(self, code):
        """
        发送代码，此处的 code 可以是代码字符串，也可以是代码文件路径
        :param code: 代码字符串或者代码文件路径
        :return:
        """
        start = time.time()
        data_packet = Parser.parse_code(code)
        print('packet use time:', time.time() - start, 's')
        self.tcp_client.send(data_packet)
        print('send use time:', time.time() - start, 's')
        # 接收来自服务器的回应
        data_frame, response_data = self.recv_response()
        # print('response_data', response_data)
        print('recv use time:', time.time() - start, 's')
        return data_frame, response_data

    def send_video(self, image_path):
        pass

    def send_audio(self, audio_path):
        pass

    def recv_response(self) -> tuple:
        """
        接收来自服务器的回应，收到的回应是一个数据包，需要解码后才能得到实际数据
        :return:
        """
        # 定义一个 bytes 类型的接收变量
        response_packet = b''
        # 接收帧头，获取数据长度
        response_packet += self.tcp_client.recv(4)
        frame_length = struct.unpack('<I', response_packet)[0] + 12
        # print('frame_length', frame_length)
        # 接收一个包的数据
        while frame_length > 0:
            chunk_size = frame_length
            received_data = self.tcp_client.recv(chunk_size)
            if not received_data:
                # 处理连接关闭或其他错误的情况
                raise ConnectionError("Connection closed or error while receiving data")
            response_packet += received_data
            frame_length -= len(received_data)
        # # 测试一次性接收的速度
        # response_packet += self.tcp_client.recv(frame_length)
        # 解数据包，获取到实际数据(dataframe, data)
        # print('real_length', len(response_packet))
        return Decoder.unpack(response_packet)

    def close(self):
        """
        关闭已有的连接
        :return: None
        """
        print('正在关闭连接')
        # 向服务器发送关闭连接的请求
        data_packet = Encoder.pack(
            'Close connection!'.encode('utf-8'),
            End(),
            False
        )
        self.tcp_client.send(data_packet)
        try:
            self.recv_response()
        except Exception as e:
            print('关闭连接失败，错误：', e)
        # 关闭连接
        if self.if_connected():
            self.tcp_client.close()
        print('连接已关闭')


#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stream_server.py
@Author  : Gyanano
@Time    : 2023/9/19 17:06
@Function: 这里是服务器端，用于监听客户端的连接请求，接收客户端发送的数据包，
解析数据包，执行相应的命令，然后将执行结果返回给客户端。
"""
import re
import gc
import sys
import time
import json
import os.path
import socket
import struct
import subprocess
import threading
import collections
import importlib
import numpy as np


from gti import utils
from gti.decoder import Decoder
from gti.data_packet import *
from gti.encoder import Encoder

main_path = r'/home/pi/class'  # 读取和保存文件所用主文件夹（树莓派上）
gti_path = r'/home/pi/class/gti_files'  # GTI 文件夹（树莓派上）
system_platform = sys.platform    # 用于判断系统是否为win
if 'win' in system_platform:
    current_path = os.getcwd()    # 获取当前文件（exe）的位置
    main_path = current_path + r'/resources/assets/class'
    gti_path = current_path + r'/resources/assets/class/gti_files'


class UDPServer:
    def __init__(self, listen_port: int = 14999, response_port: int = 14998):
        """
        初始化服务器，创建用于监听 UDP 的服务器，主要用于监听和回应设备搜索请求
        - 初始化时将本机设备的信息保存到类属性中，因为回应设备搜索请求时的数据是一样的，都是本机设备的信息
        - 创建两个 UDP 客户端，一个用于监听广播搜索设备时的请求，一个用于回应搜索请求
        :param listen_port: 监听端口
        """
        self.listen_server, self.response_server = None, None
        self.listen_port, self.response_port = listen_port, response_port
        self.device_info = utils.get_device_info()  # {'name': 'Gyan', 'ip': '192.168.123.238'}
        self.create_listen_server()
        self.create_response_server()
        self.pending_devices = collections.OrderedDict()

    def create_response_server(self):
        # 创建用于回应设备搜索请求的 UDP 服务器，设置为广播模式
        self.response_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.response_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def create_listen_server(self):
        # 创建用于监听设备搜索请求的 UDP 服务器，监听地址和端口由初始化时传入
        self.listen_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_server.bind(('', 14999))  # 只绑定端口，不绑定地址，这样就可以接收局域网下所有地址的请求

    def listen_broadcast_thread(self):
        # 监听广播请求并回应设备信息，一直监听
        while True:
            print('等待广播请求')
            data, addr = self.listen_server.recvfrom(1024)
            # 收到广播请求后，将设备信息推送待处理队列
            # data: b'{"cmd": "search_device", "device_info": {"name": "Gyan", "ip": "xxx"}}'
            print(f'从 {addr} 处收到广播请求，内容为：{data}')
            # 接收到 APP 端的 UDP 请求
            parsed_data = json.loads(data.decode('utf-8'))
            if parsed_data.get('cmd') == 'search_device':
                # 并确定为搜索请求后，将设备信息推送待处理队列
                print('收到搜索设备请求')
                self.pending_devices[addr] = parsed_data.get('device_info')

    def send_broadcast_thread(self):
        # 回应设备搜索请求，一直监听 pending_devices 队列
        while True:
            if self.pending_devices:
                print('回应设备搜索请求')
                addr, data = self.pending_devices.popitem(last=False)
                # addr: (ip, port); data: device_info  {'name': device_name,'ip': device_ip}
                self.response_server.sendto(json.dumps(self.device_info).encode('utf-8'), (addr[0], self.response_port))
                print(f'已回应设备搜索请求，内容为：{data}')
            time.sleep(0.1)

    def start_broadcast(self):
        threading.Thread(target=self.listen_broadcast_thread, args=()).start()

    def start_response(self):
        threading.Thread(target=self.send_broadcast_thread, args=()).start()

    def start(self):
        self.start_broadcast()
        self.start_response()


class TCPServer:
    """
    这个 TCP Server 是树莓派上运行的，用于监听客户端的连接请求，然后接收客户端发送的数据包，解析数据包，执行相应的命令，然后将执行结果返回给客户端
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 16999, max_conn: int = 5, file_path: str = main_path + r'/gti_files/AppFuncMapServer.json'):
        self.img = None
        self.server = None
        self.host = host
        self.port = port
        self.max_conn = max_conn
        self.create_server()
        self.library_map = {}  # 用于存储导入的库，key 为库名，value 为库
        self.object_map = {}  # 用于存储实例化的对象，key 为对象名，value 为对象
        self.json_map = self.load_json_map(file_path)

    def create_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))  # 绑定地址和端口
        self.server.listen(self.max_conn)

    @staticmethod
    def load_json_map(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_map = json.load(f)
        return json_map

    def listen(self):
        while True:
            conn, addr = self.server.accept()
            # 开启一个线程处理客户端的请求
            try:
                threading.Thread(target=self.handle_connection, args=(conn, addr,)).start()
            except Exception as e:
                self.library_map.clear()
                self.object_map.clear()
                # 手动调用垃圾回收
                gc.collect()

    def handle_connection(self, conn, addr, buf_size: int = 1024):
        """
        处理客户端的请求，要求既能接收单次数据，也能接收连续的数据，例如视频流，音频流等
        :param conn: 连接对象
        :param addr: 连接地址
        :param buf_size: 缓冲区大小，默认为 1024
        :return:
        """
        print(f'与 {addr} 建立连接')
        with conn:
            while True:
                # 不断接收数据包，这里面是一个死循环，直到客户端主动关闭连接
                try:
                    # 定义一个 bytes 类型的接收变量
                    packet = b''
                    # 接收帧头，获取数据长度
                    packet += conn.recv(4)
                    frame_length = struct.unpack('<I', packet)[0] + 12
                    start_time = time.time()
                    # 接收一个包的数据
                    while True:
                        if frame_length >= buf_size:
                            packet += conn.recv(1024)
                            frame_length -= 1024
                        elif frame_length > 0:
                            packet += conn.recv(frame_length)
                            break
                except Exception as e:
                    # 处理客户端主动关闭连接的情况
                    print(e)
                    self.library_map.clear()
                    self.object_map.clear()
                    # 手动调用垃圾回收
                    gc.collect()
                    break
                print('接收数据包耗时：', time.time() - start_time, 's')
                # 接收一个包完毕后，解码数据，直接用 Decoder 解码
                start_time = time.time()
                data_frame, data = Decoder.unpack(packet)  # 这里的 data 是 bytes 类型
                try:
                    # 根据数据类型执行相应的操作
                    continue_flag, response_data = self.handle_unpack(data_frame)
                    # print('continue_flag:', continue_flag, 'response_data:', response_data)
                    # 如果需要继续接收数据包，则将提示信息打包发送给客户端
                    self.send_response_data(conn, response_data)
                    if not continue_flag:
                        # 如果不需要继续接收数据包，则将提示信息打包发送给客户端，并跳出循环
                        # 释放 self.library_map 和 self.object_map 中的资源
                        self.library_map.clear()
                        self.object_map.clear()
                        # 手动调用垃圾回收
                        gc.collect()
                        break
                except Exception as e:
                    print(data_frame.data.decode('utf-8'), "出错了！")
                    print(e)
                    conn.sendall(str(e).encode('utf-8'))
                print('处理数据包耗时：', time.time() - start_time, 's')
        print(f'与 {addr} 的连接已关闭')

    def handle_unpack(self, data_frame):
        """
        根据数据类型执行相应的操作，并返回执行结果或者提示信息交给函数外面代码来决定是否进行打包发送
        :param data_frame: DataFrame 对象
        :return: bool, any 是否需要继续接收数据包，以及提示信息
        """
        print('handle_unpack')
        print('data_frame.data:', data_frame.data)
        # 根据数据类型执行相应的操作
        if data_frame.frame_type == 0:
            # 如果是文件，则将文件保存到指定位置
            self.save_file_content(os.path.join(gti_path, data_frame.data['name']), data_frame.data['content'])
            # 返回普通信息给客户端
            return True, f'文件 {data_frame.data["name"]} 保存成功'
        elif data_frame.frame_type == 1:
            # 看看是否是结构化数据，如果是说明这是个代码文件，否则是代码字符串
            if data_frame.structured:
                return self.run_code_file(data_frame)
            else:
                # 如果不是结构化数据，则说明是代码字符串，那么需要判断属于哪种情况，是导入库还是代码字符串
                code_str = data_frame.data.decode('utf-8')
                print('code_str:', code_str)
                flag, data = self.run_code_partly(code_str)
                # print('flag:', flag, 'data:', data)
                return flag, data
        elif data_frame.frame_type == 2:
            return True, f'图像 {data_frame.data["name"]} 保存成功'
        elif data_frame.frame_type == 3:
            return True, f'音频 {data_frame.data["name"]} 保存成功'
        elif data_frame.frame_type == 4:
            return True, f'成功接收指令'
        elif data_frame.frame_type == 5:
            return False, f'结束'
        else:
            raise TypeError('接收的数据包似乎出了错误！')

    def run_code_file(self, data_frame):
        # 如果是结构化数据，则说明是代码文件，先将代码文件保存到指定位置，然后再用子进程执行代码文件
        self.save_file_content(os.path.join(gti_path, 'temp.py'), data_frame.data['content'])
        # 执行代码文件
        process = subprocess.Popen(
            ['python', os.path.join(gti_path, 'temp.py')],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = process.communicate()
        # 将执行结果返回给客户端
        result = output if output else error
        # 删除临时文件
        os.remove(os.path.join(gti_path, 'temp.py'))
        return True, f"{data_frame.data['name']}文件执行成功，结果为：{result}"

    def run_code_partly(self, code_str):
        print('run_code_partly')
        # 此处逻辑比较复杂，先判断属于哪种情况，在调用响应的函数处进行处理
        import_lib = r'(from.*?control.*?import.*?(\w+)(.*?as.*?(\w+))?)|(import.*?)(\w+)'  # 用于匹配导入的库
        lib_match = re.search(import_lib, code_str)
        if lib_match:
            # 如果匹配到了导入语句，则执行导入语句
            if lib_match.group(4):
                self.library_map[lib_match.group(4)] = importlib.import_module(f'control.{lib_match.group(2)}')
            elif lib_match.group(2):
                self.library_map[lib_match.group(2)] = importlib.import_module(f'control.{lib_match.group(2)}')
            elif lib_match.group(6):
                self.library_map[lib_match.group(6)] = importlib.import_module(f'{lib_match.group(6)}')
            # 将执行结果返回给客户端
            return True, f'导入{lib_match.group()}成功'

        assignment = r'(\w+).*?=.*?(\w+\..*?)\((.*?)\)'  # 用于匹配实例化 control 库中的类的实例名
        assignment_match = re.search(assignment, code_str)
        if assignment_match:
            # 遇到赋值语句，将赋值语句结果保存到字典中，key 为实例名，value 为实例化对象
            lib_name, func_name = assignment_match.group(2).split('.')
            # 如果有参数，则需要将参数转换成对应的类型
            if assignment_match.group(3):
                self.object_map[assignment_match.group(1)] = self.library_map[lib_name].__getattribute__(
                    func_name)(eval(assignment_match.group(3)))
            # 如果没有参数，则直接实例化
            else:
                self.object_map[assignment_match.group(1)] = self.library_map[lib_name].__getattribute__(func_name)()
            # 将执行结果返回给客户端
            return True, f'实例化{func_name}成功，实例名为{assignment_match.group(1)}'

        func_pattern = r"((\w+)\.)?(\w*?)(\(.*?\))"  # 用于匹配调用的函数
        func_call_match = re.search(func_pattern, code_str)
        if func_call_match:
            if func_call_match.group(2):  # if 'm':
                # 说明有实例化对象
                if func_call_match.group(2) in self.library_map.keys():
                    result = self.choose_lib_or_class(func_call_match, self.library_map)
                else:
                    result = self.choose_lib_or_class(func_call_match, self.object_map)
            else:
                # 说明没有实例化对象
                result = eval(code_str)
            # 将执行结果返回给客户端
            return True, result if result else f'执行{code_str}成功\n'
        # 如果都没有匹配到，直接错误
        raise TypeError('接收的数据包似乎出了错误！')

    def choose_lib_or_class(self, func_call_match, caller_map):
        if func_call_match.group(4) == '()':
            if func_call_match.group(3) in self.json_map.get('function').keys():
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    self.json_map.get('function').get(func_call_match.group(3)))()
            else:
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    func_call_match.group(3))()
        elif len(func_call_match.group(4).split(',')) > 1:
            if func_call_match.group(3) in self.json_map.get('function').keys():
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    self.json_map.get('function').get(func_call_match.group(3)))(*eval(func_call_match.group(4)))
            else:
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    func_call_match.group(3))(*eval(func_call_match.group(4)))
        elif len(func_call_match.group(4).split(',')) == 1:
            if func_call_match.group(3) in self.json_map.get('function').keys():
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    self.json_map.get('function').get(func_call_match.group(3)))(eval(func_call_match.group(4)[1:-1]))
            else:
                result = getattr(
                    caller_map[func_call_match.group(2)],
                    func_call_match.group(3))(eval(func_call_match.group(4)[1:-1]))
        else:
            raise TypeError('参数错误')
        return self.process_result(result)

    def process_result(self, result):
        """
        处理执行结果，将执行结果的实际情况判断是否需要进行数据抽取，不需要则直接返回原结果
        :param result: 执行结果
        :return: 处理后的结果
        """
        try:
            if result.get('type') == 'img':
                # 如果是图像数据，则返回图像的数据
                return result.get('data')
            elif result.get('type') == 'audio':
                # 如果是音频数据，则返回音频的数据
                return result.get('data')
        except Exception as e:
            print('解析失败，原因是：', e)
            return result

    def send_response_data(self, conn, response_data):
        # 需要看看响应数据是什么类型的，如果是图片，需要打包成图片数据包，如果是音频，需要打包成音频数据包，其他类似
        if isinstance(response_data, str):
            conn.sendall(Encoder.pack(
                response_data.encode('utf-8'),
                Notice(),
                False
            ))
        elif isinstance(response_data, bytes):
            # 如果是 bytes 类型，则说明是文件数据
            conn.sendall(Encoder.pack(
                response_data,
                Notice(),
                False
            ))
        elif isinstance(response_data, np.ndarray):
            # 如果是 numpy 数组，则说明是图像数据，需要将图像数据打包成图像数据包
            if self.img is None:
                self.img = response_data
                print('已经从摄像头获取到图像数据，准备打包成video数据包发送')
                packet_to_send = Encoder.pack(
                    self.library_map['cv2'].imencode('.png', self.img)[1].tobytes(),
                    Video(),
                    False
                )
            else:
                packet_to_send = Encoder.pack(
                    (self.library_map['cv2'].imencode(
                        '.png', response_data - self.img
                    )[1]).tobytes(),
                    Video(),
                    False
                )
            print('packet_to_send len:', len(packet_to_send))
            conn.sendall(packet_to_send)
            print('图像数据发送成功')

    @staticmethod
    def save_file_content(file_path, content):
        """
        将文件内容保存到指定位置，content 可以是 bytes 类型或者 str 类型
        :param file_path: 保存的文件路径（需要包含文件名）
        :param content: 文件的内容，可以是 bytes 类型或者 str 类型
        :return: None
        """
        with open(file_path, 'wb') as wf:
            content = content if isinstance(content, bytes) else content.encode('utf-8')
            wf.write(content)


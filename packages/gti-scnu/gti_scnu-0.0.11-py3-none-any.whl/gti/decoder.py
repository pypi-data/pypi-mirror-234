#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import json
import queue
import struct
from gti.data_packet import *


class MyQueue(queue.Queue, object):

    def __init__(self):
        super(MyQueue, self).__init__()

    def show(self):
        if not self.empty():
            return self.queue[self.qsize() - 1]


class Decoder:
    """
    GIT 数据包解码器，用于将数据解码为实际数据
    主要用于将接收到的数据解码为实际数据
    """

    def __init__(self):
        self.buf = MyQueue()

    @staticmethod
    def unpack(packet: bytes):
        """
        将数据包解码到具体的 DataFrame 对象中，然后从 DataFrame 对象按照数据类型解码到实际数据中
        :param packet: 数据包
        :return: 解包后的字节流数据，bytes 类型
        """
        # 使用 struct 模块将数据解包
        print('start packet unpacking...')
        frame_length = struct.unpack('<I', packet[:4])[0]
        unpacked_data = struct.unpack(f'<IBB{frame_length}sBQB', packet)
        # 先取出数据的类型，然后根据数据类型创建对应的 DataFrame 对象
        data_type = unpacked_data[1]
        if data_type == 0:
            dataframe = File()
        elif data_type == 1:
            dataframe = Code()
        elif data_type == 2:
            dataframe = Video()
        elif data_type == 3:
            dataframe = Audio()
        elif data_type == 4:
            dataframe = Notice()
        elif data_type == 5:
            dataframe = End()
        else:
            raise TypeError('数据类型错误！')
        # 将解包后的数据放入 DataFrame 对象中
        dataframe.length = unpacked_data[0]
        dataframe.frame_type = unpacked_data[1]
        dataframe.frame_seq = unpacked_data[2]
        dataframe.check_bit = unpacked_data[4]
        dataframe.time = unpacked_data[5]
        dataframe.structured = unpacked_data[6]
        dataframe.data = json.loads(unpacked_data[3]) if dataframe.structured\
            else unpacked_data[3]
        print('packet unpacking finished!')
        # 根据 DataFrame 对象的数据类型，将数据解码到实际数据中
        # 直接调用 DataFrame 对象的 decode 方法，可以自动根据数据类型解码到实际数据中
        return dataframe.getdata()


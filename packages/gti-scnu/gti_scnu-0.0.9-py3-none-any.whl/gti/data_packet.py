#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


# GTI 的数据包结构 1 byte -> 255, 2 bytes -> 65535, 4 bytes -> 4294967295: 4G
# length: 帧长度，不包含帧头和帧尾，4 bytes; I
# frame_type: 帧类型（数据类型），1 byte; 0: 文件，1: 代码，2: 图片/视频，3: 音频; B
# frame_seq: 帧序号（用于流媒体传输），1 byte; 0: 第一帧，1: 第二帧，...，255: 第 255 帧; B
# data: 实际数据内容，N bytes; N
# check_bit: 校验位，1 byte; 计算方式：check_bit = sum(data) % 256; B
# time: 时间戳，8 bytes; Q
# structured: 是否为结构化数据，1 byte; 0: 非结构化数据（会被统一认为是文本数据），1: 结构化数据——JSON; B
# length(HAL)   frame_type  frame_seq   data        check_bit(HAL)  time(HAL)   structured
# 4 bytes       1 byte      1 byte      N bytes     1 byte          8 bytes     1 byte
# Total length: 4 + 1 + 1 + N + 1 + 8 + 1 = N + 16 bytes
class DataFrame:
    # 数据帧中的各个部分的索引
    LENGTH = 0
    FRAME_TYPE = 4
    FRAME_SEQ = 5
    END_FRAME = -10
    BYTES_WITHOUT_LOAD = 16

    def __init__(self):
        self.length = None
        self.frame_type = None
        self.frame_seq = None
        self.data = None
        self.check_bit = None
        self.time = None
        self.structured = 0

    def getdata(self) -> tuple:
        return self, self.data


# 文件传输的数据包
class File(DataFrame):
    """
    文件传输的数据包，主要用于上传文件保存等作用
    因此，该数据包的实际数据为文件的字节流，什么文件都可以传输
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 0


# 代码形式的数据包
class Code(DataFrame):
    """
    代码形式的数据包，主要用于远程调用函数
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 1


# 视频形式的数据包
class Video(DataFrame):
    """
    视频形式的数据包，主要用于传输视频流
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 2


# 音频形式的数据包
class Audio(DataFrame):
    """
    音频形式的数据包，主要用于传输音频流
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 3


# 包装通知信息的数据包
class Notice(DataFrame):
    """
    包装通知信息的数据包，主要用于传输通知信息，比如连接成功、连接失败之类的文本信息等
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 4


# 结束连接的数据包
class End(DataFrame):
    """
    结束连接的数据包，主要用于结束连接
    """

    def __init__(self):
        super().__init__()
        self.frame_type = 5

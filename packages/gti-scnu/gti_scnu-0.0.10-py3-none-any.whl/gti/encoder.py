#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import struct
import time


class Encoder:
    """
    GTI 数据包编码器，用于将数据编码为 GTI 数据包
    主要用于将各种数据转为 Bytes 类型的数据包，以便于发送
    """

    @staticmethod
    def pack(data: bytes, dataframe, structured=False):
        """
        将 Dataframe 以及它的各种子类对象打包成数据包
        将 data 转化成 dataframe 对象，然后将 dataframe 对象打包成数据包
        最后说明一下 data 是否为结构化数据
        :param data: 实际数据
        :param dataframe: DataFrame 类型的数据帧，或者它的子类对象
        :param structured: 是否为结构化数据
        :return: 打包好的数据包
        """
        # 先通过对象的 frame_type 看看是否为最初始的 DataFrame 对象，如果是则直接提示错误
        if dataframe.frame_type is None:
            raise TypeError('请使用具体的数据包类型！')
        # 如果不是，则将实际数据修改到对应的 DataFrame 对象中
        dataframe.data = data
        # 计算数据帧中数据的长度
        dataframe.length = len(dataframe.data)
        # 置零帧序
        dataframe.frame_seq = 0
        # 计算校验位
        dataframe.check_bit = sum(dataframe.data) % 256
        # 获取当前时间戳
        dataframe.time = time.time_ns()
        # 判断是否为结构化数据
        dataframe.structured = structured
        # 使用 struct 模块将数据打包成字节流
        return struct.pack(
            f'<IBB{dataframe.length}sBQB',
            dataframe.length,
            dataframe.frame_type,
            dataframe.frame_seq,
            dataframe.data,
            dataframe.check_bit,
            dataframe.time,
            dataframe.structured
        )


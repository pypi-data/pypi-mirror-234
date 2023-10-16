#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import json


class JsonBuilder:
    @staticmethod
    def dump_func_json(func_name, caller_name, alias, *args):
        """
        将函数调用的参数转化为 JSON 格式的字符串
        :param func_name: 函数的名称
        :param caller_name: 调用者的名称
        :param alias: 函数的别名或者说是函数的返回值的别名
        :param args: 函数的参数
        :return: JSON 格式的字符串
        """
        json_dict = {'name': args[0], 'caller': args[1], 'alias': args[2]}
        for param in range(3, len(args)):
            json_dict['arg' + str(param - 2)] = {
                'type': type(args[param]).__name__,
                'value': args[param]
            }
        return json.dumps(json_dict)

    @staticmethod
    def dump_file_json(file_name, file_content: bytes):
        """
        将文件名和文件内容转化为 JSON 格式的字符串
        :param file_name: 文件名
        :param file_content: 文件内容
        :return: JSON 格式的字符串
        """
        json_dict = {'name': file_name, 'content': file_content.decode('utf-8')}
        return json.dumps(json_dict)

    @staticmethod
    def dump_image_json(video_content: list):
        """
        将图片转化为 JSON 格式的字符串
        :param video_content: 图片的 numpy 数组
        :return: JSON 格式的字符串
        """
        json_dict = {'content': video_content}
        return json.dumps(json_dict)


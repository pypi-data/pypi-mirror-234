#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : parser.py
@Author  : Gyanano
@Time    : 2023/9/19 14:58
@Function: 用于解析用户代码，将其转换为可执行的远程模式代码
"""
import json
import os
import re
import ast
import subprocess
import sys
from _ast import stmt
import astor

from gti.data_packet import File, Code
from gti.encoder import Encoder
from gti.json_builder import JsonBuilder


class Parser:
    """
    用于解析用户代码，将其转换为远程模式的代码，即在 JSON 中包含的函数会进行指令发送
    即调用 Sender 的 __call__ 函数，将函数名和参数传入，然后发送给 GTI 服务器
    到 GTI 服务器后，GTI 服务器又会利用解包函数将其解包
    解包后利用 Parser 中的解析函数 parse_packet() 得到原始函数名和参数，然后调用
    """
    main_path = r'/home/pi/class'  # 读取和保存文件所用主文件夹（树莓派上）
    gti_path = r'/home/pi/class/gti_files'  # GTI 文件夹（树莓派上）
    code_path = sys.argv[0]  # blockly 生成的用户代码路径
    system_platform = sys.platform  # 用于判断系统是否为win
    if 'win' in system_platform:
        current_path = os.getcwd()  # 获取当前文件（exe）的位置，即可执行文件所在的文件夹路径
        main_path = current_path + r'/resources/assets/class'
        gti_path = current_path + r'/resources/assets/class/gti_files'

    default_origin_path = code_path
    default_parsed_path = os.path.join(gti_path, 'parsed.py')  # 默认的解析后的代码文件路径
    default_func_map_path = os.path.join(gti_path, 'AppFuncMapClient.json')  # 默认的函数映射文件路径

    # windows 系统下的初始化函数
    def __init__(self, origin_path: str = default_origin_path, parsed_path: str = default_parsed_path, func_map_path: str = default_func_map_path):
        self.origin_path = origin_path
        self.parsed_path = parsed_path
        self.func_map_path = func_map_path
        # lib_list 用于存储库名和库的映射关系
        self.lib_list, self.class_list = [], []
        # pro_processing 用于存储需要提前执行操作的函数
        self.pre_processing = []
        self.func_mapping = self.set_func_mapping()

    def set_func_mapping(self) -> dict:
        with open(self.func_map_path, 'r', encoding='utf-8') as f:
            func_mapping = json.load(f)
        return func_mapping

    @staticmethod
    def parse_file(file_path: str):
        """
        将传入的文件路径的文件内容按照 File 类型打包
        :param file_path: 文件路径
        :return: packet: 打包后的数据包
        """
        # 先检查是否是文件路径且看是否属于支持的文件类型
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] in ['.py', '.txt']:
            # 如果是文件路径，且是支持的文件类型，则读取文件内容并编码
            with open(file_path, 'r') as rf:
                file_content = rf.read()
            # 将文件名字和文件内容先转为 JSON 格式的字符串，然后再进行打包
            packet = Encoder.pack(
                JsonBuilder.dump_file_json(os.path.basename(file_path), file_content.encode('utf-8')).encode('utf-8'),
                File(),
                True
            )
        else:
            # 如果不是文件路径或者不是支持的文件类型，则直接报错，不支持的格式
            raise TypeError(f"Unsupported file type: '{os.path.splitext(file_path)[1]}'")
        return packet

    @staticmethod
    def parse_code(code: str):
        """
        将传入的代码字符串或者代码文件路径的文件内容按照 Code 类型打包
        :param code: 代码字符串或者代码文件路径
        :return: packet: 打包后的数据包
        """
        # 先判断 code 是否是代码文件路径，如果是则读取文件内容
        if os.path.isfile(code) and os.path.splitext(code)[1] in ['.py']:
            with open(code, 'r') as rf:
                code = rf.read()
            # 去掉三个引号之间的注释和 # 号之后的注释，\s 匹配任意空白字符，\S 匹配任意非空白字符
            code = re.sub(r'("""[\s\S]*?""")|(#.*)', '', code).strip()
            # 将文件名字和文件内容先转为 JSON 格式的字符串，然后再进行打包
            packet = Encoder.pack(
                JsonBuilder.dump_file_json(os.path.basename(code), code.encode('utf-8')).encode('utf-8'),
                Code(),
                True
            )
        else:
            # 如果不是文件路径，则说明是代码字符串，不需要转为 JSON 格式的字符串，直接打包
            packet = Encoder.pack(
                code.encode('utf-8'),
                Code(),
                False
            )
        return packet

    def change_code(self):
        module_after_parse = self.get_ast_from_file(self.origin_path)
        with open(self.parsed_path, 'w') as wf:
            wf.write(
                'from gti.client import GTIClient\nclient = GTIClient()\nclient.choice_device()\nimport os\nclient.send("import os", 1)\n\n' +
                astor.to_source(module_after_parse))

        subprocess.call(f"python \"{self.parsed_path}\"", shell=True)
        sys.exit(0)

    def get_ast_from_file(self, file_path) -> ast.Module:
        file_tree = self.remove_annotation(file_path)
        body_list = self.parse_tree(file_tree)
        # 检查是否有需要提前执行的操作
        if self.pre_processing:
            self.check_pre_processing(body_list)
        file_tree.body = body_list
        return file_tree

    @staticmethod
    def remove_annotation(file_path):
        """
        删除代码抽象语法树中的注释
        :param file_path: 代码抽象语法树
        :return: 抽象语法树
        """
        with open(file_path, 'r') as rf:
            file_content = rf.read()
        file_tree = ast.parse(file_content)
        # print(ast.dump(file_tree))
        for node in ast.walk(file_tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                # 说明这个节点是多行注释，删除这部分代码
                file_tree.body.remove(node)
        return file_tree

    def parse_tree(self, file_tree) -> list:
        """
        解析代码抽象语法树
        """
        body_list = []
        for node in file_tree.body:
            # ast.walk 的遍历方式：广度优先，一层一层地遍历
            # ast.iter_child_nodes：只会遍历传入节点的子节点，不会遍历孙子节点之后的节点
            self.parse_node(node, body_list)
            # print(ast.dump(node))
        return body_list

    def parse_node(self, node, ast_list):
        if isinstance(node, ast.ImportFrom) or isinstance(node, ast.Import):
            # 说明这个节点是导入模块的语句
            # 判断是否不是 gpio 库，如果不是则将该语句也加入到 body_list 中，本地也运行该语句
            # print('import: ', ast.dump(node), node.names[0].name)  # node.names[0].name 库名，例如 numpy；node.names[0].asname 库别名，例如 np
            # 需要判断是否是导入 gti 的库，如果在 gti 的库中，则不需要将该语句加入到 ast_list 中
            if astor.to_source(node).strip() == 'from gti.parser import Parser':
                return
            if node.names[0].name != 'gpio':
                ast_list.append(node)
            # 构造 client.send() 语句，用于机器人端导入模块
            node = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id='client', ctx=ast.Load()), attr='send', ctx=ast.Load()),
                    args=[ast.Constant(value=astor.to_source(node)), ast.Constant(value=1)], keywords=[]))
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            # 说明这个节点是赋值语句，有 = 的语句都是赋值语句
            if isinstance(node.value.func, ast.Attribute):
                # 先获取赋值语句的 value 的函数名，然后判断是否是需要两端都运行的函数
                class_name = node.value.func.attr
                if class_name in self.func_mapping.get('both_class'):
                    # 说明是两端都需要运行的类，需要将该语句加入到 body_list 中
                    self.class_list.append(node.targets[0].id)
                    ast_list.append(node)
                    # 构造 client.send() 语句，用于机器人端实例化类
                    node = ast.Expr(value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='client', ctx=ast.Load()), attr='send', ctx=ast.Load()),
                        args=[ast.Constant(value=astor.to_source(node)), ast.Constant(value=1)], keywords=[]))
                elif class_name in self.func_mapping.get('only_class'):
                    # 说明是只有机器人端实例化的类，将初始化的对象加入到 class_list 中
                    self.class_list.append(node.targets[0].id)
                    # 构造 client.send() 语句，用于机器人端实例化类
                    node = ast.Expr(value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='client', ctx=ast.Load()), attr='send', ctx=ast.Load()),
                        args=[ast.Constant(value=astor.to_source(node)), ast.Constant(value=1)], keywords=[]))
            else:
                # 看看这个赋值调用的函数名是不是 “Parser”，如果是则不要将该语句加入到 ast_list 中
                if node.value.func.id == 'Parser':
                    return
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            # 说明这个节点是函数调用语句或者是类对象初始化语句
            # 先获取函数名，然后判断是否是需要机器人执行的函数
            caller_name, func_name = node.value.func.value.id, node.value.func.attr
            # print(caller_name, func_name)
            # 判断是否有 parser 调用的函数，如果有则不需要将该语句加入到 ast_list 中
            if caller_name == 'parser':
                return
            # 判断是否有函数调用前需要执行的语句
            if func_name in self.func_mapping.get('pre_processing'):
                # 将函数名加入到 pre_processing 中
                self.pre_processing.append(func_name)
            # 判断对应的类是否在 class_list 中且判断函数名是否在 func_mapping 中
            if func_name in self.func_mapping.get('function'):
                # 构建 remote_res = client.send() 赋值语句，用于机器人端调用函数
                node = ast.Assign(targets=[ast.Name(id='remote_res', ctx=ast.Store())], value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id='client', ctx=ast.Load()), attr='send', ctx=ast.Load()),
                    args=[ast.Constant(value=astor.to_source(node)), ast.Constant(value=1)], keywords=[]))
                ast.fix_missing_locations(node)
            # 判断是否有函数调用后需要执行的语句
            if func_name in self.func_mapping.get('post_processing'):
                # 先将 node 加入到 ast_list 中，然后再将 post_processing 中的语句转为 ast 节点
                ast_list.append(node)
                post_code = self.func_mapping.get('post_processing').get(func_name)
                node = ast.parse(post_code)
        elif isinstance(node, ast.While):
            # 说明这个节点是 while 循环语句
            # 遍历 while 循环体，判断其中的函数调用语句
            # 递归调用 parse_tree 函数，获取 while 循环体中的所有语句，但是要去除掉返回值的第一项，因为第一项是 while 循环的条件
            node.body = self.parse_tree(node)
        elif isinstance(node, ast.If):
            # 说明这个节点是 if 判断语句，if 的判断条件是 node.test，else 和 elif 的判断条件是 node.orelse
            # 遍历 if 判断体，判断其中的函数调用语句
            node.body = self.parse_tree(node)
            if node.orelse:
                # print(parse_tree(node))
                else_list = []
                else_node: stmt
                for else_node in node.orelse:
                    self.parse_node(else_node, else_list)
                node.orelse = else_list
                # node.body = parse_tree(node)
                # node.orelse = parse_tree(node)
            # print('if parse', ast.unparse(node))
        elif isinstance(node, ast.With):
            # 说明这个节点是 with 语句
            # 遍历 with 语句体，判断其中的函数调用语句
            # 递归调用 parse_tree 函数，获取 with 语句体中的所有语句，但是要去除掉返回值的第一项，因为第一项是 with 管理的数据
            node.body = self.parse_tree(node)
        ast_list.append(node)

    def check_pre_processing(self, body_list):
        for func_name in self.pre_processing:
            # 说明有函数调用前需要执行的语句
            pre_codes = self.func_mapping.get('pre_processing').get(func_name)
            pre_code_list = pre_codes.split('\n')
            # 利用 ast.parse() 函数遍历将字符串转为抽象语法树
            for pre_code in pre_code_list:
                if pre_code == '':
                    continue
                # 将 pre_node 从头加入到 ast_list 中
                pre_node = ast.parse(pre_code)
                body_list.insert(0, pre_node)


#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    文件操作类
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""
import os
import shutil
from contextlib import nested

__all__ = ['copy_files', 'copy_file_to']


def copy_files(src, des):
    """
    复制文件
    :param src: 源路径
    :param des: 目标路径
    :return:
    """
    for file_index in os.listdir(src):
        # ./_/*开头文件不处理
        if file_index[0] in ('.', '_', '*'):
            continue
        # 拼接文件
        source_file = os.path.join(src, file_index)
        target_file = os.path.join(des, file_index)
        if os.path.isfile(source_file):
            if not os.path.exists(des):
                os.mkdir(des)
            if not os.path.exists(target_file) or \
                    (os.path.exists(target_file) and os.path.getsize(target_file) != os.path.getsize(source_file)):
                with nested(open(target_file, 'wb'), open(source_file, 'rb')) as (tf, sf):
                    tf.write(sf.read())
        if os.path.isdir(source_file):
            # 递归调用
            copy_files(source_file, target_file)


def copy_file_to(src_file, des_dir):
    """
    复制文件到指定目录
    :param src_file:
    :param des_dir:
    :return:
    """
    shutil.copyfile(src_file, des_dir)

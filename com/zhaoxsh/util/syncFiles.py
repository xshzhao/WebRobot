#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    同步文件到指定文件夹下
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""


import fileUtil

srcPath = 'E:/work/workspace/PyCharm/WebRobot/com/zhaoxsh/busi/'
desPath = 'E:\work\pythonScript'


def sync():
    fileUtil.copy_files(srcPath, desPath)
    print u'同步成功!'


sync()

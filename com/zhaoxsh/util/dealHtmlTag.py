#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    处理html特殊字符
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""
import re

__all__ = ['deal_html_br', 'deal_html_tags']


def deal_html_br(origin_text):
    """
    处理<br/>换行符
    :param origin_text:
    :return:
    """
    # 处理</br></br>替换为换行符
    text = re.sub(r'<br/><br/>|<br/>', '\n', origin_text)
    return text


def deal_html_tags(origin_text):
    """
    处理htmlTag
    :param origin_text:
    :return:
    """
    # 处理</br></br>替换为换行符
    text = re.sub(r'<br />|<strong>|</strong>|<a href=|target="_blank">|<div.*?>|&gt;'
                  r'|<img src=.*?>|<pre.*?class=.*?>|<p><br>.*?</p>|<p>|</p>', '', origin_text)

    return text

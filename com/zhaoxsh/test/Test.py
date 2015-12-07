#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    python常用功能
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""

import os, sys
import re
import urllib2

# 获取键盘输入
inputStr = raw_input()
print inputStr

# 打印格式输出
print u'发布人：%s\t发布内容：%s\n发布时间：%s\n%s\t%s\t%s\t%s' \
      % ('ss', 'bb', 'cc', 'dd', 'ee', 'ff', 'ss')

print sys.path[0]

print os.curdir


# 爬取网页信息
def load_page():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.101 Safari/537.36'}
    url = 'http://www.iteye.com/news/31173'
    try:
        request = urllib2.Request(url, headers=headers)
        html_str = urllib2.urlopen(request)
        html_str_decode = html_str.read().decode('utf-8')
        print html_str_decode
        item_pattern_str = '<div id="content".*?class="clearfix">.*?<div class="news_main">.*?' \
                           '<div id="news_content">(.*?)</div>.*?<div id="news_recommended_n2">'
        pattern = re.compile(item_pattern_str, re.S)
        content = re.findall(pattern, html_str_decode, 0)
        print content[0]

        return html_str_decode
    except urllib2.HTTPError, e:
        if hasattr(e, 'reason'):
            print 'error'


load_page()


# 闭包

def validator(n):
    def inner_validator(s):
        if len(s) > n:
            print 'too longer'
        else:
            print 'perfect'

    return inner_validator


print validator(2)('ss')

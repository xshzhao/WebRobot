#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    爬取ItEye内容
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""

import re
import urllib2


class IteyeTechnology:
    def __init__(self, iteye_type):
        self.url = 'http://www.iteye.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/45.0.2454.101 Safari/537.36'}
        self.pageIndex = 0
        self.enable = False
        self.items = []
        self.iteye_type = iteye_type

    # 获取转码后的html内容
    def load_page(self):
        # use_proxy()
        url = self.url + '/news/category/' + self.iteye_type + '?page=' + str(self.pageIndex)
        try:
            request = urllib2.Request(url, headers=self.headers)
            html_str = urllib2.urlopen(request)
            html_str_decode = html_str.read().decode('utf-8')
            return html_str_decode
        except urllib2.HTTPError, e:
            hasattr(e, 'reason')
            print u'连接ITeye出错，原因：' + e.reason

    # 获取格式化后的条目明细
    def get_page_items(self):
        html_str = self.load_page()
        pattern_str = '<div class="news clearfix">.*?<a href=(.*?)title=.*?>(.*?)</a>.*?<div>(.*?)</div>'
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, html_str, 0)
        page_items = []
        for item in items:
            suffix = re.sub(r"'", '', item[0].strip())
            page_items.append([suffix, item[1].strip(), item[2].strip()])
        return page_items

    # 获取每页格式化后的明细
    def load_page_items(self):
        if len(self.items) < 1:
            self.pageIndex += 1
            self.items.append(self.get_page_items())

    # 获取明细链接，取得明细内容
    def get_item_detail(self, suffix):
        # use_proxy()
        url = self.url + suffix
        try:
            request = urllib2.Request(url, headers=self.headers)
            html_str = urllib2.urlopen(request)
            html_str_decode = html_str.read().decode('utf-8')
            # 解析文本内容
            item_pattern_str = '<div id="content" class="clearfix">.*?<div class="news_main">' \
                               '.*?<div id="news_content">(.*?)</div>.*?<div id="news_recommended_n2">'
            pattern = re.compile(item_pattern_str, re.S)
            content = re.findall(pattern, html_str_decode, 0)

            print u'详细内容或链接：%s\n' % (deal_html_tag(content[0]))

        except urllib2.HTTPError, e:
            hasattr(e, 'reason')
            print u'连接ITeye出错，原因：' + e.reason

    # 获取一条明细内容
    def get_one_item_content(self, one_page_items):
        for item in one_page_items:
            command = raw_input()
            if command == 'Q':
                self.enable = False
            print '---------------------------------------------------------------------------'
            print u'标题:%s\n概述:\n%s' % (item[1], item[2])
            # 通过明细获取原文，或原文链接
            self.get_item_detail(item[0])

    def start(self):
        print u'正在读取ITeye内容，按Enter键继续......按Q键结束......'
        self.enable = True
        while self.enable:
            self.load_page_items()
            one_page_items = self.items[0]
            self.get_one_item_content(one_page_items)
            del self.items[0]


# 设置使用代理
def use_proxy():
    proxy = {'http': '192.168.2.17'}
    proxy_support = urllib2.ProxyHandler(proxy)
    openner = urllib2.build_opener(proxy_support)
    urllib2.install_opener(openner)


# 格式化html内容
def deal_html_tag(origin_text):
    # 处理</br></br>替换为换行符
    text = re.sub(r'<br />|<strong>|</strong>|<a href=|target="_blank">|<div.*?>|&gt;'
                  r'|<img src=.*?>|<pre.*?class=.*?>|<p><br>.*?</p>|<p>|</p>', '', origin_text)

    return text


# 开始服务
if __name__ == '__main__':
    print u'请输入分类信息：\n' \
          u'操作系统：1\n' \
          u'编程语言：2\n' \
          u'研发管理：3\n'

    category = raw_input()
    if category == '1':
        category = 'os'
    elif category == '2':
        category = 'language'
    elif category == '3':
        category = 'develop'
    else:
        category = 'language'

    # 开始服务
    iteyeTechnology = IteyeTechnology(category)
    iteyeTechnology.start()

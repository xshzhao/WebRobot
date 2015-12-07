#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    爬取糗事百科内容
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/3 10:56
"""

import re
import time
import urllib2


class FunnyThings:
    def __init__(self, funny_type):
        self.baseUrl = 'http://www.qiushibaike.com/' + funny_type + '/page'
        self.pageIndex = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/45.0.2454.101 Safari/537.6'}
        self.enable = False
        self.stories = []

    # 加载页面内容
    def load_page(self, page_index):
        try:
            url_str = self.baseUrl + '/' + str(page_index)
            request = urllib2.Request(url_str, headers=self.headers)
            page_code = urllib2.urlopen(request)
            return page_code.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接糗事百科出错，原因：' + e.reason

    # 获取一页段子列表
    def get_page_items(self):
        html_str = self.load_page(self.pageIndex)
        pattern_str = '<div class="article block untagged mb15".*?<h2>(.*?)' \
                      '</h2>.*?<div class="content">(.*?)<!--(.*?)-->.*?' \
                      '</div>.*?<div class="stats">.*?class="number">(.*?)</i>(.*?)' \
                      '</span>.*?<span class="dash">.*?class="number">(.*?)</i>(.*?)</a>.*?</div>'
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, html_str, 0)

        stories = []
        for item in items:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(item[2])))
            content = deal_html_tag(item[1].strip())
            stories.append([item[0].strip(),
                            content,
                            date,
                            item[3].strip(),
                            item[4].strip(),
                            item[5].strip(),
                            item[6].strip()])
        return stories

    # 将段子列表写入全局变量
    def load_content(self):
        if len(self.stories) < 1:
            self.pageIndex += 1
            self.stories.append(self.get_page_items())

    # 读取一个故事内容
    def get_one_story(self, one_page_story):
        for story in one_page_story:
            command = raw_input()
            if command == 'Q':
                self.enable = False
                return
            print '-----------------------------------------------------------------------------------'
            print u'发布人：%s\n发布内容：\n%s\n页数：%s\t%s\t%s\t%s\t%s\t%s' \
                  % (story[0], story[1], self.pageIndex, story[2], story[3], story[4], story[5], story[6])

    # 开始执行
    def start(self):
        print u'正在读取糗事百科内容......\n按Enter键继续......按Q键结束......'
        self.enable = True
        while self.enable:
            # 获取内容
            self.load_content()
            one_page_story = self.stories[0]
            # 读取一个故事内容
            self.get_one_story(one_page_story)
            # 读取完之后删除
            del self.stories[0]


'''
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>工具函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''


# 格式化html内容
def deal_html_tag(origin_text):
    # 处理</br></br>替换为换行符
    text = re.sub(r'<br/><br/>|<br/>', '\n', origin_text)
    return text


'''
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

if __name__ == '__main__':
    print u'请输入要查看的类型：\n' \
          u'最近8小时：1\n' \
          u'最近24小时：2\n'
    category = raw_input()
    if category == '1':
        category = '8hr'
    elif category == '2':
        category = 'hot'
    else:
        category = 'hot'
    funnyThings = FunnyThings(category)
    funnyThings.start()

# test merge conflicts
# master commit

# dev commit


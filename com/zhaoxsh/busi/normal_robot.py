#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
    通用网络爬虫，采用多线程技术
    @version: 1.0
    @author: xingshen.zhao
    @contact: zxswork@aliyun.com
    @time: 2015/12/4 15:34
"""
import re
import urllib2
import threading

global_pages = []  # 爬取过的页面内容
global_failed_list = []  # 爬取失败的任务
global_exists_list = []  # 已经爬取过的任务
global_ready_list = []  # 等待爬取的的任务
global_page_count = 0  # 访问过的总页面数
global_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/45.0.2454.101 Safari/537.36'}
global_thread_condition = threading.Condition()


class NormalRobot:
    def __init__(self, robot_name, begin_url, thread_num):
        self.robot_name = robot_name
        self.begin_url = begin_url
        self.thread_num = thread_num
        # 声明缓冲池
        self.thread_pool = []

    def do_it(self):
        """
            开始任务
        :return:
        """
        global global_ready_list
        global_ready_list.append(self.begin_url)
        # 访问深度
        depth = 0
        print u'正在启动网络机器人......'
        while len(global_ready_list) != 0:
            depth += 1
            self.download()
            self.update_queue_list()
            i = 0
            while i < len(global_ready_list):
                i += 1

    def download(self):
        """
        下载页面所有内容
        :return:
        """
        global global_ready_list
        global global_page_count
        i = 0
        while i < (len(global_ready_list)):
            j = 0
            while j < self.thread_num and i + j < len(global_ready_list):
                global_page_count += 1
                self.download_inner(global_ready_list[i + j], j)
                j += 1
            i += j
            for thread in self.thread_pool:
                thread.join(30)
            self.thread_pool = []
        global_ready_list = []

    def download_inner(self, cur_url, thread):
        """
        抓取内部内容
        :param cur_url:
        :param thread:
        :return:
        """
        multi_thread = MultiThread(cur_url, thread)
        self.thread_pool.append(multi_thread)
        multi_thread.start()

    def update_queue_list(self):
        global global_ready_list
        global global_exists_list
        new_url_list = []
        for content in global_pages:
            new_url_list += self.get_urls(content)
        global_ready_list = list(set(new_url_list) - set(global_exists_list))

    def get_urls(self, content):
        pattern_str = r'"(http://.+?)"'
        pattern = re.compile(pattern_str, re.DOTALL)
        url_list = re.findall(pattern, content, 0)
        return url_list


class MultiThread(threading.Thread):
    """
    多线程服务
    """

    def __init__(self, _url, thread_id):
        threading.Thread.__init__(self)
        self.url = _url
        self.thread_id = thread_id

    def run(self):
        global global_thread_condition
        global global_failed_list
        global global_ready_list
        global global_headers
        try:
            request = urllib2.Request(self.url, headers=global_headers)
            html_str = urllib2.urlopen(request)
            html_str_decode = html_str.read().decode('utf-8')
            print html_str_decode
        except urllib2.HTTPError, e:
            global_thread_condition.acquire()
            global_failed_list.append(self.url)
            global_exists_list.append(self.url)
            global_thread_condition.release()
            if hasattr(e, "reason"):
                print u'网络机器人爬取%s失败,原因:%s' % (self.url, e.reason)
            return None
        global_thread_condition.acquire()
        global_pages.append(html_str_decode)
        global_exists_list.append(self.url)
        global_thread_condition.release()


print 'begin......'
url = 'http://www.iteye.com'
robot = NormalRobot("网络机器人", url, 5)
robot.do_it()
#dev commit somethings
#2015/12/4
#dev do somethings
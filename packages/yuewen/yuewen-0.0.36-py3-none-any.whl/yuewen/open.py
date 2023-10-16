#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests


def QuickMessage_addPushMsgSubmit(
        cookie,
        data
):
    """
    添加PUSH消息
    """
    url = 'https://open.yuewen.com/api/QuickMessage/addPushMsgSubmit'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Origin": "https://open.yuewen.com",
        "Pragma": "no-cache",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/pushMsg",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0"
    }
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        json=data,
        return_json=True
    )


def QuickMessage_getAllPage(
        cookie: str
):
    """
    获取页面列表
    """
    url = 'https://open.yuewen.com/api/QuickMessage/getAllPage'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/pushMsg",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        return_json=True
    )


def QuickMessage_pushMessageList(
        cookie,
        page=1
):
    """
    获取客服消息列表
    """
    url = 'https://open.yuewen.com/api/QuickMessage/pushMessageList?p=%s&name=&id=&start_time=&end_time=&status=' % page
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/pushMsg",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def WechatMessage_addkfmsgSubmit(
        cookie,
        data
):
    """
    添加客服消息
    """
    url = 'https://open.yuewen.com/api/WechatMessage/addkfmsgSubmit'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Origin": "https://open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/customerService",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        json=data,
        return_json=True
    )


def WechatMessage_getAllPage(
        cookie
):
    """
    获取页面列表
    """
    url = 'https://open.yuewen.com/api/WechatMessage/getAllPage'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/customerService",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        return_json=True
    )


def WechatMessage_serviceMessageList(
        cookie,
        page=1
):
    """
    获取客服消息列表
    """
    url = 'https://open.yuewen.com/api/WechatMessage/serviceMessageList?p=%s&title=&start_time=&end_time=&status=' % page
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/messagePush/customerService",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def Wechatstatistics_newChapterRead(
        cookie,
        cbid,
        startchapter=1,
        endchapter=500
):
    """
    获取章节访问量，数据不重要，章节比较重要，可以借此获取章节目录
    """
    url = 'https://open.yuewen.com/api/Wechatstatistics/newChapterRead?cbid=%s&p=1&startchapter=%s&endchapter=%s' % (cbid, startchapter, endchapter)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/dataStatistics/bookStatistics/chapterPv",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def quick_app_tag_getRuleList(
        cookie: str,
        page: int = 1,
        name: str = None,  # 搜索规则名称
        status: int = -1,
        startdate: str = None,
        enddate: str = None
):
    """
    获取 推广运营-标签规则管理
    """
    url = 'https://open.yuewen.com/api/tag/getRuleList'
    data = dict()
    data['page'] = page
    data['status'] = status
    if name is None:
        pass
    else:
        data['name'] = name
    if startdate is None:
        pass
    else:
        data['startdate'] = startdate
    if enddate is None:
        pass
    else:
        data['enddate'] = enddate

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/promotion/labelManagement",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=data,
        return_json=True
    )


def wechat_wechatInfo(cookie):
    """
    获取 子账号的授权信息
    """
    url = 'https://open.yuewen.com/api/wechat/wechatInfo'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/wechat/authorization",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def wechatspread_bookSpread(cookie, page=1):
    """
    获取作品书库，主要要进入子账号才能获取
    """
    url = 'https://open.yuewen.com/api/wechatspread/bookSpread?cbid=&title=&page=%s&category1=&category2=&category3=&isfinish=&level=-1' % page
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/library",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )

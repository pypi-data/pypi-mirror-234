#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/15 15:47
# @Author  : 雷雨
# @File    : thread.py
# @Desc    :
import threading
from typing import List, Callable

from bilibili_api import sync

from src import base


def start_thread(job: Callable):
    """启动线程"""
    t = threading.Thread(target=job)
    t.start()
    return t


def Thread(
        listeners: List[base.Listener],
        uploader: base.Uploader
):
    """初始化listeners和uploader，异步运行"""
    for listener in listeners:
        listener.mq_list = [uploader.mq]
        start_thread(listener.listen)
    t = start_thread(uploader.wait)
    return t


__all__ = [
    'sync',
    'start_thread',
    'Thread'
]
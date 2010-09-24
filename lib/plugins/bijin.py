# -*- coding: utf-8 -*-
#
# bijin-tokei plugin for GNOME Photo Frame
# Copyright (c) 2010, Yoshizumi Endo <y-endo@ceres.dti.ne.jp>
# Licence: GPL3
#
# 2010-09-25 Version 1.3
# 2010-06-03 Version 1.2

import time
import random

from base import *
from ..utils.iconimage import WebIconImage


def info():
    return [BijinPlugin, BijinPhotoList, PhotoSourceBijinUI]


class BijinPlugin(PluginBase):

    def __init__(self):
        self.name = '美人時計'
        self.icon = BijinIcon
        self.hide_source_icon_on_image = True
        self.info = { 'comments': '1min 自動更新時計サイト',
                      'copyright': 'Copyright © 2010 Yoshizimi Endo',
                      'website': 'http://www.bijint.com/',
                      'authors': ['Yoshizimi Endo'], }


class BijinPhotoList(PhotoList):

    def prepare(self):
        self.photos = ['dummy']
        self.tokei = BijinTokeiList()

    def _random_choice(self):
        tokei = self._select_clock(self.target)
        (page_path, pic_path) = dict(self.tokei.list)[tokei]

        url_base = 'http://www.bijint.com/'
        url_page = url_base + page_path
        self.headers = {'Referer': url_page}

        (h, m) = time.localtime(time.time())[3:5]
        url = '%s/%02d%02d.jpg' % (url_base + pic_path, h, m)

        data = {
            'type': BijinPlugin,
            'icon': BijinIcon,
            'url': url,
            'title': '%02d:%02d (%s)' % (h, m, tokei),
            'owner_name': 'bijin-tokei',
            'page_url': url_page,
            }

        return Photo(data)

    def _select_clock(self, target):
        list = [i[0] for i in self.tokei.list if i[1][0] and i[0]
                not in self.conf.get_list('plugins/bijin/disabled')]
        result = random.choice(list) if target == 'ランダム' else target
        return result


class PhotoSourceBijinUI(PhotoSourceUI):

    def _label(self):
        tokei = BijinTokeiList()
        return [i[0] for i in tokei.list]


class BijinTokeiList(object):

    def __init__(self):
        self.list = [
            ['美人時計', ['jp', 'jp/img/clk']],
            ['美男時計', ['binan', 'binan/img/clk']],
            ['サーキット時計', ['cc', 'cc/tokei_images']],
            ['韓国時計', ['kr', 'assets/pict/kr/590x450']],
            ['香港時計', ['hk', 'assets/pict/hk/590x450']],
            ['北海道時計', ['hokkaido', 'assets/pict/hokkaido/590x450']],
            ['仙台時計', ['sendai', 'assets/pict/sendai/590x450']],
            ['京都時計', ['kyoto', 'kyoto/tokei_images']],
            ['金沢時計', ['kanazawa', 'kanazawa/tokei_images']],
            ['福岡時計', ['fukuoka', 'fukuoka/tokei_images']],
            ['岡山時計', ['okayama', 'okayama/tokei_images']],
            ['香川時計', ['kagawa', 'kagawa/tokei_images']],
            ['ランダム', [None, None]],
            ]


class BijinIcon(WebIconImage):

    def __init__(self):
        self.icon_name = 'bijin.ico'
        self.icon_url = 'http://www.bijint.com/jp/favicon.ico'

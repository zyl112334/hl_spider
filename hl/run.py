#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2022/11/2 2:10 下午
# Author: yilin

from scrapy import cmdline


name = 'hl_spider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
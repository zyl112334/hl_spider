#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2022/11/1 3:30 下午
# Author: yilin

from scrapy.exporters import JsonLinesItemExporter
from .items import Question


class HLPipeline(object):
    def __init__(self):
        self.fp_solved_question = open('hl_qa.json', 'wb')
        self.exporter_question = JsonLinesItemExporter(self.fp_solved_question, ensure_ascii=False)

    def process_item(self, item, spider):
        print('写入一条数据')
        self.exporter_question.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp_solved_question.close()
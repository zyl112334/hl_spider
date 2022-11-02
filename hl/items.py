#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2022/11/1 3:06 下午
# Author: yilin

import scrapy


class Question(scrapy.Item):
    """
    问题的数据模型【问题、问题url、问题描述、提问时间、提问人属地、律师回答、回答人数、回答时间、律师姓名、赞同人数】
    """
    question = scrapy.Field()
    question_url = scrapy.Field()
    description = scrapy.Field()
    question_time = scrapy.Field()
    question_area = scrapy.Field()
    question_type = scrapy.Field()
    answer = scrapy.Field()
    answer_number = scrapy.Field()
    answer_time = scrapy.Field()
    lawyer_name = scrapy.Field()
    agree_number = scrapy.Field()
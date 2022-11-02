#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2022/11/1 2:51 下午
# Author: yilin

import scrapy
import re
import sys
import os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(__dir__, '..'))
from items import Question
import time


# 使用普通的爬虫来爬取【华律法律咨询】
count = 1


class HLSpiderSpider(scrapy.Spider):
    name = 'hl_spider'
    allowed_domains = ['66law.cn']
    start_urls = ['https://www.66law.cn/question/list_1_r3.aspx']

    HTTPS = "https:"

    def parse(self, response):
        url_head = 'https://www.66law.cn'

        questions = response.xpath('//div[@class="w1200 ma mt40 clearfix"]//ul[@class="advisory-list"]')
        for block in questions:
            question_list = block.xpath('.//li')
            for q in question_list:
                q_url = q.xpath('.//p[@class="t"]/a//@href').get()
                q_title = re.sub(r'\s', '', q.xpath('.//p[@class="t"]/a//@title').get())
                q_type = q.xpath('.//div[@class="b"]/span/text()').get()
                q_area = re.sub(r'\s', '', q.xpath('.//div[@class="b"]/span/text()').extract()[1])

                question_url = url_head + q_url
                yield scrapy.Request(url=question_url, callback=self.parse_solved_question,
                                     meta={"info": (q_title, q_area, q_type, question_url)},
                                     cookies={})

            time.sleep(1)
            # break
        time.sleep(2)
        # break
        global count
        count += 1
        if count < 3:
            next_page = 'https://www.66law.cn/question/list_{}_r3.aspx'.format(count)
            yield scrapy.Request(next_page)


    def parse_solved_question(self, response):
        """
        爬取法律咨询数据
        :param response:
        :return:
        """
        # 获取参数信息
        q_title, q_area, q_type, question_url = response.meta.get('info')
        q_time = response.xpath('//div[@class="mt20 clearfix"]//div[@class="mt10 f12 s-ca"]//span[@class="mr30"]/text()').extract()[2]
        q_description = response.xpath('//p[@class="mt10 f18 lh32 s-c6"]')
        description = list()
        for des in q_description:
            text = des.xpath('string(.)').get()
            description.append(text)
        question_description = "".join(description)
        answer_number = response.xpath('//span[@class="f24"]/text()').get()
        answer_list = response.xpath('//ul[@class="reply-list reply-list2"]/li')
        for answer in answer_list:
            lawyer = answer.xpath('.//p[@class="ovh mb5"]/a/text()').get()
            answer_text = answer.xpath('.//p[@class="b"]/text()').get()
            answer_time = answer.xpath('.//p[@class="s-cb f12 mt15"]/text()').get()
            agree_number = re.findall(r"\d+", answer.xpath('.//span[@class="s-cb"]/text()').get())[0]

            item = Question(question=q_title, question_url=question_url,
                            description=question_description, question_time=q_time,
                            question_area=q_area, answer=answer_text,
                            question_type=q_type,
                            answer_number=answer_number, answer_time=answer_time,
                            lawyer_name=lawyer, agree_number=agree_number)
            yield item

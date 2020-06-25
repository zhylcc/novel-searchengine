# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    # 章节标题
    chapterTitle = scrapy.Field()
    # 章节链接
    chapterUrl = scrapy.Field()
    # 章节内容
    chapterContent = scrapy.Field()
    pass

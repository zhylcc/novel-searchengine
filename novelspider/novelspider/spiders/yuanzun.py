# -*- coding: utf-8 -*-
import scrapy
from ..items import NovelspiderItem

class YuanzunSpider(scrapy.Spider):
    name = 'yuanzun'
    allowed_domains = ['www.shuquge.com']
    start_urls = ['http://www.shuquge.com/txt/5809/index.html']
    base_url = "http://www.shuquge.com/txt/5809/"
    process = 0

    def parse(self, response):
        chapter_list = response.xpath("/html/body/div[5]/dl/dd[position()>13]/a")
        self.process = len(chapter_list)
        for chapter in chapter_list: # 测试时只爬取10章[:10]即可
            chapter_item = NovelspiderItem()
            chapter_item['chapterTitle'] = ' '.join(chapter.xpath("./text()").extract_first().split()[-2:])
            chapter_url = self.base_url + chapter.xpath("./@href").extract_first()
            chapter_item['chapterUrl'] = chapter_url
            yield scrapy.Request(chapter_url, callback=self.parse_chapter, meta={"item": chapter_item})


    def parse_chapter(self, response):
        chapter_item = response.meta['item']
        sentences = response.xpath('//*[@id="content"]/text()').extract()[:-3]
        chapter_content = ""
        for sentence in sentences:
            if sentence in {'\r', '\n'}:
                continue
            chapter_content += sentence.replace('\n', '')\
                .replace('\r', '\n')\
                .replace('\xa0', ' ')
        chapter_item['chapterContent'] = chapter_content
        yield chapter_item

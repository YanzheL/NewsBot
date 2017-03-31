# -*- coding: utf-8 -*-#
from scrapy.spiders import Spider
from scrapy.selector import Selector
from newsbot.items import Website
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrapy

class DmozSpider(Spider):
    name = "npr"
    allowed_domains = ["www.npr.org"]
    start_urls = [
        "http://www.npr.org/",
    ]
    # Rule(SgmlLinkExtractor(allow=(r'http://www.npr.org/sections/thetwo-way/2017/03/29/[a-z0-9]+?/'))),
    # Rule(SgmlLinkExtractor(allow=(r'http://www.npr.org/sections/thetwo-way/2017/03/29/[a-z0-9]+')), callback="parse_item"),

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()

        sel = Selector(response)

        items = []
        item = Website()

        topic_raw = sel.xpath("//article/h3[@class='slug']/a/text()").extract()
        author_raw = sel.xpath("//div/p[@class='byline__name byline__name--block']/a[@rel='author']/text()").extract()
        date_raw = sel.xpath("//div[@class='dateblock']/time/@datetime").extract()
        title_raw = sel.xpath("//div[@class='storytitle']/h1/text()").extract()

        if len(topic_raw) >=1:
            item['topic'] = str(topic_raw[0]).strip()
        if len(author_raw)>=1:
            item['author'] = str(author_raw[0]).strip()
        if len(date_raw) >= 1:
            item['date'] = str(date_raw[0]).strip()
        if len(title_raw) >= 1:
            item['title'] = str(title_raw[0]).strip()

        item['article'] = sel.xpath("//div[@id='storytext']/p/text()").extract()
        item['url'] = current_url

        temp = ""

        for i in item['article']:
            temp = temp + '\n\n' + i

        item['article'] = temp
        items.append(item)

        all_urls = sel.xpath("//a/@href").extract()

        # n = 0

        for url in all_urls:
            if "http://www.npr.org/" in url:
                # n = n + 1
                # print "------------ N = ", n
                # print "--------------------- YIELD BEGIN ---------------------"
                # print url
                yield scrapy.Request(url, callback=self.parse)
                # print "--------------------- YIELD END ---------------------"

            # if n >= 1:
            #     break
        yield item


        # return items

# -*- coding: utf-8 -*-
import scrapy


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']


    def parse(self, response):
        # url = response.xpath('// *[ @ id = "entry_653982"] / div[2] / h2 / a/@href').extract()[0]
        # url = response.xpath('// *[ @ id = "entry_653982"] / div[2] / h2 / a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
        #url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        url = response.css('div#news_list h2 a::attr(href)').extract()
        # scrapy对
        pass

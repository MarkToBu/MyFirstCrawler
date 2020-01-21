# -*- coding: utf-8 -*-
import re
import json
from urllib import parse

import scrapy
from scrapy import Request
import requests

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        """
        # url = response.xpath('// *[ @ id = "entry_653982"] / div[2] / h2 / a/@href').extract()[0]
        # url = response.xpath('// *[ @ id = "entry_653982"] / div[2] / h2 / a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
        #url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        urls = response.css('div#news_list h2 a::attr(href)').extract()

        1. 获取新闻url，交给scrapy下载后调用解析方法

        2. 获取下一个的url并交给scrapy进行下载，下载完成后交给parse继续进行处理
        """
        post_nodes = response.css('div#news_list .news_block')
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)

        next_url = response.xpath("//div[@class='pager']/a[contains(text(),'Next >']/@href").extract_first("")
        yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

        """
        方案二:
            next_node = response.css(div.pager a:last-child::text).extract_first()
            if next_node == "Next >":
               next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
               yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)      
        """

    def parse_detail(self,response):
       match_re = re.match(".*?(\d+)",response.url)
       if match_re:
           post_id = match_re.group(1)
           title =  response.css('div#news_title a::text').extract_first("")
           create_date = response.css('div#news_info span.time::text').extract_first("")
           content =  response.css('div#news_content').extract_first("")
           tag_list = response.css('div.news_tags a::text').extract()
           tags = ",".join(tag_list)
           # html = requests.get("https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=654012")
           html = requests.get(parse.urljoin(response.url,"NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
           j_data = json.load(html.text)
           # '{"ContentID":654012,"CommentCount":0,"TotalView":31,"DiggCount":0,"BuryCount":0}
           commentCount = j_data["CommentCount"]
           totalView = j_data["TotalView"]
           diggCount = j_data["DiggCount"]
           buryCount = j_data["BuryCount"]
           




       pass


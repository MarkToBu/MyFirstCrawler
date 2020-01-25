# -*- coding: utf-8 -*-
import re
import json
from urllib import parse

import scrapy
from scrapy import Request
import requests
from ArticleSpider.items import CdnBlogArtcleItem
from ArticleSpider.utils import common


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
        # todo 正式环境，解除限制
        post_nodes = response.css('div#news_list .news_block')[:1]
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        # 非调试放开这里 循环下一个url
        next_url = response.xpath("//div[@class='pager']/a[contains(text(),'Next >')]/@href").extract_first()
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        """
        方案二:
            next_node = response.css(div.pager a:last-child::text).extract_first()
            if next_node == "Next >":
               next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
               yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)      
        """

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            article_item = CdnBlogArtcleItem()
            post_id = match_re.group(1)
            # title =  response.css('div#news_title a::text').extract_first("")
            # create_date = response.css('div#news_info span.time::text').extract_first("")
            # content =  response.css('div#news_content').extract_first("")
            # tag_list = response.css('div.news_tags a::text').extract()

            title = response.xpath('//*[@id="news_title"]//a/text()').extract_first("")
            create_date = response.xpath('//div[@id="news_info"]//span[@class="time"]/text()').extract_first("")
            match_re = re.match(".*?(\d+.*)", create_date)
            if match_re:
                create_date = match_re.group(1)
            content = response.xpath('//div[@id="news_content"]').extract_first("")
            tag_list = response.xpath('//div[@class="news_tags"]//a/text()').extract()
            tags = ",".join(tag_list)

            article_item["title"] = title
            article_item["create_date"] = create_date
            article_item["url"] = response.url
            article_item["content"] = content
            article_item["tags"] = tag_list
            article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
            # 同步請请求和异步请求
            # html = requests.get("https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=654012")
            # html = requests.get(parse.urljoin(response.url,"/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.load(html.text)
            # '{"ContentID":654012,"CommentCount":0,"TotalView":31,"DiggCount":0,"BuryCount":0}

            # yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),meta={"article_item", article_item}, callback=self.parse_nums)
            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)), meta={"article_item": article_item}, callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        article_item = response.meta.get("article_item", "")
        commentCount = j_data["CommentCount"]
        totalView = j_data["TotalView"]
        diggCount = j_data["DiggCount"]
        buryCount = j_data["BuryCount"]

        # article_item = CdnBlogArtcleItem()
        article_item["praise_nums"] = diggCount
        article_item["fav_nums"] = totalView
        article_item["comment_nums"] = commentCount
        article_item["url_object_id"] = common.get_md5(article_item["url"])
        yield article_item

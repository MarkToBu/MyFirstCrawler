# -*- coding: utf-8 -*-
import codecs
import json
from datetime import datetime
import time

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import  adbapi
import MySQLdb
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'a', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 使用官方替代的实现，导出json
# 'ArticleSpider.pipelines.JsonExporterPipleline': 2,
class JsonExporterPipelline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("rm-bp1z8e736h17ic2n2ao.mysql.rds.aliyuncs.com", 'root', 'xxxx', 'mydb', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        inser_sql = """
             INSERT INTO cnblogs_article
             (url_object_id, title, url, front_image_url, front_image_path, praise_nums, comment_nums, fav_nums, tags, content, create_date)
             VALUES 
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    
        """
        params = list()
        params.append(item.get("url_object_id",""))
        params.append(item.get("title",""))
        params.append(item.get("url",""))

        front_image = ",".join(item.get("front_image_url",[]))
        params.append(front_image)

        params.append(item.get("front_image_path",""))
        params.append(item.get("praise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags",""))
        params.append(item.get("content",""))
        params.append(item.get("create_date", "2000-01-01"))
        self.cursor.execute(inser_sql, tuple(params))
        self.conn.commit()

        return item


class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        from MySQLdb.cursors import DictCursor
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DB"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            charset = 'utf8',
            cursorclass = DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparams)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.hanlde_error, item, spider)

    def do_insert(self, cursor, item):
        inser_sql = """
             INSERT INTO cnblogs_article
             (url_object_id, title, url, front_image_url, front_image_path, praise_nums, comment_nums, fav_nums, tags, content, create_date)
             VALUES 
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE praise_nums = VALUES(praise_nums), comment_nums = VALUES(comment_nums), fav_nums = VALUES(fav_nums)

        """
        params = list()
        params.append(item.get("url_object_id", ""))
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))

        front_image = ",".join(item.get("front_image_url", []))
        params.append(front_image)

        params.append(item.get("front_image_path", ""))
        params.append(item.get("praise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        cursor.execute(inser_sql, tuple(params))

    def hanlde_error(self, failure, item, spider):
        print(failure)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_file_path = ""
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item



## 项目笔记

### 1. 命令
- 查看进程
    > ps aux|grep mysqld  
      
### 2. ubuntu **Linux安装和配置mysql**
    > 可参考 https://blog.csdn.net/james_nan/article/details/82053430
 1. 安装
        > sudo apt-get install mysql-server
 2. 登录
        >  mysql -u root -p
             
      输入密码
      退出
        > exit  
                                                                            
         -  **如果mysql不用密码就能登录，可以使用如下命令**
         
       ```
        登录mysql mysql -u root -p 或 mysql 
        > use mysql;   
        > update user set authentication_string=PASSWORD("密码") where user='root';  
        > update user set plugin="mysql_native_password";  
        > flush privileges;  
        > quit;   
        > /etc/init.d/mysql restart;  
        > mysql -u root -p 密码;  
      ``` 
 3.  配置mysql  
     需要找到mysq配置文件
     配置外网访问
           $ sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
           # 修改配置文件的bind-address = 0.0.0.0
 4.  赋予用户外网访问权限 
      ```sql
       GRANT ALL PRIVILEGES ON database.* TO 'username'@'%' IDENTIFIED BY 'password' ;
       # GRANT  ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root123456' WITH GRANT OPTION; 
       flush privileges; 
      然后执行quit命令退出mysql服务，执行如下命令重启mysql：
      service mysql restart
      ```
###  3.  安装scrapy
  ```
     # 新建虚拟环境
     mkvirtualenv article_spider
     切换到虚拟目录下 
     #给目录安装 scrapy
     pip install -i https://pypi.douban.com/simple scrapy
     
  ```
  - **windows安装scrapy中报错**
   手动导入出错的包 
   https://www.lfd.uci.edu/~gohlke/pythonlibs/  
### Scrapy文档
   https://doc.scrapy.org/en/latest/intro/tutorial.html
### 4.  Scrapy爬虫课程
   #### 基本知识
    - 网页抓取常见方案： 
       深度优先， 广度优先   
   #### pycharm调试scrapy项目代码
   >在项目的根目录下建立这个文件，导入包，写入自己的爬虫（cnblogs）
   ```python
   from scrapy.cmdline import execute
   import  sys
   import os

   sys.path.append(os.path.dirname(os.path.abspath(__file__)))
   execute(["scrapy","crawl","cnblogs"])

   ```
   #### xpath的使用
   - 简介 
     xpath使用路径表达式在xml和html中导航、包含标志的函数库、 是一个w3c的标准、  
   - xpath语法  
    article 选取所有article的所以子节点  
    /article 选取所有根元素article  
    article//div 选取所有属于article元素的后代div元素，无论在哪里  
    //@class  选取所有名为class的属性元素  
    /article/div[1]  父元素的第一个div元素  
    /parent/div[last()] 选取最后一个 可以进行加减运算  
    //div[@lang]  所有有lang属性的div元素  
    //div[@lang='eng]  所有有lang属性的div元素  
    ---  
    /div/*  选取属于div元素 所有子节点
    //*     选取所有元素
    //div[@*]  选取所有带属性的元素
    /div/a | //div/p 或者  
    
   -  **例子**    
      >  //div[@id="news_list"]//h2[@class="news_entry"]/a/@href  
       
   #### css选择器复习
```python
       *  所有元素
       #container id选择器
       .container  class选择器
       li a 选取所有li下面的所有a节点 
       ul + p   ul后的第一个元素
       div#container > ul  选取指定div子元素
       ================================ 
       p ~ ul 选择前边有p元素的所有ul元素
       a[title] 选择所有有title属性的a元素
       a[href="xxxxx"] 属性为xx的a元素
       a[href*="x"] 属性xx开头的a元素
       a[href$="x"] 属性xx结尾的a元素
       input[type=radio]:checked 选择选中的表单元素
       ===================
       div:not(#container)  选取所有非·
       li:nth-child(3)  选取第三个元素
       tr:nth-child(2n)  第偶数个tr
``` 
   #### 单独使用scrapy的选择器筛选html
   使用 from scrapy import Selector
   ```python
    from scrapy import Selector
     
    def pars(text):
        sel = Selector(text=text)
        sel.css('[rule]').extract()
        pass
   ```
   #### 使用缓存调试scrapy scrapy shell
   使用 **scrapy shell {url}** 可以缓存下网页的内容，不用反复去调用 
   进入虚拟环境 运行 scrapy shell http://url.html
   之后可以测试命令进行输入
   
   #### scrapy yield使用
   yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),callback=self.parse_num)
   与  
   html = requests.get(parse.urljoin(response.url,"/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))  
   相对，yiled是异步请求，当请求完成时，会通知注册的callback方法
   
   #### scrapy item的使用
   yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)  
   - meta的使用
   response.meta.get("front_image_url ","")  
   这样可以避免出现取值meta的时候出错
   
   - scarpy item的定义
   ```python
    class CdnBlogArtcleItem(scrapy.Item):
        title = scrapy.Field()
        create_date = scrapy.Field()
        url = scrapy.Field()

        # 处理url
        url_object_id = scrapy.Field()
        front_image_url = scrapy.Field()
        front_image_path = scrapy.Field()
        praise_nums = scrapy.Field()
        comment_nums = scrapy.Field()
        fav_nums = scrapy.Field()
        tags = scrapy.Field()
        content = scrapy.Field()
```   

   - scrapy item的使用 赋值和访问
   ```python
        article_item = CdnBlogArtcleItem()
        #赋值 
        article_item["create_date"] = create_date
        article_item["url"] = response.url
        article_item["content"] = content
        article_item["tags"] = tag_list
        article_item["front_image_url"] = response.meta.get("front_image_url ", "")
        #访问
        article_item["content"]
        yield article_item
   ```
   > **scrapy item可以 yield出去，之后会经由管道(piplines)进行处理**
       
    #### python中json的使用
       import json  
       
       j_data = json.loads(response.text)
   #### scrapy 下载图片
   https://doc.scrapy.org/en/latest/topics/media-pipeline.html
   1. 修改setting文件，设置配置
        Enabling your Media Pipeline
        To enable your media pipeline you must first add it to your project ITEM_PIPELINES setting.

        For Images Pipeline, use:

        > ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
        For Files Pipeline, use:

        > ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
        Note

        You can also use both the Files and Images Pipeline at the same time.

        Then, configure the target storage setting to a valid value that will be used for storing the downloaded images. Otherwise the pipeline will remain disabled, even if you include it in the ITEM_PIPELINES setting.

        For the Files Pipeline, set the FILES_STORE setting:

        > FILES_STORE = '/path/to/valid/dir'
        For the Images Pipeline, set the IMAGES_STORE setting:

        - 设置图片存储目录(IMAGES_STORE ),下载的字段(IMAGES_URLS_FIELD)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        > IMAGES_URLS_FIELD = 'front_image_url'  
        > project_dir = os.path.dirname(os.path.abspath(__file__))
        > IMAGES_STORE = os.path.join(project_dir,'images')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
   2. 自定义图片的存储逻辑
      - 将下载的目录存储到item中,方便之后进行处理
      1. 在piplines中新建类继承自ImagesPipline,重载item的处理方法，自定义图片处理逻辑，本例将图片的下载路径存到item中
      ```python
         class ArticleImagePipline(ImagesPipeline):
            def item_completed(self, results, item, info):
                if "front_image_url" in item:
                    for ok,value in results:
                        image_file_path = value["path"]
                    item["front_image_path"] = image_file_path
                return item
     
      ```  
       2. 修改setting文件，将scrapy默认的处理类，修改为新建的 类(注释掉的为原先默认的)
      ```python
        ITEM_PIPELINES = {
           'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
           'ArticleSpider.pipelines.ArticleImagePipline': 1}
           # 'scrapy.pipelines.images.ImagesPipeline': 1}
      ```
   #### 将所得json数据导出到文件
   参考文档：  https://docs.scrapy.org/en/latest/topics/exporters.html#module-scrapy.exporters
   > 自己实现:       
   1. 新建json处理类
   
       ```python
        import codecs
        import json
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

        ```
   2. 将item的处理类，注册到pipeline中 
    在settings文件中加入该配置项,设置好优先级
        ```python
      ITEM_PIPELINES = {
        'ArticleSpider.pipelines.ArticleImagePipeline': 1,
        'ArticleSpider.pipelines.JsonWithEncodingPipeline': 2,
        'ArticleSpider.pipelines.ArticlespiderPipeline': 300}
        ```
   > 官方实现
   ```python
        from scrapy.exporters import JsonItemExporter

        class JsonExporterPipleline(object):
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
```       
> 如上，在settings文件pipeline中进行配置


   #### Twisted 异步插入数据库
   - 代码示例 
   ```python
from twisted.enterprise import  adbapi
class MysqlTwistedPipline(object):

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
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

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
        params.append(item.get("create_date", "2000-01-01"))
        cursor.execute(inser_sql, tuple(params))
        
    def hanlde_error(self, failure, item, spider):
        print(failure)
```
   
   
   #### **数据插入主键冲突的解决方案**  ON DUPLICATE KEY UPDATE
   
   ```sql
    inser_sql = """
             INSERT INTO cnblogs_article
             (url_object_id, title, url, front_image_url, front_image_path, praise_nums, comment_nums, fav_nums, tags, content, create_date)
             VALUES 
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE praise_nums = VALUES(praise_nums), comment_nums = VALUES(comment_nums), fav_nums = VALUES(fav_nums)
      
```
    
   #### scrapy itemloader提取信息
   itemLoader的使用：
   
   
   ```python
from scrapy.loader import ItemLoader
def parse_detail(self, response):
    item_loader = ItemLoader(item=CdnBlogArtcleItem(), response=response)
    item_loader.add_xpath("tags", '//div[@class="news_tags"]//a/text()')
    item_loader.add_css("xxx",'xxxx')
    item_loader.add_value("url", response.url)
    item_loader.add_value("front_image_url", response.meta.get("front_image_url", ""))
    article_item = item_loader.load_item()
```

---- 
      
   #### scrapy itemlaoder对字段逻辑进行处理
   > 使用MapComose对值进行处理
   > 使用TakeFirst()对值进行取第一个操作 
   
```python
from scrapy.loader.processors import MapCompose,TakeFirst

def addTag(value):
    return value +"--my"

class CdnBlogArtcleItem(scrapy.Item):
    title = scrapy.Field(
       input_processor = MapCompose(addTag)
       output_processor = TakeFirst()
    )
    create_date = scrapy.Field()
    url = scrapy.Field()

    # 处理url
    url_object_id = scrapy.Field(
        input_processor = MapCompose()
    )
 
```   

   #### scrapy 自定义itemloader实现特殊需求
   > 自定义itemloader
   ```python

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join

# 自定义itemloader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

# 对字段使用正则
def dateConvert(value):
    match_re = re.match(".*?(\d+.*)", value)
    if match_re:
        return match_re.group(1)
    else:
        return now.strftime("%Y-%m-%d %H-%M-%S")

# 移除某个标签
def remove_tags(value):
    if value == "linux":
        return ""
    else:
        return value

class CdnBlogArtcleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(dateConvert)
    )
    front_image_url = scrapy.Field(
        output_processor=Identity()
    )
    #对字段分割符处理
    tags = scrapy.Field(
        output_processor= Join(separator=",")
    )
    content = scrapy.Field()

```
   > 使用定义好的itemloader   
     item_loader = ArticleItemLoader(item=CdnBlogArtcleItem(), response=response)
   

         
   

       

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
       # GRANT  ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION; 
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
### Scrapy爬虫课程
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

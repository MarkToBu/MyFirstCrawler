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
    
    
    
      
import scrapy
import book.utils.DBUtil as db
from book.items import book_info
import time
import json
from scrapy.selector import Selector


class book_spider(scrapy.Spider):
    name = "book_spider"
    hasNext = True

    def start_requests(self):
        conn = db.pool.connection()
        # 获取 爬虫 配置信息
        sql = "select * from tb_spider_config where  spider_name = '%s' limit 1"
        cursor = conn.cursor()
        row = cursor.execute(sql % self.name)
        if row != 1:
            print("error for get spider config")
            raise RuntimeError('error for get spider config')

        config = json.loads(cursor.fetchone()['config'])
        baseUrl = config['baseUrl']
        step = config['step']
        startIndex = config['startIndex']
        endIndex = config['endIndex']
        # 更新爬虫状态
        cursor.execute(
            "UPDATE tb_spider_state SET spider_state = 'running',start_time = '%s' WHERE spider_name = '%s'" % (
                self.name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        conn.commit()
        # 获取所需要爬虫的URL
        cursor.execute("select * from tb_tag_info where id>= %d and id <= %d" % (startIndex, endIndex))
        # 结果集
        result = cursor.fetchall()
        for x in result:
            # url = str(baseUrl + x['spider_url'])
            for i in range(0, 1000, 20):
                # 构造URL
                url = str(baseUrl + x['spider_url']) + "?start=" + str(i) + "&type=T"
                yield scrapy.Request(url=url, meta={"tag_id": x['id']}, callback=self.parse)
                if not self.hasNext:
                    break

        # 更新爬虫状态
        cursor.execute(
            "UPDATE tb_spider_state SET spider_state = 'stop',end_time = '%s' WHERE spider_name = '%s'" % (
                self.name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        conn.commit()
        cursor.close()
        conn.close()

    def parse(self, response):
        ul = response.xpath("//*[@id='subject_list']/ul/li")
        for li in ul.getall():
            str = Selector(text=li)
            # .replace("\n", "").strip()
            book_name = str.xpath("//div[@class='info']//a/@title").get()
            spider_url = str.xpath("//div[@class='info']//a/@href").get()
            pub = str.xpath("//div[@class='pub']//text()").get().replace("\n", "").strip()
            pubs = pub.split('/')
            price = pubs[-1].strip()
            publish_time = pubs[-2].strip()
            press = pubs[-3].strip()
            authors = pubs[0:-3]
            author = ""
            for s in authors:
                author = author + s + '/'
            book_content = str.xpath("//div[@class='info']/p/text()").get()
            book = book_info()
            book['book_name'] = book_name
            book['book_author'] = author
            book['press'] = press
            book['price'] = price
            book['publish_time'] = publish_time
            book['book_content'] = book_content
            book['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            book['tag_id'] = response.meta['tag_id']
            book['spider_url'] = spider_url
            book['sync_detail'] = 0
            # print(book)
            yield book

        self.hasNext = len(ul.getall()) == 20

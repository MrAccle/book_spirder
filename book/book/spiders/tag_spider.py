import scrapy
from book.items import book_tag
import time


class tag_spider(scrapy.Spider):
    name = "tag_spider"

    def start_requests(self):
        urls = [
            'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # body = response.body
        td = response.xpath("//table[@class='tagCol']//td")
        for s2 in td.getall():
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tag = book_tag()
            str = scrapy.Selector(text=s2)
            tag['tag_name'] = str.xpath("//a/text()").get()
            tag['spider_url'] = str.xpath("//a/@href").get()
            tag['tag_count'] = str.xpath("//b/text()").get()[1:-1]
            tag['create_time'] = date
            tag['last_update_time'] = date
            yield tag

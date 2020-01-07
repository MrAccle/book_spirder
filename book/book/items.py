# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class book_tag(scrapy.Item):
    # 标签名称
    tag_name = scrapy.Field()
    # 标签书籍数量
    tag_count = scrapy.Field()
    # URL
    spider_url = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 上次更新时间
    last_update_time = scrapy.Field()


class book_info(scrapy.Item):
    # 书名
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 出版时间
    publish_time = scrapy.Field()
    # 书籍简介
    book_content = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 标签ID
    tag_id = scrapy.Field()
    # 爬虫链接
    spider_url = scrapy.Field()
    # 是否同步
    sync_detail = scrapy.Field()

# -*- coding: utf-8 -*-
import time
import book.utils.DBUtil as db


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    def process_item(self, item, spider):
        return item


# class tag_pipeline(object):
#     db = None
#     cursor = None
#
#     def __init__(self):
#         self.db = pymysql.connect("120.79.181.62", "root", "QWEqwe123...", "book_store")
#         self.cursor = self.db.cursor()
#
#     def process_item(self, item, spider):
#         sql = "INSERT INTO tb_tag_info(tag_name,tag_count,create_time,last_update_time,spider_url) VALUES('%s', %d, '%s', '%s', '%s')"
#         self.cursor.execute(sql % (
#             item['tag_name'], int(item['tag_count']), item['create_time'], item['last_update_time'],
#             item['spider_url']))
#         self.db.commit()
#         return item


class book_pipeline(object):

    def __init__(self):
        self.conn = db.pool.connection()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO tb_book_info(book_name,book_author,press,price,publish_time,book_content,create_time,tag_id,spider_url,sync_detail)" \
              "VALUES ('%s','%s','%s','%s','%s','%s','%s','%ld','%s','%d')"
        self.cursor.execute(sql % (
            item['book_name'], item['book_author'], item['press'], item['price'], item['publish_time'],
            item['book_content'], item['create_time'], item['tag_id'], item['spider_url'], item['sync_detail']))
        self.conn.commit()

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        self.conn.close()

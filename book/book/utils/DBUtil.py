import pymysql
from DBUtils.PooledDB import PooledDB
import json

pool = PooledDB(pymysql, 10, host='localhost', user='root', passwd='123456', db='book_store',
                port=3306, cursorclass=pymysql.cursors.DictCursor)  # 5为连接池里的最少连接数

if __name__ == '__main__':
    conn = pool.connection()
    # 获取 爬虫 配置信息
    sql = "select * from tb_spider_config where  spider_name = '%s' limit 1"
    cursor = conn.cursor()
    row = cursor.execute(sql % 'book_spider')
    if row != 1:
        print("error for get spider config")
        raise RuntimeError('error for get spider config')

    config = json.loads(cursor.fetchone()['config'])
    baseUrl = config['baseUrl']
    step = config['step']
    startIndex = config['startIndex']
    endIndex = config['endIndex']
    cursor.execute("select * from tb_tag_info where id>= %d and id <= %d" % (startIndex, endIndex))

    result = cursor.fetchall()
    urls = []
    for x in result:
        urls.append(str(baseUrl + x['spider_url']))
        print(x['tag_count'])
        count = x['tag_count']
        for i in range(0,1000,20):
            print(i)
    print(urls)

    # 关闭资源数据
    cursor.close()
    conn.close()

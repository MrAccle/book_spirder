from scrapy.selector import Selector


# import pymysql

def s():
    f = open('../../tags.html', mode='r', encoding='utf-8')
    body = f.read()
    # print(body)
    urls = Selector(text=body).xpath("//table[@class='tagCol']//td/a/@href")
    tags_name = Selector(text=body).xpath("//table[@class='tagCol']//td/a/text()")
    tags_count = Selector(text=body).xpath("//table[@class='tagCol']//td/b/text()")

    print(urls.getall())
    print(tags_name.getall())
    print(tags_count.getall())

    table = Selector(text=body).xpath("//table[@class='tagCol']//td")
    for s2 in table.getall():
        str = Selector(text=s2)
        url = str.xpath("//a/@href").get()
        name = str.xpath("//a/text()").get()
        count = str.xpath("//b/text()").get()[1:-1]
        print(url + "-" + name + "-" + count)


def b():
    f = open('../../book.html', mode='r', encoding='utf-8')
    body = f.read()
    # print(body)
    ul = Selector(text=body).xpath("//*[@id='subject_list']/ul/li")
    for li in ul.getall():
        str = Selector(text=li)
        # .replace("\n", "").strip()
        book_name = str.xpath("//div[@class='info']//a/@title").get()
        print(book_name)
        spider_url = str.xpath("//div[@class='info']//a/@href").get()
        print(spider_url)
        pub = str.xpath("//div[@class='pub']//text()").get().replace("\n", "").strip()
        pubs = pub.split('/')
        price = pubs[-1].strip()
        publish_time = pubs[-2].strip()
        press = pubs[-3].strip()
        authors = pubs[0:-3]
        author = ""
        for s in authors:
            author = author+s+'/'
        print(price)
        print(publish_time)
        print(press)
        print(author)
        book_content = str.xpath("//div[@class='info']/p/text()").get()
        print(book_content)



if __name__ == '__main__':
    b()

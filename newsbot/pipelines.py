# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log

from newsbot import settings
from newsbot.items import Website


class SQLPipeline(object):
    print "--------------------- PIPLINE BEGIN ---------------------"

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == Website:
            try:
                self.cursor.execute("""select * from news where title = %s""", item['title'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update news set date = %s, topic = %s, title = %s, author = %s, article = %s, url = %s where title = %s""",
                        (item['date'],
                        item['topic'],
                        item['title'],
                        item['author'],
                        item['article'],
                        item['url'],)
                    )
                else:
                    self.cursor.execute(
                        """insert into news(date,topic,title,author,article,url)
                          value (%s,%s,%s,%s,%s,%s)""",
                        (item['date'],
                        item['topic'],
                        item['title'],
                        item['author'],
                        item['article'],
                        item['url'],)
                    )

                self.connect.commit()
            except Exception as error:
                print "--------------------- ERROR BEGIN ---------------------"
                print error
                print "-------------------------------------------------------"
            return item
        else:
            pass

    print "--------------------- PIPLINE END ---------------------"
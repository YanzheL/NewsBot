# Scrapy settings for newsbot project

SPIDER_MODULES = ['newsbot.spiders']
NEWSPIDER_MODULE = 'newsbot.spiders'
DEFAULT_ITEM_CLASS = 'newsbot.items.Website'

# -*- coding: utf-8 -*-
BOT_NAME = 'npr'

MYSQL_HOST = 'yanzhe.org'
MYSQL_DBNAME = 'scrapy'
MYSQL_USER = 'guest'
MYSQL_PASSWD = 'MyQQis603001636'

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'newsbot.pipelines.SQLPipeline': 301,
}
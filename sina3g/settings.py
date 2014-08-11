# -*- coding: utf-8 -*-

# Scrapy settings for sina3g project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sina3g'

SPIDER_MODULES = ['sina3g.spiders']
NEWSPIDER_MODULE = 'sina3g.spiders'

ITEM_PIPELINES = {
    'sina3g.pipelines.MysqlStorePipeline':200
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina3g (+http://www.yourdomain.com)'

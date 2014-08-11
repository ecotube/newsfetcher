# -*- coding: utf-8 -*-


from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from sina3g.items import Sina3GItem
from scrapy.http import Request
import re

class SinamobileSpider(CrawlSpider):
    name = 'sina3g'
    allowed_domains = ['sina.com','sina.cn']
    start_urls = ['http://3g.sina.com/?vt=4']
    download_delay = 1

    def start_requests(self):
        return [Request(url='http://3g.sina.com/?vt=4',callback=self.parse_seed)]

    def parse_seed(self,response):
        sel = Selector(response)
        url_list = sel.xpath('//ul[@class="p_newslist"]/li/a/@href').extract()
        url_list.extend(sel.xpath('//ul[@class="p_newslist hard_news"]/li/a/@href').extract())
        url_list.extend(sel.xpath('//h2[@class="p_topline_h2"]/a/@href').extract())
        for url in url_list:
            valid = self.filter_url(url)
            if(valid):
                yield Request(url=url,method='get',callback=self.parse_item)

    def parse_item(self,response):
        sel = Selector(response)
        item = Sina3GItem()
        item['title'] = sel.xpath('//div[@class="articleTitle"]/h2/text()').extract()
        if(len(item['title']) == 0):
            yield
        else:
            item['url'] = response.url
            item['category'] = self.category_translate(response.url)
            item['time'] = sel.xpath('//p[@class="prot"]/text()').extract()
            item['content'] = sel.xpath('//section[@id="artCont"]/article[@id="artI"]').extract() + sel.xpath('//section[@id="artCont"]/div[@class="articlepage"]').extract()
            item['style'] = sel.xpath('//link[@rel="stylesheet"]/@href').extract()
            item['thumb_pic'] = sel.xpath('//img[1]/@src').extract()
            yield item

    def category_translate(self,url):
        url_list = url.split(".")
        subdomain = url_list[0]
        if(subdomain.find("sports") >= 0):
            return "3"
        elif(subdomain.find("ent") >= 0 or subdomain.find("fashion") >= 0):
            return "4"
        elif(subdomain.find("finance") >= 0):
            return "2"
        elif(subdomain.find("tech") >= 0):
            return "5"
        elif(subdomain.find("auto") >= 0):
            return "6"
        elif(subdomain.find("mobile") >= 0):
            return "7"
        else:
            return "1"

    def filter_url(self,url):
        if(re.search(r'photo|video|(d\.php)|redirect\.php|zhuanlan|(top\.sina\.cn)|blog|house|eladies|dp|weibo|(app\.sina\.cn)|(yd\.sina\.cn)|(book1\.sina\.cn)',url)):
            return False
        else:
            return True






# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
import codecs
import json
from scrapy import log
import time
import HTMLParser
import sys
import re
import pycurl
import cStringIO
reload(sys)
sys.setdefaultencoding('utf8')



class MysqlStorePipeline(object):
    def __init__(self):
        self.db_connect = MySQLdb.connect(host="localhost",user="huhu",passwd="huhu123",db="tdtong",cursorclass=MySQLdb.cursors.DictCursor,charset="utf8")
        self.file = codecs.open('sina3g.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        item_dict = dict(item)
        html_parser = HTMLParser.HTMLParser()
        content = self.filter_item(item_dict["content"]).replace("\r","").replace("\t","").replace("\n","").replace("', u'","").replace("'","\"")
        content = html_parser.unescape(content)
        content = self.get_rest(content,str(item_dict["url"]))
        title = self.filter_item(item_dict["title"])
        url = str(item_dict["url"])
        style = self.filter_item(item_dict["style"])
        category = str(item_dict["category"])
        thumb_pic = self.filter_item(item_dict["thumb_pic"]).replace("[","").replace("]","")
        newstime = self.filter_item(item_dict["time"]).replace("[","").replace("]","")
        if(len(newstime.rstrip( )) == 0):
            newstime = int(time.time())
        else:
            newstime = int(time.mktime(time.strptime(newstime.rstrip()+":00",'%Y-%m-%d %H:%M:%S')))
        query = "INSERT INTO news (category,content,style_url,thumb_pic,title,url,time,exec_time) VALUES ('" \
                + category + "','" \
                + content + "', '" \
                + style + "', '" \
                + thumb_pic + "', '" \
                + title + "', '" \
                + url + "', '" \
                + str(newstime) + "', '" \
                + str(int(time.time())) + "')"
        cursor = self.db_connect.cursor()
        cursor.execute(query)
        self.db_connect.commit()
        return item

    def filter_item(self,item_single):
            return str(item_single).decode("unicode_escape").replace("[u'","").replace("']","")

    def get_rest(self,content,url):
        if(content.find("余下全文") >= 0):
            url_list = url.split("?")
            url_prefix = url_list[0]
            search_sa = re.search(r'var(\s)*sa(\s)*\=(\s)*\"([a-zA-Z0-9]+)\"',content,re.M|re.I)
            if search_sa:
                sa = search_sa.group(4)
                search_page_max = re.search(r'var(\s)*page\_max(\s)*\=(\s)*([0-9]+)',content,re.M|re.I)
                if search_page_max:
                    page_max = search_page_max.group(4)
                curl_url = url_prefix + "?" + "sa=" + sa + "&action=article&page_start=2&page_end=" + page_max
            else:
                curl_url = url_prefix + "?" + "pageAction=json&spage=1"
            curl_url = curl_url + "&vt=4"
            rest = self.curl_get(curl_url)
            content = content.replace("</div></article>",rest + "</div></article>")
            content = content.replace("class=\"articlepage\"", "class=\"articlepage\" style=\"display:none\"")
            self.file.write(content + "\n")
        return content

    def curl_get(self,url):
        self.file.write(url+"\n")
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL,str(url))
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.perform()
        rest = buf.getvalue()
        buf.flush()
        buf.close()
        rest_dict = json.loads(str(rest))
        rest_article = rest_dict["content"]
        return rest_article

    # def insert_db(self,record):
    #     cursor = self.db_connect.cursor()
    #     self.file.write("INSERT INTO news (category,author,content,header_code,thumb_pic,title,url,time,exec_time) VALUES ('" +
    #                     str(record[0]) + "','" +
    #                     str(record[1]) + "','" +
    #                     str(record[2]) + "','" +
    #                     str(record[3]) + "','" +
    #                     str(record[4]) + "','" +
    #                     str(record[5]) + "','" +
    #                     str(record[6]) + "','" +
    #                     str(record[7]) + "','" +
    #                     str(int(time.time())) + "')\n")
    #
    #     #self.db_connect.commit()

    def _handle_err(self,failture,item,spider):
        """Handle occured on db interaction"""
        # just log
        log.err(failture)

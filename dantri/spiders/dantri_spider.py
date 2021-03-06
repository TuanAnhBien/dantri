# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider , Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.conf import settings
#from selenium import webdriver
import time
import datetime
from ..items import DantriItem
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
# from pymongo import MongoClient
class DantriSpider(CrawlSpider):
	name = "dantri"
	allowed_domains = [
		"dantri.com.vn",
		"http://dantri.com.vn"

	]

	start_urls = [
		r'http://dantri.com.vn/giai-tri.htm',
		r'http://dantri.com.vn/the-thao.htm',
		r'http://dantri.com.vn/suc-khoe.htm',
		r'http://dantri.com.vn/the-gioi.htm',
		r'http://dantri.com.vn/giao-duc-khuyen-hoc.htm',
		r'http://dantri.com.vn/phap-luat.htm',
		r'http://dantri.com.vn/o-to-xe-may.htm',	
		r'http://dantri.com.vn'
	]

	__queue = [
		r'http://embed2.linkhay.com'
		# r'http://cafef.vn/thoi-su*',
		# r'http://cafef.vn/thi-truong-trung-khoan*',
		# r'http://cafef.vn/bat-dong-san*',
		# r'http://cafef.vn/tai-chinh-ngan-hang*',
		# r'http://cafef.vn/tai-chinh-quoc-te*',
		# r'http://cafef.vn/vi-mo-dau-tu*',
		# r'http://cafef.vn/hang-hoa-nguyen-lieu*',
		# r'http://cafef.vn/du-lieu*',
		# r'http://cafef.vn/videos*'
	]
	# client = MongoClient(settings.get('MONGODB_URI'))
	# db = client[settings.get('MONGODB_DATABASE')]

	# cursor = db[settings.get("CRAWLER_COLLECTION")].find({}, {"url": 1})
	# for i in cursor:
	# 	if 'url' in i:
	# 		__queue.append(i['url'])

	doc_id_crawed = []

	rules = [
	    Rule(
	    	LinkExtractor(allow=(
	    		r'\/(\bgiai-tri\b|\bthe-thao\b|\bsuc-khoe\b|\bthe-gioi\b|\bgiao-duc-khuyen-hoc\b|\bphap-luat\b|\bo-to-xe-may\b).*-\d{17}.htm'
	    	), deny=__queue,
	    	restrict_xpaths=[
	    	]), 
	    	callback='parse_extract_data', follow=True
	    	)
	    ]

	def extract(self,sel,xpath,split = ' '):
		try:
			data = sel.xpath(xpath).extract()
			text = filter(lambda element: element.strip(),map(lambda element: element.strip(), data))
			return split.join(text)
			# return re.sub(r"\s+", "", ''.join(text).strip(), flags=re.UNICODE)
		except Exception, e:
			raise Exception("Invalid XPath: %s" % e)


	def parse_extract_data(self, response):
		se = re.search('\d{17}', response.url)

		if se is not None:
			doc_id = se.group()

			if doc_id not in self.doc_id_crawed:
				self.doc_id_crawed.append(doc_id)

				# Init dantri item
				dantri_item = DantriItem()

				content = self.extract(response, '//div[@id="divNewsContent"]//text()')
				label = response.url.strip().split("/")[3]

				if len(content) > 100:
					dantri_item['content'] = content
					dantri_item['label'] = label

					return dantri_item

				





		# if 'doanh-nghiep' in response.url:
		# 	item['url'] = sel.url
		# 	# import ipdb; ipdb.set_trace()
		# 	item['title'] = self.extract(sel,'//div[@class="newscontent"]/div[1]/h1/text()')
		# 	item['write_date'] = self.extract(sel,'//p[@class="date"]//text()')
		# 	item['content'] = '\n'.join([self.extract(sel,'//div[@class="newscontent_right"]//h2[@class="sapo"]//text()'),
		# 	self.extract(sel,'//div[@class="newscontent_right"]//div[@class="newsbody"]//text()')])
		# 	item['author'] = self.extract(sel,'//p[@class="author"]//text()')
		# 	item['source'] = self.extract(sel,'//p[@class="source"]//text()')
		# 	item['crawl_date'] = datetime.datetime.strftime(datetime.datetime.now(),"%b %d %Y %H:%M:%S")
		# 	return item
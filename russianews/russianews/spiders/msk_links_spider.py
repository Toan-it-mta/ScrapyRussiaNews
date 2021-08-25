import scrapy
import datetime
import json
from urllib.request import urlopen
from dateutil.relativedelta import *


class MskSpider(scrapy.Spider):
    name = 'msk_links'

    def start_requests(self):

        # Cào link ở chủ đề tin tức

        urls1 = self.create_url_news_tags(datetime.datetime(month=1, year=2012, day=1),
                                         datetime.datetime(month=8, year=2021, day=1))
        print('urls = ', len(urls1))
        for url in urls1:
            yield scrapy.Request(url=url, callback=self.parse_news_tags)

        # Cào link ở các chủ đề khác
        urls2 = self.create_url_all_tag()
        print('urls = ', len(urls2))
        for url in urls2:
            yield scrapy.Request(url=url, callback=self.parse_all_tags)

    def parse_news_tags(self, response):

        result_json = json.loads(response.text)
        childs = result_json['childs']
        for child in childs:
            # title = child['ru']['title']
            # time = child['meta'][0]['value']
            id = child['@id']
            href = 'https://www.msk.kp.ru/online/news/{}/'.format(id)

            yield {
                'title': None,
                'time': None,
                'href': href
            }

    def parse_all_tags(self, response):
        result_json = json.loads(response.text)
        childs = result_json['childs'][0]['childs']
        for child in childs:
            # title = child['ru']['title']
            # time = child['meta'][2]['value']
            if child['@class'] == 'external':
                href = child['url']
            else:
                id = child['@id']
                issue = child['issue']
                href = 'https://www.kp.ru/daily/{}/{}/'.format(issue, id)

            yield {
                'title': None,
                'time': None,
                'href': href
            }

    def create_url_news_tags(self, from_date: datetime, to_date: datetime):
        url_api = 'https://s8.stc.m.kpcdn.net/content/api/1/pages/get.json/result/?pages.age.month={}&pages.age.year={}&pages.direction=page&pages.number={}&pages.target.class=100&pages.target.id=1'
        urls = []
        date = from_date

        while date <= to_date:
            month = date.month
            year = date.year

            response = urlopen(url_api.format(month, year, 1))
            data_json = json.loads(response.read())
            pages = data_json['meta'][1]['value']
            for page in range(1, pages + 1):
                # Goi API ở trang thu page
                urls.append(url_api.format(month, year, page))
                # print(url_api.format(month, year, page))
            date += relativedelta(months=+1)
        return urls

    def create_url_all_tag(self):
        targetClass_targetId = [(15, 2996728), (207, 1), (15, 317), (207, 9), (207, 5), (207, 61), (207, 3), (207, 6),
                                (207, 8), (15, 2996581), (15, 30), (207, 85), (15, 34), (15, 16), (15, 399), (15, 137),
                                (15, 63), (207, 36), (207, 76), (15, 33),
                                (15, 109), (15, 107), (207, 7), (207, 41)]

        url_api = 'https://s8.stc.m.kpcdn.net/content/api/1/pages/get.json/result/?pages.direction=page&pages.number={}&pages.spot=1&pages.target.class={}&pages.target.id={}'
        urls = []

        for target in targetClass_targetId:

            targetclass = target[0]
            targetid = target[1]

            response = urlopen(url_api.format(1, targetclass, targetid))
            data_json = json.loads(response.read())
            pages = data_json['childs'][0]['meta'][1]['value']
            for page in range(1, pages + 1):
                # Goi API ở trang thu page
                urls.append(url_api.format(page, targetclass, targetid))
                # print(url_api.format(page, targetclass, targetid))

        return urls



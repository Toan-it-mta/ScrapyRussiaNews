import scrapy
import json


class VestiLinksSpider(scrapy.Spider):
    name = 'vesti_links'
    url_api = 'https://www.vesti.ru{}'

    start_urls = [url_api.format('/api/news?page=1')]

    def parse(self, response):
        data = json.loads(response.text)
        print('result of ', data['pagination']['next'])
        for new in data['data']:
            yield {
                'title': new['title'],
                'time': new['datePub'],
                'href': new['url']
            }

        if data['pagination']['next'] != False:
            yield scrapy.Request(url=self.url_api.format(data['pagination']['next']))

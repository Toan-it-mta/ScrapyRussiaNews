import scrapy
import datetime
import pandas as pd


class LentaNewSpider(scrapy.Spider):
    name = 'lenta_news'

    def start_requests(self):

        def get_url(path_file_links='./result/link_news.jl'):
            urls = []
            rootpath = 'https://lenta.ru'

            jsonObj = pd.read_json(path_or_buf=path_file_links, lines=True)
            for obj in jsonObj['href']:
                urls.append(rootpath + obj)

            return urls

        urls = get_url()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_context = response.css('div.b-topic-layout__left')
        div_news = div_context.css('div.b-text')
        title_news = div_context.css('h1.b-topic__title::text').get('None')
        texts = div_news.css('p::text, a::text, span::text, h1.topic-title::text').getall()
        new = ''
        for text in texts:
            new += text

        yield {
            'url': response.url,
            'title_new': title_news,
            'new': new,
        }

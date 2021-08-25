import scrapy
import datetime
import pandas as pd


class VestiNewSpider(scrapy.Spider):
    name = 'vesti_news'
    i = 1

    def start_requests(self):

        def get_url(path_file_links='./result/vesti_link.jl'):
            urls = []
            rootpath = 'https://vesti.ru'

            jsonObj = pd.read_json(path_or_buf=path_file_links, lines=True)
            for obj in jsonObj['href']:
                urls.append(rootpath + obj)

            return urls

        urls = get_url()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_context = response.css('article')[0]
        div_news = div_context.css('div.article__text')
        title_news = div_context.css('h1::text').get('None')
        texts = div_news.css('p::text, a::text, em::text').getall()
        new = ''
        for text in texts:
            new += text

        yield {
            'url': response.url,
            'title_new': title_news,
            'new': new,
        }

        print(self.i, ' Extract done ', response.url)
        self.i += 1

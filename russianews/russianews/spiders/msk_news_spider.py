import scrapy
import pandas as pd


class MskNewsSpider(scrapy.Spider):
    name = 'msk_news'
    i = 1

    def start_requests(self):
        def get_url(path_file_links='./result/last_msk_links.jl'):
            urls = []

            jsonObj = pd.read_json(path_or_buf=path_file_links, lines=True)
            for obj in jsonObj['href']:
                urls.append(obj)

            print(urls[0:1000])
            return urls

        urls = get_url()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title_news = response.css('h1.styled__Heading-j7em19-3::text').get(None)
        texts = response.css('p.styled__Paragraph-sc-1wayp1z-16 ::text').getall()
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


# css1 = response.css('p.styled__Paragraph-sc-1wayp1z-16 ::text').getall()


if __name__ == '__main__':
    get_url()

import scrapy
import datetime


class LentaSpider(scrapy.Spider):
    name = 'lentalinks'

    def start_requests(self):

        def create_url(start):
            urls = []
            date = start
            now = datetime.datetime.now()

            while (date < now):
                url = f'https://lenta.ru/{date.year}/{date.month:02}/{date.day:02}'
                self.log(url)
                urls.append(url)
                date += + datetime.timedelta(days=1)
            return urls

        urls = create_url(datetime.datetime(year=2011, month=1, day=1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for tag in response.css('div.item'):
            yield {
                'title' : tag.css('a.titles ::text').get(default='None'),
                'time': tag.css('span.g-date ::text').get(default='None'),
                'href': tag.css('a.titles ::attr(href)').get(default='None')
            }




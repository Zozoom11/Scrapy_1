import scrapy

class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['https://book24.ru/catalog/religiya-1437/']

    def parse(self, response):
        for i in response.css('div.catalog__product-list-holder a::attr(href)'):
            yield response.follow(i, callback=self.parse_book)

        for i in range(1, 10):
            next_page = f'https://book24.ru/catalog/religiya-1437/page-{i}/'
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            'name':response.css('h1.product-detail-page__title::text').get(),
            'buy':response.css('p.product-detail-page__purchased-text::text').get().split(),
            'type':response.css('div.product-characteristic__value a::attr(title)')[2].get()
        }

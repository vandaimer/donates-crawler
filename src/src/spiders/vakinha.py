# -*- coding: utf-8 -*-
import re
import scrapy


class VakinhaSpider(scrapy.Spider):
    name = 'vakinha'
    allowed_domains = ['vakinha.com.br']
    start_urls = ['https://www.vakinha.com.br/vaquinhas/explore']
    custom_settings = {
        'FEED_URI': '%(name)s_%(time)s.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def get_number_of_last_page(self, response):
        pagination = response.css('.pagination>li')
        last_page = pagination[-1]
        last_page_link = last_page.css('a::attr(href)').get()
        return int(re.findall('\d+', last_page_link).pop())

    def parse(self, response):
        list_of_items = response.css('.vakinhas-populares>.vakinha-item')
        for item in list_of_items:
            link = item.css('a::attr(href)').get()
            title = item.css('h2::text').get()
            goal = item.css('.goal>span::text').get()
            goal = re.sub(r'/\n|\s', '', goal)
            collected = item.css('.collected>span::text').get()
            collected = re.sub(r'/\n|\s', '', collected)

            yield {
                'link': link,
                'title': title,
                'goal': goal,
                'collected': collected,
            }

        next_page = response.css('.pagination>li>a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)

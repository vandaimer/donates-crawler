# -*- coding: utf-8 -*-
import re
import scrapy


class VakinhaSpider(scrapy.Spider):
    name = 'vakinha'
    allowed_domains = ['vakinha.com.br']
    start_urls = ['https://www.vakinha.com.br/vaquinhas/explore']
    date_regex = '\d{2}/\d{2}/\d{4}'
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

            item = {
                'link': link,
                'title': title,
                'goal': goal,
                'collected': collected,
            }

            yield scrapy.Request(response.urljoin(link), self.parse_item, meta={ 'item': item })


        next_page = response.css('.pagination>li>a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)

    def parse_item(self, response):
        item = response.meta.get('item')

        item_id = response.css('#vakinha-id::text').get()
        created_at = response.css('.created-at')[0].get()
        end_at = response.css('.ending-at')[0].get()
        link = response.css('#short-url::attr(value)').get()

        item['id'] = int(re.findall('\d+', item_id).pop())
        item['created_at'] = re.findall(VakinhaSpider.date_regex, created_at).pop()
        item['end_at'] = re.findall(VakinhaSpider.date_regex, end_at).pop()
        item['link'] = link

        yield item

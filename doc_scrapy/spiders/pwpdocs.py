# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from doc_scrapy.items import DocPageItem


class PWPDocsCrawler(CrawlSpider):
    name = 'public-wpdocs'
    allowed_domains = ['rc.fas.havard.edu']
    start_urls = ['https://rc.fas.harvard.edu/resources/']

    rules = (
        Rule(LinkExtractor(deny=('/#'), unique=True, callback='parse_page'))
    )

    def parse_page(self, response):
        self.logger.info('Parsing page: {}'.format(response.url))
        page = DocPageItem()
        page['title'] = response.xpath('//title/text()').extract_first()
        page['url'] = response.url
        toc_selector = response.xpath('//div[@id="toc_container"/ul')
        page['toc'] = toc_selector.xpath('//li/a/text()').extract()
        page['content'] = response.xpath('//div[@class="entry-content"]')
        return page


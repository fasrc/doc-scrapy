# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from doc_scrapy.items import DocPageItem


class PWPDocsCrawler(CrawlSpider):
    name = 'public-wpdocs'
    allowed_domains = ['www.rc.fas.harvard.edu']
    start_urls = ['https://www.rc.fas.harvard.edu/resources/']

    rules = (
        Rule(LinkExtractor(deny=('\/#', '\/events\/page\/\d*\/\?'), unique=True), follow=True,
             callback='parse_page'),
    )

    def parse_page(self, response):
        self.logger.info('Parsing page: {}'.format(response.url))
        page = DocPageItem()
        page['title'] = response.xpath('//title/text()').extract_first()
        page['url'] = response.url
        page['toc'] = response.xpath('//div[@id="toc_container"]/li/a/text()').extract()
        page['links'] = response.xpath('//a/@href').extract()
        page['content'] = response.xpath('//div[@class="entry-content"]').extract()
        return page

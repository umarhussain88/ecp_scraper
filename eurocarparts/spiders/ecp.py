# -*- coding: utf-8 -*-
import scrapy
import json
import re


class PartsSpider(scrapy.Spider):
    name = "parts"
    allowed_domains = ["www.eurocarparts.com"]
    start_urls = ["https://www.eurocarparts.com/"]

    def parse(self, response):

        nav_links = response.xpath('//ul[@class="outer-ul"]/li/a/@href').extract()
        nav_links = [
            l for l in nav_links if l.startswith("h")
        ]  # remove drop down links.

        for page in nav_links:
            self.logger.info(f"starting on {page}")
            yield scrapy.Request(f"{page}", callback=self.parse_cats)

    def parse_cats(self, response):

        products = response.xpath("//form/following-sibling::script/text()").extract()

        for i in products:

            yield eval(
                re.findall(r"{.*}", json.dumps(i.replace("\n", "").replace("\t", "")))[
                    0
                ]
            )
            self.logger.info("parse completed")

        next_page = response.xpath('//a[@class="next active"]/@href').extract_first()

        try:
            yield scrapy.Request(next_page, callback=self.parse_cats)
        except TypeError:
            self.logger.info(f"Reached end of page.")


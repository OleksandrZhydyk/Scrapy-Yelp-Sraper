# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ContractorItem(scrapy.Item):

    business_name = scrapy.Field()
    business_yelp_url = scrapy.Field()
    business_rate = scrapy.Field()
    reviewers = scrapy.Field()
    reviews = scrapy.Field()


class ReviewerItem(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()

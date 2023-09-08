import json
import scrapy

from ..get_proxy import get_proxy_url


class GetCatsSpider(scrapy.Spider):
    name = "get_categories"
    allowed_domains = ["www.yelp.com", "proxy.scrapeops.io"]

    def start_requests(self):
        url = "https://www.yelp.com/"
        yield scrapy.Request(get_proxy_url(url), callback=self.parse)

    def parse(self, response, **kwargs):
        data_with_tags = response.xpath('//script[@data-hypernova-key='
                                        '"yelpfrontend__318114__yelpfrontend__GondolaHomepage__dynamic"]').get()
        data = data_with_tags.split("<!--")[1].split("-->")[0]
        categories = self.get_categories(data)
        yield categories

    @staticmethod
    def get_categories(data):
        data_obj = json.loads(data)
        block_categories_keys = ["initialCategories", "moreCategories"]
        cats = data_obj["legacyProps"]["category_tiles_props"]
        categories = []
        for key in block_categories_keys:
            for category in cats[key]:
                categories.append(category['category']['alias'])
        return {"categories": categories}

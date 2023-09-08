import json
import time

import scrapy

from scrapy import Selector
from selenium.webdriver.common.by import By

from ..exceptions import UnsupportedInputParameter
from ..get_proxy import get_proxy_url
from ..SelenAuto import SelenAuto
from ..itemloader import ContractorLoader
from ..items import ContractorItem, ReviewerItem


class YelpSpider(scrapy.Spider):
    name = "yelp"
    allowed_domains = ["www.yelp.com", "proxy.scrapeops.io"]
    start_urls = ["https://www.yelp.com/"]
    count = 0

    def __init__(self, category=None, location=None, *args, **kwargs):
        self.available_categories = self._get_categories()
        self.category = self._check_category(category)
        self.location = self._check_location(location)
        self.available_locations = ['New York, NY', 'San Francisco, CA']
        super().__init__(*args, **kwargs)

    def start_requests(self):
        if self._is_parse_whole_site():
            for category in self.available_categories:
                for location in self.available_locations:
                    url = f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"
                    yield scrapy.Request(get_proxy_url(url), callback=self.parse)
        if self.category and self.location:
            url = f"https://www.yelp.com/search?find_desc={self.category}&find_loc={self.location}"
            yield scrapy.Request(get_proxy_url(url), callback=self.parse)
        else:
            raise UnsupportedInputParameter("Please enter both args")

    def parse(self, response, **kwargs):
        self.count += 1
        businesses = response.css('div.padding-t3__09f24__TMrIW')
        for business in businesses:
            if not business.css('span.css-8xcil9::text'):
                continue
            contractor = ContractorLoader(item=ContractorItem(), selector=business)
            contractor.add_css('business_name', 'a.css-19v1rkv::text')
            contractor.add_css('business_yelp_url', 'a.css-19v1rkv::attr(href)')
            contractor.add_css('business_rate', 'span.css-gutk1c::text')
            contractor.add_css('reviews', 'span.css-8xcil9::text')

            reviews_link = business.css('a.css-19v1rkv::attr(href)').get()

            if reviews_link:
                reviewers = self.parse_reviews(f"https://www.yelp.com{reviews_link}")
                contractor.add_value('reviewers', [reviewers])
                yield contractor.load_item()
            else:
                contractor.add_value('reviewers', [None])
                yield contractor.load_item()

        next_page_div = response.css('div.pagination__09f24__VRjN4')
        next_page_url = next_page_div.css('a.next-link.navigation-button__09f24__m9qRz.css-ahgoya ::attr(href)').get()
        print(self.count)
        if self.count < 1:
            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)

        # if next_page_url is not None:
        #     yield response.follow(get_proxy_url(next_page_url), callback=self.parse)

    @staticmethod
    def parse_reviews(url: str):

        with SelenAuto("chrome", 'spiders/chromedriver-linux64/chromedriver') as drv:
            drv.driver_get_page(url)
            time.sleep(2)
            drv.scroll_to_element(By.TAG_NAME, 'footer')
            drv.wait_until_element_presence(
                By.CSS_SELECTOR,
                "li.margin-b5__09f24__pTvws.border-color--default__09f24__NPAKY",
                10
            )
            page_source = drv.get_page()

        selector = Selector(text=page_source)
        div_reviews = selector.css("#reviews")
        li_reviews = div_reviews[0].css('li.margin-b5__09f24__pTvws.border-color--default__09f24__NPAKY')
        reviewers = []
        for index, reviewer in enumerate(li_reviews):
            if index > 4:
                break
            reviewer_item = ReviewerItem()
            reviewer_item['name'] = reviewer.css('span.fs-block.css-ux5mu6 ::text').get()
            reviewer_item['location'] = reviewer.css('span.css-qgunke ::text').get()
            reviewer_item['date'] = reviewer.css('span.css-chan6m ::text').get()
            reviewers.append(reviewer_item)
        return reviewers

    def _is_parse_whole_site(self):
        return self.category is None and self.location is None

    def _check_category(self, category):
        if category is None:
            return None
        if not isinstance(category, str) or category not in self.available_categories:
            raise UnsupportedInputParameter(f"Unsupported category {category}")
        return category.capitalize()

    @staticmethod
    def _check_location(location):
        if location is None:
            return None
        if not isinstance(location, str):
            raise UnsupportedInputParameter(f"Unsupported location {location}")
        return location

    @staticmethod
    def _get_categories():
        with open('data/categories.json', 'r') as f:
            data = f.read()
            return json.loads(data)[0]['categories']

    # @staticmethod
    # def _save_data(category: str, location: str, data: str):
    #     with open(f'data/{category}-{location}.json', 'a') as f:
    #         f.write(data)


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class YelpParserPipeline:
    def process_item(self, item, spider):
        return item


class ReviewsToIntPipeline:

    prefix_relations = {
        "k": 1000,
        "m": 1000000
    }

    def process_item(self, item, spider):
        if spider.name == 'get_categories':
            return item
        adapter = ItemAdapter(item)
        if adapter.get('reviews'):
            reviews = adapter['reviews']
            if reviews[-1].isalpha():
                adapter['reviews'] = int(float(reviews[:-1]) * self.prefix_relations[reviews[-1]])
            else:
                adapter['reviews'] = int(adapter['reviews'])
            return item
        else:
            raise DropItem(f"Missing reviews in {item}")

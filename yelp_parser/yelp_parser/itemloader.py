import re

from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.loader import ItemLoader


class ContractorLoader(ItemLoader):

    default_output_processor = TakeFirst()
    business_yelp_url_in = MapCompose(lambda x: 'https://www.yelp.com' + x)
    business_rate_in = MapCompose(lambda x: float(x.strip()))
    reviews_in = MapCompose(lambda x: x.split(" ")[0][1:])

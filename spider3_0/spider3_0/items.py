# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    """Fields match the `product` table. Names must match the SQLAlchemy columns."""

    # Columns in the `product` table
    name = scrapy.Field()        # product title
    productLink = scrapy.Field() # product URL
    price = scrapy.Field()       # regular price
    salePrice = scrapy.Field()   # sale price
    type = scrapy.Field()        # category
    gender = scrapy.Field()
    storeId = scrapy.Field()     # must match an existing store.id

    # Not columns in `product`. The pipeline uses these for other tables.
    imageLink = scrapy.Field()   # -> productimages.URL
    colors = scrapy.Field()      # -> productcolors.color (list of strings)
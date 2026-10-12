import scrapy
from scrapling.integrations.scrapy import scrapling_response
from scrapy import Request
from web_poet import ItemPage
import json, os

class ProductsExtractor(scrapy.Spider):
    name = "products"

    def __init__(self, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config  # Captures CLI arg: -a json_file="urls.json"

    async def start(self):
        if not self.config:
            self.logger.error("NEED TO PROVIDE CONFIG FILE")
            return

        spider_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(spider_dir, '..', 'configs')

        config_path = os.path.normpath(
        os.path.join(spider_dir, "..", "configs", self.config)
    )

        with open(config_path) as f:
            file = json.load(f)

            for x,y in file[0].items():
                for item in y["urls"]:
                    productLink = item["url"]
                    gender = item["gender"]
                    yield Request(
                        url = productLink, 
                        cb_kwargs={"gender": gender, "category": x},
                        callback=self.parse
                        )



    async def parseProduct(self, response, page: ItemPage, category, gender):
        """Callback to extract product details using web-poet page objects

        and append spider-level context metadata.
        """
        # Automatically injects and converts the detail Page Object into a dict/item
        item = await page.to_item()

        # # Convert to dictionary if page.to_item() returns an attrs or dataclass instance
        # if not isinstance(item, dict):
        #     item = dict(item)

        # Append spider contextual metadata passed down through cb_kwargs
        item["category"] = category
        item["gender"] = gender
        item["url"] = response.url

        yield item
        

    # @scrapling_response(adaptive=True)
    async def parse(self, response, page: ItemPage, category, gender):
        products = await page.to_item()
        for url in products["urls"]:
            # print(url)
            yield scrapy.Request(url, callback=self.parseProduct, cb_kwargs={"category": category, "gender":gender})

        # If the page object found a next page link, follow it to collect more product links.
        next_page = products.get("next_page")
        
        if next_page:
            # Scrapy will schedule this request and the web_poet middleware will provide an ItemPage for the callback.
            yield scrapy.Request(next_page, callback=self.parse, cb_kwargs={"category": category, "gender":gender})

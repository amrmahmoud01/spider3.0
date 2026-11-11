import scrapy
from scrapling.integrations.scrapy import scrapling_response
from scrapy import Request
from web_poet import ItemPage
from importlib.resources import files
import json, os


## TO RUN THIS SPIDER:

## scrapy crawl products -a config=[storeName]Config.json 
class ProductsExtractor(scrapy.Spider):
    name = "products"

    def __init__(self, config=None, h2=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config  # Captures CLI arg: -a json_file="urls.json"
        self.req_meta = {"download_handler": "h2"} if str(h2).lower() in ("1", "true") else {}

    async def start(self):
        if not self.config:
            self.logger.error("NEED TO PROVIDE CONFIG FILE")
            return

        try:
            text = (files("spider3_0") / "configs" / self.config).read_text(encoding="utf-8")
        except FileNotFoundError:
            self.logger.error("Config %s not found in package", self.config)
            return

        file = json.loads(text)

        for x, y in file[0].items():
            for item in y["urls"]:
                yield Request(
                    url=item["url"],
                    cb_kwargs={"gender": item["gender"], "category": x},
                    callback=self.parse,
                    meta=self.req_meta,
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
        item["type"] = category
        item["gender"] = gender
        item["productLink"] = response.url


        yield item
        

    # @scrapling_response(adaptive=True)
    async def parse(self, response, page: ItemPage, category, gender):
        products = await page.to_item()
        for url in products["urls"]:
            # print(url)
            yield scrapy.Request(url, callback=self.parseProduct, meta=self.req_meta, cb_kwargs={"category": category, "gender":gender})
            
        # If the page object found a next page link, follow it to collect more product links.
        next_page = products.get("next_page")
        
        if next_page:
            # Scrapy will schedule this request and the web_poet middleware will provide an ItemPage for the callback.
            yield scrapy.Request(next_page, callback=self.parse, meta=self.req_meta,  cb_kwargs={"category": category, "gender":gender})

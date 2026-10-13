# import spider3_0.pages.orPage  # Registers OrPage rules in web-poet registry
import scrapy
from web_poet import ItemPage



## TO RUN SPIDER:

## RUN FROM spider3.0\spider3_0 DIRECTORY

##  scrapy crawl categories -a url=[WEBSITE] -O "spider3_0/configs\[STORENAME]Config.json"

class OrCategoryExtractor(scrapy.Spider):
    name = "categories"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if url:
            clean_url = (
                url
                if url.startswith(("http://", "https://"))
                else f"https://{url}"
            )
            self.start_urls = [clean_url]
    
    async def parse(self, response, page: ItemPage):
        items = await page.to_item()
        yield items
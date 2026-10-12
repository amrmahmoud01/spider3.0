import json
import re
import attrs
from web_poet import WebPage, field, handle_urls,ItemPage

@handle_urls(
    # r"https?://(www\.)?or-egypt\.com/(.*/)?products/.*",
    "or-egypt.com/collections/*/products",
    instead_of=ItemPage,
    priority=300,
)
@attrs.define
class ProductPage(WebPage):

    @field
    def title(self) -> str | None:
        title = self.css("h1.product-single__title::text").get()
        return title.strip() if title else None

    @field
    def main_image(self):
        return self.css(".product-main-slide img::attr(src)").get()

    @field
    def colors(self) -> list[str]:
        return self.css('fieldset[name="Color"] .variant-input input::attr(value)').getall()

    @field
    def price(self) -> str | None:
        # On sale: the strikethrough (compare-at) price is the original price
        compare = self.css("span[data-compare-price]::text").get()
        if compare and compare.strip():
            return compare.strip()
        # Not on sale: the regular product price
        regular = self.css("span[data-product-price]::text").get()
        return regular.strip() if regular else None

    @field
    def sale_price(self) -> str | None:
        sale = self.css("span[data-product-price].on-sale::text").get()
        return sale.strip() if sale else None
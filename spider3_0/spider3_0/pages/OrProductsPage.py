import json
import re
import attrs
from web_poet import WebPage, field, handle_urls,ItemPage
from scrapling import Selector

@handle_urls(
    "or-egypt.com/collections/*/products",
    instead_of=ItemPage,
    priority=300,
)
@attrs.define
class ProductPage(WebPage):

    def _page(self):
        return Selector(self.html, url=self.url, adaptive=True)

    @field
    def name(self) -> str | None:
        page = self._page()
        els = page.css("h1.product-single__title", auto_save=True, identifier="product_title")
        if not els:
            els = page.css("h1.product-single__title", adaptive=True, identifier="product_title")
        return els[0].text.strip() if els else None

    @field
    def imageLink(self):
        page = self._page()
        els = page.css(".product-main-slide img", auto_save=True, identifier="product_main_image")
        if not els:
            els = page.css(".product-main-slide img", adaptive=True, identifier="product_main_image")
        src = els[0].attrib.get("src") if els else None
        return self.urljoin(src) if src else None
    @field
    def colors(self) -> list[str]:
        page = self._page()
        els = page.css(
            'fieldset[name="Color"] .variant-input input',
            auto_save=True,
            identifier="product_color",
        )
        if not els:
            els = page.css(
                'fieldset[name="Color"] .variant-input input',
                adaptive=True,
                identifier="product_color",
            )
        return [el.attrib.get("value") for el in els if el.attrib.get("value")]

    @field
    def price(self) -> float | None:
        page = self._page()

        regular_els = page.css("span[data-product-price]", auto_save=True, identifier="product_price")
        if not regular_els:
            regular_els = page.css("span[data-product-price]", adaptive=True, identifier="product_price")

        compare = page.css("span[data-compare-price]")
        if compare and compare[0].text.strip():
            text = compare[0].text
        elif regular_els:
            text = regular_els[0].text
        else:
            return None

        match = re.search(r"\d[\d,]*(?:\.\d+)?", text)
        return float(match.group().replace(",", "")) if match else None

    @field
    def salePrice(self) -> float | None:
        sale = self._page().css("span[data-product-price].on-sale")
        if not sale:
            return 0

        match = re.search(r"\d[\d,]*(?:\.\d+)?", sale[0].text)
        return float(match.group().replace(",", "")) if match else None    
    @field
    def storeId(self):
        return 1003
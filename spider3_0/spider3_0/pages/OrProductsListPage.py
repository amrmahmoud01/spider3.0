from scrapling import Selector
from web_poet import WebPage, ItemPage, handle_urls


@handle_urls(
    "or-egypt.com/collections",
    instead_of=ItemPage,
    priority=200,
)
class OrProductListPage(WebPage, ItemPage):

    async def to_item(self):
        urls = []
        print("IN LISTINGS PAGE")

        page = Selector(self.html, url=self.url, adaptive=True)

        # Product cards: save while the selector works, relocate one card if it doesn't
        cards = page.css(".grid__item", auto_save=True, identifier="product_card")
        if not cards:
            relocated = page.css(".grid__item", adaptive=True, identifier="product_card")
            # The fallback returns one card, so expand it to all cards
            cards = [relocated[0], *relocated[0].find_similar()] if relocated else []

        for card in cards:
            href = card.css(".grid-product__link::attr(href)").get()
            if href:
                urls.append(self.urljoin(href))

        # Optional element: plain selector, since the last page has no next link
        next_href = page.css(".next a::attr(href)").get()
        next_page = self.urljoin(next_href) if next_href else None

        return {"urls": urls, "next_page": next_page}
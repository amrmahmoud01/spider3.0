from web_poet import WebPage, ItemPage, handle_urls

@handle_urls(
    # r"https?://(www\.)?or-egypt\.com/collections/(?!.*/products/).*",
    "or-egypt.com/collections",
    instead_of=ItemPage,
    priority=200,
)
class OrProductListPage(WebPage, ItemPage):


    async def to_item(self):

        urls = []
        print("IN LISTINGS PAGE")

        allProducts = self.css(".grid__item")
        for product in allProducts:
            href = product.css(".grid-product__link::attr(href)").get()
            if href:
                productLink = self.urljoin(href)
                urls.append(productLink)

        # Try to find a "next page" link. Prefer rel="next" when available, then several common pagination selectors.
        next_href = self.css('.next a ::attr(href)').get()
        next_page = self.urljoin(next_href) if next_href else None

        return {"urls": urls, "next_page": next_page}
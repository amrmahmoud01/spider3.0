from CategoryClassifier import resolve_category
from web_poet import handle_urls
from web_poet.pages import ItemPage, WebPage



# overrides=ItemPage tells web-poet that OrPage fulfills generic ItemPage dependencies
@handle_urls(
    "or-egypt.com",
    instead_of=ItemPage,
    priority=100,
)
class OrCatsPage(WebPage, ItemPage):

    async def to_item(self) -> dict:
        result = {}
        print("IN CATS PAGE")

        for item in self.css(".site-nav__details"):
            gender = (
                (item.css(".site-nav__link::text").get() or "").strip().lower()
            )

            for link in item.css(".site-nav__dropdown-link"):
                raw_category = (link.css("::text").get() or "").strip()
                if not raw_category:
                    continue

                mapped_category = resolve_category(raw_category)
                if not mapped_category:
                    continue

                if mapped_category not in result:
                    result[mapped_category] = {"urls": []}

                href = link.css("::attr(href)").get()
                if href:
                    result[mapped_category]["urls"].append(
                        {
                            "url": self.urljoin(href),
                            "gender": gender,
                        }
                    )

        return result
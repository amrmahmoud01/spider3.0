from CategoryClassifier import resolve_category
from scrapling import Selector
from web_poet import handle_urls
from web_poet.pages import ItemPage, WebPage


# Matches the live domain, plus localhost for local testing.
# instead_of=ItemPage makes this page object replace the generic one for these URLs.
@handle_urls(
    ["or-egypt.com", "localhost:8000"],
    instead_of=ItemPage,
    priority=100,
)
class OrCatsPage(WebPage, ItemPage):

    async def to_item(self) -> dict:
        result = {}
        print("IN CATS PAGE")

        # Wrap the page HTML in a Scrapling Selector with adaptive matching on.
        # url= keeps the saved adaptive data separate per domain.
        page = Selector(self.html, url=self.url, adaptive=True)

        # ANCHOR BLOCK
        # Pick one nav group to act as the reference element for the whole menu.

        # Try the normal selector first. auto_save=True stores the match every run.
        candidates = page.css(".site-nav__details", auto_save=True)

        # No match: the site changed, so relocate the saved element instead.
        if not candidates:
            candidates = page.css(".site-nav__details", adaptive=True)

        # Nothing saved and nothing found: return an empty result.
        if not candidates:
            return result
        
        print("CANDIDATES", candidates)

        anchor = candidates[0]

        # FIND ALL NAV GROUPS
        # The anchor plus every element structurally similar to it.
        # find_similar() is what turns one reference element into the full list.
        groups = [anchor, *anchor.find_similar()]

        # EXTRACT CATEGORIES
        for item in groups:
            # The <summary> tag holds the gender label ("Men", "Women", etc.).
            # Lowercased so it's consistent in the output.
            summary = item.css("summary")
            gender = (summary[0].css("::text").get() or "").strip().lower() if summary else ""

            # Every link inside the group, including deep-dropdown links.
            for link in item.css("a[href]"):
                # The visible label of the link, cleaned of surrounding whitespace.
                raw_category = (link.css("::text").get() or "").strip()
                if not raw_category:
                    continue

                # Map the raw label to a category name, or None if unknown.
                mapped_category = resolve_category(raw_category)
                if not mapped_category:
                    continue

                # Create the category bucket the first time it appears.
                if mapped_category not in result:
                    result[mapped_category] = {"urls": []}

                # Turn the relative href into a full URL and store it with its gender.
                href = link.css("::attr(href)").get()
                if href:
                    result[mapped_category]["urls"].append(
                        {
                            "url": self.urljoin(href),
                            "gender": gender,
                        }
                    )

        return result
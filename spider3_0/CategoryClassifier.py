import re
import json
from pathlib import Path
from rapidfuzz import process, fuzz

CLEAN_PATTERN = re.compile(r"[^a-z0-9\s-]")
MULTIPLE_SPACES = re.compile(r"\s+")

CATEGORY_MAP: dict[str, str] = {
    # 1. t-shirt
    "t-shirt": "t-shirt", "tshirt": "t-shirt", "tee": "t-shirt", "tees": "t-shirt",
    "graphic tee": "t-shirt", "polo": "t-shirt", "polo shirt": "t-shirt",
    "tank top": "t-shirt", "tank tops": "t-shirt", "tank": "t-shirt",
    "sleeveless": "t-shirt", "crop top": "t-shirt", "top": "t-shirt", "tops": "t-shirt",

    # 2. shirt (Button-downs, Oxfords, Flannels)
    "shirt": "shirt", "shirts": "shirt", "button down": "shirt", "button-down": "shirt",
    "button up": "shirt", "button-up": "shirt", "dress shirt": "shirt", "dress shirts": "shirt",
    "linen shirt": "shirt", "casual shirt": "shirt", "oxford shirt": "shirt",
    "flannel": "shirt", "flannels": "shirt",

    # 3. sweatshirt
    "sweatshirt": "sweatshirt", "sweatshirts": "sweatshirt", "crewneck": "sweatshirt",
    "crew neck": "sweatshirt", "fleece": "sweatshirt",

    # 4. hoodie
    "hoodie": "hoodie", "hoodies": "hoodie", "hooded sweatshirt": "hoodie",
    "zip hoodie": "hoodie", "pullover hoodie": "hoodie",

    # 5. sweater
    "sweater": "sweater", "sweaters": "sweater", "pullover": "sweater", "pullovers": "sweater",
    "jumper": "sweater", "jumpers": "sweater", "cardigan": "sweater", "cardigans": "sweater",
    "knitwear": "sweater", "knits": "sweater", "turtleneck": "sweater",

    # 6. coat (Outerwear & Jackets)
    "coat": "coat", "coats": "coat", "jacket": "coat", "jackets": "coat",
    "trench coat": "coat", "trench coats": "coat", "raincoat": "coat", "raincoats": "coat",
    "overcoat": "coat", "overcoats": "coat", "blazer": "coat", "blazers": "coat",
    "puffer": "coat", "parka": "coat", "vest": "coat", "outerwear": "coat", "kimonos": "coat",

    # 7. pants
    "pants": "pants", "trouser": "pants", "trousers": "pants", "chino": "pants",
    "chinos": "pants", "chino trousers": "pants", "sweatpants": "pants",
    "joggers": "pants", "cargo pants": "pants", "cargos": "pants", "bottoms": "pants",

    # 8. jeans
    "jeans": "jeans", "jean": "jeans", "denim": "jeans", "denim pants": "jeans",
    "skinny jeans": "jeans", "baggy jeans": "jeans", "straight jeans": "jeans",

    # 9. leggings
    "leggings": "leggings", "legging": "leggings",

    # 10. shorts
    "shorts": "shorts", "short": "shorts", "bermuda": "shorts", "cargo shorts": "shorts",

    # 11. dress
    "dress": "dress", "dresses": "dress", "gown": "dress", "jumpsuit": "dress",
    "romper": "dress", "maxi dress": "dress",

    # 12. skirt
    "skirt": "skirt", "skirts": "skirt", "mini skirt": "skirt", "midi skirt": "skirt",
    "maxi skirt": "skirt",

    # 13. pyjama
    "pyjama": "pyjama", "pyjamas": "pyjama", "pajama": "pyjama", "pajamas": "pyjama",
    "loungewear": "pyjama", "sleepwear": "pyjama", "nightdress": "pyjama",
    "nightwear": "pyjama", "robe": "pyjama",

    # 14. underwear
    "underwear": "underwear", "bra": "underwear", "bras": "underwear",
    "boxer": "underwear", "boxers": "underwear", "trunks": "underwear",
    "boxer trunks": "underwear", "lingerie": "underwear", "innerwear": "underwear",

    # 15. shoes
    "shoes": "shoes", "shoe": "shoes", "boots": "shoes", "boot": "shoes",
    "classic shoes": "shoes", "sneakers": "shoes", "loafers": "shoes",
    "sandals": "shoes", "slippers": "shoes", "heels": "shoes", "footwear": "shoes",

    # 16. accessories
    "accessories": "accessories", "accessory": "accessories", "bags": "accessories",
    "wallets": "accessories", "bags & wallets": "accessories",
    "winter accessories": "accessories", "jewellery": "accessories",
    "jewelry": "accessories", "hair accessories": "accessories", "belts": "accessories",
    "hats": "accessories", "caps": "accessories", "fragrances": "accessories",
    "perfume": "accessories", "scarves": "accessories",

    # 17. sportswear
    "sportswear": "sportswear", "activewear": "sportswear", "tracksuit": "sportswear",
    "gymwear": "sportswear", "athletic": "sportswear", "sports apparel": "sportswear",

    # 18. swimwear
    "swimwear": "swimwear", "swim suit": "swimwear", "swimsuit": "swimwear",
    "swimsuits": "swimwear", "bikini": "swimwear", "bikinis": "swimwear",
    "swimming shorts": "swimwear", "swim shorts": "swimwear",
    "swim trunks": "swimwear", "boardshorts": "swimwear", "beachwear": "swimwear",

    # 19. socks
    "socks": "socks", "sock": "socks", "tights": "socks",
    "socks & tights": "socks", "stockings": "socks", "hosiery": "socks",
}


KNOWN_KEYS: list[str] = list(CATEGORY_MAP.keys())


def normalize_string(text: str) -> str:
    text = text.lower()
    text = CLEAN_PATTERN.sub("", text)
    return MULTIPLE_SPACES.sub(" ", text).strip()


def resolve_category(raw_string: str, score_cutoff: float = 85.0) -> str | None:
    clean_input = normalize_string(raw_string)
    if not clean_input:
        return None

    # Tier 1: Exact Hash Lookup
    if clean_input in CATEGORY_MAP:
        return CATEGORY_MAP[clean_input]

    # Tier 2: RapidFuzz Fallback
    match = process.extractOne(
        clean_input, KNOWN_KEYS, scorer=fuzz.token_set_ratio, score_cutoff=score_cutoff
    )
    if match:
        best_key = match[0]
        return CATEGORY_MAP[best_key]
    
    return "none"

# output_path = Path(__file__).resolve().parent / "categories.json"

# with open(output_path, encoding="utf-8") as f:
#     data = json.load(f)
        
# print(resolve_category("denim jeans"))
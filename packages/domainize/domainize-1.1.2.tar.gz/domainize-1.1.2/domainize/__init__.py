"""Library for extracting domains."""
import urllib.parse

# Not actual TLDs that we should practically treat as TLDs.
SPECIAL_TLDS = [
    "com.br",
    "co.uk",
    "com.au",
    "co.jp",
    "co.il",
    "co.za",
    "co.in",
    "co.nz",
    "com.cn",
    "co.id",
    "co.kr",
    "com.tr",
    "com.my",
    "com.sg",
    "com.mx",
    "com.ua",
    "com.ar",
    "com.co",
    "net.au",
    "com.hk",
    "github.io",
    "co.th",
    "org.uk",
    "ne.jp",
    "wordpress.com",
]


def get_domain(value: str) -> str:
    """Extract a standardized domain from a url."""
    if value.startswith("https://") or value.startswith("http://"):
        base_domain = urllib.parse.urlparse(value).netloc
    else:
        base_domain = value.split("/")[0]
    base_domain = base_domain.split(":")[0]
    matched = [tld for tld in SPECIAL_TLDS if base_domain.endswith(tld)]
    use_count = 2
    if matched:
        use_count = len(matched[0].split(".")) + 1
    return ".".join(base_domain.split(".")[-use_count:]).lower()

from urllib.parse import urlparse


def get_valid_base_url(base_url: str) -> str:
    try:
        parsed_url = urlparse(base_url)
    except ValueError as ex:
        raise ValueError("Invalid base_url: could not parse value") from ex
    if parsed_url.scheme not in ("http", "https", "mock"):
        raise ValueError("Invalid base_url: must use http or https scheme")
    return parsed_url.geturl()

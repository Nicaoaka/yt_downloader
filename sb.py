import re

def get_domain(url: str) -> str|None:
    """ If the url is malformed, the result may be weird """
    match = re.match(r'^(?:(?:https?:)?\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)', url)
    return match.groups()[0] if match else None



import validators
import urllib.parse


def validate_url(input_url):
    if len(input_url) > 255:
        return False, 'URL превышает 255 символов'
    if not validators.url(input_url):
        return False, 'Некорректный URL'
    return True, ''


def normalize(input_url):
    parsed_url = urllib.parse.urlparse(input_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

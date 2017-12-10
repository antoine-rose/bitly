from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_url(url):
    url_validator = URLValidator()
    url_to_validate = url
    if not "http" in url_to_validate:
        url_to_validate = 'http://' + url_to_validate
    try:
        url_validator(url_to_validate)
    except ValidationError:
        return False, ""
    return True, url_to_validate
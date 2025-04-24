from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def domain_only(url):
    """Extracts only the domain from a full URL."""
    if url:
        parsed_url = urlparse(url)
        return parsed_url.netloc  # Extracts 'example.com' from 'https://example.com'
    return ""

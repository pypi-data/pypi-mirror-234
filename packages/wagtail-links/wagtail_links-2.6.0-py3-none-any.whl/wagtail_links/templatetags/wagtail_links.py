from django import template
from ..models import Link
import logging


logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def get_wagtail_link(link_name):
    try:
        link = Link.objects.get_by_natural_key(link_name)
    except Link.DoesNotExist:
        logger.error("Wagtail Link with name [%s] does not exist.", link_name)
        return None
    return link


@register.simple_tag
def get_wagtail_link_url(link_name):
    link = get_wagtail_link(link_name)
    if link is None:
        return ""
    return link.url

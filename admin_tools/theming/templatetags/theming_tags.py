"""
Theming template tags.

To load the theming tags just do: ``{% load theming_tags %}``.
"""

from django import template
from django.conf import settings
from admin_tools.utils import get_media_url

register = template.Library()

def render_theming_css():
    """
    Template tag that renders the needed css files for the theming app.

    If ADMIN_TOOLS_THEMING_CSS is explicitely defined to None, don't render
    anything.
    """
    rval = ''
    try:
        css_path = getattr(settings, 'ADMIN_TOOLS_THEMING_CSS')
    except AttributeError:
        css_path = 'admin_tools/css/theming.css'

    if css_path is not None:
        css_url = '%s/%s' % (get_media_url(), css_path)
        rval = '<link rel="stylesheet" type="text/css" media="screen" href="%s" />' % css_url

    return rval

register.simple_tag(render_theming_css)

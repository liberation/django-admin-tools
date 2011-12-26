"""
Menu utilities.
"""
import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def get_admin_menu(context):
    """
    Returns the admin menu defined by the user or the default one.
    """
    return _get_menu_cls(getattr(
        settings,
        'ADMIN_TOOLS_MENU',
        'admin_tools.menu.DefaultMenu'
    ), context)()


# FIXME Copied from admin_tools.dashboard.utils._get_dashboard_cls... DRY alert!
def _get_menu_cls(menu_cls, context):
    if type(menu_cls) is types.DictType:
        curr_url = context.get('request').META['PATH_INFO']
        for key in menu_cls:
            admin_site_mod, admin_site_inst = key.rsplit('.', 1)
            admin_site_mod = import_module(admin_site_mod)
            admin_site = getattr(admin_site_mod, admin_site_inst)
            admin_url = reverse('%s:index' % admin_site.name)  # FIXME use current_app to reverse custom AdminSite!
            if curr_url.startswith(admin_url):
                mod, inst = menu_cls[key].rsplit('.', 1)
                mod = import_module(mod)
                return getattr(mod, inst)
    else:
        mod, inst = menu_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)
    raise ValueError('Menu matching "%s" not found' % dashboard_cls)

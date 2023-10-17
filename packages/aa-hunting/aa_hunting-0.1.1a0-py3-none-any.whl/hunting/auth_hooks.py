from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class HuntingMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("Hunting"),
            "fas fa-skull-crossbones fa-fw",
            "hunting:index",
            navactive=["hunting:index"],
        )

    def render(self, request):
        if request.user.has_perm("hunting.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return HuntingMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "hunting", r"^hunting/")


@hooks.register('discord_cogs_hook')
def register_cogs():
    return ["hunting.cogs.hunting"]

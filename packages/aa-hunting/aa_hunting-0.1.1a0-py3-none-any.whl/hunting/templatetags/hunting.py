from eveuniverse.models import EveSolarSystem

from django import template

register = template.Library()

_BASE_URL = 'http://evemaps.dotlan.net'


@register.filter
def dotlan_jump_range(
        solar_system: EveSolarSystem,
        range: str = "Super Capitals") -> str:
    """
    Dotlan Jump Range
    """

    if range == "Super Capitals":
        range_string = "/range/Avatar,5/"
    elif range == "Capital":
        range_string = "/range/Archon,5/"
    elif range == "Black Ops":
        range_string = "/range/Marshal,5/"
    elif range == "Jump Freighters":
        range_string = "/range/Marshal,5/"
    else:
        range_string = "/range/Avatar,5/"

    return f"{_BASE_URL}{range_string}{solar_system.name.replace(' ', '_')}"

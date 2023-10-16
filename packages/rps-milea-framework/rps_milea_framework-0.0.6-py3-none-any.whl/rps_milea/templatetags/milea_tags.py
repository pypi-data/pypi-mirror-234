from django.conf import settings as core_settings
from django import template
from django.contrib.staticfiles import finders

from rps_milea import settings as milea_settings

register = template.Library()

@register.simple_tag
def custom_static(path):
    """
    Prüft ob der übergebene Dateiname in static/custom existiert.
    Falls es nicht existiert, wird die Standard Milea Datei ausgeliefert.

    :param path: path of static file
    :return: path of static file
    """
    milea_path = 'milea/' + path

    if finders.find(path):
        return core_settings.STATIC_URL + path
    else:
        return core_settings.STATIC_URL + milea_path

@register.simple_tag
def milea_setting(name: str):
    """
    Prüft ob die übergebene variable in den core settings existiert
    und gibt den value aus den settings zurück.
    Falls es nicht existiert, wird der value aus den Milea Settings ausgegeben.

    :param name: name of setting variable
    :return: value of setting variable
    """
    val = getattr(core_settings, name, None)
    if val is not None:
        return val
    return getattr(milea_settings, name, "")

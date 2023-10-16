from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from rps_milea.models.choices import MileaChoices
from rps_milea.admin.defaults import MileaAdmin

@admin.register(MileaChoices)
class MileaChoicesAdmin(MileaAdmin):
    list_display = ('display', 'category', 'badge')
    list_display_links = ('display',)
    show_sysdata = True

    def badge(self, obj):
        return format_html(
            '<span class="badge bg-{}">{}</span>', obj.color, obj.get_color_display(),
        )
    badge.short_description = _("Color")

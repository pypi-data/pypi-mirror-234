from django.contrib import admin
from rps_milea import settings as milea
from django.utils.translation import gettext_lazy as _
from django.forms import Textarea
from django.db import models
from django.utils.html import format_html

# Default Naming
admin.site.site_header = admin.site.site_title = '%s Verwaltung' % getattr(milea, 'FW_NAME', "Django")
admin.site.index_title = 'Dashboard'

# Default Admin
class MileaAdmin(admin.ModelAdmin):

    show_sysdata = True  # Zeigt die Systemfelder an (created, updated, ...)

    list_display = ('verbose_id',)
    list_display_links = ('verbose_id',)
    readonly_fields = ['created_at', 'created_by', 'updated_at', 'updated_by',]
    search_fields = ['id',]
    list_per_page = 10

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 9})},
    }

    def is_active_badge(self, obj):
        return format_html(
            '<span class="badge bg-{} me-1"></span> {}', 'success' if obj.is_active else 'secondary', '',
        )
    is_active_badge.short_description = _("Active")

    def get_fieldsets(self, request, obj=None):
        # Hole die standardmäßigen Felder, die von Django automatisch generiert werden
        fieldsets = super().get_fieldsets(request, obj=obj)

        # Füge das benutzerdefinierte Feldset hinzu
        if self.show_sysdata:
            fieldsets += (
                ("System data", {
                    'classes': ('col-lg-12',),
                    'fields': (('created_at', 'created_by', 'updated_at', 'updated_by'),),
                }),
            )

        return fieldsets

    def get_fields(self, request, obj=None):
        # Hole alle Felder, die von Django automatisch generiert werden
        fields = super().get_fields(request, obj=obj)

        # Entferne die Felder, die bereits im benutzerdefinierten Feldset enthalten sind
        fields = [field for field in fields if field not in ('is_active', 'created_at', 'created_by', 'updated_at', 'updated_by')]

        return fields

    # Allow search with verbose_id
    def get_search_results(self, request, queryset, search_term):
        # Hole den Verbose Id Tag aus dem Model und modifiziere den suchstring
        if self.model.OBJ_VERB_TAG and search_term.startswith('%s.' % self.model.OBJ_VERB_TAG):
            search_term = search_term.split('.')
            search_term = int(search_term[1])
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        return queryset, use_distinct

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField


class MileaModel(models.Model):

    OBJ_VERB_TAG = ""

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_("Created at"))
    created_by = CurrentUserField(on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_created_by", verbose_name=_("Created by"))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_("Updated at"))
    updated_by = CurrentUserField(on_update=True, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_updated_by", verbose_name=_("Updated by"))

    @property
    def verbose_id(self):
        if self.OBJ_VERB_TAG:
            return "%s.%s" % (self.OBJ_VERB_TAG, str(self.id).zfill(6))
        else:
            return "%s" % (str(self.id).zfill(6))
    verbose_id.fget.short_description = _("Identifier")

    class Meta:
        abstract = True

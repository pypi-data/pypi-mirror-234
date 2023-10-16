from django.db import models
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from rps_milea.models.defaults import MileaModel

class MileaChoices(MileaModel):

    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('azure', 'Azure'),
        ('indigo', 'Indigo'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
        ('lime', 'Lime'),
        ('green', 'Green'),
        ('teal', 'Teal'),
        ('cyan', 'Cyan'),
        ('dark', 'Black'),
        ('muted', 'Gray')
    ]

    category = models.CharField(max_length=64, verbose_name=_("Category"))
    display = models.CharField(max_length=64, verbose_name=_("Display name"))
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, verbose_name=_("Color"))
    value = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.value = slugify(self.display)
        super().save(*args, **kwargs)

    def __html__(self):
        return format_html('<span class="badge bg-{} text-{}-fg me-1">{}</span>', self.color, self.color, self.display)

    def __str__(self):
        return f"{self.category} | {self.display}"

    class Meta:
        ordering = ['category', 'value']
        verbose_name = _("Selection")
        verbose_name_plural = _("Selection boxes")

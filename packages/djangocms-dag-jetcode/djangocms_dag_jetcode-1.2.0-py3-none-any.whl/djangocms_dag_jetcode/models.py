from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_attributes_field.fields import AttributesField
from multiselectfield import MultiSelectField

from .conf import settings


class JetcodeConfig(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    options = AttributesField(
        verbose_name=_("Options"),
        blank=True,
        excluded_keys=["calendarIcon"],
    )

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def get_options_string(self):
        options_list = []
        for key, value in self.options.items():
            if value != "":
                options_list.append(f"{key}={value}")
            else:
                options_list.append(f"{key}")

        return ",".join(options_list)


TYPE_CHOICES = (
    ("product", _("Product")),
    ("productselector", _("Product selector")),
    ("container", _("Product list")),
    ("package", _("Package")),
)


class Jetcode(CMSPlugin):
    jetcode_type = models.CharField(_("Type"), choices=TYPE_CHOICES, max_length=20)
    jetcode_id = models.IntegerField(_("Identifier"))
    configuration = models.ForeignKey(
        JetcodeConfig, verbose_name=_("Configuration"), on_delete=models.CASCADE
    )
    styles = MultiSelectField(
        _("Styles"), choices=settings.STYLE_CHOICES, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Jetcode")
        verbose_name_plural = _("Jetcodes")

    def __str__(self):
        return f"{self.get_jetcode_type_display()} #{self.jetcode_id} - {self.configuration}"

from django.contrib import admin
from django.utils.translation import gettext as _

from .models import JetcodeConfig


class JetcodeConfigAdmin(admin.ModelAdmin):
    list_display = ["name", "get_options_string"]
    search_fields = ["name"]

    def get_options_string(self, object):
        return ", ".join(object.options.keys())

    get_options_string.short_description = _("Options")


admin.site.register(JetcodeConfig, JetcodeConfigAdmin)

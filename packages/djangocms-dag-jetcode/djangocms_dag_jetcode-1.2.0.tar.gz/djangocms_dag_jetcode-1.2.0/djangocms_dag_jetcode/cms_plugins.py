from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from .conf import settings as local_settings
from .models import Jetcode


class JetcodePlugin(CMSPluginBase):
    model = Jetcode
    name = _("Jetcode")
    render_template = "djangocms_dag_jetcode/default.html"

    def render(self, context, instance, placeholder):
        request = context["request"]
        StaticfilesStorage = import_string(settings.STATICFILES_STORAGE)

        style_path = reverse("djangocms-dag-jetcode:css", args=[instance.pk])
        context["css_url"] = request.build_absolute_uri(style_path)

        icon_path = "djangocms_dag_jetcode/img/calendar-icon.png"
        context["calendar_icon_url"] = request.build_absolute_uri(
            StaticfilesStorage().url(icon_path)
        )

        return super().render(context, instance, placeholder)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide `styles` field if it is empty
        if len(local_settings.STYLE_CHOICES) == 0:
            self.exclude = ["styles"]


plugin_pool.register_plugin(JetcodePlugin)

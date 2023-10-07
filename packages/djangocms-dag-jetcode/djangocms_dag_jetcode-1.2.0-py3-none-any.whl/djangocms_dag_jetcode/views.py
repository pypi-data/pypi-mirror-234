import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from django.views.decorators.cache import cache_page

from .conf import settings as local_settings
from .models import Jetcode


@cache_page(local_settings.CACHE_TIMEOUT)
def get_css(request, pk):
    plugin = get_object_or_404(Jetcode, pk=pk)

    if settings.DEBUG:
        BASE_URL = os.path.join(settings.STATIC_URL, "djangocms_dag_jetcode/css/")
        response = f'@import "{BASE_URL}base.css";\n'
        response += f'@import "{BASE_URL}{plugin.jetcode_type}.css";'

        for style in plugin.styles:
            response += f'\n@import "{BASE_URL}{style}.css";'

    else:
        StaticfilesStorage = import_string(settings.STATICFILES_STORAGE)
        sfs = StaticfilesStorage()

        response = "/* base.css */\n"
        with open(sfs.path("djangocms_dag_jetcode/css/base.css")) as f:
            response += f.read()

        response += f"\n/* {plugin.jetcode_type}.css */\n"
        with open(
            sfs.path(f"djangocms_dag_jetcode/css/{plugin.jetcode_type}.css")
        ) as f:
            response += f.read()

        for style in plugin.styles:
            path = sfs.path(f"djangocms_dag_jetcode/css/{style}.css")
            if os.path.exists(path):
                with open(path) as f:
                    response += f"\n\n/* {style}.css */\n"
                    response += f.read()
            else:
                response += f"\n/* {style}.css */\n"
                response += "/* file not found! */"

    return HttpResponse(response, content_type="text/css")

# -*- coding: utf-8 -*-
from django.conf import settings


STYLE_CHOICES = getattr(settings, "DJANGOCMS_DAG_JETCODE_STYLE_CHOICES", [])

CACHE_TIMEOUT = getattr(settings, "DJANGOCMS_DAG_JETCODE_CACHE_TIMEOUT", 15 * 60)

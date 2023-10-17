from django.contrib import admin

from allianceauth.services.hooks import get_extension_logger

from .models import (
    Focus, Incursion, IncursionInfluence, IncursionsConfig, Webhook,
)

logger = get_extension_logger(__name__)


@admin.register(IncursionsConfig)
class IncursionsConfigAdmin(admin.ModelAdmin):
    filter_horizontal = ["status_webhooks", ]


@admin.register(Incursion)
class IncursionAdmin(admin.ModelAdmin):
    list_display = ["constellation", "state", "established_timestamp"]
    list_filter = ["state", ]
    filter_horizontal = ["infested_solar_systems", ]


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(IncursionInfluence)
class IncursionInfluenceAdmin(admin.ModelAdmin):
    list_display = ("incursion", "timestamp", "influence")


@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
    list_display = ["incursion",]

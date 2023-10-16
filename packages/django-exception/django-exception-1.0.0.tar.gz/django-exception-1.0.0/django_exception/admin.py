from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from .models import ExceptionModel


class ExceptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "module",
        "filename",
        "lineno",
        "exc_class",
        "exc_message",
        "timestamp",
        "time",
        "timesince",
    ]
    list_filter = [
        "module",
        "filename",
        "exc_class",
    ]
    search_fields = [
        "module",
        "filename",
        "exc_class",
        "exc_message",
        "exc_traceback",
    ]

    def time(self, obj):
        return datetime.fromtimestamp(obj.timestamp)

    def timesince(self, obj):
        return timesince(datetime.fromtimestamp(obj.timestamp)) + " ago"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(ExceptionModel, ExceptionAdmin)

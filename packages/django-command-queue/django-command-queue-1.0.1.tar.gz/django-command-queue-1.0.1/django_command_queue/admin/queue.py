from django.contrib import admin

from ..models import Queue


class QueueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


admin.site.register(Queue, QueueAdmin)

from django.contrib import admin

from yt2m.models import Download


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ("uuid", "youtube_title", "task_id", "state", "created_at", )
    list_filter = ("state", "created_at", )

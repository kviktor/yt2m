from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path


from yt2m.views import index, start_download, download, download_audio, ajax_download


urlpatterns = [
    path("", index, name="index"),
    path("start_download", start_download, name="start_download"),
    re_path(r"^d/(?P<download_id>.*)$", download, name="download"),
    re_path(r"^x/(?P<download_id>.*)$", ajax_download, name="ajax_download"),
    re_path(r"^a/(?P<download_id>.*)$", download_audio, name="download_audio"),
    path(settings.ADMIN_URL, admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar  # noqa

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

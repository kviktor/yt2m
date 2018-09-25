from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views import defaults as default_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


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


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

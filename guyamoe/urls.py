"""guyamoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from homepage.sitemaps import (
    ChapterViewSitemap,
    PagesListViewSitemap,
    PageViewSitemap,
    SeriesViewSitemap,
    StaticViewSitemap,
)
from proxy import sources

sitemaps = {
    "static": StaticViewSitemap,
    "series": SeriesViewSitemap,
    "chapter": ChapterViewSitemap,
    "pageslist": PagesListViewSitemap,
    "page": PageViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path("reader/", include("reader.urls")),
    path("read/", include("reader.urls")),
    path("api/", include("api.urls")),
    path("pages/", include("misc.urls")),
    path(
        "",
        include(
            [route for source in sources for route in source.register_shortcut_routes()]
        ),
    ),
    path("proxy/", include("proxy.urls")),
]

# Importer/Exporter is not included in the repo and is distributed using a different license
try:
    import mangadex.urls
    urlpatterns.append(path("mangadex/", include("mangadex.urls")))
except ImportError:
    pass


# only add prometheus in production

handler404 = "homepage.views.handle404"

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [
    #     path('__debug__/', include(debug_toolbar.urls)),

    #     # For django versions before 2.0:
    #     # url(r'^__debug__/', include(debug_toolbar.urls)),

    # ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


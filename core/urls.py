from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView
from drf_spectacular.views import SpectacularAPIView

app_name = "core"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("accounts.api.urls")),
    path("pets/", include("posts.api.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI:
    path("doc/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Redoc UI:
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        # Debug
        path("__debug__/", include(debug_toolbar.urls))
    ]

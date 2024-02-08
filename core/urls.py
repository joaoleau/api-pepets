from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.api.urls")),
    path("", include("posts.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

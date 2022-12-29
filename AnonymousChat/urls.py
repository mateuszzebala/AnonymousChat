
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),
    path('', include('Main.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

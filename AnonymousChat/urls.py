
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from Main.views import error404

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),
    path('', include('Main.urls')),
    re_path(r'\w', error404)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

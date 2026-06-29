from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myApp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myApp.urls')),
    path('', home, name='home'),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

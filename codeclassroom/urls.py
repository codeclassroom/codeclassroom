from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('api/', include('api.urls')),
]

admin.site.site_header = "CodeClassroom Administration"
admin.site.site_title = "CodeClassroom Admin"

# for serving media files during development, taken from Django documentation
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

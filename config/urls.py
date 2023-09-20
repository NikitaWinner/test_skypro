from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="home/")),
    path('home/', include('authentication_app.urls', namespace='authentication_app')),
    path('files/', include('file_upload_app.urls', namespace='file_upload_app')),
    path('reports/', include('reports_app.urls', namespace='reports_app')),
    path('api/v1/auth/', include('authentication_app.api.urls')),
    path('api/v1/get/', include('file_upload_app.api.urls')),
    path('api/v1/check/', include('code_verification_app.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

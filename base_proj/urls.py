from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Mealy Backend API',
        default_version='v1',
        description="Backend API for Mealy",
        contact=openapi.Contact(email="brianodhiambo530@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.site.site_header = 'Mealy Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api/', include('meal_app.urls')),
    path('media/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('redoc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

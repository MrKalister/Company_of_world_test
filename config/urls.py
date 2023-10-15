from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Larixon API',
        default_version='v1',
        description='Документация для Larixon',
        contact=openapi.Contact(email=''),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]

urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

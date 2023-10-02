"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api import urls as api_urls
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions, routers
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns


schema_view = get_schema_view(
    title="Your API",
    description="Your API description",
    version="1.0",
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

urlpatterns = [
    path("api/v1/", include(router.urls)),
]

urlpatterns += format_suffix_patterns(
    [
        path("admin/", admin.site.urls),
        path("api/v1/", include(api_urls)),
        path("api/v1/schema/", schema_view),
        path("api/v1/schema_openapi/", SpectacularAPIView.as_view(), name="schema_oas"),
        path("api/v1/schema_openapi/docs/", SpectacularSwaggerView.as_view(url_name="schema_oas")),
    ]
)

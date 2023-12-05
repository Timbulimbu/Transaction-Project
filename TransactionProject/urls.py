"""
URL configuration for TransactionProject project.

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from main.views import UserViewSet, ProfileViewSet, TransactionViewSet, AddBalanceViewSet
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Transaction API",
        default_version='v1',
        description="This API for making transactions by phone_balance",
        terms_of_service="https://itcbootcamp.com/info_pages/privacy_policy",
        
        contact = openapi.Contact(
            name = 'Natalie',
            email="natalie.marten.73@gmail.com"),
        
        license=openapi.License(name="MIT License"),
        ),
 
    public=True, 
    permission_classes=[permissions.IsAdminUser])
        



router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'users', UserViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'addbalance', AddBalanceViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("redoc/", include('django.contrib.admindocs.urls')),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

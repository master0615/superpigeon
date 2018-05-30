"""superpigeon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from superpigeon.apps.api.views import *
from superpigeon.apps import views as mainview
from rest_framework import routers, serializers, viewsets
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static

admin.site.site_header = 'Superpigeon Administration'

router = routers.DefaultRouter()
router.register(prefix=r'profile', viewset=ProfileViewSet, base_name='profile')
router.register(prefix=r'product', viewset=ProductViewSet, base_name='product')
router.register(prefix=r'sync_product', viewset=SyncProductViewSet, base_name='sync_product')
router.register(prefix=r'sync_order', viewset=SyncOrderViewSet, base_name='sync_order')
router.register(prefix=r'dimension', viewset=DimensionViewSet, base_name='dimension')
router.register(prefix=r'category', viewset=CategoryViewSet, base_name='category')
router.register(prefix=r'tag', viewset=TagViewSet, base_name='tag')
router.register(prefix=r'image', viewset=ImageViewSet, base_name='image')
router.register(prefix=r'attribute', viewset=AttributeViewSet, base_name='attribute')
router.register(prefix=r'default_attribute', viewset=DefaultAttributeViewSet, base_name='default_attribute')
router.register(prefix=r'metadata', viewset=MetaDataViewSet, base_name='metadata')
router.register(prefix=r'signup', viewset=SignupViewSet, base_name='signup')
router.register(prefix=r'auth', viewset=AuthViewSet, base_name='auth')
router.register(prefix=r'logout', viewset=LogoutViewSet, base_name='logout')

urlpatterns = [
    path('', mainview.home, name='home'),
    path('api/docs/', include_docs_urls(title='Superpigeon API docs')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views
# Create a router and register our ViewSets with it.
router = DefaultRouter()

router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    path("api/v1/", include(router.urls)),
]
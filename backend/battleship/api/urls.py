from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views
from .views import PlayerViewSet, GameViewSet
# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    path("api/v1/", include(router.urls)),
]

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'boards', views.BoardViewSet, basename='boards')
router.register(r'vessels', views.VesselViewSet, basename='vessels')
router.register(r'board-vessels', views.BoardVesselViewSet, basename='board-vessels')
router.register(r'shots', views.ShotViewSet, basename='shots')

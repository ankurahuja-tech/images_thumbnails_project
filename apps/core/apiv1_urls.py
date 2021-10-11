from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.images.api import views as image_views
from apps.images.api import viewsets as image_viewsets

app_name = "apiv1"

router = SimpleRouter()
router.register("images", image_viewsets.ImageViewSet, basename="images")

urlpatterns = [
    path(
        route="images/<uuid:uuid>/<int:height>/",
        view=image_views.ThumbnailRenderAPIView.as_view(),
        name="images_render_thumbnail",
    ),
    path(
        route="images/<uuid:uuid>/generate-link/<int:expiry_time>/",
        view=image_views.ImageGenerateLinkAPIView.as_view(),
        name="images_generate_link",
    ),
    path(
        route="images/<uuid:uuid>/link/<int:expiry_time>/",
        view=image_views.ImageExpiringLinkAPIView.as_view(),
        name="images_expiring_link",
    ),
]

urlpatterns += router.urls

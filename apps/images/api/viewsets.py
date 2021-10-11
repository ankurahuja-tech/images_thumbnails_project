from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Image
from .permissions import IsOwner
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    Base viewset for images.
    Output in JSON format.
    """

    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = ImageSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user)
        return queryset
